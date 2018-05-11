# coding: utf-8

import serial


class Port:

    port = serial.Serial

    def __init__(self, conf):
        self.port = serial.Serial(
            port=conf.get('port_settings', 'port'),
            baudrate=conf.getint("port_settings", "baudrate"),
            parity=conf.get("port_settings", "parity"),
            stopbits=conf.getint("port_settings", "stopbits"),
            bytesize=conf.getint("port_settings", "bytesize")
        )

    def openPort(self):
        try:
            self.port.open()
        except Exception as e:
            print("Error open serial port " + str(e))

    def closePort(self):
        self.port.close()

    def read(self):
        mes = self.port.readline().decode()
        if not (mes[0] == "$"):
            #print("Принято некоректное сообщение: " + mes)
            return ""
        else:
            return mes

    def write(self, message):
        self.port.write(message.encode())
