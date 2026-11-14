#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing
import sys
import os
import pathlib
import asyncio
import datetime
from curl_cffi.requests import AsyncSession, Response
from urllib.error import HTTPError

from . import libplac, libweb, meteo, render


async def fetch_meteo(
    lat: float,
    lon: float,
    *,
    timestamp: int | None,
):
    policy = libweb.ResilientHttpPolicy(max_attempts=4)
    endpoint: str = 'https://devmgramapi.meteo.pl/meteorograms/'

    async with AsyncSession(impersonate='chrome120') as session:
        if timestamp is None:
            avail_res: Response = await policy.execute(
                libweb.plain_fetch,
                session=session,
                method="GET",
                url=f'{endpoint}available',
            )
            try:
                avail_res.raise_for_status()
            except HTTPError as ex:
                print(f"[e] Server boundary execution error: HTTP status {avail_res.status_code}", file=sys.stderr)
                return None
            all_ts: list[int] = avail_res.json()['um4_60']
            latest_ts: int = max(all_ts)
            print(f'[i] Meteo returned {len(all_ts)} timestamps, {latest_ts} being the latest.', file=sys.stderr)
            timestamp = latest_ts

        dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        print(f'[i] Will query forecast for {lat}/{lon}, at {dt.isoformat()} ({timestamp})', file=sys.stderr)

        fc_res: Response = await policy.execute(
            libweb.plain_fetch,
            session=session,
            method="POST",
            url=f'{endpoint}um4_60',
            json_={"point":{"lat":str(lat),"lon":str(lon)},"date": timestamp}
        )
        try:
            fc_res.raise_for_status()
        except HTTPError as ex:
            print(f"[e] Server boundary execution error: HTTP status {fc_res.status_code}", file=sys.stderr)
            return None

        return fc_res.text


def main(
    timestamp: ("UTC timestamp to use to override remote meteo.pl REST API.", "option", "t", libplac.positive_int), # type: ignore
    lat: ("Latitude of point of interest.", 'positional', None, float), # type: ignore
    lon: ("Longitude of point of interest.", 'positional', None, float), # type: ignore
    tzname: ("Timezone name to use.", "option", "T", str) = 'Europe/Warsaw', # type: ignore
    output: ("Output image path.", "positional", None, pathlib.Path) = "krakow/60.png", # type: ignore
) -> int:
    forecast_res: str | None = asyncio.run(fetch_meteo(lat, lon, timestamp=timestamp))
    if forecast_res is None:
        return os.EX_UNAVAILABLE

    try:
        forecast = meteo.MeteoForecastEnvelope.model_validate_json(forecast_res)
    except Exception as ex:
        print(f'[!] Meteo forecast response error: {str(ex)}', file=sys.stderr)
        return os.EX_DATAERR

    print(f'[i] Fetched forecast since {forecast.fstart}')

    image: bytes = render.make_charts(forecast, tzname=tzname)
    print(f'[i] Rendered blob size: {len(image)}.', file=sys.stderr)

    with open(output, 'wb') as ofile:
        ofile.write(image)

    print(f'[i] Saved to {output}.', file=sys.stderr)

    return os.EX_OK


def cli_main() -> int:
    """
    Synchronous CLI execution wrapper launching the internal asynchronous loop.

    Returns
    -------
    int
        System execution exit code mapping standard structures.
    """
    return libplac.plac_call(main)


if __name__ == "__main__":
    sys.exit(cli_main())
