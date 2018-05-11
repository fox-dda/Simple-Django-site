import peewee

database = peewee.SqliteDatabase("db.sqlite3")

class viewNV08C_GNSSData(peewee.Model):
    time = peewee.CharField(max_length=8)
    coordinate = peewee.CharField()
    date = peewee.CharField()
    satellitesCount = peewee.CharField()
    dataFlag = peewee.CharField()

    class Meta:
        database = database


class viewNV08C_DriverStatus(peewee.Model):
    status = peewee.CharField()

    class Meta:
        database = database


try:
    viewNV08C_GNSSData.create_table()
except peewee.OperationalError:
    print("Artist table already exists!")
 
try:
    viewNV08C_DriverStatus.create_table()
except peewee.OperationalError:
    print("Album table already exists!")




