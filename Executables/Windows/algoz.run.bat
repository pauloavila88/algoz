@REM Run ZapCrawler
call %UserProfile%\Algoz\env\python %UserProfile%\Algoz\cli.py ui --host 0.0.0.0 --port 80
@REM Inform Crawl Finish
call echo Algoz Finished !
PAUSE