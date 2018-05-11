import subprocess

class UARTDriver:

    def getStatus(self):
        if self.findDriver():
            args = ["cat"+" /proc/tty/driver/xuartps"]
            process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
            data = process.communicate()
            return data[0].decode()
        else:
            return "None driver"

    def findDriver(self):
        args = ["ls"+" /proc/tty/driver"]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        data = process.communicate()        
        for line in data:
            if line.decode().find("xuartps") >-1:               
                return True
            else:
                return False


