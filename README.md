<div align="center">
  <h1>🚀 <a href="https://github.com/LostRuins/koboldcpp">KoboldCPP</a> Vector Database
</div>



* 🔥 Supported on ```Windows``` systems with an ```NVIDIA GPU```.

<div align="center"> <h2><u>REQUIREMENTS</h2></div>

1) 🐍 Python [3.11](https://www.python.org/downloads/release/python-3119/), [3.12](https://www.python.org/downloads/release/python-3128/), or [3.13](https://www.python.org/downloads/release/python-3137/)
2) 📁 [Git](https://git-scm.com/downloads)
3) 📁 [Git Large File Storage](https://git-lfs.com/)
4) 🌐 [Pandoc](https://github.com/jgm/pandoc/releases)
5) CUDA does NOT need to be installed system-wide — the installer pulls all the CUDA 12.8 runtime wheels it needs.
6) Build Tools.
   > Some dependencies don't ship pre-compiled "wheels" so you must be able to build them with [Microsoft Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and/or [Visual Studio](https://visualstudio.microsoft.com/). Visual Studio is recommended — make sure to select the "Desktop development with C++" workload and check the four boxes on the right that contain "SDK."

<div align="center"> <h1>INSTALLATION</h1></div>

### Step 1
Download the latest "release," extract its contents, and navigate to the `src` folder to run the commands below.
   > NOTE: If you clone this repository directly you will get the in-development version of this program, which may or may not be stable.

### Step 2
Open a command prompt inside the `src` folder and create a virtual environment:
```
python -m venv .
```

### Step 3
Activate the virtual environment:
```
.\Scripts\activate
```

### Step 4
Run the setup script. It will:
1. Walk you through pre-flight checks (Python version, NVIDIA GPU, Git/Git LFS/Pandoc/Build Tools).
2. Install [`uv`](https://github.com/astral-sh/uv) as the package manager.
3. Install torch 2.9 with CUDA 12.8, flash-attention, and the matching NVIDIA wheels.
4. Install the rest of the project's pinned dependencies.
5. Overlay the project's patched versions of `pdf.py`, `instructor.py`, and `SentenceTransformer.py` into the freshly installed packages.

```
python setup_windows.py
```

   > If something goes wrong and you want to reinstall from scratch, the easiest path is to deactivate, delete the venv folder, and start again from Step 2. If you'd rather wipe just the installed packages:
```
pip freeze > requirements_uninstall.txt && pip uninstall -r requirements_uninstall.txt -y && del requirements_uninstall.txt
```

### Step 5
Launch the GUI:
```
python gui.py
```

<div align="center"> <h1>USAGE</h1></div>

### Start Kobold
* Run `python download_kobold.py` from your activated virtual environment to grab the latest KoboldCpp binary, **or** download the appropriate executable directly from [KoboldCpp's releases page](https://github.com/LostRuins/koboldcpp/releases/latest). The installer presents three options:
  * `koboldcpp.exe` — default, includes CUDA. Pick this if you have an NVIDIA GPU.
  * `koboldcpp-nocuda.exe` — Vulkan/CPU only. Pick this if you don't have an NVIDIA GPU.
  * `koboldcpp-oldpc.exe` — for older CPUs without AVX2.
* Configure your launch options as desired, but **uncheck "open browser"**. The "quiet" option is recommended to keep KoboldCpp's terminal output from duplicating.
