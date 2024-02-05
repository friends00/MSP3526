from machine import Pin, SPI
import time, struct
from micropython import const

USER_SETUP_ID = 36
'''
ST7796_MISO = 16
ST7796_MOSI = 19
ST7796_SCLK = 18
ST7796_CS   = 17  # Chip select control pin
ST7796_DC   = 20  # Data Command control pin
ST7796_RST  = 21  # Reset pin (could connect to RST pin)
'''
SPI_FREQUENCY = 80000000

# Generic commands
COLOR_MODE_65K = const(0x50)
COLOR_MODE_262K = const(0x60)
COLOR_MODE_12BIT = const(0x03)
COLOR_MODE_16BIT = const(0x05)
COLOR_MODE_18BIT = const(0x06)
COLOR_MODE_16M = const(0x07)

# Color definitions
BLACK      = const(0x0000)      #   0,   0,   0 
NAVY       = const(0x000F)      #   0,   0, 128 
DARKGREEN  = const(0x03E0)      #   0, 128,   0 
DARKCYAN   = const(0x03EF)      #   0, 128, 128 
MAROON     = const(0x7800)      # 128,   0,   0 
PURPLE     = const(0x780F)      # 128,   0, 128 
OLIVE      = const(0x7BE0)      # 128, 128,   0 
LIGHTGREY  = const(0xD69A)      # 211, 211, 211 
DARKGREY   = const(0x7BEF)      # 128, 128, 128 
BLUE       = const(0x001F)      #   0,   0, 255 
GREEN      = const(0x07E0)      #   0, 255,   0 
CYAN       = const(0x07FF)      #   0, 255, 255 
RED        = const(0xF000)      # 255,   0,   0 
MAGENTA    = const(0xF81F)      # 255,   0, 255 
YELLOW     = const(0xFFE0)      # 255, 255,   0 
WHITE      = const(0xFFFF)      # 255, 255, 255 
ORANGE     = const(0xFDA0)      # 255, 180,   0 
GREENYELLOW= const(0xB7E0)      # 180, 255,   0 
PINK       = const(0xFE19)      # 255, 192, 203  #Lighter pink, was 0xFC9F
BROWN      = const(0x9A60)      # 150,  75,   0 
GOLD       = const(0xFEA0)      # 255, 215,   0 
SILVER     = const(0xC618)      # 192, 192, 192 
SKYBLUE    = const(0x867D)      # 135, 206, 235 
VIOLET     = const(0x915C)      # 180,  46, 226 
AQUA       = const(0x07FF)      #   0, 255, 255

# ST7796 specific commands
ST7796_NOP        = const(0x00)
ST7796_SWRESET    = const(0x01) #Software Reset
ST7796_RDDID      = const(0x04) #Read Display ID
ST7796_RDDST      = const(0x09) #Read Display Status

ST7796_RDMODE     = const(0x0A) #Read Display Power Mode
ST7796_RDMADCTL   = const(0x0B) #Read Display MADCTL
ST7796_RDPIXFMT   = const(0x0C) #Read Display Pixel Format
ST7796_RDIMGFMT   = const(0x0D) #Read Display Image Mode
ST7796_RDSELFDIAG = const(0x0F) #Read Display Self-Diagnostic Result

ST7796_SLPIN      = const(0x10) #Sleep in
ST7796_SLPOUT     = const(0x11) #Sleep Out
ST7796_PTLON      = const(0x12) #Partial Display Mode On
ST7796_NORON      = const(0x13) #Normal Display Mode On

ST7796_INVOFF     = const(0x20) #Display Inversion Off
ST7796_INVON      = const(0x21) #Display Inversion On

ST7796_GASET      = const(0x26) #Gamma Set

ST7796_DISPOFF    = const(0x28) #DISPLAY_OFF
ST7796_DISPON     = const(0x29) #DISPLAY_ON

ST7796_CASET      = const(0x2A) #Column Address Set
ST7796_RASET      = const(0x2B) #Row Address Set
ST7796_RAMWR      = const(0x2C) #Memory Write
ST7796_RAMRD      = const(0x2E) #Memory Read

ST7796_PTLAR      = const(0x30) #Partial Area
ST7796_VSCRDEF    = const(0x33) #Vertical Scrolling Definition
ST7796_MADCTL     = const(0x36) #Memory Data Access Control
ST7796_VSCRSADD   = const(0x37) #Vertical Scroll Start Address of RAM
ST7796_PIXFMT     = const(0x3A) #Interface Pixel Format (Color Mode)

ST7796_WRDISBV    = const(0x51) #Write Display Brightness
ST7796_RDDISBV    = const(0x52) #Read Display Brightness Value
ST7796_WRCTLD     = const(0x53) #Write CTL Display

ST7796_FRMCTL1    = const(0xB1) #Frame Rate Control (In Normal Mode/Full Colors)
ST7796_FRMCTL2    = const(0xB2) #Frame Rate Control 2 (In Idle Mode/8 colors)
ST7796_FRMCTL3    = const(0xB3) #Frame Rate Control3 (In Partial Mode/Full Colors)
ST7796_INVCTL     = const(0xB4) #Display Inversion Control
ST7796_BPC        = const(0xB5)	#Blanking Porch Control
ST7796_DFUNCTL    = const(0xB6) #Display Function Control
ST7796_EMSET      = const(0xB7) #Entry Mode Set

ST7796_PWCTL1     = const(0xC0) #Power Control 1
ST7796_PWCTL2     = const(0xC1) #Power Control 2
ST7796_PWCTL3     = const(0xC2) #Power Control 3

ST7796_VMCTL1     = const(0xC5) #VCOM Control 1
ST7796_VMCOFF     = const(0xC6) #Vcom Offset Register
ST7796_VMCTL2     = const(0xC7) #VCOM Control 2
ST7796_PWCTLA     = const(0xCB) #Power Control A
ST7796_PWCTLB     = const(0xCF) #Power Control B

ST7796_RDID4      = const(0xD3) #Read ID4

ST7796_GMCTLP1    = const(0xE0) #Positive Gamma Control
ST7796_GMCTLN1    = const(0xE1) #Negative Gamma Control
#ST7796_DOCA       = const(0xE8) #Display Output Ctrl Adjust
ST7796_DTCTLA    = const(0xE8) #Driver Timing Control A
ST7796_DTCTLB     = const(0xEA) #Driver Timing Control B
ST7796_PWONCTL    = const(0xED) #Power On Control

ST7796_CSCON      = const(0xF0) #Command Set Control
ST7796_EN3G       = const(0xF2) #Enable 3G
ST7796_PRCTL      = const(0xF7) #Pump Ratio Control

ST7796_MADCTL_MY  = const(0x80) #Memory Data Access Control
ST7796_MADCTL_MX  = const(0x40) #Memory Data Access Control
ST7796_MADCTL_MV  = const(0x20) #Memory Data Access Control
ST7796_MADCTL_ML  = const(0x10) #Memory Data Access Control
ST7796_MADCTL_RGB = const(0x00) #Memory Data Access Control
ST7796_MADCTL_BGR = const(0x08) #Memory Data Access Control
ST7796_MADCTL_MH  = const(0x04) #Memory Data Access Control
ST7796_MADCTL_COLOR_ORDER = ST7796_MADCTL_BGR

MEMORY_BUFFER = const(1024) # SPI Write Buffer
_ENCODE_PIXEL = ">H"
_ENCODE_POS = ">HH"
_DECODE_PIXEL = ">BBB"

def color565(red, green=0, blue=0):
    """
    Convert red, green and blue values (0-255) into a 16-bit 565 encoding.
    """
    try:
        red, green, blue = red  # see if the first var is a tuple/list
    except TypeError:
        pass
    return (red & 0xf8) << 8 | (green & 0xfc) << 3 | blue >> 3


def _encode_pos(x, y):
    """Encode a postion into bytes."""
    return struct.pack(_ENCODE_POS, x, y)


def _encode_pixel(color):
    """Encode a pixel color into bytes."""
    return struct.pack(_ENCODE_PIXEL, color)


class ST7796:
    def __init__(self, spi, cs, dc, rst, w, h, r):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.init_width = w
        self.init_height = h
        self.width = w
        self.height = h
        self.rotation = r
        self.xstart = 0
        self.ystart = 0
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.buffer = bytearray(MEMORY_BUFFER * 2)
        #self.color_map = bytearray(b'\x00\x00\xFF\xFF') #default white foregraound, black background
        self.hard_reset()
        self.soft_reset()
        self.sleep_mode(False)
        self._set_color_mode(COLOR_MODE_65K | COLOR_MODE_16BIT)
        time.sleep_ms(50)
        self._rotation(self.rotation)
        self.init()
        #self.inversion_mode(True)
        #time.sleep_ms(10)
        #self._write(ST7796_NORON)
        #time.sleep_ms(10)
        #self._write(ST7796_DISPON)
        time.sleep_ms(500)
        self.fill(0)

    def init(self):
      time.sleep_ms(120)
      #self._write(ST7796_SWRESET) #Software reset
      #time.sleep_ms(120)
      self._write(ST7796_CSCON,b'\xC3') #Enable extension command 2 partI
      self._write(ST7796_CSCON,b'\x96') #Enable extension command 2 partII
      
      #self._write(ST7796_RDSELFDIAG,b'\x03\x80\x02') #Read Display Self-Diagnostic Result
      #self._write(ST7796_PWCTLB,b'\x00\xc1\x30') #Power Control B
      #self._write(ST7796_PWONCTL,b'\x64\x03\x12\x81') #Power On Control
      #self._write(ST7796_DTCTLA, b'\x85\x00\x78') #Driver Timing Control a
      #self._write(ST7796_PWCTLA, b'\x39\x2c\x00\x34\x02') #Power Control A
      #self._write(ST7796_PRCTL, b'\x20') #Pump Ratio Control
      #self._write(ST7796_DTCTLB, b'\x00\x00') #Driver Timing Control B
      #self._write(ST7796_PWCTL1, b'\x23') #Power Control 1
      #self._write(ST7796_PWCTL2, b'\x10') #Power Control 2
      #self._write(ST7796_VMCTL1,b'\x3E\x28') #VCOM Control VCOM=0.9
      #self._write(ST7796_VMCTL2,b'\x86') #VCOM Control VCOM=0.9
      
      #self._write(ST7796_MADCTL,b'\x48') #Memory Data Access Control
      #self._rotation(self.rotation)
      #self._write(ST7796_PIXFMT,b'\x55') #Interface Pixel Format (Colo Mode to 655k)
      #self._write(ST7796_BPC,b'\x02\x03\x00\x04')  #Blanking Porch Control   
      #self._write(ST7796_FRMCTL1,b'\x80\x10') #Frame Rate Control (In Normal Mode/Full Colors)

      #self._write(0xE4,b'\x31')
      #self._write(ST7796_DFUNCTR,b'\x02\x02\X3B') #Display Function Control
      #self._write(ST7796_DFUNCTL, b'\x80\x02\x3B') #Display Function Control
      #self._write(ST7796_EN3G, b'\x00') #Enable 3G
      #self._write(ST7796_GASET, b'\x01') #Gamma Set
 
      self._write(ST7796_INVCTL,b'\x01') #Display Inversion Control
      self._write(ST7796_EMSET,b'\xC6') #Entry Mode Set
      self._write(ST7796_PWCTL1,b'\x80\x45') #Power control1 
      self._write(ST7796_PWCTL2,b'\x13') #Power control2  VAP(GVDD)=3.85+( vcom+vcom offset), VAN(GVCL)=-3.85+( vcom+vcom offset)
      self._write(ST7796_PWCTL3,b'\xA7') #Power control 3  Source driving current level=low, Gamma driving current level=High
      self._write(ST7796_VMCTL1,b'\x0A') #VCOM Control VCOM=0.9
      self._write(ST7796_DTCTLA,b'\x40\x8A\x00\x00\x29\x19\xA5\x33') #Display Output Ctrl Adjust
      #ST7796 Gamma Sequence
      self._write(ST7796_GMCTLP1,b'\xD0\x08\x0F\x06\x06\x33\x30/x33\x47\x17\x13\x13\x2B\x31')
      self._write(ST7796_GMCTLN1,b'\xD0\x0A\x11\x0B\x09\x07\x2F\x33\x47\x38\x15\x16\x2C\x32')

      time.sleep_ms(120)
      self._write(ST7796_CSCON,b'\xC3')  #Disable extension command 2 partI
      self._write(ST7796_CSCON,b'\x69')  #Disable extension command 2 partII
      time.sleep_ms(120)
      self._write(ST7796_INVON) #Display Inversion On
      time.sleep_ms(120)
      self._write(ST7796_DISPON) #Display on

    # This is the command sequence that rotates the ST7796 driver coordinate frame
    def _rotation(self, m):
      rotation = m % 8 # Limit the range of values to 0-7
      self._write(ST7796_MADCTL)
      if rotation == 0:  # 0 deg
          self._writedata(bytearray([ST7796_MADCTL_MX | ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_width
          self.height = self.init_height
      elif rotation == 1: # 90 deg
          self._writedata(bytearray([ST7796_MADCTL_MV | ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_height
          self.height = self.init_width
      elif rotation == 2: # 180 deg
          self._writedata(bytearray([ST7796_MADCTL_MY | ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_width
          self.height = self.init_height
      elif rotation == 3: # 270 deg
          self._writedata(bytearray([ST7796_MADCTL_MX | ST7796_MADCTL_MY | ST7796_MADCTL_MV | ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_height
          self.height = self.init_width
      # These next rotations are for bottom up BMP drawing
      elif rotation == 4: # Mirrored + 0 deg
          self._writedata(bytearray([ST7796_MADCTL_MX | ST7796_MADCTL_MY | ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_width
          self.height = self.init_height
      elif rotation == 5: # Mirrored + 90 deg
          self._writedata(bytearray([ST7796_MADCTL_MV | ST7796_MADCTL_MX | ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_height
          self.height = self.init_width
      elif rotation == 6: # Mirrored + 180 deg
          self._writedata(bytearray([ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_width
          self.height = self.init_height
      elif rotation == 7: # Mirrored + 270 deg
          self._writedata(bytearray([ST7796_MADCTL_MY | ST7796_MADCTL_MV | ST7796_MADCTL_COLOR_ORDER]))
          self.width  = self.init_height
          self.height = self.init_width
      else:
          self._writedata(bytearray([ST7796_MADCTL_COLOR_ORDER]))


    def hard_reset(self):
        """
        Hard reset display.
        """
        self.cs.off()
        self.rst.on()
        time.sleep_ms(50)
        self.rst.off()
        time.sleep_ms(50)
        self.rst.on()
        time.sleep_ms(150)
        self.cs.on()

    def soft_reset(self):
        """
        Soft reset display.
        """
        self._write(ST7796_SWRESET)
        time.sleep_ms(150)

    def sleep_mode(self, value):
        """
        Enable or disable display sleep mode.
        Args:
            value (bool): if True enable sleep mode. if False disable sleep
            mode
        """
        if value:
            self._write(ST7796_SLPIN)
        else:
            self._write(ST7796_SLPOUT)


    def inversion_mode(self, value):
        """
        Enable or disable display inversion mode.
        Args:
            value (bool): if True enable inversion mode. if False disable
            inversion mode
        """
        if value:
            self._write(ST7796_INVON)
        else:
            self._write(ST7796_INVOFF)

    def _set_color_mode(self, mode):
        """
        Set display color mode.
        Args:
            mode (int): color mode
                COLOR_MODE_65K, COLOR_MODE_262K, COLOR_MODE_12BIT,
                COLOR_MODE_16BIT, COLOR_MODE_18BIT, COLOR_MODE_16M
        """
        self._write(ST7796_PIXFMT, bytes([mode & 0x77]))

    def SetPosition(self,x,y):
        self.xstart,self.ystart = x,y

    def _write(self, command, data=None):
        self.dc.off()
        self.cs.off()
        self.spi.write(bytearray([command]))
        self.cs.on()
        if data is not None:
            self._writedata(data)

    def _writedata(self, data):
        self.dc.on()
        self.cs.off()
        self.spi.write(data)
        self.cs.on()

    def WriteBlock(self, x0, y0, x1, y1, data=None):
        self._write(ST7796_CASET, struct.pack(">HH", x0, x1))
        self._write(ST7796_RASET, struct.pack(">HH", y0, y1))
        self._write(ST7796_RAMWR, data)

    def fill_rect(self, x, y, width, height, color):
        """
        Draw a rectangle at the given location, size and filled with color.
        Args:
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            width (int): Width in pixels
            height (int): Height in pixels
            color (int): 565 encoded color
        """
        self._set_window(x, y, x + width - 1, y + height - 1)
        chunks, rest = divmod(width * height, MEMORY_BUFFER)
        pixel = _encode_pixel(color)
        self.dc.on()
        if chunks:
            data = pixel * MEMORY_BUFFER
            for _ in range(chunks):
                self._writedata(data)
        if rest:
            self._writedata(pixel * rest)
  
    def _set_columns(self, start, end):
        """
        Send CASET (column address set) command to display.
        Args:
            start (int): column start address
            end (int): column end address
        """
        if start <= end <= self.width:
            self._write(ST7796_CASET, _encode_pos(
                start+self.xstart, end + self.xstart))

    def _set_rows(self, start, end):
        """
        Send RASET (row address set) command to display.
        Args:
            start (int): row start address
            end (int): row end address
       """
        if start <= end <= self.height:
            self._write(ST7796_RASET, _encode_pos(
                start+self.ystart, end+self.ystart))

    def _set_window(self, x0, y0, x1, y1):
        """
        Set window to column and row address.
        Args:
            x0 (int): column start address
            y0 (int): row start address
            x1 (int): column end address
            y1 (int): row end address
        """
        self._set_columns(x0, x1)
        self._set_rows(y0, y1)
        self._write(ST7796_RAMWR)
    
    def vline(self, x, y, length, color):
        """
        Draw vertical line at the given location and color.
        Args:
            x (int): x coordinate
            Y (int): y coordinate
            length (int): length of line
            color (int): 565 encoded color
        """
        self.fill_rect(x, y, 1, length, color)

    def hline(self, x, y, length, color):
        """
        Draw horizontal line at the given location and color.
        Args:
            x (int): x coordinate
            Y (int): y coordinate
            length (int): length of line
            color (int): 565 encoded color
        """
        self.fill_rect(x, y, length, 1, color)

    def pixel(self, x, y, color):
        """
        Draw a pixel at the given location and color.
        Args:
            x (int): x coordinate
            Y (int): y coordinate
            color (int): 565 encoded color
        """
        self._set_window(x, y, x, y)
        self._writedata(_encode_pixel(color))
    
    def blit_buffer(self, buffer, x, y, width, height):
        """
        Copy buffer to display at the given location.
        Args:
            buffer (bytes): Data to copy to display
            x (int): Top left corner x coordinate
            Y (int): Top left corner y coordinate
            width (int): Width
            height (int): Height
        """
        self._set_window(x, y, x + width - 1, y + height - 1)
        self._writedata(buffer)

    def rect(self, x, y, w, h, color):
        """
        Draw a rectangle at the given location, size and color.
        Args:
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            width (int): Width in pixels
            height (int): Height in pixels
            color (int): 565 encoded color
        """
        self.hline(x, y, w, color)
        self.vline(x, y, h, color)
        self.vline(x + w - 1, y, h, color)
        self.hline(x, y + h - 1, w, color)

    def fill(self, color):
        """
        Fill the entire FrameBuffer with the specified color.
        Args:
            color (int): 565 encoded color
        """
        self.fill_rect(0, 0, self.width, self.height, color)

    def line(self, x0, y0, x1, y1, color):
        """
        Draw a single pixel wide line starting at x0, y0 and ending at x1, y1.
        Args:
            x0 (int): Start point x coordinate
            y0 (int): Start point y coordinate
            x1 (int): End point x coordinate
            y1 (int): End point y coordinate
            color (int): 565 encoded color
        """
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1 - x0
        dy = abs(y1 - y0)
        err = dx // 2
        if y0 < y1:
            ystep = 1
        else:
            ystep = -1
        while x0 <= x1:
            if steep:
                self.pixel(y0, x0, color)
            else:
                self.pixel(x0, y0, color)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1


    def _text8(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Internal method to write characters with width of 8 and
        heights of 8 or 16.
        Args:
            font (module): font module to use
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        for char in text:
            ch = ord(char)
            if (font.FIRST <= ch < font.LAST
                    and x0+font.WIDTH <= self.width
                    and y0+font.HEIGHT <= self.height):

                if font.HEIGHT == 8:
                    passes = 1
                    size = 8
                    each = 0
                else:
                    passes = 2
                    size = 16
                    each = 8

                for line in range(passes):
                    idx = (ch-font.FIRST)*size+(each*line)
                    buffer = struct.pack(
                        '>64H',
                        color if font.FONT[idx] & _BIT7 else background,
                        color if font.FONT[idx] & _BIT6 else background,
                        color if font.FONT[idx] & _BIT5 else background,
                        color if font.FONT[idx] & _BIT4 else background,
                        color if font.FONT[idx] & _BIT3 else background,
                        color if font.FONT[idx] & _BIT2 else background,
                        color if font.FONT[idx] & _BIT1 else background,
                        color if font.FONT[idx] & _BIT0 else background,
                        color if font.FONT[idx+1] & _BIT7 else background,
                        color if font.FONT[idx+1] & _BIT6 else background,
                        color if font.FONT[idx+1] & _BIT5 else background,
                        color if font.FONT[idx+1] & _BIT4 else background,
                        color if font.FONT[idx+1] & _BIT3 else background,
                        color if font.FONT[idx+1] & _BIT2 else background,
                        color if font.FONT[idx+1] & _BIT1 else background,
                        color if font.FONT[idx+1] & _BIT0 else background,
                        color if font.FONT[idx+2] & _BIT7 else background,
                        color if font.FONT[idx+2] & _BIT6 else background,
                        color if font.FONT[idx+2] & _BIT5 else background,
                        color if font.FONT[idx+2] & _BIT4 else background,
                        color if font.FONT[idx+2] & _BIT3 else background,
                        color if font.FONT[idx+2] & _BIT2 else background,
                        color if font.FONT[idx+2] & _BIT1 else background,
                        color if font.FONT[idx+2] & _BIT0 else background,
                        color if font.FONT[idx+3] & _BIT7 else background,
                        color if font.FONT[idx+3] & _BIT6 else background,
                        color if font.FONT[idx+3] & _BIT5 else background,
                        color if font.FONT[idx+3] & _BIT4 else background,
                        color if font.FONT[idx+3] & _BIT3 else background,
                        color if font.FONT[idx+3] & _BIT2 else background,
                        color if font.FONT[idx+3] & _BIT1 else background,
                        color if font.FONT[idx+3] & _BIT0 else background,
                        color if font.FONT[idx+4] & _BIT7 else background,
                        color if font.FONT[idx+4] & _BIT6 else background,
                        color if font.FONT[idx+4] & _BIT5 else background,
                        color if font.FONT[idx+4] & _BIT4 else background,
                        color if font.FONT[idx+4] & _BIT3 else background,
                        color if font.FONT[idx+4] & _BIT2 else background,
                        color if font.FONT[idx+4] & _BIT1 else background,
                        color if font.FONT[idx+4] & _BIT0 else background,
                        color if font.FONT[idx+5] & _BIT7 else background,
                        color if font.FONT[idx+5] & _BIT6 else background,
                        color if font.FONT[idx+5] & _BIT5 else background,
                        color if font.FONT[idx+5] & _BIT4 else background,
                        color if font.FONT[idx+5] & _BIT3 else background,
                        color if font.FONT[idx+5] & _BIT2 else background,
                        color if font.FONT[idx+5] & _BIT1 else background,
                        color if font.FONT[idx+5] & _BIT0 else background,
                        color if font.FONT[idx+6] & _BIT7 else background,
                        color if font.FONT[idx+6] & _BIT6 else background,
                        color if font.FONT[idx+6] & _BIT5 else background,
                        color if font.FONT[idx+6] & _BIT4 else background,
                        color if font.FONT[idx+6] & _BIT3 else background,
                        color if font.FONT[idx+6] & _BIT2 else background,
                        color if font.FONT[idx+6] & _BIT1 else background,
                        color if font.FONT[idx+6] & _BIT0 else background,
                        color if font.FONT[idx+7] & _BIT7 else background,
                        color if font.FONT[idx+7] & _BIT6 else background,
                        color if font.FONT[idx+7] & _BIT5 else background,
                        color if font.FONT[idx+7] & _BIT4 else background,
                        color if font.FONT[idx+7] & _BIT3 else background,
                        color if font.FONT[idx+7] & _BIT2 else background,
                        color if font.FONT[idx+7] & _BIT1 else background,
                        color if font.FONT[idx+7] & _BIT0 else background
                    )
                    self.blit_buffer(buffer, x0, y0+8*line, 8, 8)

                x0 += 8

    def _text16(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Internal method to draw characters with width of 16 and heights of 16
        or 32.
        Args:
            font (module): font module to use
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        for char in text:
            ch = ord(char)
            if (font.FIRST <= ch < font.LAST
                    and x0+font.WIDTH <= self.width
                    and y0+font.HEIGHT <= self.height):

                if font.HEIGHT == 16:
                    passes = 2
                    size = 32
                    each = 16
                else:
                    passes = 4
                    size = 64
                    each = 16

                for line in range(passes):
                    idx = (ch-font.FIRST)*size+(each*line)
                    buffer = struct.pack(
                        '>128H',
                        color if font.FONT[idx] & _BIT7 else background,
                        color if font.FONT[idx] & _BIT6 else background,
                        color if font.FONT[idx] & _BIT5 else background,
                        color if font.FONT[idx] & _BIT4 else background,
                        color if font.FONT[idx] & _BIT3 else background,
                        color if font.FONT[idx] & _BIT2 else background,
                        color if font.FONT[idx] & _BIT1 else background,
                        color if font.FONT[idx] & _BIT0 else background,
                        color if font.FONT[idx+1] & _BIT7 else background,
                        color if font.FONT[idx+1] & _BIT6 else background,
                        color if font.FONT[idx+1] & _BIT5 else background,
                        color if font.FONT[idx+1] & _BIT4 else background,
                        color if font.FONT[idx+1] & _BIT3 else background,
                        color if font.FONT[idx+1] & _BIT2 else background,
                        color if font.FONT[idx+1] & _BIT1 else background,
                        color if font.FONT[idx+1] & _BIT0 else background,
                        color if font.FONT[idx+2] & _BIT7 else background,
                        color if font.FONT[idx+2] & _BIT6 else background,
                        color if font.FONT[idx+2] & _BIT5 else background,
                        color if font.FONT[idx+2] & _BIT4 else background,
                        color if font.FONT[idx+2] & _BIT3 else background,
                        color if font.FONT[idx+2] & _BIT2 else background,
                        color if font.FONT[idx+2] & _BIT1 else background,
                        color if font.FONT[idx+2] & _BIT0 else background,
                        color if font.FONT[idx+3] & _BIT7 else background,
                        color if font.FONT[idx+3] & _BIT6 else background,
                        color if font.FONT[idx+3] & _BIT5 else background,
                        color if font.FONT[idx+3] & _BIT4 else background,
                        color if font.FONT[idx+3] & _BIT3 else background,
                        color if font.FONT[idx+3] & _BIT2 else background,
                        color if font.FONT[idx+3] & _BIT1 else background,
                        color if font.FONT[idx+3] & _BIT0 else background,
                        color if font.FONT[idx+4] & _BIT7 else background,
                        color if font.FONT[idx+4] & _BIT6 else background,
                        color if font.FONT[idx+4] & _BIT5 else background,
                        color if font.FONT[idx+4] & _BIT4 else background,
                        color if font.FONT[idx+4] & _BIT3 else background,
                        color if font.FONT[idx+4] & _BIT2 else background,
                        color if font.FONT[idx+4] & _BIT1 else background,
                        color if font.FONT[idx+4] & _BIT0 else background,
                        color if font.FONT[idx+5] & _BIT7 else background,
                        color if font.FONT[idx+5] & _BIT6 else background,
                        color if font.FONT[idx+5] & _BIT5 else background,
                        color if font.FONT[idx+5] & _BIT4 else background,
                        color if font.FONT[idx+5] & _BIT3 else background,
                        color if font.FONT[idx+5] & _BIT2 else background,
                        color if font.FONT[idx+5] & _BIT1 else background,
                        color if font.FONT[idx+5] & _BIT0 else background,
                        color if font.FONT[idx+6] & _BIT7 else background,
                        color if font.FONT[idx+6] & _BIT6 else background,
                        color if font.FONT[idx+6] & _BIT5 else background,
                        color if font.FONT[idx+6] & _BIT4 else background,
                        color if font.FONT[idx+6] & _BIT3 else background,
                        color if font.FONT[idx+6] & _BIT2 else background,
                        color if font.FONT[idx+6] & _BIT1 else background,
                        color if font.FONT[idx+6] & _BIT0 else background,
                        color if font.FONT[idx+7] & _BIT7 else background,
                        color if font.FONT[idx+7] & _BIT6 else background,
                        color if font.FONT[idx+7] & _BIT5 else background,
                        color if font.FONT[idx+7] & _BIT4 else background,
                        color if font.FONT[idx+7] & _BIT3 else background,
                        color if font.FONT[idx+7] & _BIT2 else background,
                        color if font.FONT[idx+7] & _BIT1 else background,
                        color if font.FONT[idx+7] & _BIT0 else background,
                        color if font.FONT[idx+8] & _BIT7 else background,
                        color if font.FONT[idx+8] & _BIT6 else background,
                        color if font.FONT[idx+8] & _BIT5 else background,
                        color if font.FONT[idx+8] & _BIT4 else background,
                        color if font.FONT[idx+8] & _BIT3 else background,
                        color if font.FONT[idx+8] & _BIT2 else background,
                        color if font.FONT[idx+8] & _BIT1 else background,
                        color if font.FONT[idx+8] & _BIT0 else background,
                        color if font.FONT[idx+9] & _BIT7 else background,
                        color if font.FONT[idx+9] & _BIT6 else background,
                        color if font.FONT[idx+9] & _BIT5 else background,
                        color if font.FONT[idx+9] & _BIT4 else background,
                        color if font.FONT[idx+9] & _BIT3 else background,
                        color if font.FONT[idx+9] & _BIT2 else background,
                        color if font.FONT[idx+9] & _BIT1 else background,
                        color if font.FONT[idx+9] & _BIT0 else background,
                        color if font.FONT[idx+10] & _BIT7 else background,
                        color if font.FONT[idx+10] & _BIT6 else background,
                        color if font.FONT[idx+10] & _BIT5 else background,
                        color if font.FONT[idx+10] & _BIT4 else background,
                        color if font.FONT[idx+10] & _BIT3 else background,
                        color if font.FONT[idx+10] & _BIT2 else background,
                        color if font.FONT[idx+10] & _BIT1 else background,
                        color if font.FONT[idx+10] & _BIT0 else background,
                        color if font.FONT[idx+11] & _BIT7 else background,
                        color if font.FONT[idx+11] & _BIT6 else background,
                        color if font.FONT[idx+11] & _BIT5 else background,
                        color if font.FONT[idx+11] & _BIT4 else background,
                        color if font.FONT[idx+11] & _BIT3 else background,
                        color if font.FONT[idx+11] & _BIT2 else background,
                        color if font.FONT[idx+11] & _BIT1 else background,
                        color if font.FONT[idx+11] & _BIT0 else background,
                        color if font.FONT[idx+12] & _BIT7 else background,
                        color if font.FONT[idx+12] & _BIT6 else background,
                        color if font.FONT[idx+12] & _BIT5 else background,
                        color if font.FONT[idx+12] & _BIT4 else background,
                        color if font.FONT[idx+12] & _BIT3 else background,
                        color if font.FONT[idx+12] & _BIT2 else background,
                        color if font.FONT[idx+12] & _BIT1 else background,
                        color if font.FONT[idx+12] & _BIT0 else background,
                        color if font.FONT[idx+13] & _BIT7 else background,
                        color if font.FONT[idx+13] & _BIT6 else background,
                        color if font.FONT[idx+13] & _BIT5 else background,
                        color if font.FONT[idx+13] & _BIT4 else background,
                        color if font.FONT[idx+13] & _BIT3 else background,
                        color if font.FONT[idx+13] & _BIT2 else background,
                        color if font.FONT[idx+13] & _BIT1 else background,
                        color if font.FONT[idx+13] & _BIT0 else background,
                        color if font.FONT[idx+14] & _BIT7 else background,
                        color if font.FONT[idx+14] & _BIT6 else background,
                        color if font.FONT[idx+14] & _BIT5 else background,
                        color if font.FONT[idx+14] & _BIT4 else background,
                        color if font.FONT[idx+14] & _BIT3 else background,
                        color if font.FONT[idx+14] & _BIT2 else background,
                        color if font.FONT[idx+14] & _BIT1 else background,
                        color if font.FONT[idx+14] & _BIT0 else background,
                        color if font.FONT[idx+15] & _BIT7 else background,
                        color if font.FONT[idx+15] & _BIT6 else background,
                        color if font.FONT[idx+15] & _BIT5 else background,
                        color if font.FONT[idx+15] & _BIT4 else background,
                        color if font.FONT[idx+15] & _BIT3 else background,
                        color if font.FONT[idx+15] & _BIT2 else background,
                        color if font.FONT[idx+15] & _BIT1 else background,
                        color if font.FONT[idx+15] & _BIT0 else background
                    )
                    self.blit_buffer(buffer, x0, y0+8*line, 16, 8)
            x0 += font.WIDTH

    def text(self, font, text, x0, y0, color=WHITE, background=BLACK):
        """
        Draw text on display in specified font and colors. 8 and 16 bit wide
        fonts are supported.
        Args:
            font (module): font module to use.
            text (str): text to write
            x0 (int): column to start drawing at
            y0 (int): row to start drawing at
            color (int): 565 encoded color to use for characters
            background (int): 565 encoded color to use for background
        """
        if font.WIDTH == 8:
            self._text8(font, text, x0, y0, color, background)
        else:
            self._text16(font, text, x0, y0, color, background)

    def bitmap(self, bitmap, x, y, index=0):
        """
        Draw a bitmap on display at the specified column and row
        Args:
            bitmap (bitmap_module): The module containing the bitmap to draw
            x (int): column to start drawing at
            y (int): row to start drawing at
            index (int): Optional index of bitmap to draw from multiple bitmap
                module
        """
        bitmap_size = bitmap.HEIGHT * bitmap.WIDTH
        buffer_len = bitmap_size * 2
        buffer = bytearray(buffer_len)
        bs_bit = bitmap.BPP * bitmap_size * index if index > 0 else 0

        for i in range(0, buffer_len, 2):
            color_index = 0
            for bit in range(bitmap.BPP):
                color_index <<= 1
                color_index |= (bitmap.BITMAP[bs_bit // 8]
                                & 1 << (7 - (bs_bit % 8))) > 0
                bs_bit += 1

            color = bitmap.PALETTE[color_index]
            buffer[i] = color & 0xff00 >> 8
            buffer[i + 1] = color_index & 0xff

        to_col = x + bitmap.WIDTH - 1
        to_row = y + bitmap.HEIGHT - 1
        if self.width > to_col and self.height > to_row:
            self._set_window(x, y, to_col, to_row)
            self._writedata(buffer)

    # @micropython.native
    def write(self, font, string, x, y, fg=WHITE, bg=BLACK):
        """
        Write a string using a converted true-type font on the display starting
        at the specified column and row
        Args:
            font (font): The module containing the converted true-type font
            s (string): The string to write
            x (int): column to start writing
            y (int): row to start writing
            fg (int): foreground color, optional, defaults to WHITE
            bg (int): background color, optional, defaults to BLACK
        """
        buffer_len = font.HEIGHT * font.MAX_WIDTH * 2
        buffer = bytearray(buffer_len)
        fg_hi = (fg & 0xff00) >> 8
        fg_lo = fg & 0xff

        bg_hi = (bg & 0xff00) >> 8
        bg_lo = bg & 0xff

        for character in string:
            try:
                char_index = font.MAP.index(character)
                offset = char_index * font.OFFSET_WIDTH
                bs_bit = font.OFFSETS[offset]
                if font.OFFSET_WIDTH > 1:
                    bs_bit = (bs_bit << 8) + font.OFFSETS[offset + 1]

                if font.OFFSET_WIDTH > 2:
                    bs_bit = (bs_bit << 8) + font.OFFSETS[offset + 2]

                char_width = font.WIDTHS[char_index]
                buffer_needed = char_width * font.HEIGHT * 2

                for i in range(0, buffer_needed, 2):
                    if font.BITMAPS[bs_bit // 8] & 1 << (7 - (bs_bit % 8)) > 0:
                        buffer[i] = fg_hi
                        buffer[i + 1] = fg_lo
                    else:
                        buffer[i] = bg_hi
                        buffer[i + 1] = bg_lo

                    bs_bit += 1

                to_col = x + char_width - 1
                to_row = y + font.HEIGHT - 1
                if self.width > to_col and self.height > to_row:
                    self._set_window(x, y, to_col, to_row)
                    self._writedata(buffer[0:buffer_needed])

                x += char_width

            except ValueError:
                pass

    def write_width(self, font, string):
        """
        Returns the width in pixels of the string if it was written with the
        specified font
        Args:
            font (font): The module containing the converted true-type font
            string (string): The string to measure
        """
        width = 0
        for character in string:
            try:
                char_index = font.MAP.index(character)
                width += font.WIDTHS[char_index]

            except ValueError:
                pass

        return width
    
    def circle(self, x0, y0, radius, color):
        # Circle drawing function.  Will draw a single pixel wide circle with
        # center at x0, y0 and the specified radius.
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        self._pixel(x0, y0 + radius, color)
        self._pixel(x0, y0 - radius, color)
        self._pixel(x0 + radius, y0, color)
        self._pixel(x0 - radius, y0, color)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self._pixel(x0 + x, y0 + y, color)
            self._pixel(x0 - x, y0 + y, color)
            self._pixel(x0 + x, y0 - y, color)
            self._pixel(x0 - x, y0 - y, color)
            self._pixel(x0 + y, y0 + x, color)
            self._pixel(x0 - y, y0 + x, color)
            self._pixel(x0 + y, y0 - x, color)
            self._pixel(x0 - y, y0 - x, color)

    def fill_circle(self, x0, y0, radius, color):
        # Filled circle drawing function.  Will draw a filled circule with
        # center at x0, y0 and the specified radius.
        self.vline(x0, y0 - radius, 2*radius + 1, color)
        f = 1 - radius
        ddF_x = 1
        ddF_y = -2 * radius
        x = 0
        y = radius
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.vline(x0 + x, y0 - y, 2*y + 1, color)
            self.vline(x0 + y, y0 - x, 2*x + 1, color)
            self.vline(x0 - x, y0 - y, 2*y + 1, color)
            self.vline(x0 - y, y0 - x, 2*x + 1, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        # Triangle drawing function.  Will draw a single pixel wide triangle
        # around the points (x0, y0), (x1, y1), and (x2, y2).
        self.line(x0, y0, x1, y1, color)
        self.line(x1, y1, x2, y2, color)
        self.line(x2, y2, x0, y0, color)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color):
        # Filled triangle drawing function.  Will draw a filled triangle around
        # the points (x0, y0), (x1, y1), and (x2, y2).
        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0
        if y1 > y2:
            y2, y1 = y1, y2
            x2, x1 = x1, x2
        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0
        a = 0
        b = 0
        y = 0
        last = 0
        if y0 == y2:
            a = x0
            b = x0
            if x1 < a:
                a = x1
            elif x1 > b:
                b = x1
            if x2 < a:
                a = x2
            elif x2 > b:
                b = x2
            self.hline(a, y0, b-a+1, color)
            return
        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        if dy01 == 0:
            dy01 = 1
        if dy02 == 0:
            dy02 = 1
        if dy12 == 0:
            dy12 = 1
        sa = 0
        sb = 0
        if y1 == y2:
            last = y1
        else:
            last = y1-1
        for y in range(y0, last+1):
            a = x0 + sa // dy01
            b = x0 + sb // dy02
            sa += dx01
            sb += dx02
            if a > b:
                a, b = b, a
            self.hline(a, y, b-a+1, color)
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)
        while y <= y2:
            a = x1 + sa // dy12
            b = x0 + sb // dy02
            sa += dx12
            sb += dx02
            if a > b:
                a, b = b, a
            self.hline(a, y, b-a+1, color)
            y += 1    