from requests import get
from ctypes import windll
from time import ctime
from os import getcwd
from datetime import datetime


conditions = {  # possible weather condition codes and corresponding background images
    ("0", "1"): r'\sunny.jpg',
    "2": r'\cloudy.jpg',
    "3": r'\overcast.jpg',
    ("45", "48"): r'\fog.jpg',
    ("51", "53", "55", "56", "57", "61", "66", "80"): r'\rain.jpg',
    ("63", "65", "67", "81", "82"): r'\heavy_rain.jpg',
    ("95", "96", "99"): r'\thunderstorm.jpg',
    ("71", "73", "75", "77", "85", "86"): r'\snow.jpg'
}


def get_location() -> tuple[str, str]:  # get current city from IP address
    response = get('https://ipapi.co/json').json()
    return str(response['latitude']), str(response['longitude'])


initial_path = getcwd() + r"\background_photos"
WALLPAPER_STYLE = 1
SPI_SETDESKWALLPAPER = 20
lat, lon = get_location()


def get_code() -> str:  # collect weather condition code from API
    response = get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=weather_code').json()
    return str(response['current']['weather_code'])


code = get_code()


def background_id() -> str:  # uses returned condition code from pull_weather() to pull image name from conditions
    for key in conditions.keys():
        if code in key:
            return conditions[key]


def daytime() -> bool:  # determines day or night
    response = get(f"https://api.sunrisesunset.io/json?lat={lat}&lng={lon}&time_format=24").json()
    sunrise = datetime.strptime(response['results']['sunrise'], "%H:%M:%S")
    sunset = datetime.strptime(response['results']['sunset'], "%H:%M:%S")
    current_time = datetime.strptime(ctime()[11:19], "%H:%M:%S")
    return sunrise < current_time < sunset


def set_wallpaper() -> None:  # sets system wallpaper
    if daytime():
        wallpaper_path = initial_path + background_id()
    else:
        wallpaper_path = initial_path + r'\nighttime.jpg'
    windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper_path, WALLPAPER_STYLE)


set_wallpaper()
