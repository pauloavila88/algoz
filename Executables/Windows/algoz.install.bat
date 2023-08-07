@REM Re-instalation Check
IF EXIST %UserProfile%\Algoz rmdir /s %UserProfile%\Algoz
@REM Create Project Folder
IF NOT EXIST %UserProfile%\Algoz mkdir %UserProfile%\Algoz
call cd %UserProfile%\Algoz
@REM Install Python if Required
python --version 3>NUL
IF errorlevel 1 goto :installpython
goto :skipinstallpython
:installpython
IF %PROCESSOR_ARCHITECTURE%==AMD64 powershell -command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe -OutFile ~\python3_11_4_installer.exe" && start /B /WAIT %UserProfile%\python3_11_4_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 TargetDir=%UserProfile%\python3_11_4 && del %UserProfile%\python3_11_4_installer.exe && goto :skipinstallpython
IF %PROCESSOR_ARCHITECTURE%==x86 powershell -command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.4/python-3.11.4.exe -OutFile ~\python3_11_4_installer.exe" && start /B /WAIT %UserProfile%\python3_11_4_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 TargetDir=%UserProfile%\python3_11_4 && del %UserProfile%\python3_11_4_installer.exe && goto :skipinstallpython
:skipinstallpython
@REM Install Git if Required
git --version 3>NUL
IF errorlevel 1 goto :installgit
goto :skipinstallgit
:installgit
IF %PROCESSOR_ARCHITECTURE%==AMD64 powershell -command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.3/Git-2.41.0.3-64-bit.exe -OutFile ~\git_installer.exe" && start /B /WAIT %UserProfile%\git_installer.exe && del %UserProfile%\git_installer.exe && goto :skipinstallgit
IF %PROCESSOR_ARCHITECTURE%==x86 powershell -command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.3/Git-2.41.0.3-32-bit.exe -OutFile ~\git_installer.exe" && start /B /WAIT %UserProfile%\git_installer.exe && del %UserProfile%\git_installer.exe && goto :skipinstallgit
:skipinstallgit
@REM Install Conda if Required
IF NOT EXIST %UserProfile%\miniconda3\condabin\conda.bat goto :installminiconda
goto :skipinstallminiconda
:installminiconda
IF %PROCESSOR_ARCHITECTURE%==AMD64 powershell -command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -OutFile %UserProfile%\miniconda_installer.exe" && start /B /WAIT %UserProfile%\miniconda_installer.exe /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /S /D=%UserProfile%\miniconda3 && del %UserProfile%\miniconda_installer.exe && goto :skipinstallgit
IF %PROCESSOR_ARCHITECTURE%==x86 powershell -command "Invoke-WebRequest -Uri https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86.exe -OutFile %UserProfile%\miniconda_installer.exe" && start /B /WAIT %UserProfile%\miniconda_installer.exe /InstallationType=JustMe /AddToPath=0 /RegisterPython=0 /S /D=%UserProfile%\miniconda3 && del %UserProfile%\miniconda_installer.exe && && goto :skipinstallgit
:skipinstallminiconda
@REM  Clone Repository
call git clone --branch dev https://github.com/pauloavila88/algoz.git .
@REM Create/Activate Conda Virtual Environment
call %UserProfile%\miniconda3\condabin\conda create --prefix ./env python=3.11 -y
call %UserProfile%\miniconda3\condabin\conda activate ./env
@REM Install required Libraries
call pip install -r requirements.txt
@REM Get Google Cloud Credentials
IF NOT EXIST %UserProfile%\Algoz\crawler\confidential mkdir %UserProfile%\Algoz\crawler\confidential
call echo [ WARNING ] - Before continuing insert the provided `client_secret.json` file in this dir: `%UserProfile%\Algoz\crawler\confidential`
PAUSE
call python %UserProfile%\Algoz\crawler\authorize_pygsheets.py
call move .\sheets.googleapis.com-python.json %UserProfile%\Algoz\crawler\confidential
@REM Inform Instalation Completed
call echo Instalation Completed!
PAUSE