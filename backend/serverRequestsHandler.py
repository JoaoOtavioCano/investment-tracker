from http.server import HTTPServer, BaseHTTPRequestHandler
from pages import Pages
from defaultPageRequestHandler import DefaultPageRequestHandler
from getAssets import GetAssets
from getTransactions import GetTransactions
from getIndicators import GetIndicators
from login import Login


class RequestsHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.authorization_list = {}
        super().__init__(*args, **kwargs)


    def do_GET(self):

        pages = Pages()
        
        for path in pages.listPaths():
            if self.path in path:
                page_request_handler = DefaultPageRequestHandler(self)
                page_request_handler.respond()
                break
        
        
        if self.path == "/assets":
            request_handler = GetAssets(self)
            request_handler.respond()
        
        elif self.path == "/indicators":
            request_handler = GetIndicators(self)
            request_handler.respond()
        
        elif self.path == "/gettransactions":
            request_handler = GetTransactions(self)
            request_handler.respond()

    def do_POST(self):

        if self.path == "/login":
            payload_data = formatPayload(self)
            request_handler  = Login(self, payload_data)
            request_handler.respond()
        

        

def run(server_class=HTTPServer, handler_class=RequestsHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def formatPayload(request):
    content_length = int(request.headers['Content-Length'])
    payload_data = str(request.rfile.read(content_length)).replace("b'", "", 1).replace("'", '').replace('{', '').replace('}', '').replace(',',':').replace('"', '').split(':')

    
    dict = {
        "email": payload_data[1],
        "password": payload_data[3]
    }
   
    return dict


def main():
    run()

main()