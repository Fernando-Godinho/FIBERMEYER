#!/bin/bash
# Script para descobrir informações do VPS Hostinger
# Execute este script no seu VPS

echo "========================================"
echo "   ANÁLISE DO VPS HOSTINGER - FIBERMEYER"
echo "========================================"
echo ""

echo "=== 1. INFORMAÇÕES DO SISTEMA ==="
echo "Hostname: $(hostname)"
echo "Sistema: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "Kernel: $(uname -r)"
echo "Arquitetura: $(uname -m)"
echo ""

echo "=== 2. RECURSOS DISPONÍVEIS ==="
echo "CPU Cores: $(nproc)"
echo "Memória:"
free -h
echo ""
echo "Disco:"
df -h /
echo ""

echo "=== 3. SOFTWARE JÁ INSTALADO ==="
echo -n "Docker: "
if command -v docker &> /dev/null; then
    docker --version
else
    echo "NÃO INSTALADO"
fi

echo -n "Docker Compose: "
if command -v docker-compose &> /dev/null; then
    docker-compose --version
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    echo "Docker Compose (integrado): $(docker compose version)"
else
    echo "NÃO INSTALADO"
fi

echo -n "Python3: "
if command -v python3 &> /dev/null; then
    python3 --version
else
    echo "NÃO INSTALADO"
fi

echo -n "Nginx: "
if command -v nginx &> /dev/null; then
    nginx -v 2>&1
else
    echo "NÃO INSTALADO"
fi

echo -n "Apache: "
if command -v apache2 &> /dev/null; then
    apache2 -v | head -1
else
    echo "NÃO INSTALADO"
fi

echo -n "Git: "
if command -v git &> /dev/null; then
    git --version
else
    echo "NÃO INSTALADO"
fi

echo ""

echo "=== 4. PORTAS ABERTAS/SERVIÇOS ==="
echo "Portas em uso:"
ss -tulpn | grep LISTEN | head -10
echo ""

echo "=== 5. FIREWALL STATUS ==="
if command -v ufw &> /dev/null; then
    echo "UFW Status:"
    ufw status
elif command -v firewall-cmd &> /dev/null; then
    echo "Firewalld Status:"
    firewall-cmd --state 2>/dev/null && firewall-cmd --list-all
else
    echo "Nenhum firewall detectado (ufw/firewalld)"
fi
echo ""

echo "=== 6. INFORMAÇÕES DE REDE ==="
echo "IP Público: $(curl -s ifconfig.me || echo 'Não detectado')"
echo "IPs Locais:"
ip addr show | grep "inet " | grep -v 127.0.0.1
echo ""

echo "=== 7. GERENCIADOR DE PACOTES ==="
if command -v apt &> /dev/null; then
    echo "Sistema: Ubuntu/Debian (apt)"
elif command -v yum &> /dev/null; then
    echo "Sistema: CentOS/RHEL (yum)"
elif command -v dnf &> /dev/null; then
    echo "Sistema: Fedora/CentOS Stream (dnf)"
else
    echo "Gerenciador não identificado"
fi
echo ""

echo "=== 8. ESPAÇO DISPONÍVEL ==="
echo "Diretório /opt (para aplicações):"
du -sh /opt 2>/dev/null || echo "/opt não encontrado"
echo ""
echo "Diretório /home:"
du -sh /home 2>/dev/null || echo "/home não encontrado"
echo ""

echo "========================================"
echo "   ANÁLISE CONCLUÍDA"
echo "========================================"
echo ""
echo "📋 Próximos passos:"
echo "1. Copie esta saída completa"
echo "2. Envie para análise"
echo "3. Receberá script de instalação personalizado"
echo ""