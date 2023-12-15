# About Algoz

WebCrawl [ZAP](https://zapimoveis.com.br/) into a Google Sheet with a dedicated User Interface:

<video src="readme-imgs/Algoz_Presentation.mp4" controls title="Teaser"></video>

# Oracle Cloud Server
<details open>
    <summary><h2>SSH client Connection</h2></summary>

Install a SSH Client Software, for example [PortX](https://portx.online/en/) (cross platform):

[![PortX_Download](readme-imgs/PortX-Walkthrough/PortX_Download.png)](https://portx.online/en/download/)

<details open>
    <summary><h3>Connect to File Session</h3></summary>

![PortX_FileSession-1](readme-imgs/PortX-Walkthrough/PortX_FileSession-1.png)

![PortX_FileSession-2](readme-imgs/PortX-Walkthrough/PortX_FileSession-2.png)

![PortX_FileSession-3](readme-imgs/PortX-Walkthrough/PortX_FileSession-3.png)

![PortX_FileSession-4](readme-imgs/PortX-Walkthrough/PortX_FileSession-4.png)

![PortX_FileSession-5](readme-imgs/PortX-Walkthrough/PortX_FileSession-5.png)

![PortX_FileSession-6](readme-imgs/PortX-Walkthrough/PortX_FileSession-6.png)

![PortX_FileSession-8](readme-imgs/PortX-Walkthrough/PortX_FileSession-8.png)

![PortX_FileSession-9](readme-imgs/PortX-Walkthrough/PortX_FileSession-9.png)

![PortX_FileSession-10](readme-imgs/PortX-Walkthrough/PortX_FileSession-10.png)

![PortX_FileSession-11](readme-imgs/PortX-Walkthrough/PortX_FileSession-11.png)

![PortX_FileSession-12](readme-imgs/PortX-Walkthrough/PortX_FileSession-12.png)

![PortX_FileSession-13](readme-imgs/PortX-Walkthrough/PortX_FileSession-13.png)

![PortX_FileSession-14](readme-imgs/PortX-Walkthrough/PortX_FileSession-14.png)

![PortX_FileSession-15](readme-imgs/PortX-Walkthrough/PortX_FileSession-15.png)
</details>

<details open>
    <summary><h3>Connect to Terminal Session</h3></summary>

![PortX_FileSession-1](readme-imgs/PortX-Walkthrough/PortX_FileSession-1.png)

![PortX_FileSession-2](readme-imgs/PortX-Walkthrough/PortX_FileSession-2.png)

![PortX_FileSession-3](readme-imgs/PortX-Walkthrough/PortX_FileSession-3.png)

![PortX_TerminalSession-4](readme-imgs/PortX-Walkthrough/PortX_TerminalSession-4.png)

![PortX_TerminalSession-5](readme-imgs/PortX-Walkthrough/PortX_TerminalSession-5.png)

![PortX_TerminalSession-6](readme-imgs/PortX-Walkthrough/PortX_TerminalSession-6.png)

![PortX_TerminalSession-8](readme-imgs/PortX-Walkthrough/PortX_TerminalSession-8.png)

![PortX_TerminalSession-9](readme-imgs/PortX-Walkthrough/PortX_TerminalSession-9.png)

![PortX_TerminalSession-10](readme-imgs/PortX-Walkthrough/PortX_TerminalSession-10.png)
</details>
</details>

<details open>
    <summary><h2>Web App Deploy</h2></summary>

1. Enter in [Terminal Session](https://github.com/pauloavila88/algoz/blob/main/readme-imgs/PortX-Walkthrough/PortX_TerminalSession-9.png), [more info](#connect-to-terminal-session).

    * Shell Scripts for Web App Deploy:

        * Paste in Terminal Session the following command
            ```cmd
            sudo vi /home/ubuntu/Algoz/Executables/Linux/algoz.run.service.sh

            ```
        * Exit VIM:
        
            <kbd>Esc</kbd> + <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd> + <kbd>↵ Enter</kbd>


    * Systemctl Service of Web App:

        * Edit Service:

            Paste in Terminal Session the following command
            ```cmd
            sudo vi /lib/systemd/system/algoz.service

            ```
        * Exit VIM:

            <kbd>Esc</kbd> + <kbd>:</kbd> + <kbd>w</kbd> + <kbd>q</kbd> + <kbd>↵ Enter</kbd>

        * Save Service Edition:

            Paste in Terminal Session the following command
            ```cmd
            sudo systemctl daemon-reload
            sudo systemctl restart algoz.service

            ```

        * Service Status:

            Paste in Terminal Session the following command
            ```cmd
            systemctl status algoz.service

            ```



</details>

<details open>
    <summary><h2>Edit Server Background Images</h2></summary>

1. Enter in [File Session](https://github.com/pauloavila88/algoz/blob/main/readme-imgs/PortX-Walkthrough/PortX_TerminalSession-9.png), [more info](#connect-to-file-session).

2. Go to this path:
    ```path
    /home/ubuntu/Algoz/server/ui/build/static/bck-ground-imgs
    ```

    ![Change-BckImgs](readme-imgs/PortX-Walkthrough/Change-BckImgs.PNG)

</details>

<details open>
    <summary><h2>Edit Google Cloud APIs Credentials</h2></summary>

1. Enter in [Terminal Session](https://github.com/pauloavila88/algoz/blob/main/readme-imgs/PortX-Walkthrough/PortX_TerminalSession-9.png), [more info](#connect-to-terminal-session).

2. Paste in Terminal Session the following command
    ```cmd
    bash ~/Algoz/Executables/Linux/algoz.gapi.install.sh

    ```

3. Follow the steps in [Google APIs Authorization](#google-apis-authorization)

</details>

# Instalation
<details open>
    <summary><h2>Windows</h2></summary>

* Go to CMD (command prompt):
  * <kbd>⊞ Win</kbd> + <kbd>R</kbd>
  * Search: `cmd` 
  * <kbd>Ctrl</kbd> + <kbd>⇧ Shift</kbd> + <kbd>↵ Enter</kbd>

* Copy-Paste the following comands: 
    ```cmd
    powershell -command "Invoke-WebRequest -Uri https://raw.githubusercontent.com/pauloavila88/algoz/main/Executables/Windows/algoz.install.bat -OutFile ~\algoz_installer.bat"
    %UserProfile%\algoz_installer.bat && del %UserProfile%\algoz_installer.bat

    ```

* Take a loot at [Google APIs Authorization](#google-apis-authorization)
</details>

<details open>
    <summary><h2>Linux</h2></summary>

* Go to CMD (command prompt):
  * <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>

* Copy-Paste the following comands: 
    ```sh
    wget https://raw.githubusercontent.com/pauloavila88/algoz/main/Executables/Linux/algoz.install.sh -O ~/algoz_installer.sh
    bash ~/algoz_installer.sh && rm -r ~/algoz_installer.sh

    ```

* Take a loot at [Google APIs Authorization](#google-apis-authorization)
</details>

<details open>
    <summary><h2>Google APIs Authorization</h2></summary>

* While instalation will be requested to insert Google Cloud APIs Credentials JSON file in a specific folder:

    ![Credentials Request](readme-imgs/G-APIS_client_secret.PNG)

* Authenticate the Google Sheets/Drive that will be associated with App:
    * Get Google APIs Authorization Code:

        ![Get Authorization Code](readme-imgs/G-APIS_Get-AuthorizationCode.PNG)

    * Set Google APIs Authorization Code:

        ![Set Authorization Code](readme-imgs/G-APIS_Set-AuthorizationCode.PNG)


* ***Instalation Completed:***
    ![Instalation Completed](readme-imgs/G-APIS_InstalationComplete.PNG)
</details>

# Run
<details open>
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
<details open>
    <summary><h2>Linux</h2></summary>

* Go to CMD (command prompt):
  * <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>

* Copy-Paste the following comands: 
    ```sh
    bash ~/Algoz/Executables/Linux/algoz.run.sh

    ```
</details>

# Uninstall
<details open>
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
<details open>
    <summary><h2>Linux</h2></summary>

* Go to CMD (command prompt):
  * <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>

* Copy-Paste the following comands: 
    ```sh
    bash ~/Algoz/Executables/Linux/algoz.uninstall.sh

    ```
</details>
