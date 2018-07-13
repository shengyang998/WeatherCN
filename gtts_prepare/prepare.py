from gtts import gTTS
import logging
import os

logger = logging.getLogger(__name__)


def prepare(time=0.5, status="雨", base_path="voices/"):
    """

    :param time: Int
    :param status: String
    :param base_path: String
    :return: path to voice
    """
    t = ""
    if time < 0.5:
        t = "很快就"
    elif 0.5 <= time < 1:
        t = "半个小时后"
    elif 1 <= time < 2:
        t = "一个小时后"
    elif 2 <= time:
        t = "两个小时后"
    else:
        t = "位置时间内"
        logger.error("Unknown Time")

    s = ""
    if status == "雨":
        s = "下雨"
    elif status == "多云":
        s = "多云"
    elif status == "晴":
        s = "晴天"
    else:
        s = "未知天气"
        logger.error("Unknown Weather")

    statement = t + "要" + s + "啦！"
    filename = "{0}_{1}.mp3".format(t, s)

    tts = gTTS(text=statement, lang='zh-cn')
    tts.save("{0}{1}".format(base_path, filename))

    return "{0}{1}".format(base_path, filename)


def say(s, base_path="voices/"):
    if s == "":
        return

    filename = s + ".mp3"
    if not os.path.isfile("{0}{1}".format(base_path, filename)):
        tts = gTTS(text=s, lang='zh-cn')
        tts.save("{0}{1}".format(base_path, filename))
    os.system("mpg123 {0}".format(base_path + filename))
