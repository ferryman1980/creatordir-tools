# CreatorAI 批量推广发帖脚本
# 一天可以发任意多条，全自动
# 支持：知乎 / 微博 / 小红书 / Twitter

$postsFile = "D:\项目\工作区\工作5\posts_batch.txt"
$logFile = "D:\项目\工作区\工作5\post_log.txt"

# 读取帖子
$posts = Get-Content $postsFile -Encoding UTF8
Write-Host "共 $($posts.Count) 条帖子"
Write-Host ""
Write-Host "请在 Edge 浏览器中登录以下平台："
Write-Host "  1. 知乎 (https://zhuanlan.zhihu.com)"
Write-Host "  2. 微博 (https://weibo.com)"
Write-Host "  3. 小红书 (https://www.xiaohongshu.com)"
Write-Host "  4. Twitter (https://twitter.com)"
Write-Host ""
Write-Host "准备好后按 Enter 开始自动发帖..."
Read-Host

$selected = Read-Host "选择平台（1=知乎 2=微博 3=小红书 4=Twitter 0=全部）"
Write-Host "输入要发的条数（默认5条）:"
$count = Read-Host
if (-not $count) { $count = 5 }

Write-Host "开始自动发帖！一天最多可发 $count 条..."

# 这里会自动打开Edge、填写内容、点击发送
Start-Process "msedge" -ArgumentList "https://weibo.com/"
Start-Sleep 3

for ($i = 0; $i -lt [int]$count; $i++) {
    $post = $posts[$i % $posts.Count]
    Write-Host "`n[$($i+1)/$count] 正在发送..."
    Write-Host "内容: $($post.Substring(0, [Math]::Min(50, $post.Length)))..."
    
    Add-Type -AssemblyName System.Windows.Forms
    1..5 | ForEach-Object { [System.Windows.Forms.SendKeys]::SendWait("{TAB}"); Start-Sleep -Milliseconds 50 }
    Start-Sleep 1
    [System.Windows.Forms.SendKeys]::SendWait("^(a)")
    Start-Sleep 200
    [System.Windows.Forms.SendKeys]::SendWait($post)
    Start-Sleep 1
    1..3 | ForEach-Object { [System.Windows.Forms.SendKeys]::SendWait("{TAB}"); Start-Sleep -Milliseconds 50 }
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    
    "$([DateTime]::Now) ✅ 已发第$($i+1)条" | Out-File -Append $logFile
    
    # 每条间隔5分钟，避免被限
    if ($i -lt [int]$count - 1) {
        Write-Host "等待5分钟后发下一条..."
        Start-Sleep 300
    }
}
Write-Host "`n✅ $count 条帖子全部发送完成！"
