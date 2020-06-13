import os
import time
import logging


class LCD_Hardware():
    logging.info(f"os.getenv('LOCAL_HARDWARE') {os.getenv('LOCAL_HARDWARE')}")

    lcd_state = {'msg': {'line1': "",
                         'line2': "",
                         'line3': "",
                         'line4': ""
                         },
                 'backlight': 1}

    lcd_initialized = False

    if os.getenv('LOCAL_HARDWARE') == "1":

        logging.info("Enabling Local hardware")

        import smbus

        # Define some device parameters
        I2C_ADDR = 0x27  # I2C device address
        LCD_WIDTH = 20   # Maximum characters per line

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

        # Open I2C interface
        # bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
        bus = smbus.SMBus(1)    # Rev 2 Pi uses 1

        def lcd_byte(self, bits, mode):
            # Send byte to data pins
            # bits = the data
            # mode = 1 for data
            #        0 for command

            bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
            bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

            # High bits
            self.bus.write_byte(self.I2C_ADDR, bits_high)
            self.lcd_toggle_enable(bits_high)

            # Low bits
            self.bus.write_byte(self.I2C_ADDR, bits_low)
            self.lcd_toggle_enable(bits_low)

        def lcd_toggle_enable(self, bits):
            # Toggle enable

            time.sleep(self.E_DELAY)
            self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
            time.sleep(self.E_PULSE)
            self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
            time.sleep(self.E_DELAY)

        def lcd_string(self, message, line):
            # Send string to display

            message = message.ljust(self.LCD_WIDTH, " ")

            if line == 1:
                line_address = self.LCD_LINE_1

            if line == 2:
                line_address = self.LCD_LINE_2

            if line == 3:
                line_address = self.LCD_LINE_3

            if line == 4:
                line_address = self.LCD_LINE_4

            logging.info(f"Updating LCD line '{line}' at '{line_address}' with text '{message}'")
            print(f"Updating LCD line '{line}' at '{line_address}' with text '{message}'")

            self.lcd_byte(line_address, self.LCD_CMD)
            for i in range(self.LCD_WIDTH):
                self.lcd_byte(ord(message[i]), self.LCD_CHR)
                # print(f" ch: '{message[i]}' ord: '{ord(message[i])}'")
                time.sleep(self.E_DELAY)

        def initialize_lcd(self):
            # Initialise display
            print("Initializing local hardware")

            self.lcd_byte(0x33, self.LCD_CMD)  # 110011 Initialize
            self.lcd_byte(0x32, self.LCD_CMD)  # 110010 Initialize
            self.lcd_byte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
            self.lcd_byte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
            self.lcd_byte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
            self.lcd_byte(0x01, self.LCD_CMD)  # 000001 Clear display
            time.sleep(self.E_DELAY)

            print("Initialized\n")

        def lcd_get_line(self, line):
            line_names = ['line1', 'line2', 'line3', 'line4', ]
            print(f"line {line}")
            if line < 1 or line > 4:
                return None

            line = line - 1
            print(f"line: {line}, name {line_names[line]}, value {self.lcd_state['msg'].get(line_names[line]}")
            return self.lcd_state['msg'].get(line_names[line], '')

        def lcd_get_lines(self):
            lines = []
            for i in range(4):
                lines.append(self.lcd_get_line(i))
            return lines

        def lcd_clear(self):
            self.lcd_state['msg']['line1'] = ""
            self.lcd_state['msg']['line2'] = ""
            self.lcd_state['msg']['line3'] = ""
            self.lcd_state['msg']['line4'] = ""

            self.lcd_string(self.lcd_state['msg']['line1'], 1)
            self.lcd_string(self.lcd_state['msg']['line2'], 2)
            self.lcd_string(self.lcd_state['msg']['line3'], 3)
            self.lcd_string(self.lcd_state['msg']['line4'], 4)

        def lcd_update(self, line1=None, line2=None, line3=None, line4=None):
            if line1 is not None:
                self.lcd_state['msg']['line1'] = line1

            if line2 is not None:
                self.lcd_state['msg']['line2'] = line2

            if line3 is not None:
                self.lcd_state['msg']['line3'] = line3

            if line4 is not None:
                self.lcd_state['msg']['line4'] = line4

            self.lcd_string(self.lcd_state['msg']['line1'], 1)
            self.lcd_string(self.lcd_state['msg']['line2'], 2)
            self.lcd_string(self.lcd_state['msg']['line3'], 3)
            self.lcd_string(self.lcd_state['msg']['line4'], 4)

        def post_msg_to_queue(self, action):
            self.lcd_state['msg']['line2'] = "test"
            print(f"workign with LCD: {action['action']}")
            print(f"LCD {self.lcd_state}")
            if action['action'] == 'initialize':
                print("FAIL NOP :: Initialized\n")

            if action['action'] == 'display':
                # data = task.get('data', {'msg': '', 'line': 0})
                # msg = data.get('msg', '')
                # line = data.get('line', 0)

                self.lcd_string(self.lcd_state['msg'])

            if action['action'] == 'test':
                print("test was called")

            if action['action'] == 'redisplay':

                self.lcd_string(self.lcd_state['msg']['line1'], 1)
                # lcd_string("test", 1)
                self.lcd_string(self.lcd_state['msg']['line2'], 2)
                self.lcd_string(self.lcd_state['msg']['line3'], 3)
                self.lcd_string(self.lcd_state['msg']['line4'], 4)

                logging.info(f"Line 1: '{self.lcd_state['msg']['line1']}'")
                logging.info(f"Line 2: '{self.lcd_state['msg']['line2']}'")
                logging.info(f"Line 3: '{self.lcd_state['msg']['line3']}'")
                logging.info(f"Line 4: '{self.lcd_state['msg']['line4']}'")

            logging.info("Thread - message processed\n\n")

    else:
        logging.info("No Local hardware :: creating NOP functions")

        def lcd_byte(bits, mode):
            logging.info(f"NOP :: write byte {bits}, {mode}")

        def lcd_toggle_enable(bits):
            logging.info(f"NOP :: toggle bits {bits}")

        def lcd_string(message, line):
            logging.info(f"NOP :: write string '{message}' at line {line}")

        def initialize_lcd(self):
            logging.info("NOP :: initialize LCD")
