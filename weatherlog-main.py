#!/usr/bin/python3

import MySQLdb as ms
from sshtunnel import SSHTunnelForwarder


#create ssh tunnel to cloud server
print('connecting to cloud server...')
with SSHTunnelForwarder(
    "ssh.pythonanywhere.com",
    ssh_password = "XXXXXXXXXXX",
    ssh_username = "iambrett",
    remote_bind_address=('iambrett.mysql.pythonanywhere-services.com', 3306)
) as server:
    #connect to cloud database
    print('connecting to cloud database...')
    db = ms.connect(
        host = "127.0.0.1",
        user = "iambrett",
        passwd = "weather1",
        port = server.local_bind_port,
        db = "iambrett$weatherlog")



#create cursor object
print('Creating cursor object...')
c = db.cursor()


#run mysql commands
print('Executing MySQL commands...')
c.execute("""use iambrett$weatherlog""")
str1 = c.execute("""DESCRIBE weatherVars""")


#close cursor and database
print('Closing cursor and database...')
c.close()
db.close()
