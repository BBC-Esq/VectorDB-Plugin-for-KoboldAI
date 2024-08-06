<div align="center">
  <h1>🚀 <a href="https://github.com/LostRuins/koboldcpp">KoboldCPP</a> Vector Database
</div>



* 🔥 Due to time constrains and ability to test, only supported on ```Windows``` systems with an ```Nvidia GPU```.

<div align="center"> <h2><u>REQUIREMENTS</h2></div>
  
1) 🐍[Python 3.11](https://www.python.org/downloads/release/python-3119/) (Pytorch is not compatible with Python 3.12 yet)
2) 📁[Git](https://git-scm.com/downloads)
3) 📁[Git Large File Storage](https://git-lfs.com/).
4) 🌐[Pandoc](https://github.com/jgm/pandoc/releases).
5) CUDA is technically "required" but the installation script installs it automatically.  You do not need to have it installed systemwide.
6) Build Tools.
   > Certain dependencies don't have pre-compiled "wheels" so you must build them with something like [Microsoft Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and/or [Visual Studio](https://visualstudio.microsoft.com/).  I recommend Visual Studio, but make sure to select the "Desktop development with C++" extension and check the four boxes on the right containing "SDK."

   <details>
     <summary>EXAMPLE ERROR ON WINDOWS</summary>
     <img src="https://github.com/BBC-Esq/ChromaDB-Plugin-for-LM-Studio/raw/main/sample_error.png">
   </details>

   <details>
     <summary>EXAMPLE SOLUTION ON WINDOWS</summary>
     <img src="https://github.com/BBC-Esq/ChromaDB-Plugin-for-LM-Studio/raw/main/build_tools.png">
   </details>

<div align="center"> <h1>INSTALLATION</h1></div>
  
### Step 1
Download the latest "release," extract its contents, navigate to the "src" folder to run the commands below.
  * NOTE: If you clone this repository you WILL NOT get the latest release.  Instead, you will development versions of this program which may or may not be stable.
### Step 2
Navigate to the ```src``` folder, open a command prompt, and create a virtual environment:
```
python -m venv .
```
### Step 3
Activate the virtual environment:
```
.\Scripts\activate
```
### Step 4
Run setup:
```
python setup_windows.py
```
   > If you need to try reinstalling for any reason run this command to uninstall everything and try again:
```pip freeze > requirements_uninstall.txt && pip uninstall -r requirements_uninstall.txt -y && del requirements_uninstall.txt```
### Step 5
```
python gui.py
```

<div align="center"> <h1>USAGE</h1></div>

### Start Kobold
* Navigate to KoboldCPP's github and download the appropriate .exe file or run ```python download_kobold.py``` from your virtual environment instead.
* Select any/all options you want and start the program, but make sure and uncheck the open browser option.  You can also check the "quiet" mode, which prevents the Kobold's command prompt window from printing everything in duplicate.


