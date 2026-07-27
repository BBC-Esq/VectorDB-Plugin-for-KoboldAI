import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox

if sys.platform == "win32":
    import ctypes
    _k = ctypes.windll.kernel32
    _h = _k.GetStdHandle(-11)
    _mode = ctypes.c_uint()
    if _k.GetConsoleMode(_h, ctypes.byref(_mode)):
        _k.SetConsoleMode(_h, _mode.value | 0x0004)  # enable ANSI/VT color processing in cmd.exe


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
            "triton-windows==3.5.1.post24",
            "xformers==0.0.33.post1",
            "nvidia-cuda-runtime-cu12==12.8.90",
            "nvidia-cublas-cu12==12.8.4.1",
            "nvidia-cuda-nvrtc-cu12==12.8.93",
            "nvidia-cuda-nvcc-cu12==12.8.93",
            "nvidia-cufft-cu12==11.3.3.83",
            "nvidia-cudnn-cu12==9.10.2.21",
            "nvidia-ml-py==13.610.43",
        ],
        "CPU": [],
        "COMMON": [
            "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/tesserocr-v2.9.1-tesseract-5.5.1/tesserocr-2.9.1-cp311-cp311-win_amd64.whl",
        ],
    },
    "cp312": {
        "GPU": [
            "https://github.com/kingbri1/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu128torch2.8.0cxx11abiFALSE-cp312-cp312-win_amd64.whl",
            "https://download.pytorch.org/whl/cu128/torch-2.9.0%2Bcu128-cp312-cp312-win_amd64.whl#sha256=c97dc47a1f64745d439dd9471a96d216b728d528011029b4f9ae780e985529e0",
            "https://download.pytorch.org/whl/cu128/torchvision-0.24.0%2Bcu128-cp312-cp312-win_amd64.whl#sha256=1aa36ac00106e1381c38348611a1ec0eebe942570ebaf0490f026b061dfc212c",
            "https://download.pytorch.org/whl/cu128/torchaudio-2.9.0%2Bcu128-cp312-cp312-win_amd64.whl#sha256=90cd2b4d7c375c9a5c2d79117985f8f506718f494914ad9b5c5dee5581216898",
            "triton-windows==3.5.1.post24",
            "xformers==0.0.33.post1",
            "nvidia-cuda-runtime-cu12==12.8.90",
            "nvidia-cublas-cu12==12.8.4.1",
            "nvidia-cuda-nvrtc-cu12==12.8.93",
            "nvidia-cuda-nvcc-cu12==12.8.93",
            "nvidia-cufft-cu12==11.3.3.83",
            "nvidia-cudnn-cu12==9.10.2.21",
            "nvidia-ml-py==13.610.43",
        ],
        "CPU": [],
        "COMMON": [
            "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/tesserocr-v2.9.1-tesseract-5.5.1/tesserocr-2.9.1-cp312-cp312-win_amd64.whl",
        ],
    },
    "cp313": {
        "GPU": [
            "https://github.com/kingbri1/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu128torch2.8.0cxx11abiFALSE-cp313-cp313-win_amd64.whl",
            "https://download.pytorch.org/whl/cu128/torch-2.9.0%2Bcu128-cp313-cp313-win_amd64.whl#sha256=9cba9f0fa2e1b70fffdcec1235a1bb727cbff7e7b118ba111b2b7f984b7087e2",
            "https://download.pytorch.org/whl/cu128/torchvision-0.24.0%2Bcu128-cp313-cp313-win_amd64.whl#sha256=f82cd941bc36033ebdb2974c83caa2913cc37e6567fe97cdd69f5a568ff182c8",
            "https://download.pytorch.org/whl/cu128/torchaudio-2.9.0%2Bcu128-cp313-cp313-win_amd64.whl#sha256=76df3fdb5e1194b51e69187e00d53d18bb5c2e0f3904d105e644b5c3aba5c9f4",
            "triton-windows==3.5.1.post24",
            "xformers==0.0.33.post1",
            "nvidia-cuda-runtime-cu12==12.8.90",
            "nvidia-cublas-cu12==12.8.4.1",
            "nvidia-cuda-nvrtc-cu12==12.8.93",
            "nvidia-cuda-nvcc-cu12==12.8.93",
            "nvidia-cufft-cu12==11.3.3.83",
            "nvidia-cudnn-cu12==9.10.2.21",
            "nvidia-ml-py==13.610.43",
        ],
        "CPU": [],
        "COMMON": [
            "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/tesserocr-v2.9.1-tesseract-5.5.1/tesserocr-2.9.1-cp313-cp313-win_amd64.whl",
        ],
    },
}

libs = [
    "accelerate==1.13.0",
    "aiofiles==25.1.0",
    "aiohappyeyeballs==2.6.2",
    "aiohttp==3.14.0",
    "aiosignal==1.4.0",
    "anndata==0.12.5",
    "annotated-types==0.7.0",
    "antlr4-python3-runtime==4.9.3",
    "anyio==4.13.0",
    "array-api-compat==1.14.0",
    "async-timeout==5.0.1",
    "attrs==26.1.0",
    "av==16.0.1",
    "backoff==2.2.1",
    "beautifulsoup4==4.14.3",
    "bitsandbytes==0.49.2",  # 0.48->0.49; may fix deferred Qwen-VL 4-bit crash (error 12); TEST quantized vision loading
    "cachebox==5.2.3",  # added for deepdiff 9.x (new mandatory dep)
    "certifi==2026.5.20",
    "cffi==2.0.0",
    "chardet==7.4.3",  # major 5->7, but not imported by app code; only reverse cap (requests <6) is extra-gated & inactive
    "charset-normalizer==3.4.7",
    "click==8.4.1",  # gTTS caps click<8.2 (its gtts-cli only; app uses gTTS programmatically) - already past cap; verify Google TTS
    "colorama==0.4.6",
    "colorclass==2.2.2",
    "coloredlogs==15.0.1",
    "colorlog==6.11.0",
    "compressed-rtf==1.0.7",
    "cryptography==48.0.0",  # major 46->48; only reverse cap (curl_cffi <47) is dev/test extra-gated (inactive); transitive dep
    "ctranslate2==4.6.2",  # HOLD: whisper-s2t-reborn pins ctranslate2==4.6.2 exactly (4.7.2 exists); relax the WhisperS2T-reborn fork's pin first
    "dataclasses-json==0.6.7",
    "datasets==4.8.5",
    "deepdiff==9.1.0",  # 8->9 added mandatory dep cachebox (added to libs above)
    "Deprecated==1.3.1",
    "deprecation==2.1.0",
    "dill==0.4.1",  # coupled to datasets: 0.4.1 needs a datasets that caps dill<0.4.2 (datasets 4.8.5 OK; datasets<=4.3 capped dill<0.4.1)
    "docx2txt==0.9",
    "easygui==0.98.3",
    "ebcdic==1.1.1",  # HOLD at <2: extract-msg 0.55.0 (latest, the .msg loader) requires ebcdic<2; 2.x breaks pip check / .msg handling
    "einops==0.8.2",
    "emoji==2.15.0",
    "et-xmlfile==2.0.0",
    "extract-msg==0.55.0",
    "filelock==3.29.0",
    "filetype==1.2.0",
    "flatbuffers==25.12.19",
    "frozenlist==1.8.0",
    "fsspec[http]==2026.2.0",  # capped at datasets 4.8.5 ceiling (fsspec<=2026.2.0); 2026.3.0+ blocked; coupled to datasets pin
    "greenlet==3.5.1",
    "h11==0.16.0",
    "h5py==3.16.0",
    "hf-xet==1.5.0",
    "html5lib==1.1",
    "httpcore==1.0.9",
    "httpx==0.28.1",
    "httpx-sse==0.4.3",
    "huggingface-hub==0.36.2",
    "humanfriendly==10.0",
    "idna==3.18",
    "img2pdf==0.6.3",
    "importlib_metadata==9.0.0",  # 9.0.0 unblocked by opentelemetry-api 1.42.1 dropping its importlib_metadata<8.8.0 cap (was the only blocker)
    "Jinja2==3.1.6",
    "joblib==1.5.3",
    "jsonpatch==1.33",
    "jsonpath-python==1.1.6",
    "jsonpointer==3.1.1",
    "jsonschema==4.26.0",
    "jsonschema-specifications==2025.9.1",
    "langdetect==1.0.9",
    "lark==1.3.1",
    "llvmlite==0.47.0",  # locked to numba 0.65.1 (needs llvmlite 0.47.x; numba 0.62.1 needed llvmlite<0.46)
    "lxml==6.1.1",
    "Markdown==3.10.2",
    "markdown-it-py==4.2.0",
    "MarkupSafe==3.0.3",
    "marshmallow==3.26.2",  # capped at 3.x: dataclasses-json 0.6.7 (already latest) requires marshmallow<4.0.0; 4.x blocked
    "mdurl==0.1.2",
    "more-itertools==11.1.0",
    "mpmath==1.3.0",  # HOLD: sympy (even latest 1.14.0) caps mpmath<1.4, and torch requires sympy>=1.13.3; mpmath 1.4.x unreachable until sympy raises the cap
    "msoffcrypto-tool==6.0.0",
    "multidict==6.7.1",
    "multiprocess==0.70.19",  # coupled to datasets: needs datasets cap multiprocess<0.70.20 (datasets 4.8.5 OK; datasets<=4.3 capped <0.70.17); pairs with dill 0.4.1
    "mypy-extensions==1.1.0",
    "narwhals==2.22.0",
    "natsort==8.4.0",
    "nest-asyncio==1.6.0",
    "networkx==3.6.1",
    "nltk==3.9.4",
    "numba==0.65.1",  # locked to llvmlite 0.47.x; caps numpy<2.5 (raised from 0.62.1's <2.4, which unblocks numpy 2.4.6)
    "numpy==2.3.4",  # HOLD at 2.3.4: numpy 2.4.6 possibly corrupts the heap during large TileDB builds (~1.9M chunks), causing an access violation in _create_tiledb_array (confirmed by bisection). Do not bump until that 2.4 regression is fixed upstream. numba 0.65.1 caps numpy<2.5 regardless.
    "ocrmypdf==16.13.0",
    "olefile==0.47",
    "oletools==0.60.2",
    "omegaconf==2.3.1",
    "onnxruntime==1.27.0",
    "opencv-python-headless==5.0.0.93",
    "openpyxl==3.1.5",
    "optimum==2.1.0",
    "ordered-set==4.1.0",
    "orderly-set==5.5.0",
    "orjson==3.11.9",
    "packaging==26.2",
    "pandas==3.0.3",  # major 2->3; NOT imported by app code (charts removed), but a mandatory dep of anndata/datasets/tiledb-cloud (all allow pandas 3, none cap <3) which use pandas internally - TEST manually
    "pcodedmp==1.2.6",
    "pdfminer.six==20260107",
    "pi-heif==1.3.0",
    "pikepdf==10.7.2",  # major 9->10; the gate for any ocrmypdf upgrade (used only via ocrmypdf / OCR feature) - TEST OCR
    "pillow==12.2.0",
    "platformdirs==4.10.0",
    "pluggy==1.6.0",
    "propcache==0.5.2",
    "protobuf==6.33.6",  # capped at 6.x: opentelemetry-proto (even latest 1.42.1) caps protobuf<7.0; 7.x blocked until opentelemetry raises it (googleapis 1.75.0 + onnx already allow 7)
    "psutil==7.2.2",
    "py-cpuinfo==9.0.0",
    "pyarrow==24.0.0",
    "pyclipper==1.4.0",
    "pycparser==3.0",  # major 2->3; transitive (cffi dep, not used in app code); cffi accepts any pycparser
    "pydantic==2.13.4",  # locked trio with pydantic_core (exact match) + pydantic-settings; used directly by core/config.py AppConfig - TEST config load manually
    "pydantic_core==2.46.4",  # matched to pydantic 2.13.4 (exact pin); NOT the standalone latest 2.47.0
    "pydantic-settings==2.14.1",
    "Pygments==2.20.0",
    "pypandoc==1.17",
    "pyparsing==3.3.2",
    "pypdf==6.12.2",
    "pypdfium2==5.9.0",
    "pyreadline3==3.5.6",
    "python-dateutil==2.9.0.post0",
    "python-docx==1.2.0",
    "python-dotenv==1.2.2",
    "python-iso639==2026.4.20",
    "python-magic==0.4.27",
    "python-oxmsg==0.0.2",
    "pytz==2026.2",
    "PyYAML==6.0.3",
    "rapidfuzz==3.14.5",
    "rapidocr==3.9.2",
    "red-black-tree-mod==1.22",
    "referencing==0.37.0",
    "regex==2026.5.9",
    "requests==2.34.2",
    "requests-toolbelt==1.0.0",
    "rich==15.0.0",
    "rpds-py==2026.5.1",
    "RTFDE==0.1.2.2",
    "safetensors==0.7.0",
    "scikit-learn==1.9.0",  # 1.9.0 added mandatory dep narwhals (added to libs)
    "scipy==1.17.1",
    "sentence-transformers==5.1.2",  # HOLD: replace_sourcecode.py overwrites this with patched Assets/SentenceTransformer.py (_text_length mod + debugging); any upgrade requires re-basing that patch first
    "sentencepiece==0.2.1",
    "shapely==2.1.2",
    "six==1.17.0",
    "sniffio==1.3.1",
    "soupsieve==2.8.4",
    "SQLAlchemy==2.0.50",
    "sseclient-py==1.9.0",
    "striprtf==0.0.32",
    "sympy==1.14.0",  # torch declares sympy>=1.13.3 (1.14.0 satisfies), but torch uses sympy for symbolic shapes - VERIFY torch manually; may still need 1.13.3, revert if torch.compile/dynamo breaks
    "tenacity==9.1.4",
    "termcolor==3.3.0",
    "tessdata==1.0.0",
    "tessdata.eng==1.0.0",
    "threadpoolctl==3.6.0",
    "tiktoken==0.13.0",
    "tiledb==0.36.1",
    "tiledb-cloud==0.14.4",
    "tiledb-vector-search==0.16.0",
    "timm==1.0.27",
    "tokenizers==0.22.2",  # capped at 0.22.2: ALL transformers (4.x AND 5.x) cap tokenizers<=0.23.0, and 0.23.0 stable never shipped; 0.23.1 needs a future transformers
    "tqdm==4.67.3",
    "transformers==4.57.6",
    "typing_extensions==4.15.0",
    "typing-inspection==0.4.2",
    "tzdata==2026.2",
    "tzlocal==5.3.1",
    "unstructured-client==0.44.1",
    "urllib3==2.5.0",  # HOLD: tiledb-cloud 0.14.4 (latest) caps urllib3<2.6.0, and 2.5.0 is already the highest <2.6.0 (no 2.5.x above it); 2.6/2.7 blocked until tiledb-cloud raises the cap - revisit
    "webencodings==0.5.1",
    "whisper-s2t-reborn>=1.6.0,<2",
    "win-unicode-console==0.5",
    "wrapt==2.2.1",  # major 1->2; coupled to Deprecated: 2.x needs Deprecated>=1.3.x (caps wrapt<3); Deprecated 1.2.x capped wrapt<2
    "xlrd==2.0.2",
    "xxhash==3.7.0",
    "yarl==1.24.2",
    "zipp==4.1.0",
    "zstandard==0.25.0",
]

full_install_libs = [
    "PySide6==6.11.1",
    "pymupdf==1.27.2.3",
    "unstructured==0.20.8",  # capped at 0.20.8 (highest pre-spaCy): 0.21.0+ makes spacy mandatory -> drags in ~19 pkgs (spacy/thinc/blis/cymem/srsly/typer/smart_open/etc.) + wrapt 2.x; app only does text extraction, not NLP
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
