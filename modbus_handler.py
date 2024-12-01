import serial
from time import sleep

class ModbusHandler:

   # Soros kapcsolat inicializálás
    def __init__(self, port, baudrate, timeout):

        self.serial_port = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        )

    # CRC-16 Számítás
    def calculate_crc(self, data):

        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc.to_bytes(2, byteorder='little')

    # Modbus RTU kérés küldése
    def send_request(self, device_address, function_code, register_address, value):

        message = bytearray()
        message.append(device_address)
        message.append(function_code)
        message.extend(register_address.to_bytes(2, byteorder='big'))
        message.extend(value.to_bytes(2, byteorder='big'))
        crc = self.calculate_crc(message)
        message.extend(crc)

        # Üzenet küldése
        self.serial_port.write(message)
        sleep(0.1)

        # Válasz olvasása
        response = self.serial_port.read(8)
        if not response:
            raise TimeoutError("No response from device.")
        return response

    def write_register(self, device_address, register_address, value):

        response = self.send_request(device_address, 0x06, register_address, value)
        return response

    def read_register(self, device_address, register_address):

        response = self.send_request(device_address, 0x03, register_address, 0)
        if len(response) < 7:
            raise ValueError("Invalid response length.")
        value = int.from_bytes(response[3:5], byteorder='big')
        return value

    def close(self):

        self.serial_port.close()
