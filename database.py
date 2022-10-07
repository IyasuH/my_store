#!/usr/bin/python3
"""
To manage sqlite database
"""
import sqlite3
conn = sqlite3.connect('store.db')
c = conn.cursor()
def createTables():
    c.execute("CREATE TABLE if not exists customers(customerId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, customerName TEXT NOT NULL, customerTinNumber INT NOT NULL, customerRegion TEXT NOT NULL, customerSubcity TEXT NOT NULL, customerWereda INT NOT NULL, customerPhoneN INT NOT NULL, accountCreatedDate TEXT NOT NULL, frequencyOfPurchase INT NOT NULL, totalPurchase INT NOT NULL, bankAccountNumber INT NOT NULL)")
    c.execute("CREATE TABLE if not exists inventory(itemId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, itemName TEXT NOT NULL, itemQuantity INT NOT NULL, purchasedPrice REAL NOT NULL, purchasedDate TEXT NOT NULL, sellingPriceCherecharo REAL NOT NULL, sellingPriceBulk REAL NOT NULL, updatedAt TEXT NOT NULL)")
    c.execute("CREATE TABLE if not exists sales(salesId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, itemId INT NOT NULL, customerId INT NOT NULL, itemQuantitiy INT NOT NULL, soldDate TETX NOT NULL, wayOfPayment TEXT NOT NULL, salesRevenue INT NOT NULL)")

# here performing basic CRUD
# create
def insertCustomer(cName, cTinNumber, cRegion, cSubcity, cWereda, cPhoneNumber, createdDate, frequencyPurcases, totPurchases, bankAcc):
    """
    insert function for customers table
    """
    c.execute("insert into customers (customerName, customerTinNumber, customerRegion, customerSubcity, customerWereda, customerPhoneN, accountCreatedDate, frequencyOfPurchase, totalPurchase, bankAccountNumber) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (cName, int(cTinNumber), cRegion, cSubcity, int(cWereda), int(cPhoneNumber), createdDate, int(frequencyPurcases), int(totPurchases), int(bankAcc)))
    conn.commit()
    print('data inserted successfully')

def insertItem(iName, iQuantity,  purchasedPrice, purchasedDate, priceCherecharo, priceBulk):
    """
    insert function for Item table
    """
    # initaly updateAt == purchaseDate 
    # so no need to accept updateAt argument
    c.execute("INSERT INTO inventory (itemName, itemQuantity, purchasedPrice, purchasedDate, sellingPriceCherecharo, sellingPriceBulk, updatedAt) VALUES(?, ?, ?, ?, ?, ?, ?)", (iName, iQuantity,  purchasedPrice, purchasedDate, priceCherecharo, priceBulk, purchasedDate))
    print('data inserted successfully')
    conn.commit()

def insertSales(itemId, customerId, itemQuantity, soldDate, paymentWay, salesRevenue):
    """
    insert function for sales table
    """
    c.execute("INSERT INTO sales(itemId, customerId, itemQuantity, soldDate, wayOfPayment, salesRevenue) VALUES(?, ?, ?, ?, ?)", (itemId, customerId, itemQuantity, soldDate, paymentWay, salesRevenue))
    conn.commit()

# read
def readCustomer():
    """
    read Customer table
    """
    c.execute("SELECT * FROM customers")
    customers = c.fetchall()
    return customers

def deatilCustomer(CID):
    """
    retrive all the information from database
    """
    c.execute("SELECT * FROM customers where customerId=?", (CID, ))
    customer = c.fetchone()
    return customer

def readSCustomer():
    """
    selecting only specific columns
    """
    c.execute("SELECT customerId, customerName, customerPhoneN, customerTinNumber, bankAccountNumber FROM customers")
    customers = c.fetchall()
    return customers

def readItem():
    """
    read Item table
    """
    c.execute("SELECT * FROM inventory")
    Items = c.fetchall()
    return Items

def detailItem(CID):
    """
    retrive all the information from database
    """
    c.execute("SELECT * FROM inventory where itemId=?", (CID, ))
    customer = c.fetchone()
    return customer


def readSItem():
    """
    selecting only specific columns
    """
    c.execute("SELECT itemId, itemName, itemQuantity, purchasedPrice, sellingPriceCherecharo, sellingPriceBulk FROM inventory")
    items = c.fetchall()
    cToList = []
    for x in items:
        cToList.append(list(x))
    #for x in cToList:
        #if x[2] < 
    return cToList


def readSales():
    """
    read Sales table
    """
    c.execute("SELECT * FROM sales")
    sales = c.fetchall()
    return sales

# update
def updateCustomer(cId, cName, cTinNumber, cRegion, cSubcity, cWereda, cPhoneNumber, createdDate, frequencyPurcases, totPurchases, bankAcc):
    """
    updates customer database
    """

def updateItem(iId, iName, iQuantity,  purchasedPrice, purchasedDate, priceCherecharo, priceBulk, updatedAt):
    """
    update item database
    """

def updateSales(sId, itemId, customerId, itemQuantity, soldDate, paymentWay, salesRevenue):
    """
    update sales database
    """

# delete
def deleteCustomer(cId):
    """
    deleteCustomer row with id cId
    """
    c.execute("DELETE from customers where customerId = ?", (cId))
    print("Deleted")
    conn.commit()


def deleteItem(iId):
    """
    deleteItem row with id iId
    """
    c.execute("DELETE from inventory where itemId = ?", (iId))
    print("Deleted")
    conn.commit()

def deleteSales(sId):
    """
    deleteSales row with id sId
    """
    c.execute("DELETE from sales where salesId = ?", (sId))
    print("Deleted")
    conn.commit()

def closeCursor():
    c.close()