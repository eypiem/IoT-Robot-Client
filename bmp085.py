import smbus
import time


bus = smbus.SMBus(1)


class BMP085:
    ADDR = 0x77
    OSS = 0
    ac1 = None
    ac2 = None
    ac3 = None
    ac4 = None
    ac5 = None
    ac6 = None
    b1 = None
    b2 = None
    mb = None
    mc = None
    md = None
    b5 = None

    def init(self):
        reg_data = bus.read_i2c_block_data(self.ADDR, 0xAA, 22)
        self.ac1 = reg_data[0] << 8 | reg_data[1]
        if self.ac1 > 35676:
            self.ac1 -= 65536
        self.ac2 = reg_data[2] << 8 | reg_data[3]
        if self.ac2 > 35676:
            self.ac2 -= 65536
        self.ac3 = reg_data[4] << 8 | reg_data[5]
        if self.ac3 > 35676:
            self.ac3 -= 65536
        self.ac4 = reg_data[6] << 8 | reg_data[7]
        self.ac5 = reg_data[8] << 8 | reg_data[9]
        self.ac6 = reg_data[10] << 8 | reg_data[11]
        self.b1 = reg_data[12] << 8 | reg_data[13]
        if self.b1 > 35676:
            self.b1 -= 65536
        self.b2 = reg_data[14] << 8 | reg_data[15]
        if self.b2 > 35676:
            self.b2 -= 65536
        self.mb = reg_data[16] << 8 | reg_data[17]
        if self.mb > 35676:
            self.mb -= 65536
        self.mc = reg_data[18] << 8 | reg_data[19]
        if self.mc > 35676:
            self.mc -= 65536
        self.md = reg_data[20] << 8 | reg_data[21]
        if self.md > 35676:
            self.md -= 65536

    def get_temperature(self):
        ut = self.read_ut()
        x1 = ((ut - self.ac6) * self.ac5) >> 15
        x2 = int((self.mc << 11) / (x1 + self.md))
        self.b5 = x1 + x2
        return (self.b5 + 8) >> 4

    def get_pressure(self):
        up = self.read_up()
        b6 = self.b5 - 4000
        x1 = (self.b2 * ((b6 * b6) >> 12)) >> 11
        x2 = (self.ac2 * b6) >> 11
        x3 = x1 + x2
        b3 = (((self.ac1 * 4 + x3) << self.OSS) + 2) >> 2

        x1 = (self.ac3 * b6) >> 13
        x2 = (self.b1 * ((b6 * b6) >> 12)) >> 16
        x3 = ((x1 + x2) + 2) >> 2
        b4 = (self.ac4 * (x3 + 32768)) >> 15

        b7 = (up - b3) * (50000 >> self.OSS)
        if b7 < 0x80000000:
            p = int((b7 << 1) / b4)
        else:
            p = int(b7 / b4) << 1

        x1 = (p >> 8) * (p >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        p += (x1 + x2 + 3791) >> 4

        return p

    def read_ut(self):
        bus.write_byte_data(self.ADDR, 0xF4, 0x2E)
        time.sleep(4.5 / 1000)
        reg_data = bus.read_i2c_block_data(self.ADDR, 0xF6, 2)
        return reg_data[0] << 8 | reg_data[1]

    def read_up(self):
        bus.write_byte_data(self.ADDR, 0xF4, 0x34 + (self.OSS << 6))
        time.sleep((2 + (3 << self.OSS)) / 1000)
        reg_data = bus.read_i2c_block_data(self.ADDR, 0xF6, 3)
        up = ((reg_data[0] << 16) | (reg_data[1] << 8) | reg_data[2]) >> (8 - self.OSS)
        return up

    def read(self):
        return self.get_temperature(), self.get_pressure()


def main():
    bmp = BMP085()
    bmp.init()
    try:
        while True:
            print(bmp.get_temperature())
            print(bmp.get_pressure())
            print()
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        pass
    print('Done.')


if __name__ == '__main__':
    main()
