import socket
from datetime import datetime

def scan_target(target_ip, ports_to_scan):
    print(f"\n--- Starting Scan on Host: {target_ip} ---")
    print(f"--- Time started: {datetime.now()} ---\n")

    try:
        # Loop through the list of ports we want to check
        for port in ports_to_scan:
            # 1. Create a socket object (like creating a phone line)
            # AF_INET = IPv4, SOCK_STREAM = TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # 2. Set a timeout so we don't wait forever if a port is filtered (0.5 seconds)
            socket.setdefaulttimeout(0.5)
            
            # 3. Try to connect to the port
            # connect_ex returns 0 if connection was successful (Open)
            result = s.connect_ex((target_ip, port))
            
            if result == 0:
                print(f"[+] Port {port} is OPEN")
            else:
                # Optional: Uncomment the line below to see closed ports too
                # print(f"[-] Port {port} is closed")
                pass
            
            # 4. Close the connection
            s.close()

    except KeyboardInterrupt:
        print("\nExiting Program...")
    except socket.gaierror:
        print("\nHostname could not be resolved.")
    except socket.error:
        print("\nCould not connect to server.")

if __name__ == "__main__":
    # Ask the user for input
    target = input("Enter a target website or IP (e.g., scanme.nmap.org): ")
    
    # Resolve the name to an IP (e.g., google.com -> 142.250.x.x)
    target_ip = socket.gethostbyname(target)
    
    # Define common ports to check
    # 21=FTP, 22=SSH, 80=HTTP, 443=HTTPS, 3306=MySQL
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
    
    scan_target(target_ip, common_ports)