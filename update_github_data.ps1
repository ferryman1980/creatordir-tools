# update_github_data.ps1
# 每周自动更新 GitHub Trending 数据到 CreatorAI 网站
# 配合 Windows Task Scheduler 使用

Write-Host "=== CreatorAI GitHub Data Updater ===" -ForegroundColor Cyan
Write-Host "Started at: $(Get-Date)"

# Step 1: 运行爬虫
Write-Host "`n[Step 1] Running GitHub crawler..." -ForegroundColor Yellow
python "$PSScriptRoot\crawler.py" 2>&1 | Tee-Object -FilePath "$PSScriptRoot\crawler_last_run.log"
$crawlerExit = $LASTEXITCODE

if ($crawlerExit -ne 0) {
    Write-Host "[ERROR] Crawler failed with exit code $crawlerExit" -ForegroundColor Red
    exit 1
}

# Step 2: 注入到 resources 页
Write-Host "`n[Step 2] Injecting data into resources page..." -ForegroundColor Yellow
python "$PSScriptRoot\inject_data.py" 2>&1 | Out-File -Append "$PSScriptRoot\crawler_last_run.log"
$injectExit = $LASTEXITCODE

if ($injectExit -ne 0) {
    Write-Host "[ERROR] Injection failed with exit code $injectExit" -ForegroundColor Red
    exit 1
}

# Step 3: 产出报告
$json = Get-Content "$PSScriptRoot\github_crawl_output.json" -Raw | ConvertFrom-Json
Write-Host "`n[Step 3] Summary:" -ForegroundColor Green
Write-Host "  Total repos fetched: $($json.summary.total_fetched)"
Write-Host "  Writing: $($json.summary.classified.writing)"
Write-Host "  Image: $($json.summary.classified.image)"
Write-Host "  Video: $($json.summary.classified.video)"
Write-Host "  Errors: $($json.summary.errors)"

Write-Host "`n=== Done at $(Get-Date) ===" -ForegroundColor Cyan
