#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing
import sys
import os
import pathlib
import asyncio
import datetime
import plac
import inspect
import json
from curl_cffi.requests import AsyncSession, Response
from urllib.error import HTTPError

from . import libplac, libweb, meteo, render


VERSION: typing.LiteralString = '0.0.1'
METEO_EP: typing.LiteralString = 'https://devmgramapi.meteo.pl/meteorograms/'


class MeteoInterface():
    add_help = False # for reflection by plac
    commands = 'available', 'render', 'check_state' \
        , 'help',

    def __init__(
        self,
        help: ("Show help.", "flag", "h"), # type: ignore
        #quiet: ("Disable console output.", "flag", "q"), # type: ignore
        #verbose: ("Enable verbose output.", "flag", "v"), # type: ignore
        command: ("Command to execute.", 'positional', None, str, commands)='help', # type: ignore
        *args
    ):
        self.status = os.EX_OK
        self.parser = plac.parser_from(self.__class__)

        command_fn = self.__getattribute__(command)

        if help:
            if command != 'help':
                # tweak prog from '<prog name>' -> '<prog name> <command>'
                sub_parser = plac.parser_from(
                    command_fn, prog=f'{os.path.basename(sys.argv[0])} {command}')
                sub_parser.print_help()
                return

        rv = plac.call(command_fn, arglist=args)
        if inspect.isawaitable(rv):
            self.status = asyncio.run(rv)
        else:
            self.status = rv


    def help(self) -> int:
        "Display global help. To request help for a subcommand specify its name."
        self.parser.print_help()
        return os.EX_OK


    async def _api_call(
        self,
        policy,
        session,
        *,
        method: str,
        api: str,
        json_: typing.Any|None=None,
    ) -> Response:
        res: Response = await policy.execute(
            libweb.plain_fetch,
            session=session,
            method=method,
            url=f'{METEO_EP}{api}',
            json_=json_,
        )
        res.raise_for_status()
        return res


    async def available(
        self,
        latest: ("Only print latest available timestamp.", "flag", "L"), # type: ignore
        model: ("Meteo forecast model.", 'positional', None, str, ["um4_60", "um4_120", "gfs"])='um4_60', # type: ignore
    ) -> int:
        policy = libweb.ResilientHttpPolicy(max_attempts=4)

        async with AsyncSession(impersonate='chrome120') as session:
            try:
                res: Response = await self._api_call(policy, session, method='GET', api='available')
            except HTTPError as ex:
                print(f"[e] Server boundary execution error: HTTP status {res.status_code}", file=sys.stderr)
                return os.EX_UNAVAILABLE

        all_ts: list[int] = res.json()[model]
        if latest:
            print(max(all_ts))
        else:
            json.dump(all_ts, sys.stdout, ensure_ascii=False, separators=(',', ':'))
        return os.EX_OK


    async def render(
        self,
        lat: ("Latitude of point of interest.", 'positional', None, float), # type: ignore
        lon: ("Longitude of point of interest.", 'positional', None, float), # type: ignore
        timestamp: ("Model's forecast UTC timestamp to query for.", "positional", None, libplac.positive_int), # type: ignore
        tzname: ("Timezone name to use.", "option", "T", str) = 'Europe/Warsaw', # type: ignore
        output: ("Output image path.", "positional", None, pathlib.Path) = "krakow/60.png", # type: ignore
    ) -> int:
        dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        print(f'[i] Will query forecast for {lat}/{lon}, at {dt.isoformat()} ({timestamp})', file=sys.stderr)

        policy = libweb.ResilientHttpPolicy(max_attempts=4)

        async with AsyncSession(impersonate='chrome120') as session:
            json_ = {"point":{"lat":str(lat),"lon":str(lon)},"date": timestamp}
            try:
                res: Response = await self._api_call(policy, session, method='POST', api='um4_60', json_=json_)
            except HTTPError as ex:
                print(f"[e] Server boundary execution error: HTTP status {res.status_code}", file=sys.stderr)
                return os.EX_UNAVAILABLE

        try:
            forecast = meteo.MeteoForecastEnvelope.model_validate_json(res.text)
        except Exception as ex:
            print(f'[!] Meteo forecast response error: {str(ex)}', file=sys.stderr)
            return os.EX_DATAERR

        print(f'[i] Fetched forecast since {forecast.fstart}', file=sys.stderr)

        image: bytes = render.make_charts(forecast, tzname=tzname)
        print(f'[i] Rendered blob size: {len(image)}.', file=sys.stderr)

        with open(output, 'wb') as ofile:
            ofile.write(image)

        print(f'[i] Saved to {output}.', file=sys.stderr)

        print(timestamp)

        return os.EX_OK


    def check_state(
        self,
        ignore_missing: ("Ignore missing state file.", "flag", "I"), # type: ignore
        state: ("Render state JSON file.", "positional", None, pathlib.Path) = "state.json", # type: ignore
    ) -> int:
        istr = sys.stdin.read().strip()

        try:
            timestamp = int(istr)
        except ValueError as ex:
            print(f'[!] Read input {istr[:40]}... is not an integer: {str(ex)}', file=sys.stderr)
            return os.EX_DATAERR

        try:
            with open(state, "rt") as ifile:
                s = json.load(ifile)
        except IOError as ex:
            print(f'[!] Reading from {state} failed: {str(ex)}', file=sys.stderr)
            return os.EX_OK if ignore_missing else os.EX_IOERR
        except json.JSONDecodeError as ex:
            print(f'[!] JSON decoding of {state} failed: {str(ex)}', file=sys.stderr)
            return os.EX_DATAERR

        if timestamp != s:
            print(timestamp)

        return os.EX_OK


def main():
    status = libplac.plac_call(MeteoInterface, version=VERSION).status
    return status


if __name__ == "__main__":
    sys.exit(main())
