import mysql.connector
from credentials import myHost, myUser, myPassword

#Set mysql access credentials
mydb = mysql.connector.connect(
  host=myHost,
  user=myUser,
  password=myPassword
)
#Cursor to access mysql
mycursor = mydb.cursor()

#Create bills database
mycursor.execute("CREATE DATABASE IF NOT EXISTS bills")
mycursor.execute("USE bills")

#Create table to store bills
mycursor.execute("""
CREATE TABLE IF NOT EXISTS BILLS (
    id              VARCHAR(255),
    billPayer       INT NOT NULL,
    billReceiver    INT NOT NULL,
    payDate         DATE,
    payValue        FLOAT NOT NULL,
    PRIMARY KEY (id)
);
""")

print("Database and BILLS Table created successfully!!!")