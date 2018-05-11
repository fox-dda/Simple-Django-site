
from driver import UARTDriver
from gnssLogic import *

gnss = GNSSC()  # Инициализация порта
#ser.openPort()
#gnss.getConfig()
#gnss.checkAnswer(15)
#gnss.printData(gnss.collectData(10)[0])
#gnss.dataRead()
#gnss.checkAnswer()
gnss.dataLoop(30)
gnss.closePort()

