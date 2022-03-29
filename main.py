#Run with: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Server says It's All Good Man"}


@app.get("/bills")
async def getbills():
    return {"message" : "GET /bills good"}


@app.get("/bill/{billId}")
async def getbills(billId):
    return {"message" : billId}


@app.post("/bill")
async def postbill():
    return {"message" : "POST /bill good"}


@app.put("/bill")
async def postbill():
    return {"message" : "PUT /bill good"}


@app.delete("/bill/{billId}")
async def deletebill():
    return {"message" : "DELETE /bill good"}