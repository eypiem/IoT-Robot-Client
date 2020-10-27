import smbus
import time
import math


bus = smbus.SMBus(1)


class ADXL345():
    ADDR = 0x53

    def init(self):
        bus.write_byte_data(self.ADDR, 0x2D, 0x08)
        bus.write_byte_data(self.ADDR, 0x20, 0x03)
        bus.write_byte_data(self.ADDR, 0x2C, 0x0A)
        bus.write_byte_data(self.ADDR, 0x31, 0x02)


    def read(self):
        reg_val = bus.read_i2c_block_data(self.ADDR, 0x32, 6)
        x_g_raw = (reg_val[1] << 8) | reg_val[0]
        y_g_raw = (reg_val[3] << 8) | reg_val[2]
        z_g_raw = (reg_val[5] << 8) | reg_val[4]

        if x_g_raw > 32767:
            x_g_raw -= 65536
        if y_g_raw > 32767:
            y_g_raw -= 65536
        if z_g_raw > 32767:
            z_g_raw -= 65536

        x_g = x_g_raw / 256 * 4
        y_g = y_g_raw / 256 * 4
        z_g = z_g_raw / 256 * 4

#       print(x_g)
#       print(y_g)
#       print(z_g)

        pitch = math.atan2(-x_g, z_g) * 180 / math.pi
        roll = math.atan2(-y_g, z_g) * 180 / math.pi

#       print(pitch)
#       print(roll)

        return pitch, roll


def main():
    adxl = ADXL345()
    adxl.init()
    try:
        while True:
            adxl.read()
            print()
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        pass
    print('Done.')


if __name__ == '__main__':
    main()
