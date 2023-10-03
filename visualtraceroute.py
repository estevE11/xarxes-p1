import socket
import time
import ipinfo
import matplotlib.pyplot as plt
from scapy.all import Conf, IP, ICMP, sr1


def get_ip_info(ip):
    access_token = '92ea3b28d5471d'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip)
    return details.details

def traceroute(dest_addr) :
    #Conf.route.add(net="0.0.0.0/0", dev="ens33")

    dest_name = socket.gethostbyaddr(dest_addr)
    max_ttl = 30
    ttl = 1

    while ttl < max_ttl:
        time_sent = time.time()

        package_icmp = IP(dst=dest_addr,ttl=ttl) / ICMP()
        response = sr1(package_icmp, verbose=False, timeout=2)

        time_received = time.time()

        rtt_ms = (time_received - time_sent) * 1000

        if response:
            ip = response.src
            #esto lo usaremos luego cuando decubramos como dibujar con el mapa
            ip_details = get_ip_info(ip)
            
            print_ip_details(ip_details, ttl, rtt_ms)
            
            if response.src == dest_addr:
                break
        else:
            print(f"* * * * * *")
        ttl += 1

def print_ip_details(ip_details, ttl, ms):
    print(f"{ttl}. {ip_details['ip']} {ms:.0f}ms   ", end="")
    if "hostname" in ip_details:
        print(ip_details["hostname"])
    else:
        print("*")

if __name__ == "__main__":
    #traceroute("www.google.com")
    traceroute("142.250.184.174")
