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

#Drop database
mycursor.execute("DROP DATABASE bills")