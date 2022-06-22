import requests
import json

headers = {
    "authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2MmIyNWU1MDE2ZmRjZGRjODUzM2IzZmUiLCJpYXQiOjE2NTU4NTg1NTB9.MM3jMviTCtMuBBLKAs5zlYgm7y9RT5gspWWFcIZQqXY"
}


#data = { "user": "1de665c1-e4dc-11ec-957d-080027dd5c98","name": "teste"}
#x = requests.post("http://localhost:39691/channel", headers=headers, data=data)


#------GET ALL BILLS TEST---------
x = requests.get("http://localhost:37903/bills/", headers=headers)

#------GET BILL BY ID TEST---------
#x = requests.get("http://localhost:45251/bill/8a70ab4c-ef4f-11ec-b630-da3af243af6d", headers=headers)

#------DELETE TEST---------
#x = requests.delete("http://localhost:37903/bill/741eae4f-f1c4-11ec-8678-02cc14a5a634", headers=headers)


#------POST TEST---------
#data = { "billPayer": 123456789, "billReceiver": 12345688, "payDate": "2019-05-08", "payedValue" : 15.05}
#x = requests.post("http://localhost:37903/bill", data=json.dumps(data), headers=headers)


#------PUT TEST---------
#data = {"billReceiver" : 456123789, "billPayer": 123456789, "payDate": "2019-05-08", "payedValue" : 15.05}
#x = requests.put("http://localhost:45251/bill/8a70ab4c-ef4f-11ec-b630-da3af243af6d", headers=headers ,data=json.dumps(data))

print(x)
print(x.status_code)
print(x.json())