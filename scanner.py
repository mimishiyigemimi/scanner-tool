# scanner.py

from modules import dirscan, portscan, sqlcheck, xsscheck
import sys
import json
from urllib.parse import urlparse
import os
import time
import requests

# 自动创建必要目录
os.makedirs("output", exist_ok=True)

if len(sys.argv) != 2:
    print("Usage: python scanner.py <target_url>")
    sys.exit(1)

url = sys.argv[1]
parsed = urlparse(url)
host = parsed.hostname

print("[+] Starting scan on:", url)

# 目录扫描（调用模块）
try:
    dirs = dirscan.scan_website(url, wordlist_file="wordlists/wordlist.txt")
except Exception as e:
    print("[-] 目录扫描失败:", e)
    dirs = []

# 端口扫描
try:
    open_ports = portscan.scan_ports(host)
    print("[+] Open ports:", open_ports)
except Exception as e:
    print("[-] Error during port scan:", e)
    open_ports = []

# SQL 注入检测
sql_test_url = f"http://{host}/some_page.php?id=1'"
try:
    r = requests.get(sql_test_url)
    sql_vulnerable = sqlcheck.test_sql_injection(r.text)
except Exception as e:
    print("[-] Error during SQL injection test:", e)
    sql_vulnerable = False
print("[+] SQL Injection Vulnerable:", sql_vulnerable)

# XSS 检测
try:
    xss_vulnerable = xsscheck.test_xss(url)
    print("[+] XSS Vulnerable:", xss_vulnerable)
except Exception as e:
    print("[-] Error during XSS test:", e)
    xss_vulnerable = False


# 输出报告
report = {
    "target": url,
    "host": host,
    "directories": dirs,
    "open_ports": open_ports,
    "sql_vulnerable": sql_vulnerable,
    "xss_vulnerable": xss_vulnerable,
    "scan_time": time.strftime('%Y-%m-%d %H:%M:%S')
}

with open("output/report.json", "w") as f:
    json.dump(report, f, indent=4)

print("[+] Scan complete. Report saved to output/report.json")
