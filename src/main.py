#Run with: uvicorn main:app --reload

from fastapi import FastAPI, HTTPException, Header
import mysql.connector
from uuid import UUID
from bill import Bill, UpdateBill
from typing import Optional
import ast
import requests

app = FastAPI()

#Set mysql access credentials 
file = open("/tmp/secrets/credentials", "r")
content = file.read()
config = ast.literal_eval(content)
file.close()
mydb = mysql.connector.connect(**config)


#Cursor to access mysql
mycursor = mydb.cursor()
mycursor.execute("USE bills")




@app.get("/")
async def root():
    return {"Server says It's All Good Man"}


@app.get("/bills")
async def getbills(authToken: Optional[str] = Header(None)):
    #Verify auth token
    x = requests.get('http://api:3000/posts/verifyUser', headers={'auth-token': authToken})
    if(x.status_code != 200):
        #Excepção a lançar caso autenticação inválida
        raise HTTPException(status_code=401, detail="Unauthorized, invalid authentication credentials")
    
    mycursor.execute("SELECT * FROM BILLS")
    res = []
    for value in mycursor:
        res.append({"billReceiver": int(value[1]) , "billPayer": int(value[2]), "payDate": str(value[3]), "payedValue": float(value[4])})  
    return res


@app.get("/bill/{billId}")
async def getbills(billId : str, authToken: Optional[str] = Header(None)):
    #Verify auth token
    x = requests.get('http://api:3000/posts/verifyUser', headers={'auth-token': authToken})
    if(x.status_code != 200):
        #Excepção a lançar caso autenticação inválida
        raise HTTPException(status_code=401, detail="Unauthorized, invalid authentication credentials")
    
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
async def postbill(bill : Bill, authToken: Optional[str] = Header(None)):
    #Verify auth token
    x = requests.get('http://api:3000/posts/verifyUser', headers={'auth-token': authToken})
    if(x.status_code != 200):
        #Excepção a lançar caso autenticação inválida
        raise HTTPException(status_code=401, detail="Unauthorized, invalid authentication credentials")

    #Generate an uuid and verify if it exists or not
    while True:
        mycursor.execute("SELECT uuid()")
        uuid = mycursor.fetchone()
        mycursor.execute("SELECT * FROM BILLS WHERE id = (%s)", [uuid[0]])
        #Means that uuid generated doesn't exist therefore it can be used in the database
        if not mycursor.fetchone():
            break

    #Insert bill in the database
    insert = "INSERT INTO BILLS VALUES (%s, %s, %s, %s, %s)"
    values = (uuid[0], bill.billReceiver, bill.billPayer, bill.payDate, bill.payedValue)
    mycursor.execute(insert, values)
    mydb.commit()

    if mycursor.rowcount == 0:
        raise HTTPException(status_code=500, detail="An unexpected error has occured")
    else:
        return {"uuid" : uuid[0]}


@app.put("/bill/{billId}")
async def putbill(billId : str, bill : UpdateBill, authToken: Optional[str] = Header(None)):
    #Verify auth token
    x = requests.get('http://api:3000/posts/verifyUser', headers={'auth-token': authToken})
    if(x.status_code != 200):
        #Excepção a lançar caso autenticação inválida
        raise HTTPException(status_code=401, detail="Unauthorized, invalid authentication credentials")
    
    #Verify if billId is valid
    try:
        UUID(billId)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid bill id supplied")
    
    #Check if bill exists in the db
    mycursor.execute("SELECT * FROM BILLS WHERE id = (%s)", [billId])
    if not mycursor.fetchone():
        raise HTTPException(status_code=404, detail="Bill requested cannot be found in the system")
    
    #Check if all fields are empty or not
    if bill.billReceiver == None and bill.billPayer == None and bill.payDate == None and bill.payedValue == None:
        raise HTTPException(status_code=400, detail="All fields given are empty so is impossible to perform updates")
    else:
        if bill.billPayer:
            mycursor.execute("UPDATE BILLS SET billPayer = (%s) WHERE id = (%s)", [bill.billPayer, billId])
            mydb.commit()
        if bill.billReceiver:
            mycursor.execute("UPDATE BILLS SET billReceiver = (%s) WHERE id = (%s)", [bill.billReceiver, billId])
            mydb.commit()            
        if bill.payDate:
            mycursor.execute("UPDATE BILLS SET payDate = (%s) WHERE id = (%s)", [bill.payDate, billId])
            mydb.commit() 
        if bill.payedValue:
            mycursor.execute("UPDATE BILLS SET payValue = (%s) WHERE id = (%s)", [bill.payedValue, billId])
            mydb.commit() 
        
        raise HTTPException(status_code=200, detail="Bill successfully updated")


@app.delete("/bill/{billId}")
async def deletebill(billId : str, authToken: Optional[str] = Header(None)):
    #Verify auth token
    x = requests.get('http://api:3000/posts/verifyUser', headers={'auth-token': authToken})
    if(x.status_code != 200):
        #Excepção a lançar caso autenticação inválida
        raise HTTPException(status_code=401, detail="Unauthorized, invalid authentication credentials")
    
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