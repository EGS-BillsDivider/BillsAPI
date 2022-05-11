CREATE DATABASE IF NOT EXISTS bills;

USE bills;

CREATE TABLE IF NOT EXISTS BILLS (
    id              VARCHAR(255),
    billPayer       INT NOT NULL,
    billReceiver    INT NOT NULL,
    payDate         DATE,
    payValue        FLOAT NOT NULL,
    PRIMARY KEY (id)
);