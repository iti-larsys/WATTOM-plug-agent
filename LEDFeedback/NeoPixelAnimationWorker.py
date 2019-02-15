import threading
import time
import socket
from neopixel import *

class NeoPixelAnimationWorker(threading.Thread):


    strip = None
    orientation   = 1
    running = True
    color = Color(255,0,0)
    delay = 0.2
    animations = []
    isAnimation =  False
    selectedLed = None
    background  = Color(0,0,0)
    def __init__(self, pixels, leds,socket,d,back):
        threading.Thread.__init__(self)
        self.strip = pixels
        self.delay = float(float(d)/1000)/2
        self.animations = []
        self.background = Color(back['red'],back['green'],back['blue'])
        print(len(self.animations))
        for i in range(0,len(leds)):
            self.animations.append(leds[i])
       
        for i in range(0,len(leds)):
            leds[i]['position'] = leds[i]['position']*2

        self.socket = socket
        print(len(self.animations))

    def changeDelay(self, d):
        self.delay = float(float(d)/1000)/2

    def animate(self,led):
        self.isAnimation = True
        self.selectedLed = int(led)

    def stopAnimation(self):
        for i in range(0, self.strip.numPixels()):  ## clean everything before drawing new positions             
            self.strip.setPixelColor(i, Color(0,0,0))
        
        self.strip.show()
        self.running = False  

    def calculatePos(self,pos,orientation):
        direction = 1 if orientation == 1 else -1
        pos = pos+direction
        pos = 23 if pos < 0 else pos
        pos = 0 if pos >23  else pos
        return pos

    def run(self):
        initial_pos = []
        select_count = 20
        red = 255
        green = 255
        blue = 0
        for i in range(0,len(self.animations)):
            initial_pos.append(self.animations[i]['position'])
        for i in range(0,len(initial_pos)):
            print("======= "+str(initial_pos[i])+" LEDS pos ========")

        while self.running:
           # print("===========")
            if(not self.running):
                    break
            for j in range(0,len(self.animations)):    ## calculate new positions
                if(not self.running):
                        break
                self.animations[j]['position'] = self.calculatePos(self.animations[j]['position'],self.animations[j]['orientation'])
            
            for i in range(0, self.strip.numPixels()):  ## clean everything before drawing new positions
                if(not self.running):
                    break                  
                if(self.isAnimation):
                    print("animating "+str(select_count))
                    if(select_count>0):
                        print("select_count > 0")
                        if(select_count % 2 == 0):
                            print("select_count%2==0")
                            self.strip.setPixelColor(i, Color(self.animations[self.selectedLed]['red'],self.animations[self.selectedLed]['green'],self.animations[self.selectedLed]['blue']))
                        else:
                            print("else select_count%2==0")
                            self.strip.setPixelColor(i, self.background)
                    else:
                        print("else isAnimation")
                        self.isAnimation=False
                        select_count=20
                else:
                    self.strip.setPixelColor(i, self.background)
            
            if(self.animations[0]['position']==initial_pos[0]):
                timestamp = time.time()
                # print("Vou enviar heartbeat")
                self.socket.emit("heartbeat", {"timestamp": timestamp, "hostname": socket.gethostname()})

            for j in range(0,len(self.animations)):  ## draws new positions
                if(not self.running):
                    break                  
                if not self.isAnimation:
                    self.strip.setPixelColor(self.animations[j]['position'], Color(self.animations[j]['red'],self.animations[j]['green'],self.animations[j]['blue']))
            
            self.strip.show()
            time.sleep(self.delay)
            if(self.isAnimation):
                select_count = select_count - 1