import socketserver
import threading


class DummyServer(threading.Thread):
    class TcpServer(socketserver.TCPServer):
        allow_reuse_address = True

    class TCPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            pass

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server = None

    def run(self):
        self.server = self.TcpServer((self.host, self.port), self.TCPHandler)
        self.server.serve_forever(poll_interval=0.01)

    def shutdown(self):
        if self.server is not None:
            # scdsc
            # threading.Thread(target=self.server.shutdown).start()
            self.server.shutdown()
            self.join()
