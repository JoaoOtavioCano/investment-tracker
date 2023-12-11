from http.server import HTTPServer, BaseHTTPRequestHandler
from pages import Pages
from defaultPageRequestHandler import DefaultPageRequestHandler
from getAssets import GetAssets
from getTransactions import GetTransactions
from getIndicators import GetIndicators
from login import Login


class RequestsHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server, authenticator):
        self.authenticator = authenticator
        super().__init__(request, client_address, server)

    def do_GET(self):

        pages = Pages()
        
        for path in pages.listPaths():
            if self.path in path:
                page_request_handler = DefaultPageRequestHandler(self)
                page_request_handler.respond()
                return True
        
        if self.path == "/favicon.ico":
            return True
        
        if validateAuthentication(self):
            if self.path == "/assets":
                request_handler = GetAssets(self)
                request_handler.respond()
            
            elif self.path == "/indicators":
                request_handler = GetIndicators(self)
                request_handler.respond()
            
            elif self.path == "/gettransactions":
                request_handler = GetTransactions(self)
                request_handler.respond()
        else:
            self.send_error(500, "User not authenticated")
            self.end_headers()

    def do_POST(self):

        if self.path == "/login":
            payload_data = formatPayload(self)
            request_handler  = Login(self, payload_data)
            request_handler.respond()
        

        

def run(server_class=HTTPServer, handler_class=RequestsHandler):
    server_address = ('', 8000)
    authenticator = Authenticator()
    httpd = server_class(server_address, lambda request, client_address, server: handler_class(request, client_address, server, authenticator))
    httpd.serve_forever()

def formatPayload(request):
    content_length = int(request.headers['Content-Length'])
    payload_data = str(request.rfile.read(content_length)).replace("b'", "", 1).replace("'", '').replace('{', '').replace('}', '').replace(',',':').replace('"', '').split(':')

    
    dict = {
        "email": payload_data[1],
        "password": payload_data[3]
    }
   
    return dict   

def validateAuthentication(server):
    authentication_key = server.headers["authentication_key"]
    
    print(server.authenticator.authorization_list)
    print(authentication_key )

    user_id = authentication_key.split('#', 1)[0]

    try:
        if server.authenticator.authorization_list[user_id] == authentication_key:
            return True
        else:
            return False
    except KeyError:
        return False 


class Authenticator:
    def __init__(self):
        self.authorization_list = {}


def main():
    run()

main()