@echo off
chcp 65001 >nul
cd /d "D:\项目\工作区\工作5"

set LOGFILE=_pipeline_log.txt

echo [%date% %time%] Starting pipeline... >> %LOGFILE%
echo [1/5] Global crawl...
python global_crawler.py >> %LOGFILE% 2>&1

echo [2/5] News crawl...
python news_crawler.py >> %LOGFILE% 2>&1

echo [3/5] Generate news...
python generate_news.py >> %LOGFILE% 2>&1

echo [4/5] Update homepage...
python generate_home_news.py >> %LOGFILE% 2>&1

echo [5/5] Deploy...
vercel --prod --yes >> %LOGFILE% 2>&1
echo [%date% %time%] Pipeline complete >> %LOGFILE%
