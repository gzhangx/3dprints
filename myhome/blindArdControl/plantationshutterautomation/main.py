from machine import Pin, Timer
import network
import socket
import time
from rpiserver import server

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

#tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)


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
    
ssid = "PicoW"
password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password) 
ap.active(True)

while ap.active == False:
  pass

print("Access point active")
print(ap.ifconfig())

#ap_mode('ggssid','123456789')
server.serve_forever()