# FIBERMEYER - Deploy VPS Hostinger (PowerShell)
# =============================================

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🚀 FIBERMEYER - Deploy VPS Hostinger" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 INSTRUÇÕES PARA DEPLOY MANUAL:" -ForegroundColor Green
Write-Host ""

Write-Host "1. Conecte no VPS:" -ForegroundColor White
Write-Host "   ssh root@69.62.89.102" -ForegroundColor Yellow
Write-Host "   Senha: j89hahPXbz,uVndACJM+" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Execute estes comandos no VPS:" -ForegroundColor White
Write-Host "   # Baixar script de deploy" -ForegroundColor Gray
Write-Host "   curl -s https://raw.githubusercontent.com/Fernando-Godinho/FIBERMEYER/main/deploy-hostinger.sh -o deploy.sh" -ForegroundColor Yellow
Write-Host ""
Write-Host "   # Dar permissão e executar" -ForegroundColor Gray
Write-Host "   chmod +x deploy.sh" -ForegroundColor Yellow
Write-Host "   ./deploy.sh" -ForegroundColor Yellow
Write-Host ""

Write-Host "3. Aguarde o deploy (5-10 minutos)" -ForegroundColor White
Write-Host ""

Write-Host "4. Após concluído, acesse:" -ForegroundColor White
Write-Host "   🌐 Sistema: http://69.62.89.102" -ForegroundColor Green
Write-Host "   👨‍💼 Admin: http://69.62.89.102/admin/" -ForegroundColor Green
Write-Host "   🔑 Login: admin / admin123" -ForegroundColor Green
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📋 COMANDOS RESUMIDOS PARA COPIAR:" -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$commands = @"
curl -s https://raw.githubusercontent.com/Fernando-Godinho/FIBERMEYER/main/deploy-hostinger.sh -o deploy.sh
chmod +x deploy.sh
./deploy.sh
"@

Write-Host $commands -ForegroundColor Yellow
Write-Host ""

Write-Host "🔄 Deseja que eu tente conectar automaticamente? (s/n): " -ForegroundColor Cyan -NoNewline
$response = Read-Host

if ($response -eq "s" -or $response -eq "S") {
    Write-Host ""
    Write-Host "🔐 Tentando conectar automaticamente..." -ForegroundColor Blue
    Write-Host ""
    
    # Tentar usando ssh nativo do Windows
    try {
        Write-Host "Executando SSH..." -ForegroundColor Gray
        ssh -o StrictHostKeyChecking=no root@69.62.89.102
    }
    catch {
        Write-Host "❌ Erro na conexão SSH automática." -ForegroundColor Red
        Write-Host "Use a conexão manual acima." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Script de deploy pronto para execução!" -ForegroundColor Green
Read-Host "Pressione Enter para continuar"