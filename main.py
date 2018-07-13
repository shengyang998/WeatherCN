import os
import logging
from lxml import etree
import urllib3
import json
import re
from time import sleep
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, filename="log", format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
logger = logging.getLogger(__name__)

from gtts_prepare import prepare


def extract_first(html, xpath_str):
    """

    :param html: html elements of lxml
    :param xpath_str: xpath string
    :return: string
    """
    r = html.xpath(xpath_str)
    if len(r) > 0:
        return re.sub('\s', '', html.xpath(xpath_str)[0].strip())
    else:
        logger.warning("None detected!")
        return None


def get_loc_with_GPS_macos(path_to_whereami="/usr/local/bin/whereami"):
    loc = dict()
    with os.popen(path_to_whereami) as p:
        for line in p.readlines():
            li = [x.strip() for x in line.split(':')]
            desc = li[0]
            val = li[1]
            loc[desc] = val
    return loc


def get_loc_with_ip():
    loc = dict()
    __url = 'http://ipinfo.io/json'
    data = pull_json_parse(__url)
    loca = data['loc'].split(',')
    loc['Latitude'] = loca[0]
    loc['Longitude'] = loca[1]
    return loc


def get_loc():
    loc = dict()
    try:
        loc = get_loc_with_GPS_macos()
    except:
        loc = get_loc_with_ip()

    logger.info("Location: \nLatitude: {0}, Longitude: {1}, Accuracy (m): {2}, Timestamp: {3}".format(loc["Latitude"], loc["Longitude"], loc["Accuracy (m)"], loc["Timestamp"]))
    return loc


def pull_lxml_parse(url=""):
    """

    :param url: url that is going to pull
    :return: None or html elements of lxml
    """
    html_parsed = etree.HTML(pull(url))
    return html_parsed


def pull_json_parse(url=""):
    return json.loads(pull(url))


def pull(url=""):
    if url == "":
        logger.error("url is empty.")
        return None

    logger.info("pulling url: {0}".format(url))
    http = urllib3.PoolManager()
    html = http.request('GET', url)
    logger.info("html status: {0}".format(html.status))
    if html.status != 200:
        logger.error("Cannot get html data from: {0}".format(url))
        return None
    else:
        return html.data.decode('utf-8')


if __name__ == "__main__":
    normal_last_time = datetime.now() - timedelta(minutes=120)
    rainy_last_time = datetime.now()
    last_time = ""
    while True:
        loc = get_loc()

        _home_url = "http://e.weather.com.cn/d/town/index?lat={0}&lon={1}".format(loc["Latitude"], loc["Longitude"])
        _home_html = pull_lxml_parse(_home_url)

        time = extract_first(_home_html, "/html/body/div[1]/div[2]/div[1]/time/text()")[:-2]

        if not last_time == time:
            last_time = time
            location = extract_first(_home_html, "/html/body/div[1]/div[2]/div[1]/div/div/text()")
            degree = extract_first(_home_html, "/html/body/div[1]/div[2]/div[2]/h1/span/text()")
            wind = extract_first(_home_html, "/html/body/div[1]/div[2]/div[2]/h2/span[1]/text()")
            humidity = extract_first(_home_html, "/html/body/div[1]/div[2]/div[2]/h2/span[2]/text()")

            status = extract_first(_home_html, "/html/body/div[1]/div[2]/div[2]/h1/em/text()")

            _air_json_url = "http://e.weather.com.cn/p/custom/?lat={0}&lon={1}".format(loc["Latitude"], loc["Longitude"])
            _air_html = pull(_air_json_url)[13:-3]
            logger.debug(_air_html)
            air = json.loads(_air_html)['result']['air']
            air_aqi = air['aqi']
            air_lev = air['level']

            _detail_json_url = "http://d3.weather.com.cn/webgis_rain_new/webgis/minute?lat={0}&lon={1}".format(loc["Latitude"], loc["Longitude"])
            status_desc = pull_json_parse(_detail_json_url)['msg']

            if (not "不会下雨" in status_desc) or "雨" in status_desc or "雨" in status:
                rainy_last_time = datetime.now()
                prepare.say("您好，请注意：")
                prepare.say("{0}附近".format(location))
                prepare.say("{0}".format(status_desc))
            
            if datetime.now() - normal_last_time > timedelta(minutes=120):
                normal_last_time = datetime.now()
                prepare.say("您好，接下来播报")
                prepare.say("{0}附近".format(location))
                prepare.say("的天气情况，当前温度：")
                prepare.say("{0}摄氏度".format(degree))
                prepare.say("天气：{0}".format(status))
                prepare.say("{0}".format(wind))
                prepare.say("{0}".format(humidity))
                prepare.say("空气质量：{0}".format(air_lev))
                prepare.say("另外：{0}。".format(status_desc))
                prepare.say("感谢收听，再见。")

            sleep(900)  # 15mins
