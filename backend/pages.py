class Pages:
    pages = { 
            "/login": {
                "html": "frontend/html/login.html",
                "css": "frontend/css/login.css",
                "javascript": "frontend/javascript/login.js"},
            "/portfolio": {
                "html": "frontend/html/portfolio.html",
                "css": ["frontend/css/portfolio.css", "frontend/css/base.css"],
                "javascript": ["frontend/javascript/portfolio.js", "frontend/javascript/authentication.js", "frontend/javascript/userInitials.js",  "frontend/javascript/menu.js",  "frontend/javascript/logout.js",  "frontend/javascript/delete-account.js"]},
            "/transactions": {
                "html": "frontend/html/transactions.html",
                "css": ["frontend/css/transactions.css", "frontend/css/base.css"],
                "javascript": ["frontend/javascript/transactions.js", "frontend/javascript/authentication.js", "frontend/javascript/userInitials.js",  "frontend/javascript/menu.js",  "frontend/javascript/logout.js",  "frontend/javascript/transaction-pagination.js",  "frontend/javascript/delete-account.js"]},
            "/new-transaction": {
                "html": "frontend/html/new-transaction.html",
                "css": "frontend/css/new-transaction.css",
                "javascript": "frontend/javascript/new-transaction.js"},
            "/create-account": {
                "html": "frontend/html/create-account.html",
                "css": "frontend/css/create-account.css",
                "javascript": "frontend/javascript/create-account.js"},
            "/forgot-password": {
                "html": "frontend/html/forgot-password.html",
                "css": "frontend/css/forgot-password.css",
                "javascript": "frontend/javascript/forgot-password.js"},
            "/new-password": {
                "html": "frontend/html/new-password.html",
                "css": "frontend/css/new-password.css",
                "javascript": "frontend/javascript/new-password.js"},
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