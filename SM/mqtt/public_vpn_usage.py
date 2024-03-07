from bs4 import BeautifulSoup
from paho.mqtt import client as mqtt_client
import requests
import time
import simplejson
import re
import random

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4083.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

broker = "192.168.31.135"
port = 1883
topic = "home/nodes/sensor/py-script/monitor"
username = "homeassistant"
password = "deiTh6ui3ahsoh7chaijoshei1aiMah1ahGeengath8Feiw7hei3aiz5Tieph7Ae"
use_tls = False


# broker = "x9dbae5a.ala.cn-hangzhou.emqxsl.cn"
# port = 8883
# topic = "homeassistant/traffic"
# use_tls = True
# username = "pi"
# password = "pi"
# cert_path = "./emqxsl-ca.crt"
# cert_path = "/Users/bytedance/Documents/studyNode/SM/mqtt/emqxsl-ca.crt"

# generate client ID with pub prefix randomly
client_id = f"python-mqtt-{random.randint(0, 1000)}"
# discover info
discover_tipic = 'homeassistant/sensor/rpi-hostname/'
identifiers = 'python-pvu'

def login(mail, passwd):
    login_url = "https://w1.v2ai.top/auth/login"
    login_data = {"email": mail, "passwd": passwd, "remember_me": "week"}

    # ignore error verify = False
    requests.packages.urllib3.disable_warnings()
    # login
    login_session = requests.session()
    res = login_session.post(
        url=login_url, data=login_data, headers=headers, verify=False
    )
    print("用户 " + mail + " " + (simplejson.loads(res.text)["msg"]).split("(")[0])
    return login_session


def get_user_useage(login_session):
    span_map = {"剩余流量": "surplus", "过去已用": "past_used", "今日已用": "today_used"}
    usage_info = {}
    get_user_resp = login_session.get(
        url="https://w1.v2ai.top/user", headers=headers, allow_redirects=False
    )
    print(get_user_resp)
    if get_user_resp.status_code != 200:
        return usage_info
    html_text = get_user_resp.text
    soup = BeautifulSoup(html_text, "html.parser")
    user_info_div = soup.find("div", {"class": "user-info-main"})
    divs = user_info_div.find_all("a", {"href":"/user/trafficlog"})
    #<a href="/user/trafficlog" class="tag-green">544.82MB</a>
    if len(divs) == 3:
        usage_info['surplus'] = convert_to_bytes(divs[0].text)
        usage_info['today_used'] = convert_to_bytes(divs[1].text)
        usage_info['past_used'] = convert_to_bytes(divs[2].text)
        usage_info["total"] = (
            usage_info["surplus"] + usage_info["past_used"] + usage_info["today_used"]
        )
    usage_info["timestamp"] = int(time.time())
    return usage_info


def convert_to_bytes(size_str):
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    size_regex = re.compile(r"([\d.]+)\s*(\w{1,2})B?", re.IGNORECASE)
    match = size_regex.match(size_str)
    if match:
        size, unit = match.groups()
        return float(size) * units[unit.upper()] / 1024**2
    else:
        raise ValueError("Invalid size string")


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    if use_tls:
        client.tls_set(ca_certs=cert_path)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def auto_public_usage(session, client):
    while True:
        # register_discover(mqtt_client)
        # time.sleep(1)
        msg = get_user_useage(session)
        put_msg = {"info":msg}
        result = client.publish(topic, simplejson.dumps(put_msg))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{put_msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        time.sleep(30)


def register_discover(client):
    sensors = ["surplus", "past_used", "today_used", "total"]

    for sensor in sensors:
        sensor_data = {
            "unit_of_measurement": "MB",
            "stat_t": topic,
            "ic": "mdi:vpn",
            "dev": {"identifiers": [identifiers],"manufacturer": "sst script", "name": "VPN traffic usage", "model": "RPi 4 Model B r1.2", "sw_version": "bullseye 6.1.21-v8+"},
        }
        sensor_data['name'] = f'{sensor} of vpn usage'
        sensor_data['uniq_id'] = identifiers + "_"+sensor
        sensor_data['val_tpl'] = "{{ value_json.info."+sensor+" }}"
        public_topic = f'{discover_tipic}{sensor}/config'
        result = client.publish(public_topic, simplejson.dumps(sensor_data))
        status = result[0]
        if status == 0:
            print(f"Register `{sensor_data}` to topic `{public_topic}`")
        else:
            print(f"Failed to register to topic {public_topic}")


if __name__ == "__main__":
    data = {"mail": "1970139084@qq.com", "passwd": "445247721jc"}
    login_session = login(data["mail"], data["passwd"])
    mqtt_client = connect_mqtt()
    mqtt_client.loop_start()
    register_discover(mqtt_client)
    auto_public_usage(login_session, mqtt_client)
    # usage = get_user_useage(login_session)
    # print(usage)
    # print('login time', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
