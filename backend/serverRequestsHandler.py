from http.server import HTTPServer, BaseHTTPRequestHandler
from pages import Pages
from defaultPageRequestHandler import DefaultPageRequestHandler
from getAssets import GetAssets

class RequestsHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        pages = Pages()
        
        for path in pages.listPaths():
            if self.path in path:
                page_request_handler = DefaultPageRequestHandler(self)
                page_request_handler.handle()
                break
        
        if self.path == "/assets":
            GetAssets(self)
        
        elif self.path == "/indicators":
            pass

    def do_POST(self):
        pass

def run(server_class=HTTPServer, handler_class=RequestsHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():
    run()

main()