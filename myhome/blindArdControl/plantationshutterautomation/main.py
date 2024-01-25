from machine import Pin, Timer
import network
import socket
import time
from rpiserver import server
import ujson


led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(period=2000, mode=Timer.PERIODIC, callback=tick)


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

with open('secrets.json') as sec_file:
    data = ujson.load(sec_file)
    print(data,data['ssid'],data['password'])
    connect_mode(data['ssid'],data['password'])
#ap_mode("PicoW", "123456789")

#ap_mode('ggssid','123456789')
server.serve_forever()