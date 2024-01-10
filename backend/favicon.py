class Favicon:
    def __init__(self, request):
        self.request = request

    def respond(self):
        with open('../frontend/images/favicon.png', 'rb') as image:
                    favicon = image.read()

        self.request.send_response(200, "OK")
        self.request.end_headers()
        self.request.wfile.write(favicon)

