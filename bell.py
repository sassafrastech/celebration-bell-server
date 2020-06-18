import os
if 'NO_GPIO' not in os.environ:
    import RPi.GPIO as GPIO
import time
import socket
import threading
import socketserver

STUB_FILE = os.path.dirname(os.path.realpath(__file__)) + "/pressed"
HOST = "0.0.0.0"
PORT = 4810

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while 1:
            self.data = self.request.recv(8)
            if not self.data:
                break
            self.data = self.data.strip()
            print(self.data)
            if self.data == b'RING':
                ring()
                self.request.send(b'RUNG')

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def ring():
    if 'NO_GPIO' not in os.environ:
        GPIO.output(14, GPIO.HIGH)
    else:
        print("Solenoid out")

    time.sleep(0.02)

    if 'NO_GPIO' not in os.environ:
        GPIO.output(14, GPIO.LOW)
    else:
        print("Solenoid in")

def check_button():
    if 'NO_GPIO' not in os.environ:
        return GPIO.input(27)
    else:
        return not(os.path.exists(STUB_FILE))

if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

        if 'NO_GPIO' not in os.environ:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(14, GPIO.OUT)
            GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Startup rings
        ring()
        time.sleep(0.2)
        ring()

        down = False
        while True:
            input_state = check_button()
            if input_state == False and not down:
                down = True
                ring()
            if input_state == True and down:
                down = False

        server.shutdown()
