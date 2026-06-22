# Pipeline.ps1 - Full pipeline (crawl + news + homepage + deploy)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " CreatorAI Full Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Started: $(Get-Date)"
$logFile = "D:\项目\工作区\工作5\_pipeline_log.txt"

# Cleanup stale locks
Remove-Item "D:\项目\工作区\工作5\_crawl_running.lock" -ErrorAction SilentlyContinue
Remove-Item "D:\项目\工作区\工作5\_crawl_round.json" -ErrorAction SilentlyContinue

# Step 1: Global Crawl
Write-Host "`n[Step 1/5] Running global crawler..." -ForegroundColor Yellow
python global_crawler.py 2>&1 | Out-File -Append -FilePath $logFile

# Step 2: News Crawl
Write-Host "`n[Step 2/5] Running AI news crawler..." -ForegroundColor Yellow
python news_crawler.py 2>&1 | Out-File -Append -FilePath $logFile

# Step 3: Generate News Page
Write-Host "`n[Step 3/5] Generating news page..." -ForegroundColor Yellow
python generate_news.py 2>&1 | Out-File -Append -FilePath $logFile

# Step 4: Update Homepage with Top News
Write-Host "`n[Step 4/5] Updating homepage with top news..." -ForegroundColor Yellow
python generate_home_news.py 2>&1 | Out-File -Append -FilePath $logFile

# Step 5: Deploy
Write-Host "`n[Step 5/5] Deploying to Vercel..." -ForegroundColor Yellow
$deployOutput = vercel --prod --yes 2>&1 | Out-String
Write-Host $deployOutput
if ($deployOutput -match "Aliased.*vercel.app" -or $deployOutput -match "ready" -or $LASTEXITCODE -eq 0) {
    Write-Host "[OK] Deployed!" -ForegroundColor Green
    Add-Content -Path $logFile -Value "[$(Get-Date)] DEPLOY SUCCESS"
} else {
    Write-Host "[ERROR] Deploy failed" -ForegroundColor Red
    Add-Content -Path $logFile -Value "[$(Get-Date)] DEPLOY FAILED"
    exit 1
}
Write-Host "`nPipeline Complete at $(Get-Date)" -ForegroundColor Cyan


