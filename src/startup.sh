#!/bin/sh
echo "Waiting for DB"

echo "" | nc -w 1  db 3306

while [ ! $? -eq 0 ]; do
    sleep 1
    echo "" | nc -w 1  db 3306
done
echo "DB Up"
sleep 5
echo "Starting"

uvicorn main:app --reload main:app  0.0.0.0:8000
