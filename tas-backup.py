## importing socket module
import socket
import urllib.request, json
import time, datetime, os

ipignore = ["192.168.1.120", "192.168.1.121", "192.168.1.122", "192.168.1.123"]

## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname + ".local")
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")
ipparts = ip_address.split(".")
iprange = ipparts[0]+"."+ipparts[1]+"."+ipparts[2]+"."

def TestBackup(ip):
    response = os.system("ping -c 1 " + hostname + " > /dev/null 2>&1")
    if response == 0:
        print (ip + " Found \r", end="")
        try:
            with urllib.request.urlopen("http://"+ip+"/cm?cmnd=status%205") as url:
                data = json.loads(url.read().decode())
        except (json.decoder.JSONDecodeError, urllib.error.HTTPError, urllib.error.URLError) as e:
            return
        print (ip, data['StatusNET']['Hostname'])
        urllib.request.urlretrieve("http://"+ip+"/dl?", folder+data['StatusNET']['Hostname'].replace(" ","")+".dump")    
        with urllib.request.urlopen("http://"+ip+"/cm?cmnd=wificonfig%200") as url:
            data = json.loads(url.read().decode())
    else:
      return
    
folder = time.strftime("./%Y-%m-%d/")
try:
    os.mkdir(folder)
except FileExistsError:
    print ("Directory Exists")
    
for i in range(1,255):
    ip = iprange+str(i)
    if ip in ipignore:
        print (ip+" Ignored")
    else:
        print (ip+"\r", end="")
        TestBackup(ip)
