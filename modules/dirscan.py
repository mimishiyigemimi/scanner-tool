# modules/dirscan.py

import requests
from concurrent.futures import ThreadPoolExecutor
import chardet
import time
import os

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


def scan_website(base_url,
                 wordlist_file="wordlists/wordlist.txt",
                 max_threads=10,
                 output_file="output/dir_scan.txt"):

    base_url = base_url.rstrip('/') + '/'

    try:
        encoding = detect_encoding(wordlist_file)
        with open(wordlist_file, 'r', encoding=encoding) as f:
            wordlist = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] 字典文件 {wordlist_file} 不存在")
        return []
    except UnicodeDecodeError:
        try:
            with open(wordlist_file, 'r', encoding='utf-8') as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"[-] 无法读取字典文件: {e}")
            return []

    found_dirs = []

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as out_f:
        out_f.write(f"网站目录扫描结果 - {base_url}\n")
        out_f.write(f"扫描时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_f.write("=" * 50 + "\n\n")

        def check_url(path):
            nonlocal found_dirs
            url = base_url + path
            try:
                response = requests.get(url, timeout=5)
                if response.status_code < 400:
                    result = f"[{response.status_code}] {url}"
                    out_f.write(result + "\n")
                    found_dirs.append(url)
            except requests.RequestException:
                pass

        # ===== 并发扫描核心引擎 =====
        # 使用线程池并发扫描路径，提高扫描速度（最大线程数由 max_threads 控制）
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # executor.map 会自动将 wordlist 中的每一项分配给线程执行 check_url 函数
        # 相当于启动 max_threads 个线程同时工作，提高扫描效率
            executor.map(check_url, wordlist)

        out_f.write("\n" + "=" * 50 + "\n")
        out_f.write(f"扫描完成于: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_f.write(f"发现的有效路径: {len(found_dirs)}\n")

    print(f"[+] Directory scan completed, results saved t {output_file}")
    return found_dirs
