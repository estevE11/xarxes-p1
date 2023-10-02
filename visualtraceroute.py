import socket
import time
import ipinfo
import matplotlib.pyplot as plt
from scapy.all import Conf, IP, ICMP, sr1


def get_ip_info(ip):
    access_token = '92ea3b28d5471d'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip)
    return details

def traceroute(dest_addr) :
    Conf.route.add(net="0.0.0.0/0", dev="ens33")

    dest_name = socket.gethostbyaddr(dest_addr)
    max_ttl = 30
    ttl = 1

    while True:
        time_sent = time.time()

        package_icmp = IP(dst=dest_addr,ttl=ttl) / ICMP()
        response = sr1(package_icmp,verbose=False)

        time_received = time.time()

        rtt_mls = (time_received - time_sent) * 1000

        if response:
            ip = response.src
            #esto lo usaremos luego cuando decubramos como dibujar con el mapa
            details_ip = get_ip_info(ip)
            
            print(f"RTT al host='{dest_name}' ({ip}) es de {rtt_mls:.2f} ms")
            
            if response.src == dest_addr:
                break
        else:
            print(f"* * * * * *")
