# -*- coding: utf-8 -*-

import enum
import pydantic
import datetime
import math


class MaxPcptType(enum.IntEnum):
    NoPcpt = 0
    Rain = 1
    Snow = 2
    Sleet = 3

class PointMetadata(pydantic.BaseModel):
    lat: float
    lon: float
    model: str
    grid: str
    row: int
    col: int

class MeteoParameter(pydantic.BaseModel):
    data: list[float]
    first_timestamp: int
    interval: int
    unit: str
    point: PointMetadata
    fstart: datetime.datetime

class CloudBaseParameter(MeteoParameter):
    @pydantic.field_validator('data', mode='after')
    @classmethod
    def filter_missing_clouds(cls, v: list[float]) -> list[float|None]:
        # Zamienia systemową maskę braku chmur na NaN, by Matplotlib pominął te punkty
        return [math.nan if x < 0.0 else x for x in v]

class ForecastDataContainer(pydantic.BaseModel):
    # Panel 0: Temperatura
    airtmp_point: MeteoParameter
    airtmp_max: MeteoParameter
    airtmp_min: MeteoParameter
    dwptmp_point: MeteoParameter
    wchill_point: MeteoParameter
    wchill_max: MeteoParameter
    wchill_min: MeteoParameter
    grdtmp_max: MeteoParameter
    grdtmp_min: MeteoParameter

    # Panel 1: Opady i Wilgotność
    pcpttl_aver: MeteoParameter
    pcpttl_max: MeteoParameter
    pcpttl_type_max: MeteoParameter
    pcpttlprob_point: MeteoParameter
    realhum_aver: MeteoParameter

    # Panel 2: Ciśnienie
    trpres_point: MeteoParameter
    slpres_point: MeteoParameter

    # Panel 3 & 4: Wiatr
    wind10_dr_deg_true_prev_point: MeteoParameter
    wind10_sd_true_prev_point: MeteoParameter
    wind_gust_max: MeteoParameter

    # Panel 5: Profil chmur i Widzialność
    visibl_min: MeteoParameter
    cldtop: CloudBaseParameter
    cldbse01: CloudBaseParameter
    cldbse25: CloudBaseParameter
    cldbse45: CloudBaseParameter
    cldbse65: CloudBaseParameter
    cldbse79: CloudBaseParameter

    # Panel 6: Zachmurzenie ogólne i Mgła
    cldvlow_aver: MeteoParameter
    cldlow_aver: MeteoParameter
    cldmed_aver: MeteoParameter
    cldhigh_aver: MeteoParameter
    cldtot_aver: MeteoParameter
    fog_max: MeteoParameter

class MeteoForecastEnvelope(pydantic.BaseModel):
    data: ForecastDataContainer
    fstart: str
