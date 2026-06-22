function Write-Log {
    param([string]$msg)
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$time | $msg" | Out-File -Append $LOG_FILE
    Write-Host "$msg"
}

$LOG_FILE = "D:\项目\工作区\工作5\_ops_log.txt"
$STATE_FILE = "D:\项目\工作区\工作5\_ops_state.json"

Write-Log "===== CreatorAI 运营主控 ====="

# Phase 1: Data Collection
Write-Log "[1/4] 爬虫数据采集..."
Set-Location "D:\项目\工作区\工作5"
python global_crawler.py 2>&1 | Out-File -Append $LOG_FILE
Write-Log "  完成"

# Phase 2: Content Generation
Write-Log "[2/4] 内容生成..."
python generate_news.py 2>&1 | Out-File -Append $LOG_FILE
python generate_home_news.py 2>&1 | Out-File -Append $LOG_FILE
python _update_tools_index.py 2>&1 | Out-File -Append $LOG_FILE
Set-Location "D:\项目\工作区\工作5\tools"
python gen-detail-pages.py 2>&1 | Out-File -Append $LOG_FILE
Write-Log "  完成"

# Phase 3: Deploy
Write-Log "[3/4] 部署..."
Set-Location "D:\项目\工作区\工作5"
$dep = vercel --prod --yes 2>&1 | Out-String
if ($dep -match "Aliased|ready") { Write-Log "  部署成功" }
else { Write-Log "  部署失败" }

# Phase 4: Stats
Write-Log "[4/4] 统计..."
$articles = (Get-ChildItem articles\*.html | Measure-Object).Count
$tools = (Get-ChildItem tools\details\*.html -Recurse | Measure-Object).Count
$total = (Get-ChildItem -Recurse -Filter *.html | Measure-Object).Count
Write-Log "  文章:$articles 工具:$tools 总页:$total"

$state = @{lastRun=(Get-Date -Format "yyyy-MM-dd HH:mm:ss");articles=$articles;toolPages=$tools;totalPages=$total} | ConvertTo-Json
$state | Out-File $STATE_FILE -Encoding UTF8
Write-Log "===== 完成 ====="
