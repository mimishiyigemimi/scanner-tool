import re

def test_sql_injection(response_text):
    """
    增强版SQL注入检测，包含：
    1. 多数据库错误关键词
    2. 基础/高级注入模式
    3. 编码混淆检测
    4. 数据库特定特征
    返回结构化信息，包括是否存在漏洞、匹配的关键词和正则模式
    """

    # 多数据库错误关键词（含大小写变体）
    keywords = [
        "sql syntax", "mysql_fetch", "sql error", "mysql_num_rows",
        "ora-[0-9]{5}", "pls-[0-9]{4}", "unclosed quotation",
        "incorrect syntax", "postgresql error", "db2 sql error",
        "warning: mysql", "sqlite_exception", "odbc driver",
        "jdbc error", "pdo exception"
    ]

    # 基础注入模式（使用re.IGNORECASE忽略大小写）
    base_patterns = [
        r"\b(OR|AND)\s+[\d]+\s*[=<>!]+\s*[\d]+\b",
        r"\bUNION\s+(ALL\s+)?SELECT\b",
        r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE).+?\b(FROM|INTO|SET|TABLE|DATABASE)\b",
        r"\bEXEC(UTE)?\s*\(.+\)\b",
        r"\bWAITFOR\s+DELAY\s+'0:0:[\d]'\b"
    ]

    # 高级注入技术检测
    advanced_patterns = [
        r"\bDECLARE\s+@\w+\s+(INT|VARCHAR)\b",
        r"\bEXEC\s+(MASTER\.)?SP_\w+\b",
        r"\bINTO\s+(OUTFILE|DUMPFILE)\s+'.+'\b",
        r"\bLOAD_FILE\s*\(.+\)\b",
        r"\bCONVERT\s*\(.+?,.+?\)\b",
        r"\bINFORMATION_SCHEMA\.\w+\b"
    ]

    # 编码混淆检测
    obfuscation_patterns = [
        r"\b0x[\da-f]+\b",
        r"\bCHAR\s*\(([\d]+,?\s*)+\)",
        r"\/\*!.+\*\/",
        r"--\s*[\r\n]",
        r"\;\s*[\r\n]",
        r"\bEXEC\s*\(\s*0x.+\s*\)"
    ]

    all_patterns = base_patterns + advanced_patterns + obfuscation_patterns

    # 转为小写文本进行匹配
    text = response_text.lower() if isinstance(response_text, str) else str(response_text).lower()

    hit_keywords = []
    for keyword in keywords:
        if re.search(keyword, text, re.IGNORECASE):
            hit_keywords.append(keyword)

    hit_patterns = []
    for pattern in all_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            hit_patterns.append(pattern)

    return {
        "vulnerable": bool(hit_keywords or hit_patterns),
        "matched_keywords": hit_keywords,
        "matched_patterns": hit_patterns
    }
