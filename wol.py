#!/usr/bin/env python

"""
Wake on Lan implementation in python3.
"""

import socket
import re
import struct
import argparse

class MagicPacket(object):
    def __init__(self, eth_addr):
        self.wol_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.wol_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__ETH_ADDR_PTN =  "^[a-f0-9]{12}(?i)$"
        self.eth_addr = re.sub('[-:.]', '', eth_addr)

    def validate(self):
        m = re.match(self.__ETH_ADDR_PTN, self.eth_addr)
        if not m:
            raise ValueError

    def send(self):
        try:
            self.validate()
            data_fmt = (6 * 'FF') + (16 * self.eth_addr)
            send_data = b''
            for i in range(0, len(data_fmt), 2):
                send_data += struct.pack('B', int( data_fmt[i:i + 2], 16))
            self.wol_sock.sendto(send_data, ('255.255.255.255', 7))
            print("Magic packet has been sent to \'{}\'".format(sys.argv[1]))

        except ValueError:
            print("Invalid ethernet address format.")
        finally:
            self.wol_sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send magic packet to given ethernet address.')
    parser.add_argument('ethernet_address', nargs=1, type=str, help='dot(.), dash(-) or colon(:) ethernet address format is handled')
    args = parser.parse_args()
    MagicPacket(args.ethernet_address[0]).send()






