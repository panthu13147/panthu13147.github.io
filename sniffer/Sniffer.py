from scapy.all import sniff

def packet_callback(packet):
    # Print a summary of every packet we catch
    print(packet.summary())

print("🕵️  Starting the Sniffer... (Press Ctrl+C to stop)")
sniff(prn=packet_callback, count=0)
