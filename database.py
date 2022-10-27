#!/usr/bin/python3
"""
To manage sqlite database
"""
import sqlite3
conn = sqlite3.connect('store.db')
c = conn.cursor()
def createTables():
    # DON'T USE THIS QUERY SINCE THERE IS A LOT OF CHANGES
    #c.execute("CREATE TABLE if not exists customers(customerId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, customerName TEXT NOT NULL, companyName TEXT, customerTinNumber INT NOT NULL, customerCity TEXT NOT NULL, customerPhoneN INT NOT NULL, accountCreatedDate TEXT NOT NULL, frequencyOfPurchase INT NOT NULL, totalPurchase INT NOT NULL, bankAccountNumber INT NOT NULL)")
    #c.execute("CREATE TABLE if not exists inventory(itemId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, itemName TEXT NOT NULL, itemQuantity INT NOT NULL, purchasedDate TEXT NOT NULL, sellingPriceCherecharo REAL NOT NULL, sellingPriceBulk REAL NOT NULL, updatedAt TEXT NOT NULL)")
    #c.execute("CREATE TABLE if not exists bankAcc(id INTEGER PRIMARY KEY AUTOINCREMENT, bankName TEXT NOT NULL, amount int not null, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)")
    #c.execute("CREATE TABLE if not exists expenses(id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT NOT NULL, name TEXT NOT NULL, amount int not null, date TEXT NOT NULL)")
    #c.execute("CREATE TABLE sales(salesId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, itemId INT NOT NULL, customerId INT NOT NULL, itemQuantitiy INT NOT NULL, soldDate TEXT NOT NULL, salesRevenue INT NOT NULL, bankId INT NOT NULL, add_info TEXT)")
    pass

# here performing basic CRUD
# create

def insertBankAcc(bName, bAmount, bCreated_at, bUpdated_at):
    """
    insert for bankAccount tables
    """
    c.execute("insert into bankAcc(bankName, amount, created_at, updated_at) values(?, ?, ?, ?)", (bName, bAmount, bCreated_at, bUpdated_at))
    conn.commit()

def insertXpense(eType, eName, eAmount, eDate):
    """
    insert function for expense table
    """
    c.execute("insert into expenses(type, name, amount, date) values(?, ?, ?, ?)", (eType, eName, eAmount, eDate))
    conn.commit()

def insertCustomer(cName, compName, cTinNumber, custCity, cPhoneNumber, createdDate, frequencyPurcases, totPurchases, bankAcc):
    """
    insert function for customers table
    """
    c.execute("insert into customers (customerName, companyName, customerTinNumber, customerCity, customerPhoneN, accountCreatedDate, frequencyOfPurchase, totalPurchase, bankAccountNumber) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (cName, compName, int(cTinNumber), custCity, int(cPhoneNumber), createdDate, int(frequencyPurcases), int(totPurchases), int(bankAcc)))
    conn.commit()
    print('data inserted successfully')

def insertItem(iName, iQuantity, purchasedDate, priceCherecharo, priceBulk):
    """
    insert function for Item table
    """
    # initaly updateAt == purchaseDate 
    # so no need to accept updateAt argument
    c.execute("INSERT INTO inventory (itemName, itemQuantity, purchasedDate, sellingPriceCherecharo, sellingPriceBulk, updatedAt) VALUES(?, ?, ?, ?, ?, ?)", (iName, iQuantity, purchasedDate, priceCherecharo, priceBulk, purchasedDate))
    print('data inserted successfully')
    conn.commit()

def insertSales(itemId, customerId, itemQuantity, soldDate, salesRevenue, bankId, salesInfo):
    """
    insert function for sales table
    """
    c.execute("INSERT INTO sales(itemId, customerId, itemQuantitiy, soldDate, salesRevenue, bankId, add_info) VALUES(?, ?, ?, ?, ?, ?, ?)", (itemId, customerId, itemQuantity, soldDate, salesRevenue, bankId, salesInfo))
    conn.commit()

def CreateUser(usreName, lastLogin):
    """
    Create New user
    """
    c.execute("INSERT INTO personal(Name, last_login) VALUES(?, ?)", (usreName, lastLogin))
    conn.commit()


# read
def readBankAcc():
    """
    to read bankAcc
    """
    c.execute("SELECT * FROM bankAcc")
    banks = c.fetchall()
    return banks

def detailBankAcc(bankName):
    """
    detail bankAcc using bank name
    """
    c.execute("SELECT * FROM bankAcc WHERE bankName=?", (bankName,))
    bank = c.fetchone()
    return bank

def detailBankAccId(bankId):
    """
    detail bank using bank id
    """
    c.execute("SELECT * FROM bankAcc WHERE id=?", (bankId,))
    bank = c.fetchone()
    return bank


def readSomeExpenses():
    """
    To only read name, amount and date of expenses
    """
    c.execute("SELECT type, name, amount, date FROM expenses")
    expense = c.fetchall()
    return expense

def detailExpenses(id):
    """
    To see detail expenses info
    """
    c.execute("SELECT * FROM expenses WHERE id=?", (id, ))
    expense = c.fetchone()
    return expense

def readSomeFixExpenses():
    """
    To only read name, amount and date of Fixed expenses
    """
    c.execute("SELECT id, name, amount, date FROM expenses where type = 'Fixed'")
    expense = c.fetchall()
    return expense

def readSomeVarExpenses():
    """
    To only read name, amount and date of Variable expenses
    """
    c.execute("SELECT id, name, amount, date FROM expenses where type = 'Variable'")
    expense = c.fetchall()
    return expense

def readExpenses():
    """
    To read all expenses data
    """
    c.execute("SELECT * FROM expenses")
    expense = c.fetchall()
    return expense

def readCustomer():
    """
    read Customer table
    """
    c.execute("SELECT * FROM customers")
    customers = c.fetchall()
    return customers

def readSomeCustomer():
    """
    read only some values of Customers dataTable
    """
    c.execute("SELECT customerId, customerName, companyName, totalPurchase FROM customers")
    customers = c.fetchall()
    return customers

def detailCustomer(CID):
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
    c.execute("SELECT customerId, customerName, companyName, customerCity, customerPhoneN, customerTinNumber, totalPurchase FROM customers")
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
    c.execute("SELECT * FROM inventory where itemId= ?", (int(CID),))
    customer = c.fetchone()
    return customer


def readSItem():
    """
    selecting only specific columns
    """
    c.execute("SELECT itemId, itemName, itemQuantity, sellingPriceCherecharo FROM inventory")
    items = c.fetchall()
    cToList = []
    for x in items:
        cToList.append(list(x))
    #for x in cToList:
        #if x[2] < 
    return cToList

def readSomeSales():
    """
    some amount of sales
    """
    c.execute("SELECT itemId, itemQuantitiy, salesRevenue, soldDate, salesId FROM sales")
    sales = c.fetchall()
    cToList = []
    for x in sales:
        cToList.append(list(x))
    return cToList

def readCashSales():
    """
    sales info for cash
    """
    c.execute("SELECT soldDate, salesRevenue, bankId, salesId, itemId FROM sales")
    cash = c.fetchall()
    cToList = []
    for x in cash:
        cToList.append(list(x))
    return cToList

def readSales():
    """
    read Sales table
    """
    c.execute("SELECT * FROM sales")
    sales = c.fetchall()
    return sales

def detailSales(SID):
    """
    retrive all the information from database
    """
    c.execute("SELECT * FROM sales where salesId= ?", (SID,))
    sales = c.fetchone()
    return sales


def readCustomerSales(Id):
    """
    sales made by specific customer
    """
    c.execute("SELECT * FROM sales where customerId = ?", (Id, ))
    customerSales = c.fetchall()
    return customerSales

def readPersonal():
    """
    to read all from personal
    """
    c.execute("SELECT * FROM personal")
    personal = c.fetchall()
    return personal

def readSPersonal(Id):
    """
    To read one person data
    """
    c.execute("SELECT * from personal where id = ?", (Id, ))
    person = c.fetchone()
    return person

# update
def updateCustomer(cId, cName, compName, cTinNumber, custCity, cPhoneNumber, createdDate, frequencyPurcases, totPurchases, bankAcc):
    """
    updates customer database
    """
    c.execute("UPDATE customers SET customerName = ?, companyName = ?, customerTinNumber = ?, customerCity = ?, customerPhoneN = ?, accountCreatedDate = ?, frequencyOfPurchase = ?, totalPurchase = ?, bankAccountNumber = ? WHERE customerId = ?", (cName, compName, cTinNumber, custCity, cPhoneNumber, createdDate, int(frequencyPurcases), int(totPurchases), int(bankAcc), cId))
    conn.commit()

def updateBankIdINSalesC(salesId, bankId):
    """
    change bankId in sales table from cash 12 to bankCID
        here first argument is salesId
        second argument is bankId it changed to 
    """
    c.execute("UPDATE sales SET bankId = ? WHERE salesId = ?", (bankId, salesId))
    conn.commit()

def getBankAmount(bankId):
    """
    Just to get Amount for whatever bank
    """
    c.execute("SELECT amount FROM bankAcc WHERE id = ?", (bankId, ))
    amount = c.fetchone()
    return amount

def updateBankAmountC(sRevenu, bankId, cashId):
    """
    And here update bankAcc revenue
        # subtract from Cash (the revenue)And
        # Add the to given bank 
    """
    cashRevenu = getBankAmount(cashId)[0] - int(sRevenu)
    bankRevenu = getBankAmount(bankId)[0] + int(sRevenu)
    c.execute("UPDATE bankAcc SET amount = ? WHERE id = ?", (cashRevenu, cashId))
    c.execute("UPDATE bankAcc SET amount = ? WHERE id = ?", (bankRevenu, bankId))
    conn.commit()

def updateItem(iId, iName, iQuantity, purchasedDate, priceCherecharo, priceBulk, updateAt):
    """
    update item database
    """
    c.execute("UPDATE inventory SET itemName = ?, itemQuantity = ?, purchasedDate = ?, sellingPriceCherecharo = ?, sellingPriceBulk = ?, updatedAt = ? WHERE itemID = ?", (iName, iQuantity, purchasedDate, priceCherecharo, priceBulk, updateAt, iId))
    conn.commit()

def updateSales(sId, itemId, customerId, itemQuantity, soldDate, salesRevenue, bankId):
    """
    update sales database
    """
    c.execute("UPDATE sales SET itemId = ?, customerId = ?, itemQuantitiy = ?, soldDate = ?, salesRevenue = ?, bankId = ? WHERE salesId = ?", (itemId, customerId, itemQuantity, soldDate, salesRevenue, bankId, sId))
    conn.commit()

def updateExpenses(eId, eType, eName, eAmount, eDate):
    """
    update expenses database
    """
    c.execute("UPDATE expenses SET type = ?, name = ?, amount = ?, date = ? WHERE id = ?", (eType, eName, eAmount, eDate, eId))
    conn.commit()

def updateBankAcc(bId, bName, bAmount, bCreated_at, bUpdated_at):
    """
    update bankAcc
    """
    c.execute("UPDATE bankAcc SET bankName = ?, amount = ?, created_at = ?, updated_at = ? WHERE id = ?", (bName, bAmount, bCreated_at, bUpdated_at, bId))
    conn.commit()

def updatePersonalInfo(pId, Name):
    """
    update personal info
    """
    c.execute("UPDATE personal SET Name =? WHERE id = ?", (Name, pId))
    conn.commit()

# delete
def deleteCustomer(cId):
    """
    deleteCustomer row with id cId
    """
    c.execute("DELETE from customers where customerId = ?", (cId, ))
    print("Deleted")
    conn.commit()


def deleteItem(iId):
    """
    deleteItem row with id iId
    """
    c.execute("DELETE from inventory where itemId = ?", (iId, ))
    print("Deleted")
    conn.commit()

def deleteSales(sId):
    """
    deleteSales row with id sId
    """
    c.execute("DELETE from sales where salesId = ?", (sId, ))
    print("Deleted")
    conn.commit()

def deleteExpenses(eId):
    """
    delete Expenses with id eId
    """
    c.execute("DELETE from expenses where id = ?", (eId, ))
    conn.commit()

def deleteBankAcc(bId):
    """
    delete bankAcc with id bId
    """
    c.execute("DELETE from bankAcc where id = ?", (bId, ))
    conn.commit()

def deleteExpenses(eId):
    """
    delete Expenses with id eId
    """
    c.execute("DELETE from expenses where id = ?", (eId, ))
    conn.commit()

def backUpdatabase(location='/../../..'):
    """
    This function is to backUp data from database save it as db and excel file
        requires location as an argument to be saved on
    """
    sqliteCon = sqlite3.connect('store.db')
    # new one
    backupCon = sqlite3.connect("{}/backUp.db".format(location))
    with backupCon:
        sqliteCon.backup(backupCon)

    if backupCon:
        backupCon.close()
        sqliteCon.close()

    # try:
    #     # existing DB
    #     sqliteCon = sqlite3.connect('store.db')
    #     # new one
    #     backupCon = sqlite3.connect('{}/backUp.db'.format(location))
    #     with backupCon:
    #         sqliteCon.backup(backupCon)
    # except sqlite3.Error as error:
    #     print("Error while taking backup: ", error)
    # finally:
    #     if backupCon:
    #         backupCon.close()
    #         sqliteCon.close()


def deleteEveryThingFromDatabase():
    """
    This is function is basically wipes exvery thing on all tables
        after several confirmations
        That is why the name is long to avoid mistakes :)
    """
    c.execute("DELETE from customers")
    c.execute("DELETE from inventory")
    c.execute("DELETE from sales")
    c.execute("DELETE from expesnse")
    c.execute("DELETE from bankAcc")
    conn.commit()

def closeCursor():
    c.close()