from models import viewNV08C_DriverStatus, viewNV08C_GNSSData

driverSt = viewNV08C_DriverStatus(
status = "7")
driverSt.save()

rec = viewNV08C_GNSSData(
        time ="1",
        coordinate = "2",
        date = "3",
        satellitesCount = "4",
        dataFlag ="5")
rec.save()

print("Данные записаны в базу!")


