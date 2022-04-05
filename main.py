#Run with: uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
import mysql.connector
from credentials import myHost, myUser, myPassword
from uuid import UUID
from bill import Bill



app = FastAPI()

#Set mysql access credentials
mydb = mysql.connector.connect(
  host=myHost,
  user=myUser,
  password=myPassword
)
#Cursor to access mysql
mycursor = mydb.cursor()
mycursor.execute("USE bills")




@app.get("/")
async def root():
    return {"message" : "Server says It's All Good Man"}


@app.get("/bills")
async def getbills():
    mycursor.execute("SELECT * FROM BILLS")
    res = []
    for value in mycursor:
        res.append({"billReceiver": int(value[1]) , "billPayer": int(value[2]), "payDate": str(value[3]), "payedValue": float(value[4])})  
    return res


@app.get("/bill/{billId}")
async def getbills(billId : str):
    #Verify if billId is valid
    try:
        UUID(billId)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid bill id supplied")
    
    #Search for the bill and throw 404 if not found
    select = "SELECT * FROM BILLS WHERE id = (%s)"
    mycursor.execute(select, [billId])
    value = mycursor.fetchone()
    if value == None:
        raise HTTPException(status_code=404, detail="Bill requested cannot be found in the system")
    else:
        return {"billReceiver": int(value[1]) , "billPayer": int(value[2]), "payDate": str(value[3]), "payedValue": float(value[4])}


@app.post("/bill")
async def postbill(bill : Bill):
    #Generate an uuid
    mycursor.execute("SELECT uuid()")
    uuid = mycursor.fetchone()

    #Insert bill in the database
    insert = "INSERT INTO BILLS VALUES (%s, %s, %s, %s, %s)"
    values = (uuid[0], bill.billReceiver, bill.billPayer, bill.payDate, bill.payedValue)
    mycursor.execute(insert, values)
    mydb.commit()
    #FALTA VERIRICAR UUID E OUTRAS CENAS
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=500, detail="An unexpected error has occured")
    else:
        return {"uuid" : uuid[0]}


@app.put("/bill")
async def putbill():
    return {"message" : "PUT /bill good"}


@app.delete("/bill/{billId}")
async def deletebill(billId : str):
    #Verify if billId is valid
    try:
        UUID(billId)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid bill id supplied")
    
    #Search for the bill to be deleted and throw 404 if not found
    delete = "DELETE FROM BILLS WHERE id = (%s)"
    mycursor.execute(delete, [billId])
    mydb.commit()
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Bill requested cannot be found in the system")
    else:
        raise HTTPException(status_code=200, detail="Bill successfully deleted")