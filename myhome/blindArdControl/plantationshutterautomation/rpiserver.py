

#import board
#import digitalio
import json
import time
from machine import Pin, Timer, PWM
import utime

MID=1500000
MIN=1000000
MAX=2000000

pwm = PWM(Pin(15))
pwm.freq(50)
pwm.duty_ns(MID)

pwmPins = {
    "GP15":True,
    }
from adafruit_httpserver import HTTPServer, HTTPResponse

#from secrets import secrets
from pins import PinInfo

# init all gpio pins to INPUT state and store in a dict mapped by id
pins = {}


# handle LED separately from the other pins - it's always an output and it's not
# really a pin (it's actually connected to the wifi module and not the main
# chip)
led = Pin("LED", Pin.OUT)

# connect to wifi


# http server
server = HTTPServer()


@server.route("/")
def base(request):
    print("root request")
    return HTTPResponse(filename="/index.html")


@server.route("/pico.svg")
def svg(request):
    # TODO: set headers so that this is cached by the browser. It's a large file
    # and takes a long time to load from the pi. Since it doesn't change much
    # (ever), don't re-transfer it on every page load.
    return HTTPResponse(filename="/pico.svg")


@server.route("/update", method="POST")
def update(request):
    print("dbgrm rquest data " + request.request_data)
    ur = json.loads(request.request_data)
    pin = Pin(ur['id'], Pin.IN if ur[
        'inout'] == 'IN' else Pin.OUT)
        
    if ur['id'] == 'LED' or ur['inout'] == 'OUT':
        if ur['value']:            
            pin.on()
        else:            
            pin.off()

    return HTTPResponse(body="done")


@server.route("/pinstates")
def pinstates(request):
    states = {}
    for pinID, pin in pins.items():
        pinStat = {
            "id": pinID,
            "inout":
            'In' ,
            "value": pin.value(),
        }
        if pwmPins[pinID]:
            pinState.input = 'PWM'
        states[pinID] = pinStat
    return HTTPResponse(content_type="application/json",
                        body=json.dumps(states))


@server.route("/pininfo")
def pininfo(request):
    return HTTPResponse(content_type="application/json",
                        body=json.dumps(PinInfo))


# Never returns
#server.serve_forever()
