#!/usr/bin/python3

#import MySQLdb as ms
import mysql.connector as conn
import sshtunnel
import datetime
import smbus2
import bme280


#set max timeout
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


#create ssh tunnel to cloud server
print('connecting to cloud server...')
with sshtunnel.SSHTunnelForwarder(
    ("ssh.pythonanywhere.com"),
    ssh_password = "XXXXXXXXXXXX",
    ssh_username = "iambrett",
    remote_bind_address=('iambrett.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    #connect to cloud database
    print('connecting to database...')
    db = conn.connect(
        host = "127.0.0.1",
        user = "iambrett",
        password = "weather1",
        port = tunnel.local_bind_port,
        database = "iambrett$weatherlog") 



    #define date/time variables
    print("defining date and time variables...")
    now = datetime.datetime.now()
    today = str(now.date())
    currenttime  = "{:02d}:{:02d}:{:02d}".format(now.hour,now.minute,now.second)

    
    
        #read data from sensor
    print("reading data from sensor...")
    port = 1
    address = 0x77
    bus = smbus2.SMBus(port)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)


    #define the new variables to be sent to database
    newWeatherVars = (today, currenttime, str(data.humidity), str(data.temperature), str(data.pressure))


    #write data to database
    c1 = db.cursor()
    print("defining query 1...")
    query1 = ("INSERT INTO weatherVars "
             "(date, time, humidity, temp, pressure) "
             "VALUES (%s, %s, %s, %s, %s)")
    print("executing query 1...")
    c1.execute(query1, newWeatherVars)
    print("closing cursor 1")
    c1.close()


    #read data from database (use for debugging)
##    c2 = db.cursor()
##    print("defining query2...")
##    query2 = ("SELECT * FROM weatherVars;")
##    print("executing query 2...")
##    c2.execute(query2)
##    print("\nprinting table...")
##    for i in c2:
##        print(i)
##    c2.close()



    #close cursor object and database connection
    print('closing cursor and database connection...')
    c.close()
    db.close()
