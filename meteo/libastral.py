# -*- coding: utf-8 -*-

import math
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo


def get_astral_sun(lat: float, lon: float, dt_input: datetime) -> dict:
    """
    Replika funkcjonalności `astral.sun.sun()`, przyjmująca obiekt datetime.
    Zwraca wyniki (dawn, sunrise, noon, sunset, dusk) dopasowane do strefy czasowej dt_input.
    """
    # 1. Wyciągamy czystą datę i informacje o strefie czasowej
    target_date = dt_input.date()
    input_tz = dt_input.tzinfo

    # 2. Obliczenie Julian Day i Julian Century dla południa UTC tego dnia
    # (Do wyznaczenia pozycji Słońca używamy uniwersalnego czasu odniesienia)
    dt_noon_utc = datetime.combine(target_date, time(12, 0))
    a = math.floor((14 - dt_noon_utc.month) / 12)
    y = dt_noon_utc.year + 4800 - a
    m = dt_noon_utc.month + 12 * a - 3
    julian_day = dt_noon_utc.day + math.floor((153 * m + 2) / 5) + 365 * y + math.floor(y / 4) - math.floor(y / 100) + math.floor(y / 400) - 32045
    JC = (julian_day - 2451545) / 36525

    # 3. Parametry orbity Słońca (Algorytm Meeusa / NOAA)
    geom_mean_long_sun = (280.46646 + JC * (36000.76983 + JC * 0.0003032)) % 360
    geom_mean_anom_sun = 357.52911 + JC * (35999.05029 - 0.0001537 * JC)
    eccent_earth_orbit = 0.016708634 - JC * (0.000042037 + 0.0000001267 * JC)

    sun_eq_of_ctr = (
        math.sin(math.radians(geom_mean_anom_sun)) * (1.914602 - JC * (0.004817 + 0.000014 * JC))
        + math.sin(math.radians(2 * geom_mean_anom_sun)) * (0.019993 - 0.000101 * JC)
        + math.sin(math.radians(3 * geom_mean_anom_sun)) * 0.000289
    )

    sun_true_long = geom_mean_long_sun + sun_eq_of_ctr
    sun_app_long = sun_true_long - 0.00569 - 0.00478 * math.sin(math.radians(125.04 - 1934.136 * JC))
    mean_obliq_ecliptic = 23 + (26 + (21.448 - JC * (46.815 + JC * (0.00059 - JC * 0.001813))) / 60) / 60
    obliq_corr = mean_obliq_ecliptic + 0.00256 * math.cos(math.radians(125.04 - 1934.136 * JC))

    sun_declin = math.degrees(math.asin(math.sin(math.radians(obliq_corr)) * math.sin(math.radians(sun_app_long))))
    var_y = math.tan(math.radians(obliq_corr / 2)) ** 2
    eq_of_time = 4 * math.degrees(
        var_y * math.sin(math.radians(2 * geom_mean_long_sun))
        - 2 * eccent_earth_orbit * math.sin(math.radians(geom_mean_anom_sun))
        + 4 * eccent_earth_orbit * var_y * math.sin(math.radians(geom_mean_anom_sun)) * math.cos(math.radians(2 * geom_mean_long_sun))
        - 0.5 * (var_y ** 2) * math.sin(math.radians(4 * geom_mean_long_sun))
        - 1.25 * (eccent_earth_orbit ** 2) * math.sin(math.radians(2 * geom_mean_anom_sun))
    )

    # Południe solarne w minutach dnia UTC
    solar_noon_mins = (720 - 4 * lon - eq_of_time) % 1440

    # 4. Obliczanie Kąta Godzinowego (Hour Angle)
    def get_hour_angle(zenith_degrees):
        try:
            cos_ha = (math.cos(math.radians(zenith_degrees)) / (math.cos(math.radians(lat)) * math.cos(math.radians(sun_declin)))
                      - math.tan(math.radians(lat)) * math.tan(math.radians(sun_declin)))
            if cos_ha > 1 or cos_ha < -1:
                return None  # Dzień/noc polarna
            return math.degrees(math.acos(cos_ha))
        except ZeroDivisionError:
            return None

    ha_sun = get_hour_angle(90.833)   # Wschód / Zachód
    ha_civil = get_hour_angle(96.0)   # Świt / Zmierzch cywilny

    # 5. Konwersja minut UTC na datetime z zachowaniem oryginalnej strefy czasowej
    def _mins_to_localized_datetime(minutes):
        if minutes is None:
            return None

        # Tworzymy bazowy czas w UTC dla danego dnia
        base_utc = datetime.combine(target_date, time.min)
        dt_utc = base_utc + timedelta(minutes=minutes % 1440)

        # Jeżeli wejściowy datetime miał przypisaną strefę (np. pytz, zoneinfo)
        if input_tz is not None:
            # Nadajemy obiektowi strefę UTC, a następnie konwertujemy do strefy wejściowej
            dt_utc = dt_utc.replace(tzinfo=input_tz) # Dla uproszczenia zakładamy wejście jako UTC-offset base lub robimy .astimezone()
            # Aby zachować zachowanie 'astral', zwracamy czas przekonwertowany na strefę użytkownika:
            return dt_utc.astimezone(input_tz)

        return dt_utc
    def mins_to_localized_datetime(minutes):
        if minutes is None:
            return None

        # Tworzymy bazowy czas w czystym UTC
        base_utc = datetime.combine(target_date, time.min, tzinfo=ZoneInfo("UTC"))
        dt_utc = base_utc + timedelta(minutes=minutes % 1440)

        # Jeśli użytkownik podał strefę wejściową, bezpiecznie konwertujemy czas UTC na jego strefę
        if input_tz is not None:
            return dt_utc.astimezone(input_tz)

        return dt_utc


    # Budowanie słownika wynikowego
    res = {}
    res['noon'] = mins_to_localized_datetime(solar_noon_mins)

    if ha_sun is not None:
        res['sunrise'] = mins_to_localized_datetime(solar_noon_mins - ha_sun * 4)
        res['sunset'] = mins_to_localized_datetime(solar_noon_mins + ha_sun * 4)
    else:
        res['sunrise'] = res['sunset'] = None

    if ha_civil is not None:
        res['dawn'] = mins_to_localized_datetime(solar_noon_mins - ha_civil * 4)
        res['dusk'] = mins_to_localized_datetime(solar_noon_mins + ha_civil * 4)
    else:
        res['dawn'] = res['dusk'] = None

    return res


if __name__ == '__main__':
    # --- Przykład użycia ---
    # Pobieramy aktualny datetime (np. ze strefą czasową systemu)
    now = datetime.now(ZoneInfo('Europe/Warsaw'))

    # Współrzędne dla Warszawy
    latitude = 52.2297
    longitude = 21.0122
    # Kraków
    latitude = 50.06
    longitude = 19.94

    sol_data = get_astral_sun(latitude, longitude, now)

    print(f"Przekazany obiekt: {now} {now.tzname()}")
    print(f"Dawn:    {sol_data['dawn']}")
    print(f"Sunrise: {sol_data['sunrise']}")
    print(f"Noon:    {sol_data['noon']}")
    print(f"Sunset:  {sol_data['sunset']}")
    print(f"Dusk:    {sol_data['dusk']}")
