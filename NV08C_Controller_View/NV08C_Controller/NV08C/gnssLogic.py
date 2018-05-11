import serial
import time
import configparser
import re
from portWork import *
from driver import UARTDriver
from models import viewNV08C_DriverStatus, viewNV08C_GNSSData


class GNSSC:

    def __init__(self):
        __conf__ = configparser.RawConfigParser()
        __configFilePath__ = r'settings.ini'
        __conf__.read(__configFilePath__)
        __port__ = Port(__conf__)
        self.gnss = __port__

    def closePort(self):
        self.gnss.closePort()

    def calcSum(self, message):
        rez = 0
        for i in message:
            rez = rez ^ ord(i)
        rezult = hex(rez)  # Конвертируем в 0x
        rezult = rezult.upper()
        rezult = rezult[2:]  # Функция hex возвращает строку, нужно отрезать от нее первые 2 символа, которые указывают на формат
        return rezult


    def createMessage(self, message):
        return "$" + message + "*" + self.calcSum(message) + "\r\n"


    def getConfig(self):
        n = 1
        while n < int(conf.get('Commands', 'size')) + 1:
            message = conf.get('Commands', str(n))
            self.gnss.write(createMessage(message))
            time.sleep(0.5)  # Даем время порту записать данные
            n += 1



    def checkSum(self, message):
        if not message:
            return False
        print("Проверка контрольной суммы")
        mesSum = (re.search('(?<=\*)[0-9A-F]{2}', message))
        if not (mesSum is None):
            print("sum="+mesSum.group())
        else:
            print("None sum")
        mes = re.search('[^$][A-Z0-9,.]*', message)
        if not (mes is None):
            print("mes="+mes.group())
            print("calcSum="+self.calcSum(mes.group()))
        else:
            print("None mes")

        if mesSum is None or mes is None:
            print("Не найдена сумма или сообщение")
            return False

        if self.calcSum(mes.group()) == mesSum.group():
            print("Успешно завершенно")
            return True
        else:
            print("Проверка не пройдена")
            return False


    def checkAnswer(self, time=100):
        messages = []
        i = 0
        while i < time:
            mes = self.gnss.read()
            if len(mes) == 0:
                i += 1
                continue
            print("Поступило: "+mes)
            print("Сейчас начнется проверка контрольной суммы")
            if self.checkSum(mes) == False:
                i += 1
                continue
            print("Проверка завершенна, добавляем команду в список")
            b = mes.split(',')
            if messages.count(b[0]) == 0:    # b[0] - первый элемент списка содержить индефикатор команды
                messages.append(b[0])
            i += 1
        for j in messages:
            print(j + " is received")
        if not messages:
            print("|___________Установка не отвечает___________|")


# Сбор данных для последующего внесения их  в БД
    def collectData(self, timeWork):
        import time
        isTime = False
        isCoordinate = False
        isDate = False
        isSatCount = False
        data = dict(time ="", coordinate = "", date = "",  satellitesCount = "", dataFlag = "")
        i = 0
        endTime = time.time()
        startTime = time.time()
        try:
            print("Сбор данных...")
            while endTime-startTime < timeWork:
                message = self.gnss.read()
                if self.checkSum(message) == False:
                    continue

                timegr = (re.search('[0-9]{6}[.][0-9]{2}', message))
                if not (timegr is None):
                    timeData = (timegr.group())
                    data["time"] = timeData
                    isTime = True

                coordgr = (re.search('[0-9]{4}[.][0-9]{4}[,][NS][,][0-9]{5}[.][0-9]{4}[,][EW]', message))
                if not (coordgr is None):
                    coord = (coordgr.group())
                    data["coordinate"] = coord
                    isCoordinate = True

                dategr = (re.search('[0-9]{6}(?=,)', message))
                if not (dategr is None):
                    date = (dategr.group())
                    data["date"] = date
                    isDate = True

                satellitesgr = (re.search('(?<=\,)[0-9]{2}(?=,)', message))
                if not (satellitesgr is None):
                    satellites = (satellitesgr.group())
                    data["satellitesCount"] = satellites
                    isSatCount = True
                endTime = time.time()

                if (isTime and isCoordinate and isDate and isSatCount) == True:
                    data["dataFlag"] = "all data collected"
                    break
                if (isTime and isCoordinate and isDate and isSatCount) != True:
                    data["dataFlag"] = "incomplete data"

        except Exception:
            pass
        return data


    def printData(self, data):
        for key in data:
            print(key, data[key])


    def dataLoop(self, sleep):
        try:
            while True:
                data = self.collectData(5)
                self.printData(data)
                self.checkDriver()
                self.dataRecord(data)
                time.sleep(sleep)
        except KeyboardInterrupt:
            self.closePort()


    def dataRecord(self, gnssData):
        rec = viewNV08C_GNSSData(
        time = gnssData["time"],
        coordinate = gnssData["coordinate"] + self.radToGrad(gnssData["coordinate"]),
        date = gnssData["date"],
        satellitesCount = gnssData["satellitesCount"],
        dataFlag = gnssData["dataFlag"])
        rec.save()
        dr = UARTDriver()
        driverSt = viewNV08C_DriverStatus(
        status = dr.getStatus())
        driverSt.save()
        print("Данные записаны в базу!")


    def checkDriver(self):
        driver = UARTDriver()
        for item in driver.getStatus():
            try:
                print(item.decode())
            except Exception:
                pass

        
    def radToGrad(self, coordinate):
        coordgr = (re.search('[0-9]{4}[.][0-9]{4}(?=,)', coordinate))
        if not (coordgr is None):
            coordns = float(coordgr.group())
            coordns = coordns * 180/3.14
        coordgr = (re.search('[0-9]{5}[.][0-9]{4}(?=,)', coordinate))
        if not (coordgr is None):
            coordew = float(coordgr.group())
            coordew = coordew * 180 / 3.14
        return  str(coordns) + "NS " + str(coordew)+ "EW"






