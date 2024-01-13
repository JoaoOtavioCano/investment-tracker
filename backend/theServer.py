from http.server import HTTPServer, BaseHTTPRequestHandler
from pages import Pages
from defaultPageRequestHandler import DefaultPageRequestHandler
from getAssets import GetAssets
from getTransactions import GetTransactions
from getIndicators import GetIndicators
from login import Login
from authenticator import Authenticator
from newTransaction import newTransaction
from favicon import Favicon
from logout import Logout


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
        
        if self.path == "/images/favicon.png":
            request_handler = Favicon(self)
            request_handler.respond()
            return True
        
        if self.authenticator.validateAuthentication(self):
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
            return True

        if self.authenticator.validateAuthentication(self):
            if self.path == "/newtransaction":
                payload_data = formatPayload(self)
                request_handler = newTransaction(self, payload_data)
                request_handler.respond()

            elif self.path == "/logout":
                request_handler = Logout(self)
                request_handler.respond()
                
        else:
            self.send_error(500, "User not authenticated")
            self.end_headers()

        

        

def run(server_class=HTTPServer, handler_class=RequestsHandler):
    server_address = ('', 8000)
    authenticator = Authenticator()
    httpd = server_class(server_address, lambda request, client_address, server: handler_class(request, client_address, server, authenticator))
    httpd.serve_forever()

def formatPayload(request):
    content_length = int(request.headers['Content-Length'])
    payload_data = str(request.rfile.read(content_length)).replace("b'", "", 1).replace("'", '').replace('{', '').replace('}', '').replace(',',':').replace('"', '').split(':')

    payload_data = list(payload_data)

    dict = {}

    for i in range(int(int(len(payload_data))/2)):
        dict[payload_data[i * 1 + i]] = payload_data[i * 1 + i + 1]
           
    return dict   


def main():
    run()

main()