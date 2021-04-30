import socket
import sys
import time
import math
from dataclasses import dataclass
from threading import Thread

# command to start vlc:
# vlc --intf rc --rc-host 127.0.0.1:44500


# usage:
# python main.py <max_speedup> <speedup_interval>
# where max_speedup e.g. 1.75
# speedup_interval e.g. 5 (mins) - time over which the max speedup is to be achieved

@dataclass
class Args:
    max_speedup: float
    speedup_interval: float


host = '127.0.0.1'
port = 44500


class Player():
    def __init__(self):
        pass

    def set_rate(self, rate: float):
        self.threadedreq("rate " + str(rate))
        print("Setting rate to: " + str(rate))

    def req(self, msg: str, full=False):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data
                sock.settimeout(0.7)
                sock.connect((host, port))
                response = ""
                received = ""
                sock.sendall(bytes(msg + '\n', "utf-8"))
                try:
                    while (True):
                        received = (sock.recv(1024)).decode()
                        response = response + received
                        if full:
                            b = response.count("\r\n")
                            if response.count("\r\n") > 1:
                                sock.close()
                                break
                        else:
                            if response.count("\r\n") > 0:
                                sock.close()
                                break
                except:
                    response = response + received
                sock.close()
                return response
        except:
            return None

    def threadedreq(self, msg):
        Thread(target=self.req, args=(msg,)).start()


def usage():
    print("""
python main.py <max_speedup> <speedup_interval>
where max_speedup e.g. 1.75
speedup_interval e.g. 5 (mins) - time over which the max speedup is to be achieved
""")


def main():
    if len(sys.argv) != 3:
        usage()
        return

    args = Args(float(sys.argv[1]), float(sys.argv[2]))
    player = Player()


    speedups_count = int((args.max_speedup - 1.0) * 100)
    tick = args.speedup_interval * 60 / speedups_count

    current_speed = 1.0
    while current_speed < args.max_speedup:
        time.sleep(tick)
        current_speed = round(current_speed + 0.01, 2)
        player.set_rate(current_speed)


if __name__ == '__main__':
    main()
