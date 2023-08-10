import time
from machine import I2C, Pin
from I2C_LCD import I2CLcd

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
devices = i2c.scan()
Trig = Pin(19, Pin.OUT, 0)
Echo = Pin(18, Pin.IN, 0)
button = Pin(13, Pin.IN, Pin.PULL_UP)
distance = 0
soundVelocity = 340


def getDistance():
    Trig.value(1)
    time.sleep_us(10)
    Trig.value(0)
    while not Echo.value():
        pass
    pingStart = time.ticks_us()
    while Echo.value():
        pass
    pingStop = time.ticks_us()
    distanceTime = time.ticks_diff(pingStop, pingStart) // 2
    distance = int(soundVelocity * distanceTime // 10000)
    return distance


def showDistance(distance, lcd):
    if distance:
        fulfillment = (100 - distance)*10
        setMessage(lcd, 0, 1, f"Volume: {fulfillment}L    ")
    else:
        setMessage(lcd, 0, 1, "ERROR")


def setMessage(lcd, col, line, message):
    lcd.move_to(col, line)
    lcd.putstr(message)


try:
    if devices != []:
        lcd = I2CLcd(i2c, devices[0], 2, 16)
        
        while True:
            setMessage(lcd, 0, 0, "Citerne Serre")
            lcd.backlight_on() if not button.value() else lcd.backlight_off()
            time.sleep_ms(500)
            distance = getDistance()
            print(distance)
            fulfillment = (100 - distance)*10
            setMessage(lcd, 0, 1, f"Volume: {fulfillment}L    ")
            time.sleep(1)

    else:
        print("No address found")
except:
    pass


