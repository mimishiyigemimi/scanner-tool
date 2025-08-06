import re, html, urllib.parse
from typing import Dict, List
import requests

class XSSDetector:
    def __init__(self):
        self.payloads = [
            "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
            "\"><script>alert(1)</script>", "#javascript:alert(1)",
            "%3Cscript%3Ealert(1)%3C/script%3E"
        ]
        self.patterns = [
            r"<(script|iframe|img)[^>]*>", r"\bon\w+\s*=",
            r"javascript:\s*[^\"'>]+"
        ]

    def scan(self, url: str) -> Dict:
        results = {}
        tested_urls = []
        for payload in self.payloads:
            test_url = f"{url}{'&' if '?' in url else '?'}xss={urllib.parse.quote(payload)}"
            tested_urls.append(test_url)
            try:
                r = requests.get(test_url, timeout=5)
                vuln_result = self._check(r.text, payload)
                if vuln_result:
                    results[test_url] = {
                        "payload": payload,
                        "type": vuln_result['type'],
                        "confidence": vuln_result['confidence']
                    }
            except requests.RequestException:
                continue

        return {
            "vulnerable": bool(results),
            "details": results,
            "tested_urls": tested_urls
        }

    def _check(self, text: str, payload: str) -> Dict:
        text = urllib.parse.unquote(text)
        if payload in text:
            return {'type': 'direct', 'confidence': 'high'}
        if html.escape(payload) in text:
            return {'type': 'encoded', 'confidence': 'medium'}
        if any(re.search(ptn, text, re.IGNORECASE) for ptn in self.patterns):
            return {'type': 'pattern', 'confidence': 'low'}
        return {}

def test_xss(url: str) -> Dict:
    """
    快速测试函数，返回结构化信息
    """
    return XSSDetector().scan(url)

result = test_xss("http://example.com/index.php?id=1")
if result["vulnerable"]:
    print("[VULNERABLE] XSS found!")
    for url, info in result["details"].items():
        print(f"  ├─ URL: {url}")
        print(f"  │   ├─ Payload: {info['payload']}")
        print(f"  │   ├─ Type: {info['type']}")
        print(f"  │   └─ Confidence: {info['confidence']}")
else:
    print("[SAFE] No XSS detected.")