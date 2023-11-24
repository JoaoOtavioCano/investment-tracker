from http.server import HTTPServer, BaseHTTPRequestHandler
from pages import Pages
from defaultPageRequestHandle import DefaultPageRequestHandle
import re

class RequestsHandler(BaseHTTPRequestHandler):

    pages = Pages.pages

    def do_GET(self):
        
        for page in self.pages:

            if re.compile(r"^/" + page).match(self.path) or re.compile(r"^/css").match(self.path) or re.compile(r"^/javascript").match(self.path):
                page_request_handler = DefaultPageRequestHandle(self)
                page_request_handler.handle()
                break
           
    def do_POST(self):
        pass

def run(server_class=HTTPServer, handler_class=RequestsHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():
    run()

main()