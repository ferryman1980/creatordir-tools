@echo off
chcp 65001 >nul
cd /d "D:\项目\工作区\工作5"
python global_crawler.py
python news_crawler.py
python generate_news.py
python generate_home_news.py
vercel --prod --yes
