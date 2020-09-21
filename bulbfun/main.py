import requests
import time
import logging
from datetime import datetime

from yeelight import Bulb, discover_bulbs

stop_running_after = 5*60

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

category_colors = [
    ((255, 255, 255), 100),
    ((0, 255, 0), 100),		# good
    ((255, 155, 0), 100),	# moderate
    ((255, 70, 0), 100),	# unhealthy for sensitive groups
    ((255, 0, 0), 80),		# unhealthy
    ((120, 0, 255), 100),	# hazardous
    ((255, 0, 140), 30),
]


def main():

    # Look for the bulb and keep trying if it's not found.
    # Assume five minutes between the job being kicked off again.
    start = datetime.now()
    bulbs = discover_bulbs()
    while not len(bulbs):
        time.sleep(2)
        if (datetime.now() - start).total_seconds() > stop_running_after:
            return
        bulbs = discover_bulbs()
    logger.info(bulbs)
    bulb_ip = bulbs[0]['ip']
    bulb = Bulb(bulb_ip)

    try:
        aqi_obj = requests.get('http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=94702&distance=1&API_KEY=E1C86A95-8F32-4EA5-8243-E19677A0550F').json()
        logger.info(aqi_obj)
        pm25 = aqi_obj[1]
        category = pm25['Category']['Number']
    except:
        category = 0

    (r, g, b), brightness = category_colors[category]
    bulb.set_rgb(r, g, b)
    bulb.set_brightness(brightness)


if __name__ == '__main__':
    main()

