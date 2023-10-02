import socket
import time
import ipinfo
import matplotlib.pyplot as plt
from scapy import *


def get_ip_info():
    access_token = '92ea3b28d5471d'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()
    return details

