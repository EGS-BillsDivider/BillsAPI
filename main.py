#Run with: uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
import mysql.connector
from credentials import myHost, myUser, myPassword
from uuid import UUID

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
async def postbill():
    return {"message" : "POST /bill good"}


@app.put("/bill")
async def postbill():
    return {"message" : "PUT /bill good"}


@app.delete("/bill/{billId}")
async def deletebill():
    return {"message" : "DELETE /bill good"}