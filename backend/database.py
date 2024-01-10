import mysql.connector
import possibleErrors

class Database:

    def __init__(self):
        self.__db__ = mysql.connector.connect(
            host="localhost",
            user="root",
            password="91246810",
            database="testdatabase"
        )

        self.__mycursor__ = self.__db__.cursor()
    
    def getAssets(self, user):

        sql_querry = sql_querry = ("SELECT type, Stocks.name, quantity, cost FROM Users JOIN "
            "Assets ON Users.userID = Assets.userID "
            "JOIN Stocks ON Assets.userID = Stocks.userID AND Assets.name = Stocks.name "
            f"WHERE Users.userID = {user}")
        
        self.__mycursor__.execute(sql_querry)

        assets_list = []

        for turple in self.__mycursor__:
            assets_list.append(turple)

        return assets_list

    def getTransactions(self, user):
        sql_querry = ("SELECT date_time, asset, quantity, cost, operation FROM Transactions "
            "JOIN Users ON Transactions.userID = Users.userID "
            f"WHERE Users.userID = {user} "
            "ORDER BY date_time DESC")
        
        self.__mycursor__.execute(sql_querry)

        transactions_list = []

        for turple in self.__mycursor__:
            transactions_list.append(turple)

        return transactions_list

    def getIndicators(self, user):
        return self.getAssets(user)
    
    def getUser(self, email, password):
        sql_querry = ("SELECT Users.userID, Users.name FROM Users  "
            f"WHERE Users.email = '{email}' "
            f"AND Users.password = '{password}'")
        
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
