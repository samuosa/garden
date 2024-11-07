import smbus2
import time

# BME280 default address (change to 0x77 if necessary)
BME280_I2C_ADDRESS = 0x76

# Register addresses
BME280_REG_CONTROL_HUM = 0xF2
BME280_REG_CONTROL = 0xF4
BME280_REG_CONFIG = 0xF5
BME280_REG_DATA = 0xF7

# Compensation parameter registers
BME280_REG_CALIB = 0x88
BME280_REG_CALIB_H = 0xE1

def read_calibration_params(bus, address):
    # Read temperature and pressure calibration data
    calib = bus.read_i2c_block_data(address, BME280_REG_CALIB, 24)
    # Read humidity calibration data
    calib_h = bus.read_i2c_block_data(address, BME280_REG_CALIB_H, 7)
    
    # Convert byte data to word values
    dig_T1 = calib[1] << 8 | calib[0]
    dig_T2 = (calib[3] << 8 | calib[2])
    dig_T3 = (calib[5] << 8 | calib[4])

    dig_P1 = calib[7] << 8 | calib[6]
    dig_P2 = (calib[9] << 8 | calib[8])
    dig_P3 = (calib[11] << 8 | calib[10])
    dig_P4 = (calib[13] << 8 | calib[12])
    dig_P5 = (calib[15] << 8 | calib[14])
    dig_P6 = (calib[17] << 8 | calib[16])
    dig_P7 = (calib[19] << 8 | calib[18])
    dig_P8 = (calib[21] << 8 | calib[20])
    dig_P9 = (calib[23] << 8 | calib[22])

    dig_H1 = bus.read_byte_data(address, 0xA1)
    dig_H2 = (calib_h[1] << 8 | calib_h[0])
    dig_H3 = calib_h[2]
    dig_H4 = (calib_h[3] << 4) | (calib_h[4] & 0x0F)
    dig_H5 = (calib_h[5] << 4) | (calib_h[4] >> 4)
    dig_H6 = calib_h[6]

    # Convert calibration data to signed integers
    dig_T2 = to_signed(dig_T2, 16)
    dig_T3 = to_signed(dig_T3, 16)
    dig_P2 = to_signed(dig_P2, 16)
    dig_P3 = to_signed(dig_P3, 16)
    dig_P4 = to_signed(dig_P4, 16)
    dig_P5 = to_signed(dig_P5, 16)
    dig_P6 = to_signed(dig_P6, 16)
    dig_P7 = to_signed(dig_P7, 16)
    dig_P8 = to_signed(dig_P8, 16)
    dig_P9 = to_signed(dig_P9, 16)
    dig_H2 = to_signed(dig_H2, 16)
    dig_H4 = to_signed(dig_H4, 16)
    dig_H5 = to_signed(dig_H5, 16)
    dig_H6 = to_signed(dig_H6, 8)

    return {
        'T1': dig_T1,
        'T2': dig_T2,
        'T3': dig_T3,
        'P1': dig_P1,
        'P2': dig_P2,
        'P3': dig_P3,
        'P4': dig_P4,
        'P5': dig_P5,
        'P6': dig_P6,
        'P7': dig_P7,
        'P8': dig_P8,
        'P9': dig_P9,
        'H1': dig_H1,
        'H2': dig_H2,
        'H3': dig_H3,
        'H4': dig_H4,
        'H5': dig_H5,
        'H6': dig_H6,
    }

def to_signed(val, bits):
    if val & (1 << (bits - 1)):
        return val - (1 << bits)
    else:
        return val

def write_config(bus, address):
    # Write oversampling settings and start measurement
    bus.write_byte_data(address, BME280_REG_CONTROL_HUM, 0x01)  # Humidity oversampling x1
    bus.write_byte_data(address, BME280_REG_CONTROL, 0x27)      # Temp and Pressure oversampling x1, mode normal

def read_raw_data(bus, address):
    # Read raw data from sensor
    data = bus.read_i2c_block_data(address, BME280_REG_DATA, 8)
    raw_pres = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    raw_temp = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    raw_hum = (data[6] << 8) | data[7]
    return raw_temp, raw_pres, raw_hum

def compensate_temperature(raw_temp, calib_params):
    var1 = (((raw_temp >> 3) - (calib_params['T1'] << 1)) * calib_params['T2']) >> 11
    var2 = (((((raw_temp >> 4) - calib_params['T1']) * ((raw_temp >> 4) - calib_params['T1'])) >> 12) * calib_params['T3']) >> 14
    t_fine = var1 + var2
    temperature = (t_fine * 5 + 128) >> 8
    return temperature / 100.0, t_fine

def compensate_pressure(raw_pres, t_fine, calib_params):
    var1 = t_fine - 128000
    var2 = var1 * var1 * calib_params['P6']
    var2 = var2 + ((var1 * calib_params['P5']) << 17)
    var2 = var2 + (calib_params['P4'] << 35)
    var1 = ((var1 * var1 * calib_params['P3']) >> 8) + ((var1 * calib_params['P2']) << 12)
    var1 = (((1 << 47) + var1) * calib_params['P1']) >> 33
    if var1 == 0:
        return 0  # Avoid division by zero
    p = 1048576 - raw_pres
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (calib_params['P9'] * (p >> 13) * (p >> 13)) >> 25
    var2 = (calib_params['P8'] * p) >> 19
    pressure = ((p + var1 + var2) >> 8) + (calib_params['P7'] << 4)
    return pressure / 25600.0

def compensate_humidity(raw_hum, t_fine, calib_params):
    v_x1_u32r = t_fine - 76800
    v_x1_u32r = (((((raw_hum << 14) - (calib_params['H4'] << 20) - (calib_params['H5'] * v_x1_u32r)) + 16384) >> 15) *
                 (((((((v_x1_u32r * calib_params['H6']) >> 10) * (((v_x1_u32r * calib_params['H3']) >> 11) + 32768)) >> 10) + 2097152) * calib_params['H2'] + 8192) >> 14))
    v_x1_u32r = v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * calib_params['H1']) >> 4)
    v_x1_u32r = max(v_x1_u32r, 0)
    v_x1_u32r = min(v_x1_u32r, 419430400)
    humidity = v_x1_u32r >> 12
    return humidity / 1024.0

def main():
    bus = smbus2.SMBus(1)  # Use bus 1

    address = BME280_I2C_ADDRESS

    # Read calibration parameters
    calib_params = read_calibration_params(bus, address)

    # Configure the sensor
    write_config(bus, address)

    print("Reading BME280 sensor data...")
    try:
        while True:
            # Read raw data from sensor
            raw_temp, raw_pres, raw_hum = read_raw_data(bus, address)

            # Compensate the raw data
            temperature, t_fine = compensate_temperature(raw_temp, calib_params)
            pressure = compensate_pressure(raw_pres, t_fine, calib_params)
            humidity = compensate_humidity(raw_hum, t_fine, calib_params)

            # Print the results
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Humidity: {humidity:.2f} %")
            print(f"Pressure: {pressure:.2f} hPa")
            print("-" * 30)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        bus.close()

if __name__ == '__main__':
    main()
