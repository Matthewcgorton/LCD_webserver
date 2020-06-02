from flask import render_template, session, redirect, url_for, current_app, request
# from . import lcd_state

import time

def lcd_string(message, line):
    # Send string to display
    print("sdaf")


def lcd_test(message, line):
    if current_app.config['LOCAL_HARDWARE']:
        print(f"local {message}::{line}")
    else:
        print(f"Test mode - No local hardware {message}::{line}")



# Define some device parameters
# bus = None
from .. import bus

I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005



def init_lcd(local_hardware):
    if local_hardware:
        print(f"Initializing local hardware")

        import smbus
        global bus


        # Open I2C interface
        # bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
        bus = smbus.SMBus(1)    # Rev 2 Pi uses 1


        # Initialise display
        lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
        lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
        lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
        lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        time.sleep(E_DELAY)

        print(f"Initialized\n")


    else:
        print(f"No local hardware\n")



def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command
    # import smbus
    # bus = smbus.SMBus(1)
    global bus

    print(bus)

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_highT)
    

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
    # import smbus
    # bus = smbus.SMBus(1)
    global bus

    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)



def lcd_string(message, line):
    # Send string to display
    if current_app.config['LOCAL_HARDWARE']:

        message = message.ljust(LCD_WIDTH, " ")

        message = '123456789-123456789-'

        lcd_byte(line, LCD_CMD)

        for i in range(LCD_WIDTH):
            lcd_byte(ord(message[i]), LCD_CHR)

    else:
        print(f"- lcd_string('{message}', {line})")


# def get_ip_address():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     return s.getsockname()[0]
#
#
# lcd = {'msg': ["default msg line 1",
#                "default msg line 2",
#                "default msg line 3",
#                "default msg line 4"
#                ],
#        'backlight': 1}
