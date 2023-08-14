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
