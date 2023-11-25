from pages import Pages
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

    def handle(self):

        pages = Pages.pages

        for page in pages:
            if re.compile(r"^/" + page).match(self.request_handler.path):
                with open(Pages.pages[page]["html"], 'rb') as html_file:
                    html_content = html_file.read()

                self.request_handler.send_response(200, "OK")
                self.request_handler.send_header('Content-type', 'text/html')
                self.request_handler.send_header('Access-Control-Allow-Origin', '*')
                self.request_handler.send_header('Access-Control-Allow-Methods', 'GET')
                self.request_handler.end_headers()
                self.request_handler.wfile.write(html_content)
                break
            elif checkMultipleFiles(self.request_handler.path ,Pages.pages[page]["css"]) >= -1:
                index = checkMultipleFiles(self.request_handler.path ,Pages.pages[page]["css"])

                if index == -1:
                    with open(Pages.pages[page]["css"], 'rb') as css_file:
                        css_content = css_file.read()
                else:
                    with open(Pages.pages[page]["css"][index], 'rb') as css_file:
                        css_content = css_file.read()
                
                self.request_handler.send_response(200, "OK")
                self.request_handler.send_header('Content-type', 'text/css')
                self.request_handler.send_header('Access-Control-Allow-Origin', '*')
                self.request_handler.send_header('Access-Control-Allow-Methods', 'GET')
                self.request_handler.end_headers()
                self.request_handler.wfile.write(css_content)
                break
            elif self.request_handler.path in Pages.pages[page]["javascript"]:
                with open(Pages.pages[page]["javascript"], 'rb') as javascript_file:
                    javascript_content = javascript_file.read()

                self.request_handler.send_response(200, "OK")
                self.request_handler.send_header('Content-type', 'text/javascript')
                self.request_handler.send_header('Access-Control-Allow-Origin', '*')
                self.request_handler.send_header('Access-Control-Allow-Methods', 'GET')
                self.request_handler.end_headers()
                    
                self.request_handler.wfile.write(javascript_content) 
                break
