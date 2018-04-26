# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from multiprocessing import Process
from threading import Thread
import os
import argparse
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from luma.core.legacy import text, show_message



class DisplayContent(object):

    def __init__(self, text):
        self.minSpeed = 0
        self.maxSpeed = 2

        self.minBrightness = 0
        self.maxBrightness = 255


        self._text = text
        self._speed = 0
        self._brightness = 255
    

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text.replace('\r\n', '')

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if speed > self.maxSpeed:
            speed = self.maxSpeed
        if speed < self.minSpeed:
            speed = self.minSpeed
        self._speed = speed

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        if brightness > self.maxBrightness:
            brightness = self.maxBrightness
        if brightness < self.minBrightness:
            brightness = self.minBrightness
        self._brightness = brightness

    def toJson(self):
        output = '{'
        output += '\'text\': \'' + self.text + '\','
        output += '\'speed\': ' + str(self.speed)
        output += ',\'brightness\': ' + str(self.brightness)
        output += ' }'
        return  output


app = Flask(__name__)

@app.route('/')
def hello_world():
    return dc.text


@app.route('/', methods=['POST'])
def changeDisplayContent():
    global dc
    if request.form['text']:
        dc.text = request.form['text']
    if request.form['speed']:
        dc.speed = float(request.form['speed'])

    if request.form['brightness']:
        dc.brightness = int(request.form['brightness'])
    print(dc.toJson())
    return dc.toJson() # response to your request.


def renderDisplay():
    while 1:
        global device
        device.contrast(dc.brightness)
        print(dc.text)
        show_message(device, dc.text, fill="white", font=proportional(LCD_FONT), scroll_delay = dc.speed)

def initDisplay(n, block_orientation, rotate):
        global device
        # create matrix device
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
        print("Created device")

def run_server(host, port):
	app.run(host = host, port = 80)

dc = DisplayContent('Hier koennte Ihre Werbung stehen.')



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--port', type=int, default=80,  help='On which port should it run')

    args = parser.parse_args()

    try:
        if os.environ.get("WERKZEUG_RUN_MAIN") == "true": #https://stackoverflow.com/a/9476701
            initDisplay(args.cascaded, args.block_orientation, args.rotate)
	    fred = Thread(target=renderDisplay)
            fred.daemon = True
            fred.start()
            print('starting render thread')
    except Exception as e:
        print(e)
    

    app.debug = True
#    server = Process(target=run_server, args=('192.168.1.139', 80))
#    server.start()    

#    try:
#        while 1:
#            print(dc.text)
#            pass
#    except KeyboardInterrupt:
#        server.terminate()
#        fred.terminate()
        
#        server.join()
#        fred.join()
#        pass
run_server('192.168.1.139', 80)


