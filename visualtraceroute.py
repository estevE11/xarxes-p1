import argparse
import socket
import time
import ipinfo
import matplotlib.pyplot as plt
import requests
from scapy.all import Conf, IP, ICMP, sr1
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Circle


def get_ip_info(ip):
    access_token = '92ea3b28d5471d'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip)
    return details.details

def is_ip_public(ip):
    # Lista de rangos de direcciones IP públicas
    public_ip_ranges = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255"),
        ("169.254.0.0", "169.254.255.255"),
    ]
    
    # Verificar si la IP está en un rango de IP pública
    ip_num = int(ip.replace(".", ""))
    for start_range, end_range in public_ip_ranges:
        if ip_num >= int(start_range.replace(".", "")) and ip_num <= int(end_range.replace(".", "")):
            return True
    return False

def get_status_ip(direccion_ip):
    try:
        url = f"https://ipinfo.io/{direccion_ip}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return "OK"
    except Exception as e:
        return "Error"
    return "Error"

def traceroute(dest_addr) :

    dest_name = socket.gethostbyaddr(dest_addr)
    max_ttl = 30
    ttl = 1

    ips = []
    positions = []
    
    while ttl < max_ttl:
        time_sent = time.time()

        package_icmp = IP(dst=dest_addr,ttl=ttl) / ICMP()
        response = sr1(package_icmp, verbose=False, timeout=1)

        time_received = time.time()

        rtt_ms = (time_received - time_sent) * 1000

        if response:
            ip = response.src
            ips.append(ip)
            #esto lo usaremos luego cuando decubramos como dibujar con el mapa
            ip_details = get_ip_info(ip)

            if("loc" in ip_details): 
                positions.append(parse_position(ip_details['loc']))

            print_ip_details(ip_details, ttl, rtt_ms)
            
            if response.src == dest_addr:
                break
        else:
            print(f"* * * * * *")
        ttl += 1
        
    if dest_addr == ips[-1]:
        print("Hem arribat al destí")
        for ip in ips:
            if is_ip_public(ip):
                print(f"Parsejant l'adreça IP {ip} ... {get_status_ip(ip)}!")
            else:
                print(f"Parsejant l'adreça IP {ip} ... {get_status_ip(ip)}!", end="")
                print(f"Parsejant l'adreça IP {ip} ... no es publica!", end="")
    else:
        print("No hem arribat al destí")
    

    drawmap(positions)

def parse_position(pos_str):
    spl = pos_str.split(",")
    return float(spl[0]), float(spl[1])

def print_ip_details(ip_details, ttl, ms):
    print(f"RTT al host='", end="")
    if "hostname" in ip_details:
        print(ip_details["hostname"], end="")
    else:
        print("*", end="")
    print(f"' ({ip_details['ip']}) es de {ms:.0f} ms ")

def drawmap(positions):
    # create new figure, axes instances.
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    LONMIN, LONMAX, LATMIN, LATMAX = calculate_crop(positions)

    m = Basemap(llcrnrlon=LONMIN,llcrnrlat=LATMIN,urcrnrlon=LONMAX,urcrnrlat=LATMAX,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='cyl',\
                lat_ts=20.)

    m.drawcoastlines()
    m.fillcontinents()
    
    for i in range(len(positions)):
        curr = positions[i]
        if i < len(positions)-1:
            next = positions[i+1]
            if curr == next:
                continue
            print(curr[1],curr[0],next[1],next[0])
            try:
                m.drawgreatcircle(curr[1],curr[0],next[1],next[0],linewidth=2,color='b')
            except:
                print('error drawing line')

        x, y = m(curr[1], curr[0])
        circle = Circle((x, y), 0.3, color='red', fill=True, linewidth=2)

        ax.add_patch(circle)

    plt.show()

def calculate_crop(positions, off=10): 
    max_lon = max(pos[1] for pos in positions)
    min_lon = min(pos[1] for pos in positions)
    max_lat = max(pos[0] for pos in positions)
    min_lat = min(pos[0] for pos in positions)

    LONMIN = max(-180, min_lon - off)
    LONMAX = min(180, max_lon + off)
    LATMIN = max(-90, min_lat - off)
    LATMAX = min(90, max_lat + off + 10)

    return LONMIN, LONMAX, LATMIN, LATMAX

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="traceroute")
    
    parser.add_argument("--ip_address", "-d", help="Destination to trace the route to")

    args = parser.parse_args()


    ip = args.ip_address
    if ip:
        traceroute(ip)
    else:
        traceroute("154.54.42.102")


    #traceroute("142.250.184.174")
    #traceroute("8.8.8.8")
    #traceroute("92.57.40.154")




