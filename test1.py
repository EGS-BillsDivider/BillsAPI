import requests
import json

headers = {
    "authToken": "YWxhZGRpbjpvcGVuc2VzYW1l"
}


#------GET ALL BILLS TEST---------
#x = requests.get("http://127.0.0.1:8000/bills/", headers=headers)

#------GET BILL BY ID TEST---------
#x = requests.get("http://127.0.0.1:8000/bill/b93bd466-b467-11ec-bdde-28e347778ade", headers=headers)

#------DELETE TEST---------
#x = requests.delete("http://127.0.0.1:8000/bill/b93bd466-b467-11ec-bdde-28e347778ade", headers=headers)


#------POST TEST---------
data = { "billPayer": 123456789, "payDate": "2019-05-08", "payedValue" : 15.05}
x = requests.post("http://127.0.0.1:8000/bill", data=json.dumps(data), headers=headers)


#------PUT TEST---------
#data = {"billReceiver" : 456123789, "billPayer": 123456789, "payDate": "2019-05-08", "payedValue" : 15.05}
#x = requests.put("http://127.0.0.1:8000/bill/49eb069f-b468-11ec-bdde-28e347778ade", headers=headers ,data=json.dumps(data))

print(x)
print(x.json())