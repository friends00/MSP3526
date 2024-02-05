from machine import SPI, Pin, I2C
from micropython import const
import time, os, ustruct
import kkomi2 as hanfont
import ft6336
import st7796
import micropython
micropython.alloc_emergency_exception_buf(100)

#touch
TOUCH_SCL = const(1)     # Capacitive touch screen IIC bus clock signal
TOUCH_SDA = const(0)     # Capacitive touch screen IIC bus data signal
TOUCH_RST = const(2)     # Capacitive touch screen reset control signal
TOUCH_INT = const(3)     # Capacitive touch screen IIC bus touch interrupt signal
i2c = I2C(0,scl=Pin(TOUCH_SCL),sda=Pin(TOUCH_SDA))
touch = ft6336.FT6336U(i2c,rst=Pin(TOUCH_RST))

spi = SPI(0, baudrate=27000000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
display = st7796.ST7796(spi=spi, dc=Pin(20), cs=Pin(17), rst=Pin(21), w=320, h=480, r=1)

def handle_interrupt(pin):
    gest = touch.get_gesture()
    if gest == 0:
        num_points = touch.get_points()
        if num_points > 0:
            print(touch.get_p1_x(), touch.get_p1_y())
        if num_points == 2:
            print(touch.get_p2_x(), touch.get_p2_y())
    else:
        print("Gesture:",gest)
        
pir = Pin(TOUCH_INT, Pin.IN, Pin.PULL_UP )
pir.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

display.SetPosition(0,0)
display.fill(st7796.BLACK)
display.write(hanfont,"white  월화수목금토일",0,1)
display.write(hanfont,"yellow 월화수목금토일",0,26,st7796.YELLOW,st7796.BLACK)
display.write(hanfont,"red    월화수목금토일",0,26*2,st7796.RED,st7796.BLACK)
display.write(hanfont,"green  월화수목금토일",0,26*3,st7796.GREEN,st7796.BLACK)
display.write(hanfont,"blue   월화수목금토일",0,26*4,st7796.BLUE,st7796.BLACK)
display.write(hanfont,"brown  월화수목금토일",0,26*5,st7796.BROWN,st7796.BLACK)
display.write(hanfont,"pink   월화수목금토일",0,26*6,st7796.PINK,st7796.BLACK)
display.write(hanfont,"gold   월화수목금토일",0,26*7,st7796.GOLD,st7796.BLACK)
display.write(hanfont,"aqua   월화수목금토일",0,26*8,st7796.AQUA,st7796.BLACK)
display.write(hanfont,"silver 월화수목금토일",0,26*9,st7796.SILVER,st7796.BLACK)
display.write(hanfont,"orange 월화수목금토일",0,26*10,st7796.ORANGE,st7796.BLACK)
display.write(hanfont,"olive  월화수목금토일",0,26*11,st7796.OLIVE,st7796.BLACK)
while True:
    #print(touch.get_positions())
    time.sleep_ms(100)
    