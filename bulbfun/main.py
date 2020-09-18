import requests
import logging
from yeelight import Bulb, discover_bulbs

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
    try:
        aqi_obj = requests.get('http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=94702&distance=1&API_KEY=E1C86A95-8F32-4EA5-8243-E19677A0550F').json()
        logger.info(aqi_obj)
        pm25 = aqi_obj[1]
        category = pm25['Category']['Number']
    except:
        category = 0

    bulbs = discover_bulbs()
    logger.info(bulbs)
    bulb_ip = bulbs[0]['ip']

    bulb = Bulb(bulb_ip)

    (r, g, b), brightness = category_colors[category]
    bulb.set_rgb(r, g, b)
    bulb.set_brightness(brightness)


if __name__ == '__main__':
    main()

