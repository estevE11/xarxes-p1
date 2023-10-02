import socket
import time
import ipinfo
import matplotlib.pyplot as plt
from scapy.all import *


def get_ip_info():
    access_token = '92ea3b28d5471d'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()
    return details

def traceroute(dest_name) :
    Conf.route.add(net="0.0.0.0/0", dev="ens33")

    dest_addr = socket.gethostbyname(dest_name)