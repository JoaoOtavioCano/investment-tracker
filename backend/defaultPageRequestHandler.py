from .pages import Pages

import re

def checkMultipleFiles(path, list_of_files_path):
    counter = 0

    if type(list_of_files_path) == str and path in list_of_files_path:
        return -1

    for file_path in list_of_files_path: 
        if path in file_path:
            return counter
        counter = counter + 1
    return -2

class DefaultPageRequestHandler:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def respond(self):

        pages = Pages.pages


        for page in pages:

            index_css = checkMultipleFiles(self.request_handler.path ,Pages.pages[page]["css"])
            index_js = checkMultipleFiles(self.request_handler.path ,Pages.pages[page]["javascript"])

            if re.compile(page).match(self.request_handler.path):
                with open(Pages.pages[page]["html"], 'rb') as html_file:
                    html_content = html_file.read()

                self.request_handler.send_response(200, "OK")
                self.request_handler.send_header('Content-type', 'text/html')
                self.request_handler.send_header('Access-Control-Allow-Origin', '*')
                self.request_handler.send_header('Access-Control-Allow-Methods', 'GET')
                self.request_handler.end_headers()
                self.request_handler.wfile.write(html_content)
                break
            elif index_css >= -1:

                if index_css == -1:
                    with open(Pages.pages[page]["css"], 'rb') as css_file:
                        css_content = css_file.read()
                else:
                    with open(Pages.pages[page]["css"][index_css], 'rb') as css_file:
                        css_content = css_file.read()
                
                self.request_handler.send_response(200, "OK")
                self.request_handler.send_header('Content-type', 'text/css')
                self.request_handler.send_header('Access-Control-Allow-Origin', '*')
                self.request_handler.send_header('Access-Control-Allow-Methods', 'GET')
                self.request_handler.end_headers()
                self.request_handler.wfile.write(css_content)
                break
            elif index_js >= -1:
                
                if index_js == -1:
                    with open(Pages.pages[page]["javascript"], 'rb') as js_file:
                        javascript_content = js_file.read()
                else:
                    with open(Pages.pages[page]["javascript"][index_js], 'rb') as js_file:
                        javascript_content = js_file.read()

                self.request_handler.send_response(200, "OK")
                self.request_handler.send_header('Content-type', 'text/javascript')
                self.request_handler.send_header('Access-Control-Allow-Origin', '*')
                self.request_handler.send_header('Access-Control-Allow-Methods', 'GET')
                self.request_handler.end_headers()
                    
                self.request_handler.wfile.write(javascript_content) 
                break
