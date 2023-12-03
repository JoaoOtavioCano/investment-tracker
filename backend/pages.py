class Pages:
    pages = { 
            "/login": {
                "html": "../frontend/html/login.html",
                "css": "../frontend/css/login.css",
                "javascript": "../frontend/javascript/login.js"},
            "/portfolio": {
                "html": "../frontend/html/portfolio.html",
                "css": ["../frontend/css/portfolio.css", "../frontend/css/base.css"],
                "javascript": "../frontend/javascript/portfolio.js"},
            "/transactions": {
                "html": "../frontend/html/transactions.html",
                "css": ["../frontend/css/transactions.css", "../frontend/css/base.css"],
                "javascript": "../frontend/javascript/transactions.js"},
            "/new-transaction": {
                "html": "../frontend/html/new-transaction.html",
                "css": ["../frontend/css/new-transaction.css", "../frontend/css/base.css"],
                "javascript": "../frontend/javascript/new-transaction.js"},
    }

    def listPaths(self):
        list_of_paths = []

        for page in self.pages:
            list_of_paths.extend([page])
            list_of_paths.extend([self.pages[page]["html"]])
            if type(self.pages[page]["css"]) == str:
                list_of_paths.extend([self.pages[page]["css"]])
            else:
                list_of_paths.extend(self.pages[page]["css"])
            if type(self.pages[page]["javascript"]) == str:
                list_of_paths.extend([self.pages[page]["javascript"]])
            else:
                list_of_paths.extend(self.pages[page]["javascript"])
        
        return list_of_paths