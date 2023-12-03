import mysql.connector

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

        sql_querry = sql_querry = ("SELECT type, Stocks.name, quantity, cost FROM User JOIN "
            "Assets ON User.userID = Assets.userID "
            "JOIN Stocks ON Assets.userID = Stocks.userID AND Assets.name = Stocks.name "
            f"WHERE User.userID = {user}")
        
        self.__mycursor__.execute(sql_querry)

        assets_list = []

        for turple in self.__mycursor__:
            assets_list.append(turple)

        return assets_list

    def getTransactions(self, user):
        sql_querry = ("SELECT date_time, asset, quantity, cost FROM Transactions "
            "JOIN User ON Transactions.userID = User.userID "
            f"WHERE User.userID = {user} "
            "ORDER BY date_time ASC")
        
        self.__mycursor__.execute(sql_querry)

        transactions_list = []

        for turple in self.__mycursor__:
            transactions_list.append(turple)

        return transactions_list
