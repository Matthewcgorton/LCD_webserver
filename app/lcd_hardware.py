import time
import logging

class LCD_Hardware():

    def __init__(self, bus_interface=1, I2C_ADDR=0x27, LCD_WIDTH=20, local_hardware=True):
        self.local_hardware = local_hardware
        self.I2C_ADDR = I2C_ADDR
        self.LCD_WIDTH = LCD_WIDTH
        self.bus_interface = bus_interface
        self.lcd_initialized = False

        if self.local_hardware:
            import smbus
            self.bus = smbus.SMBus(self.bus_interface)


        self.lcd_state = {'msg': {'line1': "",
                                  'line2': "",
                                  'line3': "",
                                  'line4': ""
                                  },
                          'backlight': 1}

        # Define some device constants
        self.LCD_CHR = 1  # Mode - Sending data
        self.LCD_CMD = 0  # Mode - Sending command

        self.LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
        self.LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
        self.LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

        self.LCD_BACKLIGHT = 0x08  # On
        # self.LCD_BACKLIGHT = 0x00  # Off

        self.ENABLE = 0b00000100  # Enable bit

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005


    def _lcd_byte(self, bits, mode):
        if self.local_hardware:

            # Send byte to data pins
            # bits = the data
            # mode = 1 for data
            #        0 for command

            bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
            bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

            # High bits
            self.bus.write_byte(self.I2C_ADDR, bits_high)
            self._lcd_toggle_enable(bits_high)

            # Low bits
            self.bus.write_byte(self.I2C_ADDR, bits_low)
            self._lcd_toggle_enable(bits_low)

        else:
            logging.info(f"NOP :: write byte {bits}, {mode}")
            print(f"NOP :: write byte {bits}, {mode}")


    def _lcd_toggle_enable(self, bits):
        # Toggle enable
        if self.local_hardware:

            time.sleep(self.E_DELAY)
            self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
            time.sleep(self.E_PULSE)
            self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
            time.sleep(self.E_DELAY)

        else:
            logging.info(f"NOP :: toggle bits {bits}")

    def initialize_lcd(self, new_bus=False):
        # Initialise display
        if self.local_hardware:
            print("Initializing local hardware")
            logging.info("Enabling Local hardware")

            try:
                if new_bus:
                    import smbus
                    self.bus = smbus.SMBus(self.bus_interface)

                self._lcd_byte(0x33, self.LCD_CMD)  # 110011 Initialize
                self._lcd_byte(0x32, self.LCD_CMD)  # 110010 Initialize
                self._lcd_byte(0x06, self.LCD_CMD)  # 000110 Cursor move direction
                self._lcd_byte(0x0C, self.LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
                self._lcd_byte(0x28, self.LCD_CMD)  # 101000 Data length, number of lines, font size
                self._lcd_byte(0x01, self.LCD_CMD)  # 000001 Clear display
                time.sleep(self.E_DELAY)

                self.lcd_initialized = True
                logging.info("Initialized")
                print("Initialized\n")

            except Exception:
                self.lcd_initialized = False
                logging.info("Failed :: LCD Now Initialized")
                print("Failed :: LCD Now Initialized\n")

        else:
            logging.info("NOP :: initialize")
            print("NOP :: Initialized\n")

    def lcd_reset(self):
        if self.local_hardware:
            self.initialize_lcd()
            logging.info("reseting LCD")

        else:
            logging.info("NOP :: reseting LCD")

        return


    def _lcd_string(self, message, line):
        # Send string to display
        if self.local_hardware and self.lcd_initialized:

            message = message.ljust(self.LCD_WIDTH, " ")

            if line == 1:
                line_address = self.LCD_LINE_1

            if line == 2:
                line_address = self.LCD_LINE_2

            if line == 3:
                line_address = self.LCD_LINE_3

            if line == 4:
                line_address = self.LCD_LINE_4

            # logging.info(f"Updating LCD line '{line}' at '{line_address}' with text '{message}'")
            # print(f"Updating LCD line '{line}' at '{line_address}' with text '{message}'")

            self._lcd_byte(line_address, self.LCD_CMD)
            for i in range(self.LCD_WIDTH):
                self._lcd_byte(ord(message[i]), self.LCD_CHR)
                # print(f" ch: '{message[i]}' ord: '{ord(message[i])}'")
                time.sleep(self.E_DELAY)
        else:
            logging.info(f"NOP :: write string '{message}' at line {line}")



    def lcd_get_line(self, line):
        line_names = ['line1', 'line2', 'line3', 'line4', ]
        print(f"\nline {line}")
        if line < 1 or line > 4:
            return None

        line = line - 1
        # print(f"line: {line}, name {line_names[line]}, value '{self.lcd_state['msg'][line_names[line]]}'")
        # print(f"line: {line}, name {line_names[line]}, value '{self.lcd_state['msg']}'")
        return self.lcd_state['msg'][line_names[line]]

    def lcd_get_lines(self):
        lines = []
        for i in range(4):
            lines.append(self.lcd_get_line(i + 1))
        # print(f"Lines: {lines}")

        return lines

    def lcd_clear(self):
        self.lcd_state['msg']['line1'] = ""
        self._lcd_string(self.lcd_state['msg']['line1'], 1)

        self.lcd_state['msg']['line2'] = ""
        self._lcd_string(self.lcd_state['msg']['line2'], 2)

        self.lcd_state['msg']['line3'] = ""
        self._lcd_string(self.lcd_state['msg']['line3'], 3)

        self.lcd_state['msg']['line4'] = ""
        self._lcd_string(self.lcd_state['msg']['line4'], 4)

    def lcd_update(self, line1=None, line2=None, line3=None, line4=None):
        if line1 is not None and line1 != self.lcd_state['msg']['line1']:
            self.lcd_state['msg']['line1'] = line1
            self._lcd_string(self.lcd_state['msg']['line1'], 1)

        if line2 is not None and line2 != self.lcd_state['msg']['line2']:
            self.lcd_state['msg']['line2'] = line2
            self._lcd_string(self.lcd_state['msg']['line2'], 2)

        if line3 is not None and line3 != self.lcd_state['msg']['line3']:
            self.lcd_state['msg']['line3'] = line3
            self._lcd_string(self.lcd_state['msg']['line3'], 3)

        if line4 is not None and line4 != self.lcd_state['msg']['line4']:
            self.lcd_state['msg']['line4'] = line4
            self._lcd_string(self.lcd_state['msg']['line4'], 4)
