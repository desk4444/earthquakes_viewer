import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
import requests
from earthquake_map import config


def fetch_and_save_yesterday_earthquakes():
    today_datetime = datetime.now(timezone.utc)
    yesterday_datetime = today_datetime - timedelta(1)
    today = today_datetime.strftime('%Y-%m-%d')
    yesterday = yesterday_datetime.strftime('%Y-%m-%d')

    params = {
            "format": "geojson",
            "starttime": yesterday,
            "endtime": today,
            "minmagnitude": config.MIN_MAGNITUDE,
    }

    response = requests.get(config.USGS_URL, params=params, timeout=30)
    response.raise_for_status()
    api_data = response.json()

    file_name = "{0}/{1}.geojson".format(config.DATA_DIR, yesterday)
    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(api_data, file, indent=2)

    return file_path
