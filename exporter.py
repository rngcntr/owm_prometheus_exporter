from prometheus_client import start_http_server, Gauge, Info
import requests
import time
import os


ENDPOINT = "https://api.openweathermap.org/data/2.5/weather?units=metric&lat={}&lon={}&appid={}"


if __name__ == '__main__':
    interval = int(os.environ.get("WEATHER2PROMETHEUS_INTERVAL", "30"))
    lat = os.environ.get("WEATHER2PROMETHEUS_LAT", "0")
    lon = os.environ.get("WEATHER2PROMETHEUS_LON", "0")
    apikey = os.environ.get("WEATHER2PROMETHEUS_APIKEY", "")

    main = Gauge("openweather_main", "Main weather data", ["key"])
    visibility = Gauge("openweather_visibility", "Visibility data")
    wind = Gauge("openweather_wind", "Wind data", ["key"])
    clouds = Gauge("openweather_clouds", "Cloud data", ["key"])
    sun = Gauge("openweather_sys", "Sun data", ["key"])
    info = Info("openweather", "General info")

    start_http_server(9001)

    while True:
        json = requests.get(ENDPOINT.format(lat, lon, apikey)).json()
        for key in json["main"]:
            main.labels(key).set(float(json["main"][key]))
        for key in json["wind"]:
            wind.labels(key).set(float(json["wind"][key]))
        for key in json["clouds"]:
            clouds.labels(key).set(float(json["clouds"][key]))
        sun.labels("rise").set(float(json["sys"]["sunrise"]))
        sun.labels("set").set(float(json["sys"]["sunset"]))
        visibility.set(float(json["visibility"]))
        collected_info = {
                "lon": str(json["coord"]["lon"]),
                "lat": str(json["coord"]["lat"]),
                "desc": str(json["weather"][0]["description"]),
                "dt": str(json["dt"]),
                "tz": str(json["timezone"]),
                "region": str(json["name"])
        }
        info.info(collected_info)

        time.sleep(interval)
