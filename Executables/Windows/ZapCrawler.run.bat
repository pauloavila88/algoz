@REM Go to Project Folder
call cd %UserProfile%\ZapCrawler
@REM Activate Conda Virtual Environment
call %UserProfile%\miniconda3\condabin\conda activate ./env
@REM Run ZapCrawler
call python ZapCrawler_BugFix.py
@REM Inform Crawl Finish
call echo ZapCrawl Finished !
PAUSE