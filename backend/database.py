import mysql.connector
import possibleErrors
import os
from dotenv import load_dotenv

load_dotenv()

class Database:

    def __init__(self):
        self.__db__ = mysql.connector.connect(
            host="localhost",
            user=os.getenv('DB_USER'),
            password=os.getenv("DB_PASSWORD"),
            database="testdatabase"
        )

        self.__mycursor__ = self.__db__.cursor()
    
    def getAssets(self, user):

        sql_querry = sql_querry = ("SELECT type, Stocks.name, quantity, cost FROM Assets "
                                   "JOIN Stocks ON Assets.userID = Stocks.userID AND Assets.name = Stocks.name "
                                   f"WHERE Assets.userID = {user}")
        
        self.__mycursor__.execute(sql_querry)

        assets_list = []

        for turple in self.__mycursor__:
            assets_list.append(turple)

        return assets_list

    def getTransactions(self, user, frame):
        sql_querry = ("SELECT date_time, asset, quantity, cost, operation FROM Transactions "
                      f"WHERE Transactions.userID = {user} "
                      "ORDER BY date_time DESC "
                      f"LIMIT 20 OFFSET {int(frame) * 20}")
        
        self.__mycursor__.execute(sql_querry)

        transactions_list = []

        for turple in self.__mycursor__:
            transactions_list.append(turple)

        return transactions_list

    def getIndicators(self, user):
        return self.getAssets(user)
    
    def getUser(self, email):
        sql_querry = ("SELECT Users.userID, Users.name, Users.password FROM Users  "
            f"WHERE Users.email = '{email}'")
        
        self.__mycursor__.execute(sql_querry)

        user = []

        for turple in self.__mycursor__:
            user.append(turple)

        return user
    
    def addNewTransaction(self, user, asset, quantity, price, date, operation, type):
        sql_querry_insert_into_transactions_table = ("INSERT INTO Transactions(userID, date_time, asset, quantity, cost, operation) "
                      f"VALUES ({user}, '{date}', '{asset}', {quantity}, {price}, '{operation}');")
        
        self.__mycursor__.execute(sql_querry_insert_into_transactions_table)

        if operation == "buy":
            if not self.__userHasThisStock__(user, asset):
                sql_querry_insert_into_assets_table = ("INSERT INTO Assets(userID, name, type) "
                        f"VALUES ({user}, '{asset}', '{type}')")
            
                sql_querry_insert_into_stocks_table = ("INSERT INTO Stocks(userID, name, quantity, cost) "
                        f"VALUES ({user}, '{asset}', {quantity}, {price})")
            
                self.__mycursor__.execute(sql_querry_insert_into_assets_table)
                self.__mycursor__.execute(sql_querry_insert_into_stocks_table)

            else:
                stock_quantity, stock_avg_price = self.__getConsolidatedStockData__(user, asset)

                new_quantity = stock_quantity + float(quantity)

                new_avg_price = ((stock_quantity * stock_avg_price) + (float(quantity) * float(price))) / new_quantity

                sql_querry_update_stocks_table = ("UPDATE Stocks SET "
                                                f"`quantity` = {new_quantity}, "
                                                f"`cost` = {new_avg_price} "
                                                f"WHERE (`userID` = {user}) and (`name` = '{asset}');")
                
                self.__mycursor__.execute(sql_querry_update_stocks_table)

        elif operation == "sell":
            if self.__userHasThisStock__(user, asset):
                stock_quantity, stock_avg_price = self.__getConsolidatedStockData__(user, asset)

                new_quantity = stock_quantity - float(quantity)

                if new_quantity < 0:
                    raise possibleErrors.NegativeQuantity
                
                elif new_quantity == 0:
                    sql_querry_delete_asset = ("DELETE FROM Assets "
                                            f"WHERE userID = {user} AND "
                                            f"name = '{asset}'")
                    
                    self.__mycursor__.execute(sql_querry_delete_asset)

                else:
                    sql_querry_update_stocks_table = ("UPDATE Stocks SET "
                                                f"`quantity` = {new_quantity} "
                                                f"WHERE (`userID` = {user}) AND "
                                                f"(`name` = '{asset}');")      
                    
                    self.__mycursor__.execute(sql_querry_update_stocks_table)          

            else:
                raise possibleErrors.AssetNotInPortfolio
        

        self.__db__.commit()

    def __userHasThisStock__(self, user, stock):
        sql = f"SELECT * FROM Assets WHERE userID = {user} AND name = '{stock}'"

        self.__mycursor__.execute(sql)

        respostas = self.__mycursor__

        for resposta in respostas:
            return True
        
        return False
    
    def __getConsolidatedStockData__(self, user, stock):
        sql = f"SELECT quantity, cost FROM Stocks WHERE userID = {user} AND name = '{stock}'"

        self.__mycursor__.execute(sql)

        respostas = self.__mycursor__

        for resposta in respostas:
            return resposta[0], resposta[1]

    def createUser(self, name, email, password_hash):
        sql = ("INSERT INTO Users(email, password, name) "
            f"VALUES('{email}', '{password_hash}', '{name}')")
        
        self.__mycursor__.execute(sql)

        self.__db__.commit()

    def addNewPasswordRequest(self, code, user):
        sql = ("INSERT INTO NewPasswordsRequests(code, userID) "
            f"VALUES('{code}', {user})")
        
        self.__mycursor__.execute(sql)

        self.__db__.commit()

    def getUserId(self, email):
        sql = ("SELECT userID FROM Users "
            f"WHERE email = '{email}'")
        
        self.__mycursor__.execute(sql)

        user_id = self.__mycursor__

        for result in user_id:
            return result[0]


    def deletePasswordRequest(self, user):
        sql = ("DELETE FROM NewPasswordsRequests "
            f"WHERE userID = {user}")
        
        self.__mycursor__.execute(sql)

        self.__db__.commit()

    def getUserIdUsingCode(self, code):
        sql = ("SELECT userID FROM NewPasswordsRequests "
            f"WHERE code = '{code}'")
        
        self.__mycursor__.execute(sql)

        user_id = self.__mycursor__

        for result in user_id:
            return result[0]
        
    def updateUserPassword(self, user, new_password):
        sql = ("UPDATE Users "
               f"SET password = '{new_password}' "
               f"WHERE userID = {user}")
        
        self.__mycursor__.execute(sql)

        self.__db__.commit()