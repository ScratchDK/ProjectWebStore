import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """

        if self.path == "/":
            file_path = os.path.join(base_dir, "templates", "home.html")
        elif self.path == "/contacts":
            file_path = os.path.join(base_dir, "templates", "contacts.html")
        elif self.path == "/categories":
            file_path = os.path.join(base_dir, "templates", "categories.html")
        elif self.path == "/catalogs":
            file_path = os.path.join(base_dir, "templates", "catalogs.html")
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes("<html><body><h1>404 - Не найдено</h1></body></html>", "utf-8"))
            return

        with open(file_path, 'rb') as file:
            content = file.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        print("Полученные данные от клиента:")
        for key, value in parsed_data.items():
            print(f"{key}: {value}")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Данные получены успешно!</h1></body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Сервер запущен по адресу http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
