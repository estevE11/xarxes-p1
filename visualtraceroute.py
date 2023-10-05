import socket
import time
import ipinfo
import matplotlib.pyplot as plt
from scapy.all import Conf, IP, ICMP, sr1
from mpl_toolkits.basemap import Basemap


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

    positions = []

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

            if("loc" in ip_details): 
                positions.append(parse_position(ip_details['loc']))

            print_ip_details(ip_details, ttl, rtt_ms)
            
            if response.src == dest_addr:
                break
        else:
            print(f"* * * * * *")
        ttl += 1

    print("Hem arribat al destí") 

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
    
    # los primeros 4 son para el zoom
    m = Basemap(llcrnrlon=-130.,llcrnrlat=0.,urcrnrlon=20.,urcrnrlat=60.,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',projection='merc',\
                lat_ts=20.)
    
    for i in range(len(positions)-2):
        curr = positions[i]
        next = positions[i+1]
        if curr == next:
            continue
        m.drawgreatcircle(curr[1],curr[0],next[1],next[0],linewidth=2,color='b')


    m.drawcoastlines()
    m.fillcontinents()
    ax.set_title('Hay q poner titulo?')
    plt.show()

if __name__ == "__main__":
    #traceroute("www.google.com")
    #traceroute("142.250.184.174")
    traceroute("154.54.42.102")
    #traceroute("8.8.8.8")

