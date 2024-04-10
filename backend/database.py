import psycopg2
import possibleErrors
import os
from dotenv import load_dotenv

load_dotenv()

class Database:

    def __init__(self):
        self.__db__ = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
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
        sql_querry = ("SELECT date_time, asset, quantity, cost, operation, id FROM Transactions "
                      f"WHERE Transactions.userID = {user} "
                      "ORDER BY date_time DESC, id DESC "
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

        stock_avg_price = -1

        if "stock" in type:
            country = type.replace("stock", "").replace("(", "").replace(")", "")

        if operation == "buy":
            if not self.__userHasThisStock__(user, asset):
                sql_querry_insert_into_assets_table = ("INSERT INTO Assets(userID, name, type) "
                        f"VALUES ({user}, '{asset}', '{type}')")
            
                sql_querry_insert_into_stocks_table = ("INSERT INTO Stocks(userID, name, quantity, cost, country) "
                        f"VALUES ({user}, '{asset}', {quantity}, {price}, {country})")
            
                self.__mycursor__.execute(sql_querry_insert_into_assets_table)
                self.__mycursor__.execute(sql_querry_insert_into_stocks_table)

            else:
                stock_quantity, stock_avg_price = self.__getConsolidatedStockData__(user, asset)

                new_quantity = stock_quantity + float(quantity)

                new_avg_price = ((stock_quantity * stock_avg_price) + (float(quantity) * float(price))) / new_quantity

                sql_querry_update_stocks_table = ("UPDATE Stocks SET "
                                                f"quantity = {new_quantity}, "
                                                f"cost = {new_avg_price} "
                                                f"WHERE (userID = {user}) and (name = '{asset}');")
                
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
                                                f"quantity = {new_quantity} "
                                                f"WHERE (userID = {user}) AND "
                                                f"(name = '{asset}');")      
                    
                    self.__mycursor__.execute(sql_querry_update_stocks_table)          

            else:
                raise possibleErrors.AssetNotInPortfolio
            
        sql_querry_insert_into_transactions_table = ("INSERT INTO Transactions(userID, date_time, asset, quantity, cost, operation, current_avg_cost, type) "
                                                        f"VALUES ({user}, '{date}', '{asset}', {quantity}, {price}, '{operation}', {stock_avg_price}, '{type}');")
        
        self.__mycursor__.execute(sql_querry_insert_into_transactions_table)
        

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
        
        try:
            self.__mycursor__.execute(sql)
        except psycopg2.errors.UniqueViolation:
            raise possibleErrors.UserAlreadyExists

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
    
    def deleteUser(self, user):
        sql = ("DELETE FROM Users "
            f"WHERE userID = {user}")
        
        self.__mycursor__.execute(sql)

        self.__db__.commit()

    def delete_transaction(self, transaction_id):
        sql_get_transaction_data = ("SELECT userid, asset, quantity, cost, operation, current_avg_cost, type FROM Transactions "
                                    f"WHERE id = {transaction_id}")
        
        self.__mycursor__.execute(sql_get_transaction_data)

        for result in self.__mycursor__:
            user_id = result[0]
            transaction_asset = result[1]
            transaction_quantity = result[2]
            transaction_cost = result[3]
            transaction_operation = result[4]
            transaction_prior_avg_cost = result[5]
            transaction_asste_type = result[6]

        if self.__userHasThisStock__(user_id, transaction_asset):

            current_asset_quantity, current_asset_cost = self.__getConsolidatedStockData__(user_id, transaction_asset)

            if transaction_operation == "buy":
                new_quantity =  current_asset_quantity - float(transaction_quantity)
                
                if new_quantity == 0 :
                    sql_querry_delete_asset = ("DELETE FROM Assets "
                                            f"WHERE userID = {user_id} AND "
                                            f"name = '{transaction_asset}'")
                            
                    self.__mycursor__.execute(sql_querry_delete_asset)
                else:
                    sql_querry_update_stocks_table = ("UPDATE Stocks SET "
                                                    f"quantity = {new_quantity}, "
                                                    f"cost = {transaction_prior_avg_cost} "
                                                    f"WHERE (userID = {user_id}) AND "
                                                    f"(name = '{transaction_asset}');")      
                            
                    self.__mycursor__.execute(sql_querry_update_stocks_table)
            else:
                new_quantity = current_asset_quantity + transaction_quantity

                sql_querry_update_stocks_table = ("UPDATE Stocks SET "
                                                    f"quantity = {new_quantity}, "
                                                    f"cost = {transaction_prior_avg_cost} "
                                                    f"WHERE (userID = {user_id}) AND "
                                                    f"(name = '{transaction_asset}');")      
                            
                self.__mycursor__.execute(sql_querry_update_stocks_table)
        else:
            new_quantity = transaction_quantity

            sql_querry_insert_into_assets_table = ("INSERT INTO Assets(userID, name, type) "
                                                  f"VALUES ({user_id}, '{transaction_asset}', '{transaction_asste_type}')")
            
            sql_querry_insert_into_stocks_table = ("INSERT INTO Stocks(userID, name, quantity, cost) "
                                                  f"VALUES ({user_id}, '{transaction_asset}', {new_quantity}, {transaction_prior_avg_cost})")
            
            self.__mycursor__.execute(sql_querry_insert_into_assets_table)
            self.__mycursor__.execute(sql_querry_insert_into_stocks_table)


        sql_delete_transaction = ("DELETE FROM Transactions "
                                 f"WHERE id = {transaction_id}")
        
        self.__mycursor__.execute(sql_delete_transaction)

        self.__db__.commit()