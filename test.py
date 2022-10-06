from ili934 import ILI9341, color565
from machine import Pin, SPI, Timer
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
import time

#setting constants
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(23)
TFT_MISO_PIN = const(19)

TFT_CS_PIN = const(15)
TFT_RST_PIN = const(4)
TFT_DC_PIN = const(2)

spi = SPI(
    1,
    baudrate=500000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))
print(spi)

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

def leaderBoard():
    #storing info
    initials = str(input("Enter your initials: "))
    file = open ("H_Highscore.txt", "a")
    points = str(input("Enter your score: "))
    file.write(f"{initials},{points}pts\n")
    file.close()
    time.sleep(0.5)

def addScores():
    display.set_color(color565(207, 186, 112), color565(0, 0, 0))
    text2= "HIGH SCORES\n"
    display.print(text2)
    display.set_color(color565(255,255,255), color565(0,0,0,))
    f = open('H_Highscore.txt', 'r')
    leaderboard = [line.strip().split(',') for line in f.readlines() if line.strip()]
    leaderboard = [(i[0], int(i[1][:-3])) for i in leaderboard]
    leaderboard.sort(key=lambda tup: tup[1], reverse=True)
    num = 1
    for i in leaderboard[:5]:
        display.set_font(tt24)
        display.print('#'+ str(num) +' '+ str(i[0]) +' '+ str(i[1]) +' pts')
        #print(i[0], i[1],'pts')
        num += 1
    f.close()
    time.sleep(1)
    
def timerHelp(x):
    global second, minute, hour
    second += 1
    if(second == 60):
        second= 0
        minute += 1
        if(minute == 60):
            minute = 0
            hour += 1
            if(hour == 12):
                hour = 0
    display.erase()
def timer():
    secTmr = Timer(0)
    while True:
        if(switch.value() == 0):
            if state == 0:
                secTmr.init(period=1000, mode =Timer.PERIODIC, callback = timerHelp)
                state = 1
            else:
                state = 0
                secTmr.deinit()
                display.print("H:{}".format(hour))
                display.print("M:{}".format(minute))
                display.print("S:{}".format(second))
                second = 0
                minute = 0
                hour = 0
            time.sleep(0.25)
#Initializations
second = 0 
minute = 0
hour = 0
state = 0
switch = Pin(3,Pin.IN)
#Display Begins
display.erase()
display.set_pos(0,0)
    
fonts = [glcdfont,tt14,tt24,tt32]          #sets the diff fonts, using 24
display.set_color(color565(207, 186, 112), color565(0, 0, 0))
text = 'Mode Select: \n   check remote!'
display.set_font(tt24)
display.print(text)
display.print("\n")


addScores()
leaderBoard()
display.erase()
display.set_pos(0,0)
addScores()

#display.set_color(color565(255, 255, 0), color565(150, 150, 150))
#display.print("\nline 64")

time.sleep(1)

display.set_pos(1,10)

print("- bye-")