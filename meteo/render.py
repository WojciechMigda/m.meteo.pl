# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import numpy as np
import datetime
import locale
import zoneinfo
import more_itertools
import collections
import io

from . import libmath, liblocale
from .meteo import MeteoForecastEnvelope, MaxPcptType

from .libastral import get_astral_sun


IMG_W = 540
IMG_H = 660
DPI = 100
COLOR_TRANSPARENT = ('black', 0.0)
CANVAS_BG = "#FFFBF0"  # The warm cream/beige background color
TEXT_NAVY = "#00008b"   # The retro deep navy blue for text/labels
FONT_FAMILY = "Arial"
FONT_STRETCH = 'condensed'
FOOTER_FONT_SIZE = 9.0
HEADER_FONT_SIZE = 8.5
LEFT_MARGIN_FONT_SIZE = 8.5
RIGHT_MARGIN_FONT_SIZE = 8.5
RENDER_DT_FONT_SIZE = 7.0

# Z: ground, dew, mid, wchill
COLOR_TEMP_AIR_PT = "#ff0000"
COLOR_TEMP_AIR_RNG = "#fadcdc"
COLOR_TEMP_WCHILL_PT = "#0000ff"
COLOR_TEMP_WCHILL_RNG = "#b9dcff"
COLOR_TEMP_GROUND = "#a52a2a"
COLOR_TEMP_BELOW_0 = "#87cefa"
COLOR_TEMP_DEW_PT = "#6a5acd"
COLOR_HUMIDITY = "#dc4614"
COLOR_PCPT_MAX = 'red'
COLOR_PCPT_RAIN = '#00aa00'
COLOR_PCPT_SNOW = '#1331c7'
#COLOR_PCPT_SLEET = '#096e64'
#COLOR_PCPT_SLEET = '#2156FF'
COLOR_PCPT_SLEET = '#0c8b7f'
COLOR_SLPRES = 'black'
COLOR_WIND_SPEED = '#101098'
COLOR_WIND_GUST = 'red'
COLOR_WIND_ARROW = '#101098'
#COLOR_CLOUD_BG = '#87cefa'
COLOR_CLOUD_BG = ('#28a7f6', 0.56)
COLOR_VISIBILITY = '#ff9600'
COLOR_VIS_LABEL = '#ff7700'
COLOR_CLOUD_BASE_79 = '#000000'
COLOR_CLOUD_BASE_65 = '#5a5a5a'
COLOR_CLOUD_BASE_45 = '#969696'
COLOR_CLOUD_BASE_25 = '#c8c8c8'
COLOR_CLOUD_BASE_01 = '#ffffff'
COLOR_CLOUD_TOP = '#a52a2a'
COLOR_FOG_BAR = '#ffb400'
COLOR_FOG_LABEL = '#ff7700'
COLOR_CLOUD_VLOW = '#3c3c3c'
COLOR_CLOUD_LOW = '#5a5a5a'
COLOR_CLOUD_MED = '#969696'
COLOR_CLOUD_HIGH = '#ffffff'
COLOR_VBAR_DAY = '#ffffff'
COLOR_VBAR_NIGHT = '#e0e0e0'
COLOR_RENDER_DT = '#e0e0e0'


PCPT_TO_COLOR = {
    MaxPcptType.NoPcpt: COLOR_TRANSPARENT,
    MaxPcptType.Rain: COLOR_PCPT_RAIN,
    MaxPcptType.Snow: COLOR_PCPT_SNOW,
    MaxPcptType.Sleet: COLOR_PCPT_SLEET,
}


SPEED_TO_COLOR = collections.defaultdict(lambda: 'magenta', {
    0: '#80ffff',
    1: "#00ffff",
    2: "#00c3ff",
    3: "#0082ff",
    4: "#004b82",
    5: "#008200",
    6: "#1ec800",
    7: "#4bff1e",
    8: "#82ff4b",
    9: "#c8ff82",
    10: "#ffff4b",
    11: "#ffc800",
    12: "#ff8200",
    13: "#c84b00",
    14: "#961e00",
    15: "#820a0a",
    16: "#c81414",
    17: "#ff2828",
    18: "#ff4b4b",
    19: "#ff8282",
    20: "#ff82ff",
    21: "#dc5adc",
    22: "#c83cc8",
    23: "#b41eb4",
    24: "#a000a0",
    25: "#5a1e5a",
    26: "#783c78",
    27: "#965a96",
    28: "#b478b4",
    29: "#d296d2",
    30: "#e6b4e6",
    31: "#ebb9eb",
    32: "#f0bef0",
    33: "#f5c3f5",
    34: "#fac8fa",
    35: "#ffcdff",
    36: "#ffd2ff",
    37: "#ffd7ff",
    38: "#ffdcff",
    39: "#ffe1ff",
    40: "#ffe6ff",
    41: "#ffebff",
    42: "#fff0ff",
    43: "#fff5ff",
    44: "#fffaff",
    45: "#fafafa",
    46: "#f0f0f0",
    47: "#e6e6e6",
})


PRES_TO_COLOR = collections.defaultdict(lambda: 'magenta', {
    # 1034: '#de3d82',
    # 1032: '#e33067',
    # 1030: '#e8224b',
    # 1028: '#ec1430', # eb001e
    # # amsterdam niż, cherbourg wiatr

    # 1026: '#f01900', # web f01900
    # 1024: '#f53700', # web f53700
    # 1022: '#fa5f00', # web fa5f00
    # 1020: '#ff8700', # web ff8700
    # 1018: '#ffaf00', # web ffaf00
    # 1016: '#ffd700', # web ffd700
    # 1014: '#ffff00', # web ffff00
    # 1012: '#c8ff14', # web c8ff14
    # 1010: '#96ff00', # 96ff00 web:96ff00
    # 1008: '#64ff00', # web 64ff00
    # 1006: '#32eb00', # web 32eb00
    # 1004: '#00cd00', # web 00cd00
    # 1002: '#00aa00', # web 00aa00
    # 1000: '#00cd46', # web 00cd46
    #  998: '#00eb8c', # web 00eb8c
    #  996: '#00ffd2', # web 00ffd2
    #  994: '#0fffff',
    #  992: '#0fdcff',
    #  990: '#0fb4ff',# web 0fb4ff
    #  988: '#0f96ff',
    #  986: '#0f78f0',
    #  984: '#0f5ad2',
    #  982: '#0f3cb4',
    #  980: '#0f2396', # ok
    #  978: '#0f1482', #
    945: "#f5f5f5",
    947: "#ebf0f0",
    949: "#d2e6e6",
    951: "#c3dcdc",
    953: "#b4d2d2",
    955: "#a5c8c8",
    957: "#96bebe",
    959: "#87b4b9",
    961: "#78aab4",
    963: "#69a5aa",
    965: "#5aa0a0",
    967: "#4b8ca0",
    969: "#3c788c",
    971: "#2d5a6e",
    973: "#1e465a",
    975: "#0f3246",
    977: "#0f235a",
    979: "#0f1482",
    981: "#0f2396",
    983: "#0f3cb4",
    985: "#0f5ad2",
    987: "#0f78f0",
    989: "#0f96ff",
    991: "#0fb4ff",
    993: "#0fdcff",
    995: "#0fffff",
    997: "#00ffd2",
    999: "#00eb8c",
    1001: "#00cd46",
    1003: "#00aa00",
    1005: "#00cd00",
    1007: "#32eb00",
    1009: "#64ff00",
    1011: "#96ff00",
    1013: "#c8ff14",
    1015: "#ffff00",
    1017: "#ffd700",
    1019: "#ffaf00",
    1021: "#ff8700",
    1023: "#fa5f00",
    1025: "#f53700",
    1027: "#f01900",
    1029: "#eb001e",
    1031: "#e60f3c",
    1033: "#e11e5a",
    1035: "#dc2d78",
    1037: "#d73c96",
    1039: "#d24bb4",
    1041: "#cd5ad2",
    1043: "#d769f0",
    1045: "#e178ff",
    1047: "#eb87ff",
    1049: "#f596ff",
    1051: "#ffa5ff",
    1053: "#f5b4f5",
    1055: "#ebc3eb",
    1057: "#e1cde1",
    1059: "#d7d7d7",
    1061: "#dcdcdc",
    1063: "#e1e1e1",
    1065: "#e6e6e6",
    1067: "#ebebeb",
    1069: "#f0f0f0",
    1071: "#f5f5f5",
})


def setup_rc_styles():
    # Set the retro styling globally
    plt.rcParams['font.family'] = FONT_FAMILY  # Matches the clean, fixed-width text look
    plt.rcParams['font.size'] = 9
    plt.rcParams['font.stretch'] = FONT_STRETCH
    plt.rcParams['text.color'] = TEXT_NAVY         # Sets default text color
    plt.rcParams['axes.labelcolor'] = 'black'    # Sets axis label color
    plt.rcParams['axes.edgecolor'] = 'black'     # Sets subplot border outline color
    plt.rcParams['xtick.color'] = 'black'        # Sets tick markings color
    plt.rcParams['xtick.labelsize'] = 9.0
    plt.rcParams['xtick.major.pad'] = 0
    plt.rcParams['xtick.minor.pad'] = 0
    #plt.rcParams['xtick.size'] = 0
    plt.rcParams['ytick.color'] = 'black'
    plt.rcParams['ytick.labelsize'] = 8.0
    plt.rcParams['ytick.major.pad'] = 0
    plt.rcParams['ytick.minor.pad'] = 0


def make_axes(fig):
    # Define 7 stacked rows with exact height ratios
    gs = gridspec.GridSpec(7, 1, height_ratios=[1, 1, 1, 1, 0.4, 1, 1], hspace=0, wspace=0)

    axes = []
    for ix in range(7):
        pos = gs[ix].get_position(fig)
        ax = fig.add_axes(pos)
        axes.append(ax)
    return axes


def render_side_labels(axes):
    # -------------------------------------------------------------
    # PLACING LABELS CLOSE TO LEFT AND RIGHT MARGINS PER PANEL
    # -------------------------------------------------------------
    panel_labels = {
        0: ("temperatura\n(°C)", "(°C)\ntemperatura"),
        1: ("opad\n(mm/h, kg/m²/h)", "(%)\nwilgotność wzgl."),
        2: ("ciśnienie\n(hPa)", "(mmHg)\nciśnienie"),
        3: ("wiatr\n(m/s)", "(km/h)\nwiatr"),
        5: ("pion. rozciągł. chm.\n(km)", "(km)\nwidzialność"),
        6: ("zachmurzenie      \n(oktanty)", "(frakcja)\nmgła")
    }

    # side labels
    for idx, (left_txt, right_txt) in panel_labels.items():
        ax = axes[idx]

        ax.text(-0.115, 0.5, left_txt, rotation=90, va='center', ha='center', ma='center', linespacing=1.1,
            fontsize=LEFT_MARGIN_FONT_SIZE, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH, transform=ax.transAxes)

        ax.text(1.115, 0.5, right_txt, rotation=90, va='center', ha='center', ma='center', linespacing=1.1,
            fontsize=RIGHT_MARGIN_FONT_SIZE, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH, transform=ax.transAxes)

    # Wind side labels
    ax = axes[4]
    ax.text(-0.115, 0.5, " N\nW  E\nS", rotation=0, va='center', ha='center', ma='center', linespacing=0.67,
        fontsize=LEFT_MARGIN_FONT_SIZE, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH, transform=ax.transAxes)

    ax.text(1.115, 0.5, " N\nW  E\nS", rotation=0, va='center', ha='center', ma='center', linespacing=0.67,
        fontsize=RIGHT_MARGIN_FONT_SIZE, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH, transform=ax.transAxes)


def render_header_footer(fig, *, lat, lon, start_dt, tzname):
    sol_data = get_astral_sun(lat, lon, start_dt)
    sunrise: str = f'{sol_data["sunrise"].strftime("%H:%M %Z")}'
    sunset: str = f'{sol_data["sunset"].strftime("%H:%M %Z")}'

    lat_d = libmath.floor(lat)
    lat_m = libmath.floor((lat - lat_d) * 60)
    lat_s = libmath.floor(((lat - lat_d) * 60 - lat_m) * 60)

    lon_d = libmath.floor(lon)
    lon_m = libmath.floor((lon - lon_d) * 60)
    lon_s = libmath.floor(((lon - lon_d) * 60 - lon_m) * 60)

    # Header
    fig.text(0.5, 1 - 2 / IMG_H, f"{lon_d}°{lon_m}'{lon_s}\"E, {lat_d}°{lat_m}'{lat_s}\"N\n(x=232, y=466)",
        horizontalalignment='center', verticalalignment='top', linespacing=1.1,
        fontsize=HEADER_FONT_SIZE, color=TEXT_NAVY, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH,)
    fig.text(3 / IMG_W, 1 - 2 / IMG_H, f"wschód słońca: {sunrise}\nzachód słońca: {sunset}",
        horizontalalignment='left', verticalalignment='top', multialignment='center', linespacing=1.1,
        fontsize=HEADER_FONT_SIZE, color=TEXT_NAVY, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH,)
    fig.text(1 - 3 / IMG_W, 1 - 2 / IMG_H, "wysokość (min, środek, max)\n204 - 223 - 324 m",
        horizontalalignment='right', verticalalignment='top', multialignment='center', linespacing=1.1,
        fontsize=HEADER_FONT_SIZE, color=TEXT_NAVY, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH,)
    # Footer
    fig.text(20 / IMG_W, 7 / IMG_H, "meteo@icm.edu.pl",
        horizontalalignment='left',
        fontsize=FOOTER_FONT_SIZE, color=TEXT_NAVY, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH,)
    fig.text(0.375, 7 / IMG_H, datetime.datetime.now(zoneinfo.ZoneInfo(tzname)).strftime('%F %T'),
        horizontalalignment='center',
        fontsize=RENDER_DT_FONT_SIZE, color=COLOR_RENDER_DT, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH,)
    fig.text(1 - 15 / IMG_W, 7 / IMG_H, f"© 2007-{datetime.datetime.now(datetime.UTC).year} ICM, Uniwersytet Warszawski",
        horizontalalignment='right',
        fontsize=FOOTER_FONT_SIZE, color=TEXT_NAVY, fontfamily=FONT_FAMILY, stretch=FONT_STRETCH,)


def style_panels(axes, forecast):
    # Apply shared formatting across all panels
    for is_first, is_last, (ix, ax) in more_itertools.mark_ends(enumerate(axes)):
        # Set the inner plotting area color
        ax.set_facecolor(COLOR_TRANSPARENT)
        bb_left, bb_bottom, bb_width, bb_height = ax.get_position().bounds
        padding = 0.0022 if ix == 4 else 0.0022 * 3
        ax.set_position([bb_left, bb_bottom + padding, bb_width, bb_height - 2 * padding])

        #ax.grid(True, linestyle='--', color='black', linewidth=0.5, zorder=1)
        ax.grid(True, linestyle=(0, (1, 2)), color='black', linewidth=1, zorder=1, antialiased=False)
        ax.tick_params(bottom=False, top=False, left=False, right=False, labeltop=is_first, labelbottom=is_last)

        # Hide x-axis text
        if not (is_first or is_last):
            ax.set_xticklabels([])

        ax.set_xlim(0, len(forecast.data.airtmp_point.data) - 1)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=3, offset=2))


def plot_circles(ax, *, x_ticks, y_data, radius, color, zorder):
    if np.size(x_ticks) == 0 or np.size(y_data) == 0:
        return
    from matplotlib.patches import Circle
    from matplotlib.collections import PatchCollection
    marker = Circle((0, 0), radius / DPI, snap=False)
    # Ustawiamy rozmiar w punktach (np. średnica 5 punktów)
    # Ponieważ używamy punktów jako jednostki rozmiaru, dajemy width = height
    coords = list(zip(x_ticks, y_data))

    pc = PatchCollection(
        [marker],
        facecolor=color,
        edgecolor='none',
        antialiased=True,
        offsets=coords,       # Pozycje punktów w jednostkach danych
        transOffset=ax.transData,  # Układ współrzędnych dla pozycji środków
        zorder=zorder,
        snap=False,
    )

    # 4. KLUCZ: Mówimy kolekcji, że kształt geometrii (wzorcowej elipsy)
    # jest zdefiniowany w punktach ekranowych (nie zależy od skali osi)
    pc.set_transform(ax.get_figure().dpi_scale_trans)

    # Dodajemy kolekcję do osi wykresu
    ax.add_collection(pc)


def render_temperature_panel(ax_temp, forecast: MeteoForecastEnvelope):
    x_ticks = np.arange(len(forecast.data.airtmp_point.data))

    ax_temp.yaxis.set_major_locator(ticker.MultipleLocator(5))

    ax_temp.vlines(
        x=x_ticks,
        ymin=forecast.data.grdtmp_min.data,
        ymax=forecast.data.grdtmp_max.data,
        colors=COLOR_TEMP_GROUND, linewidth=0.5, capstyle='butt', zorder=-1, aa=False)
    plot_circles(ax_temp, x_ticks=x_ticks, y_data=forecast.data.dwptmp_point.data, radius=2, color=COLOR_TEMP_DEW_PT, zorder=-2)

    # Pozostałe wykresy liniowe i wypełnienia
    ax_temp.plot(x_ticks, forecast.data.airtmp_point.data, color=COLOR_TEMP_AIR_PT, linewidth=1.5, zorder=-3)
    ax_temp.plot(x_ticks, forecast.data.wchill_point.data, color=COLOR_TEMP_WCHILL_PT, linewidth=1.5, zorder=-4)
    ax_temp.fill_between(x_ticks, forecast.data.airtmp_min.data, forecast.data.airtmp_max.data, color=COLOR_TEMP_AIR_RNG, linewidth=0, zorder=-5)
    ax_temp.fill_between(x_ticks, forecast.data.wchill_min.data, forecast.data.wchill_max.data, color=COLOR_TEMP_WCHILL_RNG, linewidth=0, zorder=-6)
    y_min, y_max = ax_temp.get_ylim()
    ax_temp.fill_between(x_ticks, y_min, 0, color=COLOR_TEMP_BELOW_0, linewidth=0, zorder=-10)
    ax_temp.set_ylim(y_min, y_max) # restore limits, because fill_between expands y axis range
    ax_temp_rhs = ax_temp.twinx()
    ax_temp_rhs.set_ylim(ax_temp.get_ylim())
    #ax_temp_rhs.set_yticks(ax_temp.get_yticks(), ax_temp.get_yticklabels())
    ax_temp_rhs.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax_temp_rhs.tick_params(axis='y', left=False, right=False)
    ax_temp.tick_params(axis='y', left=False, right=False)




def render_precip_panel(ax_main, forecast: MeteoForecastEnvelope):
    x_ticks = np.arange(len(forecast.data.airtmp_point.data))

    ax_hum = ax_main.twinx()
    ax_pcp = ax_main.twinx()

    ax_main.set_zorder(2)
    ax_hum.set_zorder(1)
    ax_pcp.set_zorder(0)

    num_total_segments = 5
    pcpt_ylim_clip = 5.1
    pcpt_ylim_max = 5.2
    max_pcpt = max(forecast.data.pcpttl_max.data)
    pcpt_ylim_multiplier = (1) if max_pcpt <= 5 else (4)
    ax_main.set_ylim(0, pcpt_ylim_max * pcpt_ylim_multiplier)
    ax_main.yaxis.set_major_locator(ticker.MultipleLocator(pcpt_ylim_multiplier))
    num_grid_segments = 5
    num_bottom_segments = 0
    ax_main.tick_params(axis='y', left=False, right=False)

    # setup ax_pcp to have the same scale as ax_main, but no labels
    ax_pcp.set_ylim(0, pcpt_ylim_max * pcpt_ylim_multiplier)
    ax_pcp.set_yticklabels([])
    ax_pcp.tick_params(axis='y', left=False, right=False)
    ax_pcp.set_facecolor(COLOR_TRANSPARENT)

    hum_data = forecast.data.realhum_aver.data
    min_hum = min(hum_data)
    max_hum = max(hum_data)
    hum_span = max_hum - min_hum
    if (hum_span / num_grid_segments) <= 5:
        step = 5
    else:
        step = 10
    hum_grid_min = np.floor(min_hum / step) * step
    hum_grid_max = np.ceil(max_hum / step) * step
    actual_segments = int((hum_grid_max - hum_grid_min) / step)
    while actual_segments < num_grid_segments:
        if hum_grid_min > 0:
            hum_grid_min -= step
            actual_segments += 1
        elif hum_grid_max < 100:
            hum_grid_max += step
            actual_segments += 1
        else:
            break
    total_hum_span = hum_grid_max - hum_grid_min
    grid_unit_value = total_hum_span / num_grid_segments
    y_lim_min = hum_grid_min - (num_bottom_segments * grid_unit_value)
    y_lim_max = y_lim_min + (num_total_segments * grid_unit_value) * pcpt_ylim_max / num_total_segments
    ax_hum.set_ylim(y_lim_min, y_lim_max)
    ax_hum.yaxis.set_major_locator(ticker.MultipleLocator(step))

    ax_hum.plot(x_ticks, hum_data, color=COLOR_HUMIDITY, linewidth=1.5, zorder=-4)
    ax_hum.tick_params(axis='y', left=False, right=False, colors=COLOR_HUMIDITY)

    pcpt_max_clip_mask = np.asarray(forecast.data.pcpttl_max.data) >= (pcpt_ylim_multiplier * pcpt_ylim_clip)
    plot_circles(ax_pcp, x_ticks=x_ticks[pcpt_max_clip_mask], y_data=[pcpt_ylim_clip] * pcpt_max_clip_mask.sum(), radius=2, color=COLOR_PCPT_MAX, zorder=-2)
    pcpt_colors = [PCPT_TO_COLOR[v] for v in forecast.data.pcpttl_type_max.data]
    ax_pcp.vlines(
        x=x_ticks,
        ymax=np.clip(forecast.data.pcpttl_max.data, max=pcpt_ylim_multiplier * pcpt_ylim_clip),
        ymin=0, colors=pcpt_colors, linewidth=0.5, capstyle='butt', zorder=-1, aa=False)
    ax_pcp.bar(
        x_ticks,
        forecast.data.pcpttl_aver.data,
        color=pcpt_colors, width=1.0, edgecolor='none', align='center', zorder=-1)
    # TODO: burza, opad konwekcyjny


def render_press_panel(ax_hpa, forecast: MeteoForecastEnvelope):
    x_ticks = np.arange(len(forecast.data.airtmp_point.data))
    ax_mmhg = ax_hpa.twinx()

    ax_hpa.plot(x_ticks, np.asarray(forecast.data.slpres_point.data) / 100, color=COLOR_SLPRES, linewidth=1.5, zorder=-4)

    # ax_hpa.yaxis.set_major_locator(ticker.MaxNLocator(steps=[5, 10], min_n_ticks=3, nbins='auto')) # nbins = max, 6 for meteo
    # ax_mmhg.yaxis.set_major_locator(ticker.MaxNLocator(steps=[5, 10], min_n_ticks=3, nbins='auto')) # nbins = max, 6 for meteo
    ax_hpa.yaxis.set_major_locator(ticker.MaxNLocator(steps=[2, 5, 10], min_n_ticks=3, nbins=4)) # nbins = max, 6 for meteo
    ax_mmhg.yaxis.set_major_locator(ticker.MaxNLocator(steps=[2, 5, 10], min_n_ticks=3, nbins=4)) # nbins = max, 6 for meteo

    ax_hpa.tick_params(axis='y', left=False, right=False)
    ax_mmhg.tick_params(axis='y', left=False, right=False)

    y_min, y_max = ax_hpa.get_ylim()
    press_data = np.asarray(forecast.data.slpres_point.data) / 100
    for xi, (this, before, after) in zip(
        x_ticks,
        more_itertools.take(
            len(press_data),
            more_itertools.stagger(press_data, offsets=(0, -1, +1), longest=True))
    ):
        before = this if before is None else before
        after = this if after is None else after
        x_segment = [xi - 0.5, xi, xi + 0.5]
        y_segment = [0.5 * (before + this), this, 0.5 * (this + after)]

        color = PRES_TO_COLOR[libmath.floor_to_odd(this)]
        ax_hpa.fill_between(
            x_segment,
            y_segment,
            y_min,
            color=color,
            edgecolor=color, # Zapobiega powstawaniu mikroszczelin między segmentami
            linewidth=0.5,
            zorder=-5,
        )
    ax_hpa.set_ylim(y_min, y_max) # restore limits, because fill_between expands y axis range

    ax_mmhg.set_ylim(y_min, y_max)
    ax_mmhg.yaxis.set_major_formatter(lambda hpa, _: f'{hpa / 1.3332:.0f}')


def render_wind_panel(ax_ms, forecast: MeteoForecastEnvelope):
    x_ticks = np.arange(len(forecast.data.airtmp_point.data))
    ax_kmh = ax_ms.twinx()

    speed_ms = np.asarray(forecast.data.wind10_sd_true_prev_point.data)
    gust_ms = np.asarray(forecast.data.wind_gust_max.data)
    # speed_kmh = speed_ms / 3.6
    # gust_kmh = gust_ms / 3.6

    ax_ms.plot(x_ticks, speed_ms, color=COLOR_WIND_SPEED, linewidth=1.5, zorder=-4)

    ax_ms.tick_params(axis='y', left=False, right=False)
    ax_kmh.tick_params(axis='y', left=False, right=False)

    ax_ms.hlines(
        y=gust_ms,
        xmin=x_ticks - 0.43,
        xmax=x_ticks + 0.43,
        colors=COLOR_WIND_GUST, linewidth=0.5, capstyle='butt', zorder=-1, aa=False, joinstyle='bevel')

    ax_ms.yaxis.set_major_locator(ticker.MaxNLocator(steps=[2, 5], min_n_ticks=4, nbins='auto')) # nbins = max, 6 for meteo

    for xi, (this, before, after) in zip(
        x_ticks,
        more_itertools.take(
            len(speed_ms),
            more_itertools.stagger(speed_ms, offsets=(0, -1, +1), longest=True))
    ):
        before = this if before is None else before
        after = this if after is None else after
        x_segment = [xi - 0.5, xi, xi + 0.5]
        y_segment = [0.5 * (before + this), this, 0.5 * (this + after)]

        color = SPEED_TO_COLOR[libmath.floor(this)]
        ax_ms.fill_between(
            x_segment,
            y_segment,
            0,
            color=color,
            edgecolor=color, # Zapobiega powstawaniu mikroszczelin między segmentami
            linewidth=0.5,
            zorder=-5,
        )

    y_min, y_max = ax_ms.get_ylim()
    y_min = 0
    ax_ms.set_ylim(y_min, y_max) # restore limits, because fill_between expands y axis range

    ax_kmh.set_ylim(y_min, y_max)
    ax_kmh.yaxis.set_major_formatter(lambda kmh, _: f'{kmh * 3.6:.0f}')
    ax_kmh.yaxis.set_major_locator(ticker.MaxNLocator(steps=[2, 5], min_n_ticks=4, nbins='auto')) # nbins = max, 6 for meteo


from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.transforms import Affine2D

def plot_wind_arrows(ax, *, x_ticks, wdir_deg, color='black', zorder=3):
    if np.size(x_ticks) == 0 or np.size(wdir_deg) == 0:
        return

    # Base arrow geometry centered at (0, 0) pointing RIGHT (0° math angle)
    # Units are inches (matching fig.dpi_scale_trans)
    L = 7.5 / DPI   # Half-length of shaft
    hw = 2.0 / DPI  # Half-width of arrowhead
    hl = 5.0 / DPI  # Length of arrowhead

    verts = [
        (-L, 0),
        (L, 0),
        (L - hl, hw),
        (L, 0),
        (L - hl, -hw),
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
    ]
    base_path = Path(verts, codes)

    patches = []
    coords = []

    for xi, deg in zip(x_ticks, wdir_deg):
        if np.isnan(deg):
            continue
        # Convert meteorological degrees (0=down, 90=left, 180=up, 270=right) to math angle
        math_deg = 270.0 - deg
        rotated_path = base_path.transformed(Affine2D().rotate_deg(math_deg))
        patches.append(PathPatch(rotated_path))
        coords.append((xi, 0))

    if not patches:
        return

    pc = PatchCollection(
        patches,
        facecolor=color,
        edgecolor=color,
        linewidth=0.75,
        capstyle='butt',
        joinstyle='miter',
        antialiased=True,
        offsets=coords,
        transOffset=ax.transData,
        zorder=zorder,
    )

    # Geometry is in inches, scaled to display pixels independent of axis aspect ratio
    pc.set_transform(ax.get_figure().dpi_scale_trans)
    pc.set_clip_on(False)
    ax.add_collection(pc)


def render_wind_dir_panel(ax_dir, forecast: MeteoForecastEnvelope):
    x_ticks = np.arange(len(forecast.data.airtmp_point.data))
    wdir = forecast.data.wind10_dr_deg_true_prev_point.data

    plot_wind_arrows(ax_dir, x_ticks=x_ticks, wdir_deg=wdir, color=COLOR_WIND_ARROW, zorder=3)

    ax_dir.set_ylim(-1, +1)
    ax_dir.yaxis.set_major_locator(ticker.NullLocator())
    ax_dir.tick_params(axis='y', left=False, right=False, labelleft=False, labelright=False)


def render_cloud_cover_panel(ax_main, forecast: MeteoForecastEnvelope):
    x_ticks = np.arange(len(forecast.data.airtmp_point.data))

    ax_c = ax_main.twinx()
    ax_c.set_facecolor(COLOR_CLOUD_BG)

    ax_vis = ax_main.twinx()

    ax_main.set_zorder(2)
    ax_vis.set_zorder(1)
    ax_c.set_zorder(0)

    grid_levels = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    cloud_ticks = np.array([0.0, 0.5, 2.0, 7.0, 15.0])
    vis_ticks = np.array([0.0, 1.0, 5.0, 20.0, 100.0])

    vis_data = np.array(forecast.data.visibl_min.data) / 1000
    vis_xform = np.interp(vis_data, vis_ticks, grid_levels)

    cldtop_xform = np.interp(forecast.data.cldtop.data, cloud_ticks, grid_levels)
    cldbse01_xform = np.interp(forecast.data.cldbse01.data, cloud_ticks, grid_levels)
    cldbse25_xform = np.interp(forecast.data.cldbse25.data, cloud_ticks, grid_levels)
    cldbse45_xform = np.interp(forecast.data.cldbse45.data, cloud_ticks, grid_levels)
    cldbse65_xform = np.interp(forecast.data.cldbse65.data, cloud_ticks, grid_levels)
    cldbse79_xform = np.interp(forecast.data.cldbse79.data, cloud_ticks, grid_levels)

    # setup lhs labels on ax_main for the grid
    ax_main.set_ylim(0, 4)
    ax_main.yaxis.set_major_locator(ticker.FixedLocator(grid_levels))
    ax_main.yaxis.set_major_formatter(ticker.FixedFormatter([f'{v:.1f}' for v in cloud_ticks]))
    ax_main.tick_params(axis='y', left=False, right=False, colors='black')

    # setup ax_c to have the same scale as ax_main, but no labels
    ax_c.set_ylim(0, 4)
    ax_c.set_yticklabels([])
    ax_c.tick_params(axis='y', left=False, right=False)

    # setup ax_fog to have rhs labels
    ax_vis.set_ylim(0, 4)
    ax_vis.yaxis.set_major_locator(ticker.FixedLocator(grid_levels))
    ax_vis.yaxis.set_major_formatter(ticker.FixedFormatter([f'{v:.0f}' for v in vis_ticks]))
    ax_vis.tick_params(axis='y', left=False, right=False, colors=COLOR_VIS_LABEL)

    ax_vis.plot(x_ticks, vis_xform, color=COLOR_VISIBILITY, linewidth=1.5, zorder=-1)

    radius = 3
    plot_circles(ax=ax_c, x_ticks=x_ticks, y_data=cldbse79_xform, radius=radius, color=COLOR_CLOUD_BASE_79, zorder=-2)
    plot_circles(ax=ax_c, x_ticks=x_ticks, y_data=cldbse65_xform, radius=radius, color=COLOR_CLOUD_BASE_65, zorder=-3)
    plot_circles(ax=ax_c, x_ticks=x_ticks, y_data=cldbse45_xform, radius=radius, color=COLOR_CLOUD_BASE_45, zorder=-4)
    plot_circles(ax=ax_c, x_ticks=x_ticks, y_data=cldbse25_xform, radius=radius, color=COLOR_CLOUD_BASE_25, zorder=-5)
    plot_circles(ax=ax_c, x_ticks=x_ticks, y_data=cldbse01_xform, radius=radius, color=COLOR_CLOUD_BASE_01, zorder=-6)
    plot_circles(ax=ax_c, x_ticks=x_ticks, y_data=cldtop_xform, radius=radius, color=COLOR_CLOUD_TOP, zorder=-7)


def render_cloud_height_panel(ax_main, forecast: MeteoForecastEnvelope):
    x_ticks = np.arange(len(forecast.data.airtmp_point.data))

    '''Visual requirement is to have a grid on the top, then fog plot below,
    and cloud plot at the bottom.
    The only way to satisfy this is to derive two axes from ax_main, re-order
    their zorder to have main > fog > cloud, on ax_main plot only grid and lhs labels,
    on ax_fog plot fog data and rhs labels, and on ax_c plot cloud data and no labels
    '''
    ax_c = ax_main.twinx()
    ax_c.set_facecolor(COLOR_CLOUD_BG) # it will go to the bottom, hence it has facecolor set

    ax_fog = ax_main.twinx()

    ax_main.set_zorder(2)
    ax_fog.set_zorder(1)
    ax_c.set_zorder(0)

    # setup lhs labels on ax_main for the grid
    ax_main.set_ylim(0, 8)
    ax_main.yaxis.set_major_locator(ticker.FixedLocator([0, 2, 4, 6, 8]))
    ax_main.tick_params(axis='y', left=False, right=False, colors='black')

    # setup ax_c to have the same scale as ax_main, but no labels
    ax_c.set_ylim(0, 8)
    ax_c.set_yticklabels([])
    ax_c.tick_params(axis='y', left=False, right=False)

    # setup ax_fog to have rhs labels
    ax_fog.set_ylim(0, 1)
    fog_ticks = [0, 0.25, 0.5, 0.75, 1]
    ax_fog.yaxis.set_major_locator(ticker.FixedLocator(fog_ticks))
    ax_fog.yaxis.set_major_formatter(ticker.FixedFormatter([f'{v}' for v in fog_ticks]))
    ax_fog.tick_params(axis='y', left=False, right=False, colors=COLOR_FOG_LABEL)

    ax_fog.bar(
        x_ticks,
        forecast.data.fog_max.data,
        color=COLOR_FOG_BAR, width=0.5, edgecolor='none', align='center', zorder=-4, aa=True)

    cld_factor = 8
    cld_high = cld_factor * np.asarray(forecast.data.cldhigh_aver.data)
    cld_med = cld_factor * np.asarray(forecast.data.cldmed_aver.data)
    cld_low = cld_factor * np.asarray(forecast.data.cldlow_aver.data)
    cld_vlow = cld_factor * np.asarray(forecast.data.cldvlow_aver.data)

    ax_c.plot(x_ticks, cld_high, color=COLOR_CLOUD_HIGH, linewidth=1, zorder=-1)
    ax_c.plot(x_ticks, cld_med, color=COLOR_CLOUD_MED, linewidth=1, zorder=-2)
    ax_c.plot(x_ticks, cld_low, color=COLOR_CLOUD_LOW, linewidth=1, zorder=-3)
    ax_c.plot(x_ticks, cld_vlow, color=COLOR_CLOUD_VLOW, linewidth=1, zorder=-4)
    ax_c.fill_between(x_ticks, 0, cld_vlow, color=COLOR_CLOUD_VLOW, linewidth=0, zorder=-10)
    ax_c.fill_between(x_ticks, 0, cld_low, color=COLOR_CLOUD_LOW, linewidth=0, zorder=-11)
    ax_c.fill_between(x_ticks, 0, cld_med, color=COLOR_CLOUD_MED, linewidth=0, zorder=-12)
    ax_c.fill_between(x_ticks, 0, cld_high, color=COLOR_CLOUD_HIGH, linewidth=0, zorder=-13)


def render_x_labels(top_ax, bottom_ax, forecast, tzname):
    n_xpoints = len(forecast.data.airtmp_point.data)
    ts_utc_start: int = forecast.data.airtmp_point.first_timestamp
    ts_utc_delta: int = forecast.data.airtmp_point.interval
    start_dt = datetime.datetime.fromtimestamp(ts_utc_start, tz=zoneinfo.ZoneInfo(tzname))
    end_dt = datetime.datetime.fromtimestamp(ts_utc_start + n_xpoints * ts_utc_delta, tz=zoneinfo.ZoneInfo(tzname))

    def local_formatter(x, pos):
        dt = datetime.datetime.fromtimestamp(ts_utc_start + ts_utc_delta * x, tz=zoneinfo.ZoneInfo(tzname))
        dt_utc = datetime.datetime.fromtimestamp(ts_utc_start + ts_utc_delta * x, tz=datetime.timezone.utc)
        if pos % 2 == 1:
            return f'{dt.hour:02d}'
        elif dt_utc.hour == 12:
            with liblocale.temporary_locale(locale.LC_TIME, 'pl_PL.UTF-8') as _:
                return f'{dt.strftime("%a")}, {dt.day:02d}.{dt.month:02d}\n'
    top_xaxis = top_ax.xaxis
    top_xaxis.set_tick_params(length=0)
    top_xaxis.set_major_formatter(local_formatter)
    start_tzname = start_dt.strftime('%Z')
    end_tzname = end_dt.strftime('%Z')
    top_ax.text(-3.25, 1.00, start_tzname,
        transform=top_ax.get_xaxis_transform(),
        ha='center', va='bottom', color='black',
        clip_on=False)
    top_ax.text(n_xpoints + 2.25, 1.00, end_tzname,
        transform=top_ax.get_xaxis_transform(),
        ha='center', va='bottom', color='black',
        clip_on=False)

    # for label in axes[0].get_xticklabels():
    #     label.set_bbox(dict(facecolor='none', edgecolor='tab:orange', linewidth=0.6, boxstyle='square,pad=0'))
    #     ## Optional: inspect exact (x, y) anchor coordinates in axis/data space
    #     print(label.get_text(), label.get_position(), label.get_ha(), label.get_va(), label.get_c)

    def utc_formatter(x, pos):
        dt = datetime.datetime.fromtimestamp(ts_utc_start + ts_utc_delta * x, tz=datetime.timezone.utc)
        if pos % 2 == 1:
            return f'{dt.hour:02d}'
        elif dt.hour == 12:
            return f'\n{dt.day:02d}.{dt.month:02d}'
    bottom_xaxis = bottom_ax.xaxis
    bottom_xaxis.set_tick_params(length=0, pad=3.5)
    bottom_xaxis.set_major_formatter(utc_formatter)
    bottom_ax.text(-3.25, -0.062, 'UTC',
        transform=bottom_ax.get_xaxis_transform(),
        ha='center', va='top', color='black',
        clip_on=False)
    bottom_ax.text(n_xpoints + 2.25, -0.062, 'UTC',
        transform=bottom_ax.get_xaxis_transform(),
        ha='center', va='top', color='black',
        clip_on=False)
    # top_ax.text(len(forecast.data.airtmp_point.data) + 2.25, 1.00, 'CET',
    #     transform=top_ax.get_xaxis_transform(),
    #     ha='center', va='bottom', color='black',
    #     clip_on=False)


def render_day_night_bands(ax_top, ax_bottom, forecast):
    # collect all unique days spanning the forecast
    n_xpoints = len(forecast.data.airtmp_point.data)
    n_xranges = n_xpoints - 1
    ts_utc_start: float = forecast.data.airtmp_point.first_timestamp
    ts_utc_delta: float = forecast.data.airtmp_point.interval
    ts_span = ts_utc_delta * n_xranges
    ts_utc_end: float = ts_utc_start + ts_utc_delta * n_xranges

    lat = forecast.data.airtmp_point.point.lat
    lon = forecast.data.airtmp_point.point.lon

    astral_set = set()
    for x in range(n_xpoints):
        sol_data = get_astral_sun(lat, lon, datetime.datetime.fromtimestamp(ts_utc_start + x * ts_utc_delta, tz=datetime.timezone.utc))
        astral_set.add((sol_data['sunrise'], sol_data['sunset']))
    astrals = sorted(astral_set)
    #print(astrals)
    intervals = []
    def to_x(dt):
        return (dt.timestamp() - ts_utc_start) / ts_span * n_xranges
    for d1, d2 in more_itertools.stagger(astrals, (-1, 0), longest=True):
        if d1 is None:
            # d2 is the first day in sequence
            sunrise, sunset = d2
            midnight = datetime.datetime.combine(sunrise.date(), datetime.time.min, tzinfo=sunrise.tzinfo)
            intervals.append((to_x(midnight), to_x(sunrise), True))
        elif d2 is None:
            # d1 is the last day in sequence
            sunrise, sunset = d1
            midnight = datetime.datetime.combine(sunrise.date(), datetime.time.min, tzinfo=sunrise.tzinfo) + datetime.timedelta(days=1)
            intervals.append((to_x(sunrise), to_x(sunset), False))
            intervals.append((to_x(sunset), to_x(midnight), True))
        else:
            sunrise1, sunset1 = d1
            sunrise2, sunset2 = d2
            intervals.append((to_x(sunrise1), to_x(sunset1), False))
            intervals.append((to_x(sunset1), to_x(sunrise2), True))
    #print(intervals)

    from matplotlib.patches import Rectangle
    from matplotlib.transforms import blended_transform_factory

    fig = ax_top.get_figure()
    # X in data coordinates (time), Y in figure coordinates (0..1)
    trans = blended_transform_factory(ax_top.transData, fig.transFigure)

    renderer = fig.canvas.get_renderer()
    pos_top = ax_top.get_position()
    pos_bot = ax_bottom.get_position()

    # Get the exact top of the top X-tick labels and bottom of the bottom X-tick labels in figure coordinates
    top_bboxes = [lbl.get_window_extent(renderer) for lbl in ax_top.get_xticklabels() if lbl.get_text()]
    bot_bboxes = [lbl.get_window_extent(renderer) for lbl in ax_bottom.get_xticklabels() if lbl.get_text()]

    y_top_fig = max(b.y1 for b in top_bboxes) / fig.bbox.height if top_bboxes else pos_top.y1
    y_bot_fig = min(b.y0 for b in bot_bboxes) / fig.bbox.height if bot_bboxes else pos_bot.y0
    for x_start, x_end, is_night in intervals:
        x_start = np.clip(x_start, 0, n_xranges)
        x_end = np.clip(x_end, 0, n_xranges)
        if x_start == x_end:
            continue
        #print(f'plot {x_start:.2f} - {x_end:.2f} | {int(is_night)}')
        color = COLOR_VBAR_NIGHT if is_night else COLOR_VBAR_DAY
        rect = Rectangle(
            (x_start, y_bot_fig),
            width=(x_end - x_start),
            height=(y_top_fig - y_bot_fig),
            transform=trans,
            facecolor=color,
            edgecolor='none',
            zorder=-20,
        )
        fig.patches.append(rect)


def make_charts(forecast: MeteoForecastEnvelope, *, tzname='Europe/Warsaw', chart_locale=('pl_PL', 'UTF-8')) -> bytes:
    ts_utc_start: int = forecast.data.airtmp_point.first_timestamp
    start_dt = datetime.datetime.fromtimestamp(ts_utc_start, tz=zoneinfo.ZoneInfo(tzname))

    setup_rc_styles()

    # Create a figure mimicking the narrow, tall aspect ratio of the images
    fig = plt.figure(figsize=(IMG_W / DPI, IMG_H / DPI), dpi=DPI)

    fig.patch.set_facecolor(CANVAS_BG)

    fig.subplots_adjust(left=62.5 / IMG_W, right=1 - 62.5 / IMG_W, top=0.92, bottom=0.08)

    lat = forecast.data.airtmp_point.point.lat
    lon = forecast.data.airtmp_point.point.lon
    render_header_footer(fig, lat=lat, lon=lon, start_dt=start_dt, tzname=tzname)

    axes = make_axes(fig)
    render_side_labels(axes)

    style_panels(axes, forecast)

    render_temperature_panel(axes[0], forecast)
    render_precip_panel(axes[1], forecast)
    render_press_panel(axes[2], forecast)
    render_wind_panel(axes[3], forecast)
    render_wind_dir_panel(axes[4], forecast)
    render_cloud_cover_panel(axes[5], forecast)
    render_cloud_height_panel(axes[6], forecast)

    render_x_labels(axes[0], axes[-1], forecast, tzname)

    render_day_night_bands(axes[0], axes[-1], forecast)

    bio = io.BytesIO()
    plt.savefig(bio, dpi=DPI, facecolor=fig.get_facecolor())

    bio.seek(0)
    return bio.read()
