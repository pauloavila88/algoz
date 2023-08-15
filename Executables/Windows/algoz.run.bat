@REM Run ZapCrawler
call %UserProfile%\Algoz\env\python %UserProfile%\Algoz\cli.py ui --host 127.0.0.1 --port 80
@REM Inform Crawl Finish
call echo Algoz Finished !
PAUSE