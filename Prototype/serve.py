import BaseHTTPServer
import os
import SimpleHTTPServer


class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    do_POST = SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET

    def guess_type(self, path):
        if "@@" in path:
            return "text/html"
        return SimpleHTTPServer.SimpleHTTPRequestHandler.guess_type(self, path)


if __name__ == "__main__":
    directory = os.path.dirname(__file__)
    os.chdir(os.path.join(directory, os.pardir))
    print("You can view the prototype at http://localhost:8000/Prototype/")
    BaseHTTPServer.test(RequestHandler, BaseHTTPServer.HTTPServer)
