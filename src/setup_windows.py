import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox


_triton_cache = os.path.join(
    os.environ.get("USERPROFILE", os.path.expanduser("~")),
    ".triton",
)
if os.path.isdir(_triton_cache):
    print(f"\nRemoving Triton cache at {_triton_cache}…")
    subprocess.run(f'rmdir /S /Q "{_triton_cache}"', shell=True, check=False)
else:
    print("\nNo Triton cache found to clean.\n")


start_time = time.time()


def has_nvidia_gpu():
    try:
        result = subprocess.run(
            ["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


python_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
hardware_type = "GPU" if has_nvidia_gpu() else "CPU"


def tkinter_message_box(title, message, type="info", yes_no=False):
    root = tk.Tk()
    root.withdraw()
    if yes_no:
        result = messagebox.askyesno(title, message)
    elif type == "error":
        messagebox.showerror(title, message)
        result = False
    else:
        messagebox.showinfo(title, message)
        result = True
    root.destroy()
    return result


def check_python_version_and_confirm():
    major, minor = map(int, sys.version.split()[0].split('.')[:2])
    if major == 3 and minor in (11, 12, 13):
        return tkinter_message_box(
            "Confirmation",
            f"Python version {sys.version.split()[0]} was detected, which is compatible.\n\n"
            "Click YES to proceed or NO to exit.",
            yes_no=True,
        )
    tkinter_message_box(
        "Python Version Error",
        "This program requires Python 3.11, 3.12, or 3.13.\n\nExiting the installer...",
        type="error",
    )
    return False


def manual_installation_confirmation():
    for prompt in (
        "Have you installed Git?",
        "Have you installed Git Large File Storage?",
        "Have you installed Pandoc?",
        "Have you installed Microsoft Build Tools and/or Visual Studio with the C++ workload?",
    ):
        if not tkinter_message_box(
            "Confirmation",
            f"{prompt}\n\nClick YES to confirm or NO to cancel installation.",
            yes_no=True,
        ):
            return False
    return True


if not check_python_version_and_confirm():
    sys.exit(1)

if has_nvidia_gpu():
    gpu_msg = "An NVIDIA GPU has been detected.\n\nDo you want to proceed with the installation?"
else:
    gpu_msg = (
        "No NVIDIA GPU has been detected. An NVIDIA GPU is required for this script "
        "to function properly.\n\nDo you still want to proceed with the installation?"
    )
if not tkinter_message_box("GPU Detection", gpu_msg, yes_no=True):
    sys.exit(1)

if not manual_installation_confirmation():
    sys.exit(1)


priority_libs = {
    "cp311": {
        "GPU": [
            "https://github.com/kingbri1/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu128torch2.8.0cxx11abiFALSE-cp311-cp311-win_amd64.whl",
            "https://download.pytorch.org/whl/cu128/torch-2.9.0%2Bcu128-cp311-cp311-win_amd64.whl#sha256=dc6f6c6e7d7eed20c687fc189754a6ea6bf2da9c64eff59fd6753b80ed4bca05",
            "https://download.pytorch.org/whl/cu128/torchvision-0.23.0%2Bcu128-cp311-cp311-win_amd64.whl#sha256=70b3d8bfe04438006ec880c162b0e3aaac90c48b759aa41638dd714c732b182c",
            "https://download.pytorch.org/whl/cu128/torchaudio-2.9.0%2Bcu128-cp311-cp311-win_amd64.whl#sha256=daa01250079ef024987622429f379723d306e92fad42290868041a60d4fef2e6",
            "nvidia-cuda-runtime-cu12==12.8.90",
            "nvidia-cublas-cu12==12.8.4.1",
            "nvidia-cuda-nvrtc-cu12==12.8.93",
            "nvidia-cuda-nvcc-cu12==12.8.93",
            "nvidia-cufft-cu12==11.3.3.83",
            "nvidia-cudnn-cu12==9.10.2.21",
            "nvidia-ml-py==13.580.82",
        ],
        "CPU": [],
        "COMMON": [],
    },
    "cp312": {
        "GPU": [
            "https://github.com/kingbri1/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu128torch2.8.0cxx11abiFALSE-cp312-cp312-win_amd64.whl",
            "https://download.pytorch.org/whl/cu128/torch-2.9.0%2Bcu128-cp312-cp312-win_amd64.whl#sha256=c97dc47a1f64745d439dd9471a96d216b728d528011029b4f9ae780e985529e0",
            "https://download.pytorch.org/whl/cu128/torchvision-0.24.0%2Bcu128-cp312-cp312-win_amd64.whl#sha256=1aa36ac00106e1381c38348611a1ec0eebe942570ebaf0490f026b061dfc212c",
            "https://download.pytorch.org/whl/cu128/torchaudio-2.9.0%2Bcu128-cp312-cp312-win_amd64.whl#sha256=90cd2b4d7c375c9a5c2d79117985f8f506718f494914ad9b5c5dee5581216898",
            "nvidia-cuda-runtime-cu12==12.8.90",
            "nvidia-cublas-cu12==12.8.4.1",
            "nvidia-cuda-nvrtc-cu12==12.8.93",
            "nvidia-cuda-nvcc-cu12==12.8.93",
            "nvidia-cufft-cu12==11.3.3.83",
            "nvidia-cudnn-cu12==9.10.2.21",
            "nvidia-ml-py==13.580.82",
        ],
        "CPU": [],
        "COMMON": [],
    },
    "cp313": {
        "GPU": [
            "https://github.com/kingbri1/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu128torch2.8.0cxx11abiFALSE-cp313-cp313-win_amd64.whl",
            "https://download.pytorch.org/whl/cu128/torch-2.9.0%2Bcu128-cp313-cp313-win_amd64.whl#sha256=9cba9f0fa2e1b70fffdcec1235a1bb727cbff7e7b118ba111b2b7f984b7087e2",
            "https://download.pytorch.org/whl/cu128/torchvision-0.24.0%2Bcu128-cp313-cp313-win_amd64.whl#sha256=f82cd941bc36033ebdb2974c83caa2913cc37e6567fe97cdd69f5a568ff182c8",
            "https://download.pytorch.org/whl/cu128/torchaudio-2.9.0%2Bcu128-cp313-cp313-win_amd64.whl#sha256=76df3fdb5e1194b51e69187e00d53d18bb5c2e0f3904d105e644b5c3aba5c9f4",
            "nvidia-cuda-runtime-cu12==12.8.90",
            "nvidia-cublas-cu12==12.8.4.1",
            "nvidia-cuda-nvrtc-cu12==12.8.93",
            "nvidia-cuda-nvcc-cu12==12.8.93",
            "nvidia-cufft-cu12==11.3.3.83",
            "nvidia-cudnn-cu12==9.10.2.21",
            "nvidia-ml-py==13.580.82",
        ],
        "CPU": [],
        "COMMON": [],
    },
}

libs = [
    "accelerate==1.11.0",
    "aiohttp==3.13.2",
    "aiosignal==1.4.0",
    "annotated-types==0.7.0",
    "anyio==4.11.0",
    "async-timeout==5.0.1",
    "attrs==25.4.0",
    "av==16.0.1",
    "backoff==2.2.1",
    "beautifulsoup4==4.14.2",
    "bitsandbytes==0.48.2",
    "certifi==2025.10.5",
    "cffi==2.0.0",
    "chardet==5.2.0",
    "charset-normalizer==3.4.4",
    "click==8.3.0",
    "cloudpickle==3.1.2",
    "colorama==0.4.6",
    "coloredlogs==15.0.1",
    "ctranslate2==4.6.2",
    "dataclasses-json==0.6.7",
    "datasets==4.3.0",
    "deepdiff==8.6.1",
    "Deprecated==1.2.18",
    "deprecation==2.1.0",
    "dill==0.3.8",
    "docx2txt==0.9",
    "einops==0.8.1",
    "emoji==2.15.0",
    "et-xmlfile==2.0.0",
    "extract-msg==0.55.0",
    "filetype==1.2.0",
    "filelock==3.20.0",
    "frozenlist==1.8.0",
    "fsspec[http]==2025.9.0",
    "greenlet==3.2.4",
    "h11==0.16.0",
    "h5py==3.15.1",
    "hf-xet==1.2.0",
    "httpcore==1.0.9",
    "httpx==0.28.1",
    "httpx-sse==0.4.3",
    "huggingface-hub==0.36.0",
    "humanfriendly==10.0",
    "idna==3.11",
    "importlib_metadata==8.7.0",
    "Jinja2==3.1.6",
    "joblib==1.5.2",
    "jsonpatch==1.33",
    "jsonpath-python==1.0.6",
    "jsonpointer==3.0.0",
    "langchain==0.3.27",
    "langchain-community==0.3.31",
    "langchain-core==0.3.79",
    "langchain-huggingface==0.3.1",
    "langchain-text-splitters==0.3.11",
    "langdetect==1.0.9",
    "langsmith==0.4.37",
    "llvmlite==0.45.1",
    "lxml==6.0.2",
    "Markdown==3.9",
    "markdown-it-py==4.0.0",
    "MarkupSafe==3.0.3",
    "marshmallow==3.26.1",
    "mdurl==0.1.2",
    "more-itertools==10.8.0",
    "mpmath==1.3.0",
    "multidict==6.7.0",
    "multiprocess==0.70.16",
    "mypy-extensions==1.1.0",
    "natsort==8.4.0",
    "nest-asyncio==1.6.0",
    "networkx==3.5",
    "nltk==3.9.1",
    "numba==0.62.1",
    "numpy==2.3.4",
    "olefile==0.47",
    "openpyxl==3.1.5",
    "optimum==2.0.0",
    "ordered-set==4.1.0",
    "orjson==3.11.4",
    "packaging==25.0",
    "pandas==2.3.3",
    "pillow==12.0.0",
    "platformdirs==4.5.0",
    "protobuf==6.33.0",
    "psutil==7.1.3",
    "py-cpuinfo==9.0.0",
    "pyarrow==22.0.0",
    "pycparser==2.23",
    "pydantic==2.12.3",
    "pydantic_core==2.41.4",
    "pydantic-settings==2.11.0",
    "Pygments==2.19.2",
    "pypandoc==1.15",
    "pypdf==6.1.3",
    "pyreadline3==3.5.4",
    "python-dateutil==2.9.0.post0",
    "python-docx==1.2.0",
    "python-dotenv==1.1.1",
    "python-iso639==2025.2.18",
    "python-magic==0.4.27",
    "pytz==2025.2",
    "PyYAML==6.0.3",
    "rapidfuzz==3.14.3",
    "regex==2025.10.23",
    "requests==2.32.5",
    "requests-toolbelt==1.0.0",
    "rich==14.2.0",
    "safetensors==0.6.2",
    "scikit-learn==1.7.2",
    "scipy==1.16.3",
    "sentence-transformers==5.1.2",
    "sentencepiece==0.2.1",
    "six==1.17.0",
    "sniffio==1.3.1",
    "soupsieve==2.8",
    "SQLAlchemy==2.0.44",
    "sseclient-py==1.8.0",
    "striprtf==0.0.29",
    "sympy==1.13.3",
    "tenacity==9.1.2",
    "termcolor==3.2.0",
    "threadpoolctl==3.6.0",
    "tiktoken==0.12.0",
    "tiledb==0.36.0",
    "tiledb-cloud==0.14.4",
    "tiledb-vector-search==0.16.0",
    "timm==1.0.20",
    "tokenizers==0.22.1",
    "tqdm==4.67.1",
    "transformers==4.57.4",
    "typing-inspection==0.4.2",
    "typing_extensions==4.15.0",
    "unstructured-client==0.42.3",
    "tzdata==2025.2",
    "tzlocal==5.3.1",
    "urllib3==2.5.0",
    "whisper-s2t-reborn>=1.6.0,<2",
    "wrapt==1.17.3",
    "xlrd==2.0.2",
    "xxhash==3.6.0",
    "yarl==1.22.0",
    "zipp==3.23.0",
]

full_install_libs = [
    "PySide6==6.10.0",
    "pymupdf==1.26.5",
    "unstructured==0.18.15",
]


def upgrade_pip_setuptools_wheel(max_retries=5, delay=3):
    upgrade_commands = [
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--no-cache-dir"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "--no-cache-dir"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "wheel", "--no-cache-dir"],
    ]
    for command in upgrade_commands:
        package = command[5]
        for attempt in range(max_retries):
            try:
                print(f"\nAttempt {attempt + 1} of {max_retries}: Upgrading {package}...")
                subprocess.run(command, check=True, capture_output=True, text=True, timeout=480)
                print(f"\033[92mSuccessfully upgraded {package}\033[0m")
                break
            except subprocess.CalledProcessError as e:
                print(f"Attempt {attempt + 1} failed. Error: {e.stderr.strip()}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to upgrade {package} after {max_retries} attempts.")
            except Exception as e:
                print(f"An unexpected error occurred while upgrading {package}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)


def pip_install(library, with_deps=False, max_retries=5, delay=3):
    pip_args = ["uv", "pip", "install", library]
    if not with_deps:
        pip_args.append("--no-deps")
    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1} of {max_retries}: Installing {library}"
                  f"{' with dependencies' if with_deps else ''}")
            subprocess.run(pip_args, check=True, capture_output=True, text=True, timeout=600)
            print(f"\033[92mSuccessfully installed {library}"
                  f"{' with dependencies' if with_deps else ''}\033[0m")
            return attempt + 1
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} failed. Error: {e.stderr.strip()}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to install {library} after {max_retries} attempts.")
                return 0


def install_libraries(libraries, with_deps=False):
    failed, multiple = [], []
    for library in libraries:
        attempts = pip_install(library, with_deps=with_deps)
        if attempts == 0:
            failed.append(library)
        elif attempts > 1:
            multiple.append((library, attempts))
        time.sleep(0.1)
    return failed, multiple


print("Upgrading pip, setuptools, and wheel:")
upgrade_pip_setuptools_wheel()

print("\nInstalling uv:")
subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)

print("\nInstalling priority libraries:")
try:
    hardware_specific_libs = priority_libs[python_version][hardware_type]
    common_libs = priority_libs[python_version].get("COMMON", [])
    priority_failed, priority_multiple = install_libraries(hardware_specific_libs + common_libs)
except KeyError:
    tkinter_message_box(
        "Version Error",
        f"No libraries configured for Python {python_version} with {hardware_type} configuration",
        type="error",
    )
    sys.exit(1)

print("\nInstalling other libraries:")
other_failed, other_multiple = install_libraries(libs)

print("\nInstalling libraries with dependencies:")
full_install_failed, full_install_multiple = install_libraries(full_install_libs, with_deps=True)

print("\n----- Installation Summary -----")
all_failed = priority_failed + other_failed + full_install_failed
all_multiple = priority_multiple + other_multiple + full_install_multiple

if all_failed:
    print("\033[91m\nThe following libraries failed to install:\033[0m")
    for lib in all_failed:
        print(f"\033[91m- {lib}\033[0m")

if all_multiple:
    print("\033[93m\nThe following libraries required multiple attempts to install:\033[0m")
    for lib, attempts in all_multiple:
        print(f"\033[93m- {lib} (took {attempts} attempts)\033[0m")

if not all_failed and not all_multiple:
    print("\033[92mAll libraries installed successfully on the first attempt.\033[0m")
elif not all_failed:
    print("\033[92mAll libraries were eventually installed successfully.\033[0m")

if all_failed:
    sys.exit(1)


end_time = time.time()
total_time = end_time - start_time
hours, rem = divmod(total_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"\033[92m\nTotal installation time: {int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}\033[0m")
