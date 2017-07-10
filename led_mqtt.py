# -*- coding: utf-8 -*- 
'''
led_mqtt.py
在micropython上使用mqtt，默认已经按照了mqtt库，在unix的micropyth无法import time
本程序改为main.py上传到8266，启动后自动执行，在服务器上启动mosquitto，并用mosquitto_pub -t gpio -m on/off控制LED
设置ESP8266 WIFI
启动ESP8266 之后 import led_mqtt 程序运行
import network
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
wlan.isconnected()      # check if the station is connected to an AP
wlan.connect('essid', 'password') # connect to an AP
wlan.config('mac')      # get the interface's MAC adddress
wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses
'''
import time
from umqtt.robust import MQTTClient
from machine import Pin
import network

p2 = Pin(2, Pin.OUT) #LED

def sub_cb(topic, msg):
    if msg == b'on':
        p2.value(0)
    if msg == b'off':
        p2.value(1)

server_address = "118.89.144.148" #mqtt 服务器
ap_essid = 'nubia Z17'
ap_passwd = 'luping123'


wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)
wlan.connect(ap_essid,ap_passwd ) # connect to an AP
time.sleep(2) #等待2秒
# Print diagnostic messages when retries/reconnects happens

c = MQTTClient("umqtt_client", server_address)
c.DEBUG = True
c.set_callback(sub_cb)
# Connect to server, requesting not to clean session for this
# client. If there was no existing session (False return value
# from connect() method), we perform the initial setup of client
# session - subscribe to needed topics. Afterwards, these
# subscriptions will be stored server-side, and will be persistent,
# (as we use clean_session=False).
#
# There can be a problem when a session for a given client exists,
# but doesn't have subscriptions a particular application expects.
# In this case, a session needs to be cleaned first. See
# example_reset_session.py for an obvious way how to do that.
#
# In an actual application, it's up to its developer how to
# manage these issues. One extreme is to have external "provisioning"
# phase, where initial session setup, and any further management of
# a session, is done by external tools. This allows to save resources
# on a small embedded device. Another extreme is to have an application
# to perform auto-setup (e.g., clean session, then re-create session
# on each restart). This example shows mid-line between these 2
# approaches, where initial setup of session is done by application,
# but if anything goes wrong, there's an external tool to clean session.
if not c.connect(clean_session=False):
    print("New session being set up")
    c.subscribe(b"/esp8266")

while 1:
    c.wait_msg()

c.disconnect()
