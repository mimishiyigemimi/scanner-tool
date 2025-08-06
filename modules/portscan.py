# modules/portscan.py
import socket

def scan_ports(host, ports=[21, 22, 23, 80, 443, 3306, 8080]):
    """
    简单端口扫描，检测指定 host 上的开放端口。
    """
    open_ports = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
        except:
            continue
    return open_ports
