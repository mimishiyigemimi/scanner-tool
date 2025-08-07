# 🛡️ 基于 Python 的网站漏洞扫描器

一个轻量级的漏洞扫描工具，使用 Python 编写，支持网站目录扫描、端口扫描、SQL 注入检测与 XSS 漏洞检测。适用于网络安全学习与简单的站点安全评估。

---

## 🚀 项目功能

本工具可实现以下四大模块的漏洞扫描功能：

1. **网站目录扫描（Directory Scan）**
   - 基于字典，测试常见路径是否可访问
   - 扫描结果输出到 `output/dir_scan.txt`

2. **端口扫描（Port Scan）**
   - 探测目标主机是否开放常见端口（如 80、443、21 等）

3. **SQL 注入检测（SQL Injection Check）**
   - 通过构造基本的 SQL payload 检查是否存在注入点
   - 提供匹配关键词和模式的反馈结果

4. **XSS 漏洞检测（Cross-Site Scripting）**
   - 基于反射 payload 模式匹配进行检测
   - 输出疑似漏洞 URL 和置信度标记

---

## 📦 安装依赖

建议使用虚拟环境运行本项目。

1. 克隆本项目：

```bash
git clone https://github.com/mimishiyigemimi/scanner-tool.git
cd scanner-tool
安装依赖：

bash
复制
编辑
pip install -r requirements.txt
🛠️ 使用方法
运行扫描器：

bash
复制
编辑
python scanner.py <目标网址>
⚠️ 建议输入完整 URL，包括协议（http:// 或 https://）

示例：
bash
复制
编辑
python scanner.py https://www.example.com
📁 输出说明
扫描完成后，结果将保存在 output/ 目录下：

output/dir_scan.txt：网站目录扫描结果

output/report.json：包含所有模块的扫描综合报告（JSON 格式）

📌 注意事项
本工具仅用于学习与授权测试，请勿在未授权的网站上使用！

XSS/SQL 检测为基础模式匹配，建议结合手动验证使用

后期可扩展支持验证码识别、Cookie 注入、爬虫模块等功能

📚 项目结构简述
bash
复制
编辑
scanner-tool/
│
├── scanner.py                # 主调度文件
├── requirements.txt          # 依赖库列表
├── output/                   # 扫描结果输出目录
│   ├── dir_scan.txt
│   └── report.json
└── modules/                  # 功能模块
    ├── dirscan.py
    ├── portscan.py
    ├── sqlcheck.py
    └── xsscheck.py
🤝 作者信息
👤 GitHub: @mimishiyigemimi

📧 欢迎交流学习，建议与改进请提交 Issue 或 PR！
