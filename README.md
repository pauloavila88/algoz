# About Algoz

WebCrawl [ZAP](https://zapimoveis.com.br/) into a Google Sheet with a dedicated User Interface:
![Teaser](Teaser.PNG)

# Oracle Cloud Server
<details>
    <summary><h2>SSH client Connection</h2></summary>

Install a SSH Client Software, for example [PortX](https://portx.online/en/) (cross platform):

<details>
    <summary><h3>Connect to File Session</h3></summary>

![PortX_FileSession-1](PortX-Walkthrough/PortX_FileSession-1.png)

![PortX_FileSession-2](PortX-Walkthrough/PortX_FileSession-2.png)

![PortX_FileSession-3](PortX-Walkthrough/PortX_FileSession-3.png)

![PortX_FileSession-4](PortX-Walkthrough/PortX_FileSession-4.png)

![PortX_FileSession-5](PortX-Walkthrough/PortX_FileSession-5.png)

![PortX_FileSession-6](PortX-Walkthrough/PortX_FileSession-6.png)

![PortX_FileSession-8](PortX-Walkthrough/PortX_FileSession-8.png)

![PortX_FileSession-9](PortX-Walkthrough/PortX_FileSession-9.png)

![PortX_FileSession-10](PortX-Walkthrough/PortX_FileSession-10.png)

![PortX_FileSession-11](PortX-Walkthrough/PortX_FileSession-11.png)

![PortX_FileSession-12](PortX-Walkthrough/PortX_FileSession-12.png)

![PortX_FileSession-13](PortX-Walkthrough/PortX_FileSession-13.png)

![PortX_FileSession-14](PortX-Walkthrough/PortX_FileSession-14.png)

![PortX_FileSession-15](PortX-Walkthrough/PortX_FileSession-15.png)
</details>

<details>
    <summary><h3>Connect to Terminal Session</h3></summary>

![PortX_FileSession-1](PortX-Walkthrough/PortX_FileSession-1.png)

![PortX_FileSession-2](PortX-Walkthrough/PortX_FileSession-2.png)

![PortX_FileSession-3](PortX-Walkthrough/PortX_FileSession-3.png)

![PortX_TerminalSession-4](PortX-Walkthrough/PortX_TerminalSession-4.png)

![PortX_TerminalSession-5](PortX-Walkthrough/PortX_TerminalSession-5.png)

![PortX_TerminalSession-6](PortX-Walkthrough/PortX_TerminalSession-6.png)

![PortX_TerminalSession-8](PortX-Walkthrough/PortX_TerminalSession-8.png)

![PortX_TerminalSession-9](PortX-Walkthrough/PortX_TerminalSession-9.png)

![PortX_TerminalSession-10](PortX-Walkthrough/PortX_TerminalSession-10.png)
</details>
</details>

<details>
    <summary><h2>Web App Deploy</h2></summary>

1. Connect to Terminal Session

    * Shell Scripts for Web App Deploy:

        Paste in Terminal Session the following command
        ```cmd
        sudo vi /home/ubuntu/Algoz/Executables/Linux/algoz.run.service.sh
        ```

    * Systemctl Service of Web App:
    
        Paste in Terminal Session the following command
        ```cmd
        sudo vi /lib/systemd/system/algoz.service
        ```

</details>

<details>
    <summary><h2>Edit Server Background Images</h2></summary>

1. Connect to File Session

2. Go to this path:
    ```path
    /home/ubuntu/Algoz/server/ui/build/static/bck-ground-imgs
    ```

    ![Change-BckImgs](PortX-Walkthrough/Change-BckImgs.PNG)

</details>

# Instalation
<details>
    <summary><h2>Windows</h2></summary>

* Go to CMD (command prompt):
  * <kbd>⊞ Win</kbd> + <kbd>R</kbd>
  * Search: `cmd` 
  * <kbd>Ctrl</kbd> + <kbd>⇧ Shift</kbd> + <kbd>↵ Enter</kbd>

* Copy-Paste the following comands: 
    ```cmd
    powershell -command "Invoke-WebRequest -Uri https://raw.githubusercontent.com/pauloavila88/algoz/dev/Executables/Windows/algoz.install.bat -OutFile ~\algoz_installer.bat"
    %UserProfile%\algoz_installer.bat
    del %UserProfile%\algoz_installer.bat

    ```

* Take a loot at `Google APIs Authorization`
</details>

<details>
    <summary><h2>Linux</h2></summary>

* Go to CMD (command prompt):
  * <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>

* Copy-Paste the following comands: 
    ```sh
    wget https://raw.githubusercontent.com/pauloavila88/algoz/dev/Executables/Linux/algoz.install.sh -O ~/algoz_installer.sh
    bash ~/algoz_installer.sh
    rm -r ~/algoz_installer.sh

    ```

* Take a loot at `Google APIs Authorization`
</details>

<details>
    <summary><h2>Google APIs Authorization</h2></summary>

* While instalation will be requested to insert Google Cloud APIs Credentials JSON file in a specific folder:

    ![Credentials Request](G-APIS_client_secret.PNG)

* Authenticate the Google Sheets/Drive that will be associated with App:
    * Get Google APIs Authorization Code:

        ![Get Authorization Code](G-APIS_Get-AuthorizationCode.PNG)

    * Set Google APIs Authorization Code:

        ![Set Authorization Code](G-APIS_Set-AuthorizationCode.PNG)


* ***Instalation Completed:***
    ![Instalation Completed](G-APIS_InstalationComplete.PNG)
</details>

# Run
<details>
    <summary><h2>Windows</h2></summary>

* Go to CMD (command prompt):
  * <kbd>⊞ Win</kbd> + <kbd>R</kbd>
  * Search: `cmd` 
  * <kbd>Ctrl</kbd> + <kbd>⇧ Shift</kbd> + <kbd>↵ Enter</kbd>

* Copy-Paste the following comands: 
    ```cmd
    %UserProfile%\Algoz\Executables\Windows\algoz.run.bat

    ```
</details>
<details>
    <summary><h2>Linux</h2></summary>

* Go to CMD (command prompt):
  * <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>

* Copy-Paste the following comands: 
    ```sh
    bash ~/Algoz/Executables/Linux/algoz.run.sh

    ```
</details>

# Uninstall
<details>
    <summary><h2>Windows</h2></summary>

* Go to CMD (command prompt):
  * <kbd>⊞ Win</kbd> + <kbd>R</kbd>
  * Search: `cmd` 
  * <kbd>Ctrl</kbd> + <kbd>⇧ Shift</kbd> + <kbd>↵ Enter</kbd>

* Copy-Paste the following comands: 
    ```cmd
    %UserProfile%\Algoz\Executables\Windows\algoz.uninstall.bat

    ```
</details>
<details>
    <summary><h2>Linux</h2></summary>

* Go to CMD (command prompt):
  * <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>

* Copy-Paste the following comands: 
    ```sh
    bash ~/Algoz/Executables/Linux/algoz.uninstall.sh

    ```
</details>
