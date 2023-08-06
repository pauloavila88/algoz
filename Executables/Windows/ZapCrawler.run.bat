@REM Go to Project Folder
call cd %UserProfile%\Algoz
@REM Activate Conda Virtual Environment
call %UserProfile%\miniconda3\condabin\conda activate ./env
@REM Run ZapCrawler
call python cli.py ui
@REM Inform Crawl Finish
call echo Algoz Finished !
PAUSE