#!/usr/bin/python3

#import MySQLdb as ms
import mysql.connector as conn
import sshtunnel
import datetime


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


    today = "{}/{}/{}".format(now.month,now.day,now.year)
    currenttime  = "{}:{}:{}".format(now.hour,now.minute,now.second)

    
    

    #test connection by printing table information
    print("\nTable information")
    c = db.cursor()
    c.execute("DESCRIBE weatherVars;")
    for i in c.fetchall():
        print(i)


    #close cursor object and database connection
    print('closing cursor and database connection...')
    c.close()
    db.close()
