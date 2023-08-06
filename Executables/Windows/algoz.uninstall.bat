@REM Delete Project Folder
IF EXIST %UserProfile%\Algoz rmdir /s %UserProfile%\Algoz
@REM Inform Uninstall Completed
IF NOT EXIST %UserProfile%\Algoz echo Algoz Uninstaled!
PAUSE