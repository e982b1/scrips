#!/usr/bin/env bash
# ==============================================================================
# 远程扫描 CVE-2025-68615 - Net-SNMP snmptrapd 缓冲区溢出
# 修复：grep -P 兼容性问题 | 全系统通用 | 适合防火墙/网络设备
# ==============================================================================

set -euo pipefail

PORT=162
TIMEOUT=1

version_lt() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$1" ] && [ "$1" != "$2" ]
}

is_vulnerable_version() {
    local ver="$1"
    if echo "$ver" | grep -q "^5\\.10\\.pre1$"; then
        return 0
    fi
    version_lt "$ver" "5.9.5"
}

scan_ip() {
    local IP="$1"
    echo "========================================================================"
    echo "[*] 扫描目标：$IP"
    echo "========================================================================"

    echo "[*] 检查 UDP 162 端口（snmptrapd）..."
    if ! nc -v -u -w $TIMEOUT -z $IP $PORT >/dev/null 2>&1; then
        echo "[SAFE] $IP:162 端口未开放"
        echo "RESULT|$IP|CVE-2025-68615|SAFE|PORT_CLOSED"
        echo
        return
    fi

    echo "[WARN] $IP:162 端口开放 → snmptrapd 服务暴露"
    echo "[*] 尝试获取 SNMP 版本..."

    SNMP_VERSION=""
    if command -v snmpget &>/dev/null; then
        raw=$(snmpget -v2c -c public $IP 1.3.6.1.2.1.1.1.0 2>/dev/null || true)
        if echo "$raw" | grep -q "Net-SNMP"; then
            SNMP_VERSION=$(echo "$raw" | sed 's/.*Net-SNMP //g' | awk '{print $1}' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+')
        fi
    fi

    if [ -z "$SNMP_VERSION" ]; then
        echo "[WARN] 无法识别版本，但端口开放 → 高风险暴露"
        echo "RESULT|$IP|CVE-2025-68615|VULNERABLE|PORT_OPEN_UNKNOWN_VERSION"
        echo
        return
    fi

    echo "[INFO] 识别版本：$SNMP_VERSION"

    if is_vulnerable_version "$SNMP_VERSION"; then
        echo "[CRITICAL] 目标存在高危漏洞 CVE-2025-68615 (可DoS/RCE)"
        echo "RESULT|$IP|CVE-2025-68615|VULNERABLE|$SNMP_VERSION"
    else
        echo "[SAFE] 版本已修复"
        echo "RESULT|$IP|CVE-2025-68615|SAFE|$SNMP_VERSION"
    fi

    echo
}

main() {
    if [ $# -lt 1 ]; then
        echo "使用方法：$0 <IP 或 IP列表文件>"
        echo "示例："
        echo "  $0 192.168.1.100"
        echo "  $0 ip.txt"
        exit 1
    fi

    TARGET="$1"
    if [ -f "$TARGET" ]; then
        while IFS= read -r ip; do
            scan_ip "$ip"
        done < "$TARGET"
    else
        scan_ip "$TARGET"
    fi
}

main "$@"
