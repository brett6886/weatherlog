#!/usr/bin/python3

#import MySQLdb as ms
import mysql.connector as conn
import sshtunnel


#set max timeout
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0


#create ssh tunnel to cloud server
with sshtunnel.SSHTunnelForwarder(
    ("ssh.pythonanywhere.com"),
    ssh_password = "XXXXXXXXXXXXXXXXX",
    ssh_username = "iambrett",
    remote_bind_address=('iambrett.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    #connect to cloud database
    db = conn.connect(
        host = "127.0.0.1",
        user = "iambrett",
        password = "weather1",
        port = tunnel.local_bind_port,
        db = "iambrett$weatherlog") 


#c = db.cursor()
#headers = c.description

#for header in headers:
#    print(header)
 
db.close()
