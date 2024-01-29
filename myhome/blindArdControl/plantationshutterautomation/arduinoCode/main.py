from machine import Pin, Timer
import network
import socket
import time
import rpiserver
import ujson
import json
import ggsettings

import urequests;

ggsettings.init()

DOWIFI = False

baseUrl ='http://192.168.2.147:18082'
led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

led.off()
def ledFlash(period):
    print("period " + str(period))
    #tim.init(period=period, mode=Timer.PERIODIC, callback=tick)


def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)
    while ap.active() == False:
        pass
    print("Access point active")
    print(ap.ifconfig())
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    #s.bind(('', 80))
    #s.listen(5)
    

def connect_mode(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan() # list with tuples (ssid, bssid, channel, RSSI, security, hidden)
    networks.sort(key=lambda x:x[3],reverse=True) # sorted on RSSI (3)
    for i, w in enumerate(networks):
      print(i+1, w[0].decode(), w[1], w[2], w[3], w[4], w[5])
    print("connect " + ssid+":"+password)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(5)
    print(wlan.ifconfig())
    return wlan.ifconfig()

ifCfg = None
name = None
ledFlash(500)

if DOWIFI:
    with open('secrets.json') as sec_file:
        data = ujson.load(sec_file)
        name = data["name"]
        print(data,data['ssid'],data['password'])
        ifCfg = connect_mode(data['ssid'],data['password'])
#ap_mode("PicoW", "123456789")

if DOWIFI:
    ggsettings.name = name
    print("ifCfg", ifCfg)
    ipAddress = ifCfg[0]
    print(ipAddress,'if0')
    ggsettings.ipAddress = ipAddress
    rpiserver.copyControls()

    print("sending name ",name)
    reqbody=json.dumps({"ip":ggsettings.ipAddress,"name":ggsettings.name,
                        "controls":ggsettings.controls})
    print("reqbody",reqbody)
    ledFlash(50)
    while True:
        try:
            urequests.post(url=baseUrl+'/registerBlinds', headers = {'content-type': 'application/json'},data=reqbody)
            break
        except:
            ledFlash(1000)
            continue

    ledFlash(500)
    for i in range(1):
        url = baseUrl+'/getBlinds?ip='+ipAddress+"&id="+str(i)
        print("request " ,i)
        #res = urequests.get(url)

        #print(res.text,"text")
        #jdata = json.loads(res.text)
        #print(i, jdata) #jdata['some']
        #res.close()


#ap_mode('ggssid','123456789')
if DOWIFI:
    rpiserver.server.serve_forever()