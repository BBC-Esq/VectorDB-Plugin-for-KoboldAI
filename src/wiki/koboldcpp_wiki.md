# The KoboldCpp FAQ and Knowledgebase
[**NEED A GGUF MODEL? CLICK HERE AND READ!**](https://github.com/LostRuins/koboldcpp/wiki#what-models-does-koboldcpp-support-what-architectures-are-supported)  
[**Completely Lost? Click here!**](https://github.com/LostRuins/koboldcpp/wiki#quick-start)  
[**Check out our step-by-step guides here!**](https://github.com/LostRuins/koboldcpp/wiki#step-by-step-guides)  
Welcome to the KoboldCpp knowledgebase! If you have issues with KoboldCpp, please check if your question is answered here or in one of the link reference first. If not, you can open an issue on Github, or contact us on our [KoboldAI Discord Server](https://koboldai.org/discord). You can find me there as Concedo, or just ask around (we have plenty of people around to help).

## Introduction
### **What is KoboldCpp?**  
KoboldCpp is an easy-to-use AI text-generation software for GGML and GGUF models, inspired by the original **KoboldAI**. It's a single self-contained distributable that builds off **llama.cpp** and adds many additional powerful features, with multiple compatibility API endpoints, Stable Diffusion image generation, speech-to-text, voice recognition, image recognition, as well as a fancy UI with persistent stories, editing tools, save formats, memory, world info, author's note, characters, scenarios and everything in a single file.

## Getting an AI model file
### **What models does KoboldCpp support? What architectures are supported?**  
Generally, **all up-to-date GGUF models are supported**. Note that there are **thousands** of models across hundreds of architectures, text-generation, image-generation, text-to-speech, voice-recognition, so it can be tricky to know what works with KoboldCpp. This list recommends some easy options but in general, if it's GGUF, it should work.
- The best place to get GGUF text models is **Huggingface**. For image models, **CivitAI** has a good selection. Here are some to get you started. **You can also get them by clicking 'Help' in the GUI launcher and browsing the Newbie Templates**
  - General Text Generation: [Qwen3-VL-8B](https://huggingface.co/unsloth/Qwen3-VL-8B-Instruct-GGUF/resolve/main/Qwen3-VL-8B-Instruct-Q4_K_S.gguf) **(Most Recommended, best all rounder model)**
    - Optionally, add [Qwen3-VL-8B MMproj file](https://huggingface.co/unsloth/Qwen3-VL-8B-Instruct-GGUF/resolve/main/mmproj-BF16.gguf) if you also want Image Recognition vision capabilities.
  - Creative Writing and Roleplay: [L3-8B-Stheno-v3.2](https://huggingface.co/bartowski/L3-8B-Stheno-v3.2-GGUF/resolve/main/L3-8B-Stheno-v3.2-Q4_K_S.gguf)
  - If you just want a small and fast model to test (or for mobile users and old PCs), you can use [Gemma3-4B](https://huggingface.co/ggml-org/gemma-3-4b-it-GGUF/resolve/main/gemma-3-4b-it-Q4_K_M.gguf)
  - Image Generation: [PicX Real](https://huggingface.co/koboldcpp/imgmodel/resolve/main/picx_real_q8_0.gguf)
  - Speech Recognition: [Whisper models for Speech-To-Text](https://huggingface.co/koboldcpp/whisper/tree/main)
  - Text-To-Speech: [TTS models for Narration](https://huggingface.co/koboldcpp/tts/tree/main)
  - This is just a list for noobs to get started! There are hundreds more GGUFs out there!
  - [**All-in-one single-click Starter Pack!**](https://huggingface.co/koboldcpp/kcppt/resolve/main/starter-pack.kcppt): If you're too lazy and just want a template to try out **everything** in it, this comes with Gemma3-4B (text & vision), PicXReal (image gen), arctic-snowflake-m (embedding model), Kokoro (text-to-speech), and Whisper-Base (voice recognition). Right click and save the `.kcppt` file to your PC and open it in KoboldCpp. Recommended for 12gb GPUs and up. Feel free to edit and remove excess components.  
  - [**All-in-one Starter Pack V2**](https://huggingface.co/koboldcpp/kcppt/resolve/main/starter-pack-v2.kcppt): An updated version of the starter pack with different models and a newer image generation model. Requires 8GB VRAM and up. Thanks to @basxto for the model suggestions!
  - [more newbie templates](https://huggingface.co/koboldcpp/newbie-templates) - Contains premade KoboldCpp quick launch templates curated for newbies.  
  - [more popular templates](https://huggingface.co/koboldcpp/popular-templates) - Contains premade KoboldCpp quick launch templates curated for popularity.  
  - [more templates](https://huggingface.co/koboldcpp/kcppt/tree/main)

Other formats such as safetensors and pytorch.bin models are not natively supported, and must be converted to GGUF/GGML! (see below)  

### **Where can I find or download GGUF and GGML models for KoboldCpp?**  
- GGML models can be found uploaded on [Huggingface](https://huggingface.co/models), simply by searching for `GGML` or `GGUF`. They should be a file in `.bin` or `.gguf` format
- A large selection of high quality models can also be found on [Bartowski's Huggingface Repo](https://huggingface.co/bartowski), look for GGUF. 
- Lastly, you can also convert the models yourself, using the [appropriate quantization and conversion tools](https://kcpptools.concedo.workers.dev).
- A repository of popular supported models and .kcppt templates can be found at our [KoboldCpp huggingface repo](https://huggingface.co/koboldcpp)

### **What's the difference between GGUF and GGML formats**  
GGUF is a newer format designed to (hopefully) be more future proof. As of Oct 2023, it is the latest and recommended format for LLAMA and LLAMA2 models. For other architectures, the old format is still used. KoboldCpp remains compatible with any version of both formats.

### **What are the differences between the different files for each model? Do I need them all? Which Quantization? F16? Q4_0? Q5_1?**  
No, you don't need all the files, just a single one. Each GGML model is just a single .bin or .gguf file. The multiple files represent different compression levels of each model, from worst to best (least to most bits-per-weight) in ascending order. A Q4_0 of a specific model will be smaller than a Q5_1, but of slightly lower quality. [Read more here](https://www.reddit.com/r/LocalLLaMA/comments/13l0j7m/a_comparative_look_at_ggml_quantization_and/).
- In general the quality (from worst to best) and filesize (from smallest to biggest) follows this order: 
- Q2K, Q3_K_S, Q3_K_M, Q3_K_L, Q4_0, Q4_K_S, Q4_1, Q4_K_M, Q5_0, Q5_1, Q5_K_S, Q5_K_M, Q6_K, Q8_0, F16

## Quick Start
### **How do I get started with KoboldCpp? What do I need? How do I compile KoboldCpp from source code?**  
This depends on the platform you are using, and what capabilities you want to use. First, **obtain and download a GGUF model file as stated above**. Next: 
- Windows, Using Prebuilt Executable (Easiest):  
  - [Download the latest koboldcpp.exe release here](https://github.com/LostRuins/koboldcpp/releases/latest)
  - Double click KoboldCPP.exe and select model OR run "KoboldCPP.exe --help" in CMD prompt to get command line arguments for more control.
  - Generally you don't have to change much besides the `Presets` and `GPU Layers`. Run with Cuda or Vulkan for GPU acceleration.
  - Select your GGUF or GGML model [you downloaded earlier](https://github.com/LostRuins/koboldcpp/wiki#getting-an-ai-model-file), and connect to the displayed URL once it finishes loading. If you need help finding a model, click the red "Get Help" button for some easy options.

- Linux, Precompiled Binary or AutoInstall script (Easy):  
  - On Linux, we provide a `koboldcpp-linux-x64` PyInstaller prebuilt binary on the **[releases](https://github.com/LostRuins/koboldcpp/releases/latest)** page for modern systems. Simply download and run the binary (You may have to `chmod +x` it first).  
  - Alternatively, you can also install koboldcpp to the current directory by running the following terminal command: `curl -fLo koboldcpp https://github.com/LostRuins/koboldcpp/releases/latest/download/koboldcpp-linux-x64 && chmod +x koboldcpp`. 
  - When you can't use the precompiled binary directly, we provide an automated build script which uses conda to obtain all dependencies, and generates (from source) a ready-to-use a pyinstaller binary for linux users. Simply execute the build script with `./koboldcpp.sh dist` and run the generated binary.

- MacOS (Precompiled Binary)
  - PyInstaller binaries for Modern ARM64 MacOS (M1, M2, M3) are now available! **[Simply download the MacOS binary](https://github.com/LostRuins/koboldcpp/releases/latest)**
  - In a MacOS terminal window, set the file to executable with `chmod +x koboldcpp-mac-arm64` and run it with `./koboldcpp-mac-arm64`.
  - In newer MacOS you may also have to whitelist it in security settings if it's blocked. [Here's a video guide](https://youtube.com/watch?v=NOW5dyA_JgY).

- MacOS and Linux (Self Compile):  
  - To compile your binaries from source, clone the repo with `git clone https://github.com/LostRuins/koboldcpp.git`
  - A makefile is provided, simply run `make`.
  - Optional Vulkan: Link your own install of Vulkan SDK manually with `make LLAMA_VULKAN=1`
  - You can attempt a CUDA build with `make LLAMA_CUBLAS=1` or using the provided CMake file, you will need CUDA toolkit installed.
  - For a full featured build, do `make LLAMA_VULKAN=1 LLAMA_CUBLAS=1`
  - After all binaries are built, you can run the python script with the command `koboldcpp.py [ggml_model.gguf] [port]`
- MacOS Notes:
  - You may want to compile with `make LLAMA_METAL=1`, and enable it afterwards by passing --gpulayers (number)
  
- Windows, Compiling from Source Code:  
  - You're encouraged to use the .exe released, but if you want to compile your binaries from source at Windows, the easiest way is:
    - Get the latest release of w64devkit (https://github.com/skeeto/w64devkit). Be sure to use the "vanilla one", not i686 or other different stuff. If you try they will conflit with the precompiled libs!
    - Clone the repo with `git clone https://github.com/LostRuins/koboldcpp.git`
    - Make sure you are using the w64devkit integrated terminal, then run `make` at the KoboldCpp source folder. This will create the .dll files.
    - If you want to generate the .exe file, make sure you have the python module PyInstaller installed with pip (`pip install PyInstaller`). Then run the script `make_pyinstaller.bat`
    - The koboldcpp.exe file will be at your dist folder.
  - **Building with CUDA**: Visual Studio, CMake and CUDA Toolkit is required. Clone the repo, then open the CMake file and compile it in Visual Studio. Copy the `koboldcpp_cublas.dll` generated into the same directory as the `koboldcpp.py` file. If you are bundling executables, you may need to include CUDA dynamic libraries (such as `cublasLt64_11.dll` and `cublas64_11.dll`) in order for the executable to work correctly on a different PC.
  - **Replacing Libraries (Not Recommended)**: If you wish to use your own version of the additional Windows libraries (Vulkan), you can do it with:
    - Move the respectives .lib files to the /lib folder of your project, overwriting the older files.
    - Also, replace the existing versions of the corresponding .dll files located in the project directory root.
    - Make the KoboldCpp project using the instructions above.
  
- Android: 
  - Please refer to the "Installing KoboldCpp on Android via Termux" guide below. For easy setup, simply install Termux and run the `android_install.sh` script, which will guide you step by step.
  
- WSL:
  - You could, but why would you want to? The basic `make` should work without issues with build essentials. Finding appropriate libraries for GPU acceleration may be difficult.
 
## KoboldCpp General Usage and Troubleshooting  
### **I don't want to use the GUI launcher. How to use the command line terminal with extra parameters to launch koboldcpp?**  
Here are some easy ways to start koboldcpp from the command line. Pick one that suits you best.  
- Windows: Go to Start > Run (or WinKey+R) and input the full path of your koboldcpp.exe followed by the launch flags. e.g. `C:\mystuff\koboldcpp.exe --usecuda --gpulayers 10`. Alternatively, you can also create a desktop shortcut to the koboldcpp.exe file, and set the desired values in the `Properties > Target` box. Lastly, you can also start command prompt in your koboldcpp.exe directory (with `cmd`), and pass the desired flags to it from the terminal window.  
- Linux/OSX: Navigate to the koboldcpp directory, and build koboldcpp with `make` (as described in 'How do I compile KoboldCpp'). Then run the command `python3 koboldcpp.py --model (path to your model)`, plus whatever flags you need e.g. `--usevulkan`

### **How do I see the available commands and how to use them?**  
You can launch KoboldCpp from the command line with the `--help` parameter to view the available command list. See the section on "How to use the command line terminal"

### **How much RAM/VRAM do I need to run Koboldcpp? What about my GPU?**  
The amount of RAM required depends on multiple factors such as the context size, quantization type, and parameter count of the model. In general, assuming a 2048 context with a Q4_0 quantization:
- LLAMA 3B needs at least 4GB RAM
- LLAMA 7B needs at least 8GB RAM
- LLAMA 13B needs at least 16GB RAM
- LLAMA 30B needs at least 32GB RAM
- LLAMA 65B needs at least 64GB RAM  

Offloading layers to the GPU VRAM can help reduce RAM requirements, while a larger context size or larger quantization can increase RAM requirements.
For number of layers to offload, see the section on GPU layer offloading.

### **What does GPU layer offloading do? How many layers can I offload?**  
Just running with `--usecuda` or `--usevulkan` will perform prompt processing on the GPU, but combined with GPU offloading via `--gpulayers` takes it one step further by offloading individual layers to run on the GPU, for per-token inference as well, greatly speeding up inference. The number of layers you can offload to GPU vram depends on many factors, some of which are already mentioned above, and can also change depending on which backend (CUDA/CL/Metal) that you are using. For reference, at 2048 context in Q4_0, a 6GB Nvidia RTX 2060 can comfortably offload:
- 32 layers with LLAMA 7B
- 18 layers with LLAMA 13B
- 8 layers with LLAMA 30B
You can specify `--gpulayers -1` and allow KoboldCpp to guess how many layers it should offload, though this is often not the most accurate, and doesn't work accurately for multi-gpu setups. You are recommended to determine the optimal layer fit through trial and error for best results. In new versions, the autofit will be triggered with `-1` layers which automatically handles all layer estimations.

### **What does `--autofit` do?**  
Using `--autofit` makes KoboldCpp automatically try to give the a good fit for a specified text model on your GPU. It will set the appropriate layers, MoE tensor overrides and tensor splits to try and use an optimal amount of memory. It's also enabled if you set `--gpulayers` to `-1` and do not set any incompatible flags (Autofit is not compatible with manual tensor overrides, tensor splits or `--moecpu`).

### **How can I run KoboldCpp on my android phone (Termux)?**  
Inference directly on a mobile device is probably not optimal as it's likely to be slow and memory limited. Consider running it remotely instead, as described in the "Running remotely over network" section. If you still want to proceed, the best way on Android is to build and run KoboldCpp within Termux. Also, check out the guide below "Installing KoboldCpp on Android via Termux".

- [Install and run Termux from F-Droid](https://f-droid.org/en/packages/com.termux/)
- Enter the command `termux-change-repo` and choose `Mirror by BFSU`
- Install dependencies with `pkg install wget git python` (plus any other missing packages)
- Install dependencies `apt install openssl` (if needed)
- Clone the repo `git clone https://github.com/LostRuins/koboldcpp.git`
- Navigate to the koboldcpp folder `cd koboldcpp`
- Build the project `make`
- Grab a small GGUF model, such as `wget https://huggingface.co/TheBloke/phi-2-GGUF/resolve/main/phi-2.Q2_K.gguf`
- Start the python server `python koboldcpp.py --model phi-2.Q2_K.gguf`
- Connect to `http://localhost:5001` on your mobile browser
- If you encounter any errors, make sure your packages are up-to-date with `pkg up`

### **What are my options to make it go FASTER? (CUDA/Metal/Accelerate/ROCm/Vulkan)**  
By default, launching with no parameters set will attempt to pick the best backend available, but this can be optimized.  
Here are some options to Make It Fast:  
- CUDA: Only for Nvidia GPUs. Launch with `--usecuda` to use this. Prepackaged for windows .exe users, but requires installing CUDA toolkit for all other platforms (see compiling with CUDA from source, OSX/Mac section). Can be combined together with `--gpulayers` for even faster GPU offloading.
- Metal: Only for Apple Silicon users (eg. Mac M2), GPU acceleration with Metal. Can be combined together with `--gpulayers`. See compiling with Metal from source.
- Accelerate: Only for mac users, CPU only. Automatically supported if you build on a mac. If BLAS is slowing you down, try `--noblas`.
- ROCm: Not directly supported, but see [YellowRoseCx/koboldcpp-rocm](https://github.com/YellowRoseCx/koboldcpp-rocm) fork via HIPBLAS for AMD devices only. Alternatively, try the Vulkan option.
- Vulkan: For most users, you can get very decent speeds by selecting the **Vulkan** option instead, which supports both Nvidia and AMD GPUs. Vulkan is a newer option that provides a good balance of speed and utility compared to the OpenCL backend.
- CLblast (Removed): CLBlast has been deprecated and removed. CLBlast is considered outdated and no longer recommended.
- OpenBLAS (Removed): OpenBLAS was a BLAS acceleration library formerly used for prompt processing on the CPU. It has been deprecated and is no longer available. Instead, just use `--usecpu` to automatically launch in CPU mode, everything is handled automatically.

### **How do I run KoboldCpp on a different device than my PC over the network? Remote play?**  
There are multiple ways to use KoboldCpp on a different device over the network.  
1. If on a different LAN (Windows or Linux) - Use a Cloudflared tunnel. After launching KoboldCpp with default port 5001, run the `Remote-Link.cmd` included in the repo, which will create a cloudflared tunnel. Then just open your mobile browser to the displayed trycloudflare URL. In newer versions of KoboldCpp, there's a helper command to do all that for you, simply use `--remotetunnel` and it will proceed to setup a tunnel with a usable URL.
2. If on a different LAN (Any, Public) - Use the AI Horde. KoboldCpp comes with an embedded AI Horde worker (see section on Horde). You can start a worker, and then connect to it via the web version of Kobold Lite at https://lite.koboldai.net
3. If on same LAN - If you're on the same Wifi network, you can probably connect over LAN by navigating to the local IP of the host device (the PC running koboldcpp). For example, http://192.168.1.85:5001 or similar, check your LAN IP address. If that fails, try using the `--host` option with your LAN IP. If you setup port forwarding to a public IP, then it will be accessible over the internet as well.
4. There is a [Colab Notebook](https://github.com/LostRuins/koboldcpp/blob/concedo/colab.ipynb) included here. It should work out of the box, and is powered by Google Cloud GPUs. use it at your own risk.

### **What port does Koboldcpp use? How do I change the port that koboldcpp uses?**  
By default KoboldCpp uses port 5001, but this can be changed with the `--port` launch parameter. You would connect your browser locally to that port for the UI or API, in the format http://localhost:port (e.g. http://localhost:5001). If the connection does not work, check your wifi or firewall settings, or try using a different port.

### **How do I use streaming? What are the types of streaming supported?**  
KoboldCpp now supports a variety of streaming options. Kobold Lite UI supports streaming out of the box, which can be toggled in Kobold Lite settings.  _Note: the `--stream` parameter is now deprecated and should not be used._ 
- Polled-Streaming (Recommended): This is the default used by the Kobold Lite UI. It polls for updates on the `/api/extra/generate/check` endpoint every second. It is relatively fast and simple to use, although some may find it a bit "chunky" as it does not update instantaneously every single token.
- Pseudo-Streaming: This is an older method that is no longer recommended, due to performance overheads. To use it with Kobold Lite, enable streaming, then append a `&streamamount=x` at the end of the Lite URL where X is the number of tokens per request. Negative performance impact.
- SSE (True Streaming): This type of streaming is only supported by a few third party clients such as SillyTavern and Agnaistic, available only via the API. It provides instantaneous per-token updates, but requires a persistent connection and some special handling on the client side with SSE support. This mode is not used in Lite or the main KoboldAI client. It uses a different API endpoint, so configure this from your third party client according to their provided instructions.

### **How to choose how many threads to use? What about `--blasthreads`?**  
Set number of threads to be used for inference. The optimal number of threads to use is usually approximately equal to the number of physical CPU cores your system has. So a i7-9750H with 12 logical processors and 6 physical cores would do best with either 5 or 6 threads. Setting `--blasthreads` will use a different number of threads during BLAS if specified. Otherwise, has the same value as `--threads`. Tf you leave the parameter blank, it will be set to a good default also based on slightly less than your CPU count. If running with full GPU offload, then setting 1 thread may be enough.  
_Note: The flag `psutil_set_threads` has been deprecated and should not be used._

### **What is BLAS? What is blasbatchsize? How does it affect me?**  
BLAS (Basic Linear Algebra Subprograms) is what is used to perform large matrix to matrix multiplication, which is needed for accelerated prompt processing. There are multiple backends this can be done with, such as CUDA(Nvidia), or Vulkan(AMD and Nvidia). The `--blasbatchsize` indicates the number of tokens in a single batch to be processed at once. Usually, you do not need to change this value (defaults to 512 for llama and 256 otherwise), but you can try lower values such as 128 for devices with less memory, at the expense of lower prompt processing speeds. BLAS is not used during stochastic sampling (generation). Setting it to `-1` will disable batching, processing all tokens one at a time.

### **What is Mirostat? How do I use it?**  
Mirostat is a newer sampling method that adjusts the value of k in top-k decoding to keep the perplexity within a specific range. In this way, it avoids two common problems in text generation: the boredom trap, in which the generated text becomes repetitive, and the perplexity trap, in which the generated text loses coherence. It can be used as a replacement for more classic samplers like Top-P, if enabled it replaces your samplers with mirostat. Takes 3 parameters = [type(0/1/2), tau(5.0), eta(0.1)]. Mirostat can now also be set on a per-generation basis within the API.  
_Note: the `--usemirostat` launch parameter has been deprecated and should not be used._

### **What is Grammar Sampling**  
Grammar Sampling allows you to specify a GBNF grammar format to be used when generating, constraining the AI to a specific syntax in the response. For more info, check out [this link](https://github.com/ggerganov/llama.cpp/pull/1773).

### **What is `--nomodel`**  
This parameter launches the KoboldAI Lite UI alone without loading a model. The Kobold Lite UI can be used to connect to an external KoboldCpp instance, or other AI services such as the AI Horde.

### **What is `--config`? What are .kcpps files?**  
`.kcpps` files are configuration files that store your KoboldCpp launcher preferences and settings. You can save and load them into the GUI, or run them directly with the `--config` flag. You can export configs from command line with `--exportconfig` flag.

### **What are .kcppt files?**  
`.kcppt` files are configuration *templates* that store KoboldCpp launcher preferences and settings. You can save and load them into the GUI, or run them directly with the `--config` flag. The difference between this and .kcpps files is that .kcppt files are intended to be shared, thus they will not include device specific settings like the GPU to use, instead those are decided by the other user. You can export templates from command line with `--exporttemplate` flag.

### **Can I remove the BOS token?**  
By default, the begin-of-stream (BOS) token is appended to all inputs before generation. Some models (e.g. Qwen) may not like this so much. If you want to prevent the BOS token from being automatically added, launch with the `--nobostoken` flag.

### **What is `--multiuser` mode?**  
Multiuser mode allows multiple people to share a single KoboldCpp instance, connecting different devices to a common endpoint (over LAN, a port forwarded public IP, or through an internet tunnel). It's enabled by default. It automatically handles queuing requests and dispatching them to the correct clients. An optional extra parameter number allows you to specify the max simultaneous users. Set to `--multiuser 0` to disable this.

### **What is `--foreground`**  
This parameter is intended for window users. It sends the console terminal to the foreground every time a new prompt is generated, to avoid some idling slowdown issues.

### **What is `--quiet`**  
This parameter prevents prompt and generation output information from being displayed on the terminal. Useful for added privacy.

### **What is `--unpack`**  
Launching with this flag allows the internal contents of the KoboldCpp pyinstaller binary to be unpacked into a directory. This is useful for modifying or replacing files, and KoboldCpp can then be launched by running `python3 koboldcpp.py`

### **What is `--showgui`**  
Adding the `--showgui` flag allows the GUI to be shown even with command line flags are used. Instead, command line flags will get imported into the GUI itself, allowing them to be modified. This also works with .kcpps config files, all settings are loaded into the existing GUI input fields. This can be used to load a common configuration while still allowing the user to edit one or two customized settings before starting the server.

### **What is `--preloadstory`**  
You can pass a Kobold Lite JSON file with this parameter when launching the KoboldCpp server. The save file will automatically be served and loaded to any new Kobold Lite clients who connect to your server, effectively giving you a preconfigured story that you can easily share over the network.

### **Can I save stories to the koboldcpp server remotely? (Server Side Saves)**  
Server-Sided (networked) save slots can be used. You can specify a database file when launching KoboldCpp using `--savedatafile`. Then, you will be able to save and load persistent stories over the network to that KoboldCpp server, and access it from any other browser or device connected to it over the network. This can also be combined with `--password` to require an API key to save/load the stories.

### **What is `--chatcompletionsadapter`**  
You can pass an optional ChatCompletions Adapter JSON file to force custom instruct tags when launching the KoboldCpp server. This is useful when using the OpenAI compatible Chat Completions API with third party clients. The adapter file takes the following JSON format, all fields are optional.

```
{
"max_length":512,
"system_start":"str",
"system_end":"str",
"user_start":"str",
"user_end":"str",
"assistant_start":"str",
"assistant_end":"str",
"tools_start":"str",
"tools_end":"str",
"add_sd_negative_prompt":"str",
"add_sd_prompt":"str",
}
```
KoboldCpp comes with a few built in adapters included for convenience. The `AutoGuess.json` adapter will try to heuristically infer the correct instruct template to be used for the chat completions endpoint, based on the detected Jinja template from the model.

### **What is `--jinja` and `--jinjatools`**  
Some models require very specific instruct tags and instruct templates to work correctly. Using the `--jinja` flag will enable this template to be used directly with a jinja parser in Chat Completions mode. If `--jinjatools` is provided, the template will be used for tool calls as well, replacing KoboldCpp's universal tool calling.

### **What is `--smartcache`**  
This is a feature that allows intelligent context switching by saving KV cache snapshots to RAM. When used, it will record "save states" of your conversation session when you change to a different one (or for RNN models, at some intervals). Then when it detects an old snapshot can be reused, it will load that snapshot, saving effort reprocessing the entire prompt again. Uses more memory based on the number of cache slots used, which can be defined by `--smartcache X` for X slots.

### **How to use `--onready`**  
This is an advanced parameter intended for script or command line usage. You can pass a terminal command (e.g. start a python script) to be executed after Koboldcpp has finished loading. This runs as a subprocess, and can be useful for starting cloudflare tunnels, displaying URLs etc.

### **Phrase Banning (Anti-Slop): How do I stop my model from generating (specific symbol), e.g. `[` or specific phrases**  
Sometimes, you want to prevent a model from using a specific symbol, e.g. the left square bracket `[` like Kobold United does. Adding `[` to the Phrase/Token Ban field in Kobold Lite will prevent it from generating this specific substring. You can now provide a specified list of words or phrases prevented from being generated, by backtracking and regenerating when they appear. 
- Logit Bias: For advanced users. Setting `logit_bias` over the API allows you to prioritize or reduce the chance of specific token IDs appearing in the AI output, without banning it completely.

### **What is Smart Context?**  
Smart Context is enabled via the command `--smartcontext`. In short, this reserves a portion of total context space (about 50%) to use as a 'spare buffer', permitting you to do prompt processing much less frequently (context reuse), at the cost of a reduced max context.  
How it works: when enabled, Smart Context can trigger once you approach max context, *and* then send two consecutive prompts with enough similarity (e.g. the second prompt has more than half the tokens matching the first prompt). Imagine the max context size is 2048. When triggered, KoboldCpp will truncate away the first half of the existing context (top 1024 tokens), and 'shift up' the remaining half (bottom 1024 tokens) to become the start of the new context window. Then when new text is generated subsequently, it is trimmed to that position and appended to the bottom. The new prompt need not be recalculated as there will be free space (1024 tokens worth) to insert the new text while preserving existing tokens. This continues until all the free space is exhausted, and then the process repeats anew.

> Analogy: Imagine there is a Bus with a capacity for 50 seats. At each stop, 5 people want to get on. Now imagine that once the bus is full, the driver has to kick out the earliest 5 passengers off the bus, before the next 5 people can get on the bus. Assume kicking any number of people off the bus is very difficult and disruptive because they are slow and stubborn.
> So for the first 10 stops, everything is fine. But at stop 11, the bus is full, and then every stop after becomes slow due to kicking 5 off before 5 new can board.
> What if, instead of kicking 5 off when the bus is full, the driver kicks off half the bus (25 people)? That takes the same amount of time as kicking 5 people off. But then for the next 5 stops after that, people can board the bus in peace as there will be free space. This continues until the bus is full again, and then half the people get kicked out.
> That's smartcontext

### **What is ContextShift?**  
Context Shifting is a better version of Smart Context that only works for GGUF models. This feature utilizes KV cache shifting to automatically remove old tokens from context and add new ones without requiring any reprocessing. So long as memory is not changed or edited and you don't use world info, you should be able to avoid almost all reprocessing between consecutive generations even at max context. This does not consume any additional context space, making it superior to SmartContext. Context Shifting is enabled by default, and will override `smartcontext` if both are enabled. Your outputs may be different with shifting enabled, but both seem equally coherent. To disable Context Shifting, use the flag `--noshift`. 

### **What is FastForwarding?**  
Fast forwarding is enabled by default, and allows the AI to skip reused tokens in the context that have already been processed in the previous turn. To disable Fast Forwarding, use the flag `--nofastforward`. 
 
### **How do I make the AI handle longer context than 2048? Also, the Kobold Lite max context slider only goes up to 2048 / My koboldcpp crashed while processing a long prompt / How do I increase context size?**  
First, you need to allocate extra RAM for buffers when using extended context above 2048. Set `--contextsize` to the desired max context size you want to use, e.g. `--contextsize 4096` for a 4K context, or `--contextsize 8192` for 8K context limit. If you're using a GGUF model, your RoPE scaling should be automatically configured correctly. KoboldCpp supports a contextsize up to 16k for GGML models and 32k for GGUF models.  
You may also need to change the "Max Tokens" value in Kobold Lite beyond the default slider limit of 2048. To do so, click and edit the number above the Max Tokens slider, it is an editable text inputbox that can be overriden to a higher value beyond the slider range.

### **What is RoPE config? What is NTK-Aware scaling?  What values to use for RoPE config?**  
RoPE scaling (via `--ropeconfig`) is a novel technique capable of extending the useful context of existing models without finetuning. It can be used to stretch a model's context limit by over 4x (e.g. 2048 to 8192) with minor to moderate quality degradation.  
The default is `--ropeconfig 1.0 10000`, 1x unscaled. There are 2 scaling modes, which can be combined if desired.  
- Linear Scaling, set with the 'frequency scale`, the first parameter of `--ropeconfig`, e.g. for 2x linear scale, use `--ropeconfig 0.5 10000`, for 4x, use `--ropeconfig 0.25 10000`.
- NTK-Aware Scaling, set with 'frequency base`, the second parameter of `--ropeconfig`, e.g. `--ropeconfig 1.0 32000` for approx 2x scale, or `--ropeconfig 1.0 82000` for approx 4x scale. Experiment to find optimal values. If `--ropeconfig` is not set, NTK-Aware scaling is the default, automatically set based off your `--contextsize` value.
- You can also use `--overridenativecontext` to adjust the default "trained context" of a model, allowing automatic scaling to be done based on the new value.

### **What is mmap**  
mmap, or memory-mapped file I/O, maps files or devices into memory. It is a method of reducing the amount of RAM needed for loading the model, as parts can be read from disk into RAM on demand. You can enable it with `--usemmap`

### **What is mlock**  
mlock is a technique used to force a model to remain in RAM after it has been loaded. On some systems, especially when RAM is scarce, the OS may trigger memory swapping too frequently, reducing performance. Setting `--usemlock` will prevent that from happening. mlock is disabled by default.

### **How do I use multiple GPUs?**  
Multi-GPU is only available when using CUDA. When not selecting a specific GPU ID after `--usecuda` (or selecting "All" in the GUI), weights will be distributed across all detected Nvidia GPUs automatically. You can change the ratio with the parameter `--tensor_split`, e.g. `--tensor_split 3 1` for a 75%/25% ratio.

### **How can I pick specific devices to use**  
For example, if you have 3 GPUs but only want to use 2 of them, you can specifically override the device list sent to KoboldCpp using `--device`. For example, on Vulkan, you can pass flags like this: `--device Vulkan0,Vulkan1` and the devices will be picked.

### **What does lowvram do for CUDA**  
lowvram can be added to `--usecuda` to reduce VRAM usage at the cost of speed, by not offloading the scratch buffers and KV buffers. 
_Update Oct 2023: lowvram is no longer triggered in the newest GGUF models. It is still currently preserved for compatibility purposes with older GGML models._
_Update Jan 2024: lowvram is now in use again. If enabled, it prevents the per-layer KV offloading to GPU, KV will not be offloaded at all if enabled._

### **What does Quantized Mat Mul (MMQ) do for CUDA**  
`mmq` is an upstream feature can be added to `--usecuda` to use quantized matrix multiplication in CUDA during prompt processing, instead of using cuBLAS for matrix multiplication. Experimentally this uses slightly less memory, and is slightly faster for Q4_0 but slower for K-quants. In newer versions, it is enabled by default, and you must use `nommq` to disable it instead if unwanted.

### **What's the difference between row and layer split**  
This only affects multi-GPU setups, and controls how the tensors are divided between your GPUs. The best way to gauge performance is to try both, but generally layer split should be best overall, while row split can help some older cards.

### **What is LoRA and LoRA Base**  
LoRA is an adapter model that can be applied on top of the weights of an existing model to modify them, adjusting their output similar to the finetuning process. An alternative is to merge the LoRA into the model before converting the end result into GGUF format for optimal quality.
- For text models, you can select a lora with `--lora` and set the strength with `--loramult`. Text LoRAs are quite uncommon and seldom useful.
- For image models, LoRAs are more common and widely used. Set it with `--sdlora` and adjust strength with `--sdloramult`
- `--sdlora` now supports specifying directories as well. All the image LoRAs there will be loadable at runtime by using the LoRA syntax in your image generation prompt in the form `<lora:filename:multiplier>`.

### **What is mmproj (Vision and Audio)**  
`--mmproj` can be used to load a multimodal projector onto a model (e.g. LLaVA), allowing the model to have AI vision/audio capabilities, to perceive and react to images or sounds you send it. KoboldCpp supports a variety of options, for quick testing of vision and audio input, Qwen-Omni is recommended, you download the [base model](https://huggingface.co/ggml-org/Qwen2.5-Omni-3B-GGUF/resolve/main/Qwen2.5-Omni-3B-Q4_K_M.gguf?download=true) and then the [mmproj](https://huggingface.co/ggml-org/Qwen2.5-Omni-3B-GGUF/resolve/main/mmproj-Qwen2.5-Omni-3B-Q8_0.gguf?download=true) and load both. Multiple images and audio files can be used together, though be aware that you will need a high context especially for large audio files.

You can get more projectors for some popular architectures [at this link](https://huggingface.co/koboldcpp/mmproj/tree/main), make sure you pick the correct projector for your architecture! (E.g. A Gemma3 12B model MUST pick the gemma3 12B mmproj gguf). Once loaded, it can be toggled by clicking on any image in Lite and selecting Multimodal Vision for AI Vision, then simply chat with the model normally and it will recognize whatever images you upload. You can adjust the maximum resolution of each image with `--visionmaxres`. To save VRAM, you can put the mmproj on the CPU instead with `--mmprojcpu ` at the cost of slower speed.

### **With Chat Completions, how do I control how many tokens the AI outputs?**  
You can control the AI output length by setting the `max_tokens` field in the API request to `/v1/completions` and `/v1/chat/completions`. However, some third party clients do not set this field. In those cases, you can use the flag `--defaultgenamt` to controls the max amount of tokens generated by default if not specified.

### **What are Embeddings and how can they be used?**  
GGUF embedding models can now be loaded with `--embeddingsmodel` and accessed from `/v1/embeddings` or `/api/extra/embeddings`, this can be used to encoding text for search or storage within a Vector database. This allows searching and matching text input to other semantically similar (related) text in a VectorDB with cosine similarity. It can be used in KoboldAI Lite via the TextDB feature, or with third-party vector DB solutions. You can control the maximum embedding context size with `--embeddingsmaxctx`. You can also offloading embeddings model layers to GPU with `--embeddingsgpu` (not recommended as there is minimal speedup)

### **Flash Attention**  
`--flashattention` can be used to enable flash attention when running with Vulkan or CUDA, which can be more memory efficient especially at large context sizes. It's also supported on image generation using `--sdflashattention`
- Update: Flash attention is now enabled **by default** and can be disabled with `--noflashattention` instead.

### **Sliding Window Attention (SWA)**  
Sliding Window Attention mode uses much less memory for the KV cache, use `--useswa` to enable. Note: SWA mode is not compatible with ContextShifting, and may result in degraded output when used with FastForwarding.

### **Quantized KV Cache**  
You can now utilize the Quantized KV Cache feature in KoboldCpp with `--quantkv [level]`, where `level 0=f16, 1=q8, 2=q4`. Note that fully quantized KV cache is only available if flash attention is used, otherwise only K cache can be quantized.

### **Speculative Decoding (Draft Models)**  
You can explore speculative decoding by loading a draft model. This is intended to be a smaller fast model with the same vocab as the big model, that tries to speed up inference by guessing tokens. Use `--draftmodel` to select the speculative decoding model.
  - `--draftgpulayers` - Set number of layers to offload for speculative decoding draft model
  - `--draftgpusplit` - GPU layer distribution ratio for draft model (default=same as main). Only works if using multi-GPUs.

### **Overriding MoE models**  
`--moeexperts` - Overwrite the number of experts to use in MoE models
`--moecpu` - Keep the Mixture of Experts (MoE) weights of the first N layers in the CPU, e.g. `--moecpu 999 --gpulayers 999` will keep ALL shared MoE layers on GPU while everything else is on CPU. If no value is provided, applies to all layers. This helps improve MoE speeds when partial offloading, as the heavily used shared tensors are kept on the GPU while the less used MoE ones can be kept in RAM. This can also be manually replicated with `--overridetensors` but this is a faster way to do it.

### **What is Admin mode? Can I switch models at runtime?**  
You can switch models, settings and configs at runtime. This also allows for remote model swapping. Launch with `--admin` to enable this feature, and also provide `--admindir` containing `.kcpps` launch configs. Optionally, provide `--adminpassword` to secure admin functions. You will be able to swap between any model's config at runtime from the Admin panel in Lite. You can prepare `.kcpps` configs for different layers, backends, models, etc.
KoboldCpp will then terminate the current instance and relaunch to a new config.  

<img width="506" height="425" alt="image" src="https://github.com/user-attachments/assets/ac772307-db51-4175-9ab1-22d175af02f4" />  

After launching in Admin mode, you get an extra button in KoboldAI Lite that will allow you to easily swap between .kcpps configs. If you select two configs, they will be combined during load.

### **What is Router mode? How can I hotswap models?**  
Automatic model and config hotswapping is finally available in the OpenAI Compatible API. Note that this functions differently from the llama.cpp version, it's more like llama-swap, allowing you to perform full config-reloads similar to the existing admin endpoint, but also within the existing request and response via a reverse proxy. Requires admin mode enabled. Enable it with --routermode. Streaming is supported with a small delay. You can hotswap between models within each OpenAI API request by using router mode, which can be enabled with `--routermode` (requires admin mode). When router mode is enabled, sending a request referencing a different model will automatically unload the current model, load the desired model and then completely the request, all within the same response. 

### **Can I unload models automatically after some idle time?**  
You can set an idle timeout with `--adminunloadtimeout`. This unloads the existing config (unloading all models) after a specified number of seconds. Works best with router mode to allow for auto reloading. Can also manually reload with admin endpoint.


### **What is Whisper?**  
Whisper is a speech-to-text model that can be used for transcription and voice control within Kobold Lite. Load a Whisper GGML model with `--whispermodel`. In Kobold Lite, uses microphone when enabled in settings panel. You can use Push-To-Talk (PTT) or automatic Voice Activity Detection (VAD) aka Hands Free Mode, everything runs locally within your browser including resampling and wav format conversion, and interfaces directly with the KoboldCpp transcription endpoint.

If you're using OpenWebUI or other OpenAI-compatible clients that send /v1/audio/transcriptions in formats like webm/mp3 — you'll need to convert to WAV. [Here is a simple third party proxy script that does it](https://github.com/user-attachments/files/20555552/OPEN-WEBUI%2BKOBOLDCPP-DLYA-WHISPER-proxy.py.txt) written by @AliveDedSec

### **What is Text To Speech?**  
KoboldCpp supports three main text to speech options, Qwen3TTS, OuteTTS and Kokoro. Parler and Dia are also supported but not recommended.
- The recommended option for weak GPUs is Kokoro, which is a single standalone TTS model that works very quickly with good quality. [Download it here](https://huggingface.co/koboldcpp/tts/resolve/main/Kokoro_no_espeak_Q4.gguf) and load it with `--ttsmodel`. You can then enable narration in KoboldAI Lite, or simply generate speech with "Add File".
- For powerful GPUs, Qwen3TTS is the best option. It's recommended to use the **Vulkan** backend with `--ttsgpu` to run it. You can get the Qwen3TTS GGUFs here: [Qwen3TTS 1.7B Model](https://huggingface.co/koboldcpp/tts/resolve/main/Qwen3-TTS-12Hz-1.7B-Base-q8_0.gguf) and [Qwen3TTS WavTokenizer](https://huggingface.co/koboldcpp/tts/blob/main/qwen3-tts-tokenizer-q8_0.gguf), which you should load with `--ttsmodel` and `--ttswavtokenizer` respectively. 0.6B models are also available on our huggingface. Lastly, if you want to use voice cloning, select a directory containing sample .wav files with `--ttsdir` (only qwen3tts can voice clone), you can then use the voice samples to make voice clones by selecting that voice in your request.
- OuteTTS is another older text-to-speech model that can be used for narration by generating audio within Kobold Lite. You need two models, an OuteTTS GGUF and a WavTokenizer GGUF which you can find [here](https://github.com/LostRuins/koboldcpp/wiki#getting-an-ai-model-file). Once downloaded, load them in the Audio tab or using `--ttsmodel` and `--ttswavtokenizer`. 
  - You can also use `--ttsgpu` to load them on the GPU instead.
  - Use `--ttsthreads` to set a custom thread count used.
  - Use `--ttsmaxlen` to limit the maximum amount of audio tokens that will be generated in output for a request.
  - Check the API documentation to see how to change speakers or use voice cloning.

### **Can I generate music within KoboldCpp?**  
As of v1.110, Music Generation is now possible inside KoboldCpp using the AceStep 1.5 model. Requires 4 files (AceStep LM, diffusion, embedder and VAE which are found https://huggingface.co/koboldcpp/music/tree/main), but for your convenience you can load the [.kcppt template for 6GB users](https://huggingface.co/koboldcpp/music/resolve/main/ace-step-sftturbo-6GB-1.7B.kcppt). A music gen GUI has also been added and is available at http://localhost:5001/musicui

### **Can I use SSL?**  
You can now import your own SSL cert to use with KoboldCpp and serve it over HTTPS with `--ssl [cert.pem] [key.pem]` or via the GUI. The `.pem` files must be unencrypted, you can also generate them with OpenSSL, eg. `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -config openssl.cnf -nodes` for your own self signed certificate.

### **How can I see the data inside a GGUF file**  
KoboldCpp now allows you to use `--analyze` on any GGUF file, which will display the metadata and tensor names, dimensions and types within that file.

### **Can I add authentication?**  
You can add a password with the `--password` launch flag, which will require the user to request generations using an API key. You can also use a reverse proxy to provide it on the OpenAI API such as https://gitgud.io/khanon/oai-reverse-proxy

### **How can I better secure a public KoboldCpp instance?**  
Shared KoboldCpp instances are inherently safe as the do not allow users to access or write to arbitrary files on disk. However, you can add additional safeguards through a few flags. 
  - Do not use `--admin` on a public instance, or ensure it's used with a strong password
  - Set a `--password` to prevent unauthorized generations
  - Set `--maxrequestsize` to limit the maximum size of incoming requests which may be exploited to overload the server
  - Set `--ratelimit` to prevent spamming by controlling how frequently each IP address can send a request
  - Set `--genlimit` to limit the maximum allowed generation length over the API per request

### **The program just closes and nothing is shown.**  
The program probably crashed, but the terminal closed too quickly to read the output. You should relaunch koboldcpp via the command prompt/terminal, and read the error message printed on the console. To do this, refer to the section "How to use the command line/terminal".

### **My AI continues rambling / writing rambling after it should have stopped generating / What does Unban Tokens do?**  
Some models will use a special "EOS" (End-Of-Stream) token to indicate when they have finished responding. That is often generated at the end of a paragraph, or when the AI doesn't know how to continue, or believes it has finished speaking. If this EOS token is banned, the model will continue generating indefinitely until the requested tokens are all consumed. You can toggle this behavior in the Kobold Lite Settings for `EOS Token Ban` (set to Auto or Unban to allow EOS), or by setting the `use_default_badwordsids` payload parameter to `false` when using the generate API.  Generally, EOS token unban is usually good for Instruct mode, situationally useful in Chat and Adventure mode, but should not be used in Story mode.  
_Note: `--unbantokens` has been deprecated and should not be used._

### **My model is generating nonsense/rubbish output!**  
This may be a bug, and if so, you should report it. However, there are a few options to check first:
- Make sure you are using a known good GGUF or GGML model. Bad quantizations do exist, especially some K-quants that have been incorrectly converted. Redownload a known good model from a reliable source.
- Make sure your RoPE config is applicable for the model you're using. Some models require specific `--ropeconfig` settings to function, such as 8K and 16K versions of SuperHOT. If the defaults don't work, try again with a different RoPE scale.
- Make sure your model is actually supported. Some architectures are not supported in KoboldCpp, or have been modified in non-standard ways for specific projects. Those GGML models will not work.
- Check your sampler order and sampler values. For more information, read the "Samplers" section of Kobold Lite below. Good defaults are Top-P=0.92, RepPen=1.1, Temperature=0.7 and a sampler order of [6,0,1,3,4,2,5].

### **My koboldcpp crashed while loading a model / WinError / I think I don't have AVX2 / Old CPU help / What is NoAvx2**  
Some older devices do not have support for AVX2, which is a required instruction for fast inference. KoboldCpp has a fallback option for such users, No AVX2 mode. To use this, launch via the command line (see how to above) with the flag `--noavx2`. Alternatively, in the GUI, select the "Old CPU, no AVX2" preset, and AVX1 instructions will be used instead. If it still doesn't work, as a last resort, you can try enabling "Failsafe" mode, with the flags `--failsafe` and see if that works. This is also selectable in the GUI (bottom option labelled Failsafe). Be aware that GPU support is not enabled for these modes and they will be significantly slower. Failsafe mode disables all CPU intrinsics and GPU usage.

### **I saw some error message about not enough space in the scratch memory / context memory / failed allocation**  
This is likely due to the context or scratch buffer size being insufficient for the current context. First, try reducing the max context size that you are using, and also try lowering `--blasbatchsize` to 128 or 64. If that still does not work, please file a bug report on Koboldcpp github.

### **Koboldcpp is not working on windows 7.**  
Windows 7 is not a recommended OS to use for KoboldCpp. If you still want to use it, you must use one of the fallback "Old CPU" modes, e.g. `--noavx2` or "Failsafe Mode" with `--failsafe` for it to work correctly, but it will be slow. You are recommended to upgrade your OS to Windows 10.

### **I have issues with the GUI launcher**  
The GUI launcher uses Python TKinter, so ensure that works correctly on your system. For self setups, you might need to install the `customtkinter` package. On Linux, you might need to install Zenity or YAD for a better file picker UI. On Linux with Wayland, you will encounter issues with fractional scaling above 100%, please disable it in your Linux graphics settings.

### **I have issues with the Web Browser launching**  
KoboldCpp can be configured to open a web browser window after loading, from the GUI or by settings `--launch`. If this fails, simply open any browser to `http://localhost:5001` by default instead. Launching a web browser on Linux may require `xdg-open` to be installed on the system.

### **My GGML model is detected as the wrong type/version**  
This can happen if the model was incorrectly converted or quantized, or corrupted during download. Try downloading a fresh copy of the model. If it still fails, check if your koboldcpp is up to date and the architecture is supported. 

### **Can I benchmark my system performance?**  
You can use `--benchmark`, which automatically runs a benchmark with your provided settings, outputting run parameters, timing and speed information as well as testing for coherence, and exiting on completion. You can provide a filename e.g. `--benchmark result.csv` and it will write CSV formatted data appended to that file.

### **What is `--prompt`**  
This flag can be to run KoboldCpp directly from the command line without running the server, the output of the prompt will be generated and printed into the terminal before exiting. When running with --prompt, all other console outputs are suppressed, except for that prompt's response which is piped directly to stdout. You can control the output length with --genlimit. These 2 flags can also be combined with --benchmark, allowing benchmarking with a custom prompt and returning the response. Note that this mode is only intended for quick testing and simple usage, no sampler settings will be configurable.

### **Can I chat with KoboldCpp interactively from the Command Line / Command Prompt directly?**  
The flag `--cli` launches KoboldCpp with an interactive command line interface without running the server, allowing you to use it without a GUI, just like  llama.cpp. Simply run it with --cli to enter terminal mode, where you can chat interactively using the command line shell.

### **How can I generate images with KoboldCpp?**  
Yes, KoboldCpp now natively supports Local Image Generation, thanks to stable-diffusion.cpp. It provides a ComfyUI and A1111 compatible txt2img endpoint which you can use within the embedded Kobold Lite, or in many other compatible frontends such as SillyTavern. 
  - Just select a compatible SD3, Flux, SD1.5 or SDXL `.safetensors` model to load, either through the GUI launcher or with `--sdmodel`
  - For WAN, Qwen Image, Flux and SD3, you will need additional files (e.g. T5, VAE, Clip encoders), load them from the image tab as necessary.
  - Note: VAEs and LoRAs should be baked inside the model itself, unless you specify them with `--sdvae`,`--sdvaeauto` or `--sdlora`. FP16 is recommended.
  - KoboldCpp also provides a bundled StableUI at http://localhost:5001/sdui, which is an easy frontend for generating and managing images.
  - Supported flags:
```
--sdmodel           Specify a stable diffusion model to enable image generation.
--sdthreads         Use a different number of threads for image generation if specified. 
--sdquant           If specified, loads the model quantized to save memory. Accepts a parameter [0/1/2] that specifies quantization level.
--sdclamped         If specified, limit generation steps and resolution settings for shared use. Optionally allows setting max size.
--sdclampedsoft     If specified, limit max image size to curb memory usage. Less strict than `--sdclamped`, as it limits by total resolution.
--sdlora            If specified, tries to load a Stable Diffusion LoRA model
--sdloramult        Set the LoRA multiplier
--sdvae             Set a custom VAE
--sdvaeauto         Use built in fallback VAE (TAESD)
--sdvaecpu          Runs the VAE on CPU, will be slower but can fix issues.
--sdtiledvae        Adjust the automatic VAE tiling trigger for images above this size. 0 disables VAE tiling.
--sdt5xxl           For Flux and SD3, you need to load a T5-XXL language model as well. Some files bundle it with the main model.
--sdclip1           For Flux and SD3, you need to load a Clip-L model as well. Some files bundle it with the main model.
--sdclip2           For SD3, you need to load a Clip-G model as well. Some files bundle it with the main model.
--sdphotomaker      Load a Photomaker model along with another SDXL model, allowing you to do face cloning.
--sdflashattention  Enables flash attention for image generation.
--sdconvdirect      Toggles Conv direct. Generally not needed.
--sdoffloadcpu      Swaps away components from GPU memory when not in-use. Useful if you have low VRAM.
--sdclipgpu         Runs CLIP or text encoding models on the GPU instead, can be faster.
```
  - For a quick example, [here are some known working Image Generation models you can try](https://github.com/LostRuins/koboldcpp/wiki#getting-an-ai-model-file)
  - If you're running a shared server, it's recommended to use both `--sdclamped` and `--sdquant` to avoid running out of memory.

### **What about Image Editing?**  
This can be done with the Flux Kontext, Flux Klein, and Qwen Image Edit models. They are powerful image editing models that can edit images using natural language. Easily replace backgrounds, edit text, or add extra items into your images. For a quick test with Flux Kontext, you can [download a ready-to-use kcppt template here](https://huggingface.co/koboldcpp/kcppt/resolve/main/Flux-Kontext.kcppt), simply load it into KoboldCpp and all necessary model files will be downloaded on launch. Then open StableUI at http://localhost:5001/sdui, add your prompt, reference images and generate. Alternatively, you can use any normal SDXL image model and do editing with the Img2Img and inpainting tools in StableUI.

## Kobold Lite Web UI

<img src="https://github.com/LostRuins/koboldcpp/assets/39025047/7845b69e-b5a5-4de5-8fb5-0d39b68b441d" width="600">  

*(Image guide originally from /lmg/, thanks anon)*

### **What is Kobold Lite? How do I use it?**  
Kobold Lite is a lightweight, standalone Web UI for KoboldCpp, KoboldAI Client, and AI Horde, which requires no dependencies, installation or setup. It comes pre-bundled with all distributions of KoboldCpp and is ready to use out of the box. After starting KoboldCpp (default port is 5001), just navigate your local browser such as Chrome, Firefox or Safari to http://localhost:5001 and Kobold Lite will be launched.

### **Basic Modes of Kobold Lite**  
Kobold Lite has 4 different modes, which you can toggle using the 'Format' Dropdown inside the "Basic Settings" panel. 
- Story Mode: For creative fiction and novel writing, the AI continues your story based on your input.
- Chat Mode: Simulates a character persona with an interactive AI chatbot. Ask the AI anything, or chit-chat with it in turn based conversation.
- Instruct Mode: ChatGPT styled instruction-response. Give the AI a task, and it will try to fulfill the instruction.
- Adventure Mode: AIDungeon styled interactive fiction, choose-your-own-adventure, describe an action and the AI narrates the result.
The best way to get started after launching Kobold Lite is to jump into a pre-crafted **Scenario**, which you can select from the "Scenarios" button.

### **UI Style Select**  
In newer Kobold Lite versions, you can pick from 3 different UIs (not all are available in all modes).
- Classic: This is the default Kobold notepad look and feel, simple, clean, efficient, and available for all modes.
- Messenger: This is an alternative UI for chat mode, which shows up as a messenger style chat between you and the AI.
- Aesthetic: This is an alternative UI for chat and instruct mode, which allows great customization of text styles, colors, padding and inclusion of image portraits.
- Corpo: This UI attempts to mimic the look and feel of Corporate AI Assistants such as ChatGPT.

### **What are samplers? How do I change or disable them? What are the best samplers?**  
Samplers are basically how the AI determines the next token to choose, from the list all possible tokens. There are many different samplers with different properties, though you will generally only need a few. Good defaults to use are Top-P=0.92, RepPen=1.1, Temperature=0.7 and a sampler order of [6,0,1,3,4,2,5], leaving everything else disabled (default).  
- Top-K: This setting limits the number of possible words to choose from to the top K most likely options, removing everything else. Can be used with Top-P. Set value to 0 to disable its effect.
- Top-A: Alternative to Top-P. Remove all tokens that have softmax probability less than top_a*m^2 where m is the maximum softmax probability. Set value to 0 to disable its effect.
- Top-P: Discards unlikely text in the sampling process. Only considers words with the highest cumulative probabilities summing up to P. Low values make the text predictable, as uncommon tokens are removed. Set value to 1 to disable its effect.
- TFS: Alternative to Top-P, this setting removes the least probable words from consideration during text generation, considering second order derivatives. Can improve the quality and coherence of the generated text.
- Typical: Selects words randomly from the list of possible words, with each word having an equal chance of being selected. This method can produce text that is more diverse but may also be less coherent. Set value to 1 to disable its effect.
- Temperature: Controls how 'Random' the output is by scaling probabilities without removing options. Lower value are more logical, but less creative.
- Repetition Penalty: Applies a penalty to reduce usage of words that have already been used recently, making the output of the AI less repetitive.
- Mirostat: Alternative sampling method that overrides other samplers. See mirostat section.
- Min-P: An experimental alternative to Top-P that removes tokens under a certain probability. Set value to 0 to disable its effect.
- DynaTemp: Dynamic Temperature Sampling is a variant of normal Temperature sampling where the temperature is allowed to automatically vary between two preset limits. Temperature is allowed to be automatically adjusted dynamically between DynaTemp ± DynaTempRange. Set DynaTemp Range to 0, or set min and max to the same value, to disable it.
- DRY: DRY is a dynamic N-gram anti-repetition sampler, used as an alternative or together with Repetition Penalty. Only recommended for advanced users.
- XTC:  XTC (Exclude Top Choices) sampler is creative writing sampler designed by the same author of DRY. It removes common tokens with high probability when there are many choices, allowing for more creative and flavorful text. To use it, increase xtc_probability above 0 (recommended values to try: xtc_threshold=0.15, xtc_probability=0.5)

### **What is sampler order? What is the best sampler order? I got a warning for bad suboptimal sampler orders.**  
Sampler order controls the order in which the above samplers are applied in sequence, to the list of token candidates when choosing the next token. It is **STRONGLY** not advised to change this from the default of [6,0,1,3,4,2,5] as that can lead to very poor outputs.

### **What are Logprobs? Can I view token probabilities?**  
You can now use the built-in Token Probability Viewer to display token probabilities, based on returned logprobs. This allows you to visualize alternative possible tokens that the AI could have chosen for every token in the returned output.

### **What are custom presets?**  
Presets are pre-configured sampler settings that have been contributed or collected over time to emulate specific writing styles or platforms. Some of them have sub-optimal configurations or sampler orders, but they should be considered artistic rather than practical - you will likely still get optimal results from the default preset.

### **Max Ctx. Tokens (Context Size)**  
Context size determines the maximum number of tokens (context window) that will be sent to the AI, in other words, it controls how far back in, and how much of the text the AI gets to access, remember and use. Most models are limited to 2048 tokens of context, but some have been trained with larger context sizes. Bigger contexts take more memory and are slower to process and generate with. To extend context, refer to the sections on "longer context above 2048" and "RoPE scaling". This field can be manually overridden past the slider limit by editing the text input field.

### **Amount to Generate**  
Maximum number of tokens the AI can generate for it's response to each submitted request. Each token is roughly about four letters long.

### **Token Streaming**  
Enable this option to allow tokens from an incomplete AI response to be gradually streamed into the UI instead of only responding when the generation is complete. Not applicable for AI Horde users.

### **Trim Whitespace**  
This option combines multiple consecutive newlines into one single newline. It also removes trailing whitespace at the end of the submitted prompt.

### **Trim Sentences**  
This option trims the AI's response down to the last complete sentence, if possible.

### **EOS Token Ban**  
This option controls the AI's usage of the End-Of-Stream Token, a special token that lets the AI stop responding early when it thinks the response is complete. It replaces the old `--unbantokens` launcher flag.  
- Auto: Automatically determine whether to use EOS tokens or not.
- Unban: Always allow the EOS token to be used.
- Ban: Prevent the EOS token from being generated.

### **Placeholder Tags**  
This option allows the placeholder tags `{{user}}` `{{char}}` `{{[INPUT]}}` and `{{[OUTPUT]}}` to be used by character card or scenario authors, which will be dynamically replaced with the correct value on runtime. For example, `{{char}}` will get replaced with the chatbot's selected nickname.

### **Thinking Tags**  
In some modern reasoning models like Deepseek R1, the model performs a chain-of-thought process that outputs thinking steps before deriving a final answer. In Settings > Tokens > Thinking, you can specify regex to handle output from reasoning models, to hide, remove, or ignore the Chain-Of-Thought tags like `<think>`. It's easiest to toggle thinking by changing the Instruct tags in the Settings Presets panel.

### **Persist Autosave Session**  
This option autosaves your story and settings, which will be restored the next time you start KoboldCpp again. However, to avoid data loss you are still recommended to manually export your saved story .json files from time to time.

### **Save File Includes Settings**  
This option allows your Kobold Lite UI, generation and sampler settings to be saved directly into the story json file itself, and loaded again in future.

### **Show Rename Save File**  
This option triggers a popup when you save your story, allowing you to rename the target save file name.

### **Autoscroll Text**  
This option scrolls down the text window to the bottom every time a new AI response is received.

### **Invert Colors**  
This option inverts all the colors for the UI, useful for e-ink displays or people who prefer a light theme.

### **Chat/Story - Idle Responses**  
Enabling this option allows the AI to automatically send new responses after the player has been idle for a few seconds, useful to simulate a real-time chat conversation.

### **Chat - Multiline Replies**  
This allows the AI to respond to your chat messages with more than a single-line response. This may result in more verbose and lengthy chat responses, but the output can also become wildly incoherent and unpredictable, or the AI might even start talking as someone else. **Not recommended for beginners**.

### **Chat - Continue Bot Replies**  
This option allows the AI to stop speaking halfway (incomplete reply), and then resume speaking within the same message, when you press the submit button again. If disabled, each response from the AI will instead start on a new line with the AI name prefix added (IRC style). Enabling 'Continue Bot Replies' may result in the AI refusing to speak if it does not know what to say. **Not recommended for beginners**.

### **Chat - Your Name / AI Name**  
You can set your displayed name and the AI name for the current chat session, useful for roleplaying specific characters.

### **Instruct - Start and End Sequence**  
Set this to the Instruct start and end instruct sequences that the model was trained on for best quality. For Alpaca, this is `### Instruction: ` and `### Response: `, which should generally work well for most instruct models. You can add newlines with `\n` if desired.

### **Instruct - Enable Markdown**  
This allows instruct mode to generate formatted markdown, such as item lists, tables and code blocks. Useful for coding tasks.

### **Adventure - Adventure Prompt**  
This option injects a pre-prompt to the AI to make it take adventure mode more seriously, useful especially if your prompt is short. **Highly recommended to keep enabled for beginners, unless using a custom scenario.**

### **How do I make the AI remember things?**  
As contexts gets very long, eventually the earlier parts of your story will exceed the maximum context length and get trimmed away. There are some features in the 'Memory' panel to preserve the overall aspets of your story in such scenarios.  
- Memory - This is a sequence of text that will always be injected into the start of each prompt sent to the AI. It is useful for things the AI should always remember even over very long stories, such as main theme(s) of your story, the broad strokes of the setting, central conflict(s), and protagonist. As it uses up context space, try to keep Memory short, at most a paragraph or two.
- Author's Note - This is similar to memory, but is injected *near* the *end* of the prompt rather than at the start. It's used to describe recent situations, or guide the AI to behave in a certin way for the current scene. A/N Strength affects how far back this text is injected.
- World Info - This is text that is only situationally injected into the prompt. When the World Info "Key" is matched, the corresponding "Content" text gets injected into the start of the prompt. Useful for reminding the AI of facts, character names, ages, personalities, places as well as plot points, like a dictionary or encyclopedia.

### **For text models, is classifier-free guidance supported? (CFG)**  
Yes, but it is **not recommended**. classifier-free guidance in theory is supposed to allow you to set a "negative prompt" to steer the output away from a concept or style. In practice, it often does not work. If you wish to use it simple check `Enable Guidance` or use `--enableguidance`, then set a negative prompt and CFG scale from the lite tokens menu. Note that guidance doubles KV usage and halves generation speed.

### **What are stop sequences (stopping tokens)?**  
Stop Sequences are a set of specially designated tokens or phrases that should make the model stop generating early. For example, if you wanted the output to end after a new paragraph, you could use `\n\n` as a stopping sequence. Chat mode, Instruct mode and Adventure mode all come with preconfigured stop sequences.

### **What are the buttons above the user text input box?**  
- Back - This functions like an Undo button, reversing the most recent action or AI response.
- Redo - This is a Redo button, which reverses the 'Back' button and restores deleted text from history.
- Retry - This button retries your most recent action or message, useful if you don't like the AI response and want something different.
- Branch - This button allows you to create parallel 'Branches' in your session, which duplicates the current conversation which then becomes an independent divergent conversation history. It can be used to explore alternative responses or paths.
- Add File - This is used to attach media to the AI, such as uploading images and audio. You can also use it to generate images, audio and text-to-speech if you have the models for them loaded and they are enabled in settings.
- Edit - This is not a button but a checkbox toggle. When enabled, you'll be able to retroactively modify any part of your existing story, or the response from the AI.

### **My chat mode is malfunctioning. How do I stop the AI from replying as myself?**  
This can happen when the model is poorly prompted, especially with 'Multiline Replies' enabled. Often, the solution is just to retry the most recent request. However, here are some tips to avoid this:  
- Disable 'Multiline Replies'
- Use a good model, preferably finetuned on chat conversations
- Make sure the initial prompt or character card is well formatted. Names should be consistent, well-formatted layout wise, and not misspelled. A few good examples in memory goes a long way, if the chat history is bad, the chat future will be bad too.
- In extreme cases, set your chat username as a custom stopping token. This will have unintended side effects.

### **My AI response is very short / the AI response in the console is longer, some words got trimmed from the terminal to the UI.**  
This is the opposite problem to the above, sometimes the AI has many interesting things to say, but they get trimmed away because it responded across multiple lines or even multiple paragraphs. Enabling 'Multiline Replies' allow such responses to be used. Remember - the AI learns from examples. A boring prompt or dull messages from the user can lead to dull AI replies.

### **What is AI Vision?**  
AI Vision is an attempt to provide multimodality by allow the model to recognize and interpret uploaded or generated images. There are three modes supported to provide vision.
  - Interrogate (AI Horde): This uses AI Horde to perform image interrogation online, giving you a basic description of the image.
  - Interrogate (Local): local A1111 or Forge endpoint to perform image interrogation to generate a simple description.
  - Multimodal Vision: This is *true* vision, it requires using a multimodal projector (mmproj) and allows the model to recognize and interpret images naturally in great detail.
Click on any image and you can enable it within the dropdown box in KoboldAI Lite.

### **What file formats does Kobold Lite support?**  
Kobold Lite supports many file formats, automatically determined when the file is loaded. These include:
- KoboldAI Classic .json saves (Default)
- KoboldAI United .json saves (V2 format)
- KoboldAI KAISTORY files
- TavernAI and SillyTavern Character Cards (JSON format, WebP and PNG all supported)
- Oobabooga charaacter and story exports
- Agnai and Tavern world info formats
- Raw text files

### **What are Usermods?**  
Usermods are custom chunks of third-party user-provided javascript that can be added to modify your KoboldAI Lite experience. It can replace functions or monkey patch them, or modify the browser client itself. A sample script is provided for your convenience.

### **Where can I find the source code for Kobold Lite? What about the online version?**  
The source code for Kobold Lite is under AGPLv3, and [can be found here](https://github.com/LostRuins/lite.koboldai.net).
The web version powered by Horde can be accessed at https://lite.koboldai.net

### **Can I run a UI without Javascript, (e.g. from a very old browser) or over the command line (e.g. SSH?)**  
You can use KoboldCpp NoScript WebUI, which does not require Javascript to work. It should be W3C HTML compliant and should run on every browser in the last 20 years, even text-based ones like Lynx (e.g. in the terminal over SSH). It is accessible by default at `/noscript` e.g. `http://localhost:5001/noscript` . This can be helpful when running KoboldCpp from systems which do not support a modern browser with Javascript. Noscript mode also supports basic image generation and chat mode.

### **Windows Shell Integration**  
KoboldCpp can be set to handle opening `.kcpps` and `.gguf` files by default when you double click them in windows. You can trigger this from the Extras tab in the GUI launcher, to register and unregister the default handler. If launched this way `--singleinstance` is applied, which allows this KoboldCpp instance to be shut down by any new instance requesting the same port, preventing duplicate servers from clashing on a port.

## KoboldCpp Integrations  
### **What is KoboldAI United? How to use KoboldAI Client / Kobold United?**  
[KoboldAI United](https://github.com/henk717/KoboldAI) is the current actively developed version of KoboldAI, while [KoboldAI Client](https://github.com/KoboldAI/KoboldAI-Client) is the classic/legacy (Stable) version of KoboldAI that is no longer actively developed.  
KoboldCpp maintains compatibility with both UIs, that can be accessed via the `AI/Load Model > Online Services > KoboldAI API` menu, and providing the URL generated after launching KoboldCpp.  

### **What GUIs are available or provided for KoboldCpp**  
By default, KoboldCpp bundles the KoboldAI Lite Web UI which can be found at http://localhost:5001, this UI is capable of accessing almost all KoboldCpp features and is recommended as a first option. For those who prefer a more corporate looking UI, we bundle the llama.cpp GUI as well at http://localhost:5001/lcpp/ which runs in parallel. For music generation, we provide a Music Gen UI at http://localhost:5001/musicui. For image generation, StableUI is bundled at http://localhost:5001/sdui. Lastly, KoboldCpp can also be connected to by third party UIs such as SillyTavern, through the OpenAI and Ollama compatible APIs exposed.

### **What is Horde? How do I use it? How do I share my model with Horde?**  
The AI Horde is a crowdsourced distributed cluster of Image generation workers and Text generation workers, where people can share their own processing power to generate images and text for other users. KoboldCpp now comes included with an embedded *lightweight Horde Worker* which allows anyone to share their ggml models with the AI Horde without downloading additional dependences apart from KoboldCpp.
- To use Horde as an end-user, you can go to https://lite.koboldai.net
- To share your own models and compute power over Horde using Koboldcpp:
  - Register for an [AI Horde API key](https://horde.koboldai.net/register).
  - Enable the Horde config from the GUI and fill in all details, or launch by setting `--hordekey`, `--hordemodelname` and `--hordeworkername` which will start a Horde worker for you that serves horde requests automatically in the background. 
  - Exclude your `--hordekey` to continue using your own standalone Horde worker (e.g. Haidra Scribe / KAI Horde Bridge - Note that this is no longer recommended since KoboldCpp has a dedicated built in worker, you do not need to run a third party worker script.)
  - Supported Flags:
```
--hordemodelname  Sets your AI Horde display model name.
--hordeworkername Sets your AI Horde worker name.
--hordekey        Sets your AI Horde API key.
--hordemaxctx     Sets the maximum context length your worker will accept.
--hordegenlen     Sets the maximum number of tokens your worker will generate.
```

### **I'm encountering SSL errors with my horde worker**  
You can try `--nocertify` mode which allows you to disable SSL certificate checking on your embedded Horde worker. This can help bypass some SSL certificate errors.

### **What is SillyTavern? What is Pygmalion? What is Agnaistic? How do I use them?**  
SillyTavern and Agnaistic are third-party frontend user interfaces that specialize in interaction with chat/roleplay with AI characters. They include support for KoboldCpp as a backend, via the KoboldAI API. Pygmalion is a community that focuses on using AI for chat, they also have created their own finetuned chat model. In the 'Other established resources' references below you can find documentation for using Pygmalion and SillyTavern together with KoboldCpp.

### **How can I use the Kobold API? Is there an API reference or API documentation? How does the KoboldCpp API differ from the KoboldAI United API?**  
The KoboldAI web API is the interface which downstream applications can communicate with KoboldCpp. The full KoboldCpp Swagger API reference can be found at [https://lite.koboldai.net/koboldcpp_api](https://lite.koboldai.net/koboldcpp_api) as well as within the program by visiting `http://localhost:5001/api`. 
- For a simple python example, [check out this script which uses the KoboldCpp API](https://github.com/LostRuins/koboldcpp/blob/concedo/examples/api_example.py).
- In general, the most important endpoint is `/api/v1/generate`, which is the endpoint used to send prompts and receive responses from the AI. 
- Other useful endpoints are `/api/v1/model`, `/api/v1/config/max_length` and `/api/v1/config/max_context_length`
- In addition, KoboldCpp also implements a few additional endpoints not found in the original KoboldAI API, these include 
  - `/api/extra/generate/stream` for SSE streaming
  - `/api/extra/version` for version information 
  - `/api/extra/perf` for performance and timing information
  - `/api/extra/abort` to abort an in-progress generation
  - `/api/extra/generate/check` to get the partially completed text for an in-progress generation
  - `/api/extra/tokencount` to tokenize and accurately measure how many tokens any string has.
  - `/api/extra/true_max_context_length` to get the actual ctx length loaded from the launcher.
- You can also use the OpenAI Chat Completions compatible API as mentioned below. 

### **Is there an OpenAI API?**  
Yes, there is now a simple OpenAI compatible completions and chat completions API, which will allow KoboldCpp to be used with other projects that require an OpenAI API, you can access it at `/v1/completions` and `/v1/chat/completions`. You can access OpenAI documentation for [Completions API](https://developers.openai.com/api/reference/resources/completions/methods/create) and [Chat Completions API](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create), or view the [KoboldCpp online API reference](https://lite.koboldai.net/koboldcpp_api). 

### **Is there an Ollama API?**  
Yes, there is now a simple Ollama compatible API, which will allow KoboldCpp to be used with other projects that require Ollama specifically. For normal usage, this is NOT recommended, and only exists to provide unparalleled larger ecosystem compatibility.

### **What is WebSearch**  
When WebSearch is enabled, KoboldCpp now optionally functions as a WebSearch proxy with a new `/api/extra/websearch` endpoint, allowing your queries to be augmented with web searches. Works with all models, needs top be enabled both on Lite and on Kcpp with `--websearch` or in the GUI. The websearch is executed locally from the KoboldCpp instance, and is powered by DuckDuckGo.

### **Can I Talk To or Search my Documents**  
KoboldCpp offers a TextDB Document Lookup in KoboldAI Lite - This is a very rudimentary form of browser-based RAG. You can access it from the Context > TextDB tab. It's powered by a text-based minisearch engine, you can paste a very large text document which is chunked and stored into the database, and at runtime it will find relevant snippets to add to the context depending on the query/instruction you send to the AI. You can use the historical context as a document, or paste a custom text document to use. Note that this is NOT an embedding model or true vector database, it uses lunr and minisearch for retrieval scoring instead. 

### **What is the `--gendefaults` and `--gendefaultsoverwrite` flags?**  
You can insert additional generation parameters from the KoboldCpp backend using the `--gendefaults` flag, which accepts a JSON dictionary. For example, doing `--gendefaults "{\"temperature\":0.9}"` will apply a 0.9 temperature if unspecified. If `--gendefaultsoverwrite` is set, then it will override any values sent by the API, effectively forcing this parameter for all requests.

### **Where do models I specify by URL get downloaded?**  
By default, all models downloaded via a URL will be stored in the same directory as your KoboldCpp.exe or binary file. You can set a different directory with `--downloaddir`

### **What does --overridekv and --overridetensors do?**  
They are launcher flags which work in the same way as llama.cpp's `--override-kv` and `--override-tensor` flags.
`--overridekv` allows you to specify a single metadata property to be overwritten. Input format is `keyname=type:value`. You can also specify multiple values separated by commas
`--overridetensors` allow you to place tensors matching a pattern onto a specific backend. Input format is `tensornamepattern=buffertype`

### **Are my chats private? What is with the Share button?**  
KoboldCpp is capable of running fully locally offline without internet, and does not send your inputs to anywhere else. Generated content using the API is displayed in the terminal console, which is cleared when the application is closed. Likewise, Kobold Lite UI will store your content only locally within the browser, it is not sent to any other external server. KoboldCpp and Kobold Lite are fully open source with AGPLv3, and you can compile from source or review it on github.  

If you use KoboldCpp with third party integrations or clients, they may have their own privacy considerations. When using Horde, your responses are sent between the volunteer and the user over the horde network and potentially can be read from either end, so do not send privacy sensitive information with Horde.

The "Share" button in Kobold Lite has multiple modes: 
- TextData: Does not actually upload any data anywhere, rather it compresses your entire story into a very string (which encoded the data within it), that can be reloaded on a different device by reimporting it.
- Web URL: Uploads the current story onto a public pastebin, and generates a short url that can be used to fetch it again. You can specify how long the upload lasts for. Anyone with the link will have access to download it.

### **Command Line Arguments Reference**  
```
positional arguments:
  model_param           Model file to load (positional)
  port_param            Port to listen on (positional)

options:
  -h, --help            show this help message and exit
  --model [filenames] [[filenames] ...], -m [filenames] [[filenames] ...]
                        Model file to load. Accepts multiple values if they are URLs.
  --port [portnumber]   Port to listen on. (Defaults to 5001)
  --host [ipaddr]       Host IP to listen on. If this flag is not set, all routable interfaces are accepted.
  --launch              Launches a web browser when load is completed.
  --config [filename]   Load settings from a .kcpps file. Other arguments will be ignored
  --threads [threads], -t [threads]
                        Use a custom number of threads if specified. Otherwise, uses an amount based on CPU cores
  --usecuda [[main GPU ID] [mmq|nommq] [rowsplit] ...], --usecublas [[main GPU ID] [mmq|nommq] [rowsplit] ...], --usehipblas [[main GPU ID] [mmq|nommq] [rowsplit] ...]
                        Use CUDA for GPU Acceleration. Requires CUDA. Enter a number afterwards to select and use 1 GPU. Leaving no number will   
                        use all GPUs.
  --usevulkan [[Device IDs] ...]
                        Use Vulkan for GPU Acceleration. Can optionally specify one or more GPU Device ID (e.g. --usevulkan 0), leave blank to    
                        autodetect.
  --usecpu              Do not use any GPU acceleration (CPU Only)
  --contextsize [256 to 262144], --ctx-size [256 to 262144], -c [256 to 262144]
                        Controls the memory allocated for maximum context size, only change if you need more RAM for big contexts. (default       
                        8192).
  --gpulayers [[GPU layers]], --gpu-layers [[GPU layers]], --n-gpu-layers [[GPU layers]], -ngl [[GPU layers]]
                        Set number of layers to offload to GPU when using GPU. Requires GPU. Set to -1 to try autodetect, set to 0 to disable     
                        GPU offload.
  --tensor_split [Ratios] [[Ratios] ...], --tensorsplit [Ratios] [[Ratios] ...], --tensor-split [Ratios] [[Ratios] ...], -ts [Ratios] [[Ratios] ...]
                        For CUDA and Vulkan only, ratio to split tensors across multiple GPUs, space-separated list of proportions, e.g. 7 3      
  --autofit, --fit, -fit
                        Automatically attempt to fit the model in the best possible way. Overrides everything else. Experimental.
  --showgui             Always show the GUI instead of launching the model right away when loading settings from a .kcpps file.
  --skiplauncher        Doesn't display or use the GUI launcher. Overrides showgui.

Advanced Commands:
  --version             Prints version and exits.
  --analyze [filename]  Reads the metadata, weight types and tensor names in any GGUF file.
  --maingpu [Device ID], --main-gpu [Device ID], -mg [Device ID]
                        Only used in a multi-gpu setup. Sets the index of the main GPU that will be used.
  --batchsize {-1,16,32,64,128,256,512,1024,2048,4096}, --blasbatchsize {-1,16,32,64,128,256,512,1024,2048,4096}, --batch-size {-1,16,32,64,128,256,512,1024,2048,4096}, -b {-1,16,32,64,128,256,512,1024,2048,4096}
                        Sets the batch size used in batched processing (default 512). Setting it to -1 disables batched mode, but keeps other     
                        benefits like GPU offload.
  --blasthreads [threads], --batchthreads [threads], --threadsbatch [threads], --threads-batch [threads]
                        Use a different number of threads during batching if specified. Otherwise, has the same value as --threads
  --lora [lora_filename] [[lora_filename] ...]
                        GGUF models only, applies a lora file on top of model.
  --loramult [amount]   Multiplier for the Text LORA model to be applied.
  --noshift, --no-context-shift
                        If set, do not attempt to Trim and Shift the GGUF context.
  --nofastforward       If set, do not attempt to fast forward GGUF context (always reprocess). Will also enable noshift
  --useswa              If set, allows Sliding Window Attention (SWA) KV Cache, which saves memory but cannot be used with context shifting.      
  --smartcache [limit]  Enables intelligent context switching by saving KV cache snapshots to RAM. Requires fast forwarding.
  --ropeconfig [rope-freq-scale] [[rope-freq-base] ...]
                        If set, uses customized RoPE scaling from configured frequency scale and frequency base (e.g. --ropeconfig 0.25 10000).   
                        Otherwise, uses NTK-Aware scaling set automatically based on context size. For linear rope, simply set the freq-scale     
                        and ignore the freq-base
  --overridenativecontext [trained context]
                        Overrides the native trained context of the loaded model with a custom value to be used for Rope scaling.
  --usemmap             If set, uses mmap to load model.
  --usemlock, --mlock   Enables mlock, preventing the RAM used to load the model from being paged out. Not usually recommended.
  --noavx2              Do not use AVX2 instructions, a slower compatibility mode for older devices.
  --failsafe            Use failsafe mode, extremely old CPU compatibility mode that should work on all devices.
  --debugmode [DEBUGMODE]
                        Shows additional debug info in the terminal.
  --onready [shell command]
                        An optional shell command to execute after the model has been loaded.
  --benchmark [[filename]]
                        Do not start server, instead run benchmarks. If filename is provided, appends results to provided file.
  --prompt [prompt], -p [prompt]
                        Passing a prompt string triggers a direct inference, loading the model, outputs the response to stdout and exits. Can be  
                        used alone or with benchmark.
  --cli                 Does not launch KoboldCpp HTTP server. Instead, enables KoboldCpp from the command line, accepting interactive console    
                        input and displaying responses to the terminal.
  --genlimit [token limit], --promptlimit [token limit]
                        Sets the maximum number of generated tokens, it will restrict all generations to this or lower. Also usable with
                        --prompt or --benchmark.
  --multiuser [limit]   Runs in multiuser mode, which queues incoming requests instead of blocking them.
  --multiplayer         Hosts a shared multiplayer session that others can join.
  --websearch           Enable the local search engine proxy so Web Searches can be done.
  --remotetunnel        Uses Cloudflare to create a remote tunnel, allowing you to access koboldcpp remotely over the internet even behind a      
                        firewall.
  --highpriority        Experimental flag. If set, increases the process CPU priority, potentially speeding up generation. Use caution.
  --foreground          Windows only. Sends the terminal to the foreground every time a new prompt is generated. This helps avoid some idle       
                        slowdown issues.
  --preloadstory [savefile]
                        Configures a prepared story json save file to be hosted on the server, which frontends (such as KoboldAI Lite) can        
                        access over the API.
  --savedatafile [savefile]
                        If enabled, creates or opens a persistent database file on the server, that allows users to save and load their data      
                        remotely. A new file is created if it does not exist.
  --quiet               Enable quiet mode, which hides generation inputs and outputs in the terminal. Quiet mode is automatically enabled when    
                        running a horde worker.
  --ssl [cert_pem] [[key_pem] ...]
                        Allows all content to be served over SSL instead. A valid UNENCRYPTED SSL cert and key .pem files must be provided        
  --nocertify           Allows insecure SSL connections. Use this if you have cert errors and need to bypass certificate restrictions.
  --mmproj [filename]   Select a multimodal projector file for vision models like LLaVA.
  --mmprojcpu, --no-mmproj-offload
                        Force CLIP for Vision mmproj always on CPU.
  --visionmaxres [max px]
                        Clamp MMProj vision maximum allowed resolution. Allowed values are between 512 to 2048 px (default 1024).
  --draftmodel [filename], --model-draft [filename], -md [filename]
                        Load a small draft model for speculative decoding. It will be fully offloaded. Vocab must match the main model.
  --draftamount [tokens], --draft-max [tokens], --draft-n [tokens]
                        How many tokens to draft per chunk before verifying results
  --draftgpulayers [layers], --gpu-layers-draft [layers], --n-gpu-layers-draft [layers], -ngld [layers]
                        How many layers to offload to GPU for the draft model (default=full offload)
  --draftgpusplit [Ratios] [[Ratios] ...]
                        GPU layer distribution ratio for draft model (default=same as main). Only works if multi-GPUs selected for MAIN model     
                        and tensor_split is set!
  --password [API key]  Enter a password required to use this instance. This key will be required for all text endpoints. Image endpoints are     
                        not secured. Can also be set with env var KCPP_PASSWORD
  --ratelimit [seconds]
                        If enabled, rate limit generative request by IP address. Each IP can only send a new request once per X seconds.
  --ignoremissing       Ignores all missing non-essential files, just skipping them instead.
  --chatcompletionsadapter [filename]
                        Select an optional ChatCompletions Adapter JSON file to force custom instruct tags.
  --jinja               Enables using jinja chat template formatting for chat completions endpoint. Other endpoints are unaffected. Tool calls    
                        are done without jinja.
  --jinja_tools, --jinja-tools, --jinjatools
                        Enables using jinja chat template formatting for chat completions endpoint. Other endpoints are unaffected. Tool calls    
                        are done with jinja.
  --jinja_kwargs {"parameter":"value",...}, --jinja-kwargs {"parameter":"value",...}, --jinjakwargs {"parameter":"value",...}, --chat-template-kwargs {"parameter":"value",...}
                        Set additiona fields for Jinja JSON template parser, must be a valid JSON object.
  --noflashattention, --no-flash-attn, -nofa
                        Disables flash attention.
  --lowvram, -nkvo, --no-kv-offload
                        If supported by the backend, do not offload KV to GPU (lowvram mode). Not recommended, will be slow.
  --quantkv [quantization level 0/1/2]
                        Sets the KV cache data type quantization, 0=f16, 1=q8, 2=q4, 3=bf16. Requires Flash Attention for full effect, otherwise  
                        only K cache is quantized.
  --smartcontext        Reserving a portion of context to try processing less frequently. Outdated. Not recommended.
  --unpack destination  Extracts the file contents of the KoboldCpp binary into a target directory.
  --exportconfig [filename]
                        Exports the current selected arguments as a .kcpps settings file
  --exporttemplate [filename]
                        Exports the current selected arguments as a .kcppt template file
  --nomodel             Allows you to launch the GUI alone, without selecting any model.
  --moeexperts [num of experts]
                        How many experts to use for MoE models (default=follow gguf)
  --moecpu [[layers affected]], --n-cpu-moe [[layers affected]], -ncmoe [[layers affected]]
                        Keep the Mixture of Experts (MoE) weights of the first N layers in the CPU. If no value is provided, applies to all       
                        layers.
  --defaultgenamt DEFAULTGENAMT
                        How many tokens to generate by default, if not specified. Must be smaller than context size. Usually, your frontend GUI   
                        will override this.
  --nobostoken          Prevents BOS token from being added at the start of any prompt. Usually NOT recommended for most models.
  --enableguidance      Enables the use of Classifier-Free-Guidance, which allows the use of negative prompts. Has performance and memory
                        impact.
  --maxrequestsize [size in MB]
                        Specify a max request payload size. Any requests to the server larger than this size will be dropped. Do not change if    
                        unsure.
  --overridekv [name=type:value], --override-kv [name=type:value]
                        Override metadata value by key. Separate multiple values with commas. Format is name=type:value. Types: int, float,       
                        bool, str
  --overridetensors [tensor name pattern=buffer type], --override-tensor [tensor name pattern=buffer type], -ot [tensor name pattern=buffer type] 
                        Override selected backend for specific tensors matching tensor_name_regex_pattern=buffer_type, same as in llama.cpp.      
  --singleinstance      Allows this KoboldCpp instance to be shut down by any new instance requesting the same port, preventing duplicate
                        servers from clashing on a port.
  --nopipelineparallel  Disable Pipeline Parallelism. Pipeline Parallelism provides faster multigpu speeds but using more memory, only active     
                        for multigpu.
  --gendefaults {"parameter":"value",...}
                        Sets extra default parameters for some fields in API requests, as a JSON string.
  --gendefaultsoverwrite
                        Allow the gendefaults parameters to overwrite the original value in API payloads.
  --mcpfile [mcp json file]
                        Specify path to mcp.json which contains the Cladue Desktop compatible MCP server config.
  --device <dev1,dev2,..>, -dev <dev1,dev2,..>
                        Set llama.cpp compatible device selection override. Comma separated. Overrides normal device choices.
  --downloaddir [directory]
                        Specify a directory that models will be downloaded to or searched from, if unset uses the working directory.
  --autofitpadding [padding in MB]
                        How much spare allowance in MB should autofit reserve? If it's too little, the load might fail.

Horde Worker Commands:
  --hordemodelname [name]
                        Sets your AI Horde display model name.
  --hordeworkername [name]
                        Sets your AI Horde worker name.
  --hordekey [apikey]   Sets your AI Horde API key.
  --hordemaxctx [amount]
                        Sets the maximum context length your worker will accept from an AI Horde job. If 0, matches main context limit.
  --hordegenlen [amount]
                        Sets the maximum number of tokens your worker will generate from an AI horde job.

Image Generation Commands:
  --sdmodel [filename]  Specify an image generation safetensors or gguf model to enable image generation.
  --sdthreads [threads]
                        Use a different number of threads for image generation if specified. Otherwise, has the same value as --threads.
  --sdclamped [[maxres]]
                        If specified, limit generation steps and image size for shared use. Accepts an extra optional parameter that indicates    
                        maximum resolution (eg. 768 clamps to 768x768, min 512px, disabled if 0).
  --sdclampedsoft [maxres]
                        If specified, limit max image size to curb memory usage. Similar to --sdclamped, but less strict, allows trade-offs       
                        between width and height (e.g. 640 would allow 640x640, 512x768 and 768x512 images).
  --sdt5xxl [filename]  Specify a T5-XXL safetensors model. Leave blank if prebaked or unused.
  --sdclip1 [filename], --sdclipl [filename]
                        Specify first safetensors Clip model (SD3 or Flux Clip-L, WAN or QwenImg vision). Leave blank if prebaked or unused.      
  --sdclip2 [filename], --sdclipg [filename]
                        Specify second safetensors Clip model (SD3 Clip-G). Leave blank if prebaked or unused.
  --sdphotomaker [filename]
                        PhotoMaker is a model that allows face cloning. Specify a PhotoMaker safetensors model which will be applied replacing    
                        img2img. SDXL models only. Leave blank if unused.
  --sdupscaler [filename]
                        You can use ESRGAN as an upscaling model to resize images. Leave blank if unused.
  --sdflashattention    Enables Flash Attention for image generation.
  --sdoffloadcpu        Offload image weights in RAM to save VRAM, swap into VRAM when needed.
  --sdvaecpu            Force VAE to CPU only for image generation.
  --sdclipgpu           Put CLIP and T5 to GPU for image generation. Otherwise, CLIP will use CPU.
  --sdconvdirect {off,vaeonly,full}
                        Enables Conv2D Direct. May improve performance or reduce memory usage. Might crash if not supported by the backend. Can   
                        be 'off' (default) to disable, 'full' to turn it on for all operations, or 'vaeonly' to enable only for the VAE.
  --sdvae [filename]    Specify an image generation safetensors VAE which replaces the one in the model.
  --sdvaeauto           Uses a built-in tiny VAE via TAE SD, which is very fast, and fixed bad VAEs.
  --sdquant [[quantization level 0/1/2]]
                        If specified, loads the model quantized to save memory. 0=off, 1=q8, 2=q4
  --sdlora [filename] [[filename] ...]
                        Specify image generation LoRAs safetensors models to be applied. Multiple LoRAs are accepted.
  --sdloramult [amounts] [[amounts] ...]
                        Multipliers for the image LoRA model to be applied.
  --sdtiledvae [maxres]
                        Adjust the automatic VAE tiling trigger for images above this size. 0 disables vae tiling.
  --sdmaingpu [Device ID]
                        If specified, Image Generation weights will be placed on the selected GPU index

Whisper Transcription Commands:
  --whispermodel [filename]
                        Specify a Whisper .bin model to enable Speech-To-Text transcription.

TTS Narration Commands:
  --ttsmodel [filename]
                        Specify the TTS Text-To-Speech GGUF model.
  --ttswavtokenizer [filename]
                        Specify the WavTokenizer GGUF model.
  --ttsgpu              Use the GPU for TTS.
  --ttsmaxlen TTSMAXLEN
                        Limit number of audio tokens generated with TTS.
  --ttsthreads [threads]
                        Use a different number of threads for TTS if specified. Otherwise, has the same value as --threads.
  --ttsdir [directory]  Select directory containing voices for voice cloning.

Music Gen Commands:
  --musicllm [filename]
                        Select music LLM model (e.g acestep-5Hz-lm-0.6B)
  --musicembeddings [filename]
                        Select music embedding model (e.g Qwen3-Embedding-0.6B)
  --musicdiffusion [filename]
                        Select music diffusion (DiT) model (e.g acestep-v15-turbo)
  --musicvae [filename]
                        Select music VAE model
  --musiclowvram        Unload music models when not in use

Embeddings Model Commands:
  --embeddingsmodel [filename]
                        Specify an embeddings model to be loaded for generating embedding vectors.
  --embeddingsmaxctx [amount]
                        Overrides the default maximum supported context of an embeddings model (defaults to trained context).
  --embeddingsgpu       Attempts to offload layers of the embeddings model to GPU. Usually not needed.

Administration Commands:
  --admin               Enables admin mode, allowing you to unload and reload different configurations or models.
  --adminpassword [password]
                        Require a password to access admin functions. You are strongly advised to use one for publically accessible instances!    
                        Can also be set with env var KCPP_ADMINPASSWORD
  --admindir [directory]
                        Specify a directory to look for .kcpps configs in, which can be used to swap models.
  --adminunloadtimeout ADMINUNLOADTIMEOUT
                        Set an idle timeout in seconds after which KoboldCpp will automatically unload the current model.
  --routermode          Router mode uses a reverse proxy router, allowing you to easily hotswap models and configs within a single request.       
                        Requires admin mode.
  --autoswapmode        Autoswap mode builds on router mode to allow switching of model types within the same config automatically. Requires      
                        admin mode and router mode. All models desired must be defined within the same config.
```

---

# Step-by-Step Guides

This section provides step by step guides on using common features of KoboldCpp.
- [Basic text model usage for ChatGPT refugees (Text Generation, System Prompts, Memory)](https://github.com/LostRuins/koboldcpp/wiki#basic-text-model-usage-for-chatgpt-refugees-text-generation-system-prompts-memory)
- [Vibe coding a HTML webpage](https://github.com/LostRuins/koboldcpp/wiki#vibe-coding-a-html-webpage)
- [Multimodal usage with Qwen-Omni (Text Generation, Vision Recognition, Audio Recogition)](https://github.com/LostRuins/koboldcpp/wiki#multimodal-usage-with-qwen-omni-text-generation-vision-recognition-audio-recogition)
- [Image Generation with PicX Real (Image Generation, Stable Diffusion)](https://github.com/LostRuins/koboldcpp/wiki#image-generation-with-picx-real-image-generation-stable-diffusion)
- [Chatting with a Tavern AI Character Card](https://github.com/LostRuins/koboldcpp/wiki#chatting-with-a-tavern-ai-character-card)
- [Setting up MCP tool calling](https://github.com/LostRuins/koboldcpp/wiki#mcp-tool-calling)
- [Generating music with AceStep, speech and cloning voices with Qwen3TTS](https://github.com/LostRuins/koboldcpp/wiki#music-and-tts-voice-cloning)

## Basic text model usage for ChatGPT refugees (Text Generation, System Prompts, Memory)
In this guide, we will be using the Gemma3 12B or 4B model as an AI Assistant for a ChatGPT replacement. This demo is ideal for beginners starting with KoboldCpp.
1. First, [download the latest version of KoboldCpp here](https://github.com/LostRuins/koboldcpp/releases/latest). **Pick the correct version for your OS and GPU**.
2. You have a choice on which model to use. 
  - For Low-Spec devices or those running on CPU only, use [Gemma3-4B-Instruct](https://huggingface.co/ggml-org/gemma-3-4b-it-GGUF/resolve/main/gemma-3-4b-it-Q4_K_M.gguf)
  - For those with a better GPU, use [Gemma3-12B-Instruct](https://huggingface.co/unsloth/gemma-3-12b-it-GGUF/resolve/main/gemma-3-12b-it-Q4_K_M.gguf)
3. Launch KoboldCpp GUI Launcher, and select the model you downloaded into the **Text Model** field, and click **Launch**. For this demo, I will use Gemma3-12B.  You can adjust the backend or layers next time, but for newbies it's fine to leave all other settings as default, and click **Launch**. 
<img width="500" height="326" alt="image" src="https://github.com/user-attachments/assets/e7775f87-3e9f-42d9-9678-894af99f8329" />  

4. KoboldCpp will begin loading. When done, it will launch a KoboldAI Lite browser window to [http://localhost:5001](http://localhost:5001). You may pick whichever theme you like - use Corpo for a ChatGPT feel, Aesthetic for a customizable chatbot style, or Classic for a simple and clean UI. You can always change it in the settings later. For now, I will show it on Corpo UI theme.  
<img width="300" height="214" alt="image" src="https://github.com/user-attachments/assets/74b381f6-4861-4016-8fc3-9ce15274119d" />  

5. Once the AI is loaded, we can set a system prompt or memory message. This defines the AI's behavior and allows you to control it's personality. You can set this in 2 places, **System Prompt** in settings (which persists when you start a new session) or **Context Memory** which will be cleared when you start a new session. For now, let's put it in "**Memory**", which you can access with the **Context** button in Classic UI, or in the **(+)** panel in Corpo UI.
<img width="403" height="329" alt="image" src="https://github.com/user-attachments/assets/3270758c-8da9-48e8-9b3f-e86f4b02776b" />

6. Click "Add Instruction" in the Memory field, enter some instructions for the AI, e.g. "You are a funny robot named BobBot. Always respond with a lot of jokes." 
<img width="261" height="204" alt="image" src="https://github.com/user-attachments/assets/2645e2c9-fbfb-45b2-8e0b-263a86dff71e" />

6. Now you can send it a message with your request or simply chat with the AI. You can easily undo, redo or edit any part of past responses, or send follow up messages.
<img width="460" height="256" alt="image" src="https://github.com/user-attachments/assets/8d5dfaee-02f5-40f5-abea-fd2564682317" />


## Vibe coding a HTML webpage  
In this guide, we will be using the Gemma3 12B or 4B model to assist us with Vibe Coding a simple HTML webpage. This guide picks up from the previous guide, so if you need help setting up KoboldCpp, please follow steps 1 to 4 in the [previous section](https://github.com/LostRuins/koboldcpp/wiki#basic-text-model-usage-for-chatgpt-refugees-text-generation-system-prompts-memory).

1. Once the AI is loaded, you can send it a message with your request. Here, I will ask the AI `Please give me the HTML code to a simple promotional page for my rock band "The Kobolds"`, then click the arrow to send the message. The AI will begin to generate.  
<img width="400" height="398" alt="image" src="https://github.com/user-attachments/assets/f61c6c3c-64a8-4cbb-873b-8b2ef35d6f43" />  

2. Sometimes, the reply is very long. **If the AI has not finished the response, click the arrow submit button to continue the incomplete message**. TIP: If you want to make the AI permit longer replies, you can adjust the "**Max Output**" slider in settings.

3. Once the response is done and you are satisfied, click the **Copy To Clipboard** button 📋 on the top right corner of the generated code. Or, you can just select all the code in the box. Open Notepad, paste it inside and save it as a new HTML file such as *demo.html*, and you can open it in a browser!
<img width="400" height="426" alt="image" src="https://github.com/user-attachments/assets/1d57fe99-6519-432e-a872-e6b9d171f09c" />


## Multimodal usage with Qwen-Omni (Text Generation, Vision Recognition, Audio Recogition)
In this guide, we will be using the Qwen 2.5 Omni 3B model as an AI assistant to process vision and audio content. This demo will require at least 8GB RAM and 5GB disk space, and is ideal for beginners or those with low spec devices.
1. First, [download the latest version of KoboldCpp here](https://github.com/LostRuins/koboldcpp/releases/latest). **Pick the correct version for your OS and GPU**.
2. Get both the [Qwen 2.5 Omni 3B model](https://huggingface.co/ggml-org/Qwen2.5-Omni-3B-GGUF/resolve/main/Qwen2.5-Omni-3B-Q4_K_M.gguf), as well as the [Mmproj multimodal projector](https://huggingface.co/ggml-org/Qwen2.5-Omni-3B-GGUF/resolve/main/mmproj-Qwen2.5-Omni-3B-Q8_0.gguf)
3. Launch KoboldCpp GUI Launcher, and go to the Loaded Files tab. Load the base GGUF model into "**Text Model**" and the mmproj GGUF into "**MMProj File**". You can adjust the backend or layers next time, but for newbies it's fine to leave all other settings as default, and click **Launch**.  
<img width="500" height="528" alt="image" src="https://github.com/user-attachments/assets/0c5a14ff-ac48-43a8-962b-4b4fb9e35e66" />  

4. KoboldCpp will begin loading. When done, it will launch a KoboldAI Lite browser window to [http://localhost:5001](http://localhost:5001). You may pick whichever theme you like - use Corpo for a ChatGPT feel, Aesthetic for a customizable chatbot style, or Classic for a simple and clean UI. You can always change it in the settings later. For now, I will show it on Classic theme.  
<img width="300" height="214" alt="image" src="https://github.com/user-attachments/assets/74b381f6-4861-4016-8fc3-9ce15274119d" />  

5. Let's verify the model is loaded and working. Send a simple message by typing in the input box "Who are you?", send it, and the AI should reply. Now you have a basic AI assistant which you can chat anything with!  
<img width="400" height="254" alt="image" src="https://github.com/user-attachments/assets/9bedf37e-00da-45f6-ae1d-db35a3373d40" />  

6. Now let's give the AI something to see. Let's use the [Lena test image, which you can get here](https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png). Save it to your PC, go back to KoboldAI Lite, and click "**Add File**" to insert the image. _TIP: You can also use the clipboard or copy and paste the image directly into the text inputbox!_  
<img width="363" height="43" alt="image" src="https://github.com/user-attachments/assets/838d235d-d313-4cbc-bed6-ac92c0e93e4a" /><br>
<img width="425" height="429" alt="image" src="https://github.com/user-attachments/assets/ace3ed52-41dd-482e-962a-365f26ef47d5" />

7. If correctly loaded, the image should appear with an "Eye" icon which means vision is enabled for it. Now you can ask the AI anything about the image!    
<img width="400" height="450" alt="image" src="https://github.com/user-attachments/assets/9a18d077-ec53-486b-a03e-98dccf7cad6c" />

8. Using the same method, you can also give the AI audio to listen to. [You can get a test sound file here](https://upload.wikimedia.org/wikipedia/commons/0/01/Hello%2C_everyone%21.ogg). Use "**Add File**" to insert it in the same manner, a clip with a ear icon will appear indicating Audio Recognition is being used, then you can talk to the AI about it.  
<img width="400" height="150" alt="image" src="https://github.com/user-attachments/assets/88a1495d-9fac-4f0f-87a3-c94946de4400" />

9. That concludes this simple demo. You can ask the AI follow up questions, but note that the AI will get confused if you give it too many images and sounds. Multiple images and audio files can be used together, though be aware that you will need a high context especially for large audio files. You are recommended to save the session and start afresh again with "**New Session**" to avoid this issue.

## Image Generation with PicX Real (Image Generation, Stable Diffusion)
KoboldCpp supports generating images using common image generation models such as Stable Diffusion, SDXL, Flux, Chroma, Kontext, Qwen Image and even video generation with WAN. For a beginner, let's start off with a simple all-in-one model. In future, more advanced models can come in multiple parts and require multiple files to work, but for now we shall use a Stable Diffusion 1.5 based model called **PicX Real**. 
1. First, [download the latest version of KoboldCpp here](https://github.com/LostRuins/koboldcpp/releases/latest). **Pick the correct version for your OS and GPU**.
2. Download the ["PicX Real" image gen model which you can find here](https://huggingface.co/koboldcpp/imgmodel/resolve/main/picx_real_q8_0.gguf). Go to the "**Image Gen**" tab and pick the image gen model we downloaded. If you have very little VRAM, you can set the "Compress Weights" to q4 or q8, which will quantize the weights to take less space. **Launch** when ready.  
_TIP: It's possible to use **both an Image Generation model and a Text Generation model** together if you have enough memory to load them both._  
<img width="500" height="446" alt="image" src="https://github.com/user-attachments/assets/4ea56e91-8981-4915-b11d-1ded5e0c558d" />  

3. You can generate images in KoboldAI Lite (along with your chats) or standalone using the bundled Stable UI (SDUI). I will show both methods.
4. For KoboldAI Lite, let's do classic mode. Once KoboldCpp is launched, open a browser to [http://localhost:5001](http://localhost:5001). Simply press the "**Add File**" button, and select "**Generate Image (From Prompt)**"  
<img width="392" height="302" alt="image" src="https://github.com/user-attachments/assets/854c8a45-90a8-4d56-b9df-fa77c2b17fd3" />  

5. Type in a prompt "Cat wearing a hat" and press OK. The image will start generating. Once it's done, it should appear in the UI!  
<img width="400" height="260" alt="image" src="https://github.com/user-attachments/assets/9245f83b-cbb4-4121-b480-0de1162a6040" />

6. If you have a text generation model loaded, you can also generate text along with your images, and images with your text. For example, you could write a story, then click "Generate Image (Automatic)" and it would make an image to fit your story or chat session!

7. Next, we will try Stable UI (SDUI). You can launch it at [http://localhost:5001/sdui](http://localhost:5001/sdui). The UI should be very similar to software like Forge or Automatic1111, simply type in your prompt, adjust settings, and generate. 
<img width="400" height="233" alt="image" src="https://github.com/user-attachments/assets/6bbf6968-d4a5-4fd1-9821-9096298416dd" />

8. When using more advanced models, make sure you have all the required component models! A common one is the T5 text encoder, or custom Clip models and VAEs. In general, only SD1.5 and SDXL models come all-in-one, everything else will require multiple models.

## Creating narrations with Kokoro (Text-To-Speech, Narration)

## Speech recognition and voice input with Whisper (Speech-To-Text, Audio Transcriptions)

## Chatting with a Tavern AI Character Card
KoboldCpp and KoboldAI Lite can be used for a wide variety of purposes such as coding and adventure games. However, one very popular use case is doing **Roleplays with Chatbots**. In this guide we will setup a simple chatbot persona and have a conversation with it. This guide picks up from the previous guide, so if you need help setting up KoboldCpp, please follow steps 1 to 4 in the [previous section](https://github.com/LostRuins/koboldcpp/wiki#basic-text-model-usage-for-chatgpt-refugees-text-generation-system-prompts-memory).

1. The most popular way chatbots are shared is via **SillyTavern Character Cards**. These are self-contained files that describe the personality, behavior and mannerisms of an AI character during roleplay, and can provide an immersive and colorful experience. You can get character cards from many sites such as [chub.ai](https://chub.ai), [aicharactercards.com](https://aicharactercards.com) and more. KoboldAI Lite also supports importing characters directly from these sites, or any compatible SillyTavern AI Character Card. 

2. For this demo, we'll use the **Lara Lightland character**, who is a scientist working on portals. [You can get the card here](https://chub.ai/characters/shaolan98/lara-lightland), or save it directly off this page (Right Click + Save As): 
<img width="200" height="300" alt="image" src="https://github.com/user-attachments/assets/96d567c8-541e-4088-96bc-f72ac40da0c9" />  

3. Once the AI is loaded, we will use the Aesthetic UI theme. Then, click **Save/Load > Open File** and navigate to your downloaded character card, and import it. When importing, you will be given a choice to use Chat or Instruct mode, the best choice is dependent on the model, but for this demo let's use Chat mode.  
<img width="550" height="258" alt="image" src="https://github.com/user-attachments/assets/f0bab9e2-def8-472a-a72e-06173583ff2c" />
<img width="300" height="187" alt="image" src="https://github.com/user-attachments/assets/a896d0f7-2083-431e-b029-ba09f532b0d8" />

4. If you like, you can set your Chat Persona name in **Settings > Your Name**. I will name myself "**Charles**". Also, feel free to adjust UI styles under **Aesthetic **settings.  
<img width="400" height="182" alt="image" src="https://github.com/user-attachments/assets/accb22f5-3e46-44e9-924e-e8bf255f1904" />

5. You can begin chatting with the AI! Most character cards are already fully configured and work well out of the box.  
<img width="400" height="373" alt="image" src="https://github.com/user-attachments/assets/9f22580c-1f17-4c12-a66b-55e3dea845fb" />

6. If you need to adjust or edit the card, you can do so in "**Memory**" section, which you can access with the **Context** button in Classic UI, or in the **(+)** panel in Corpo UI.
<img width="403" height="329" alt="image" src="https://github.com/user-attachments/assets/3270758c-8da9-48e8-9b3f-e86f4b02776b" />

## MCP Tool Calling
As of KoboldCpp 1.106, MCP tool calling is now fully supported and can be used as a drop-in replacement for Claude Desktop. MCP tool calling greatly extends the capabilities of KoboldCpp, allowing easy integration with the **thousands of MCP servers out there** capable of performing many various tasks like playing music, organizing your files, reading system info and writing to databases.

What is MCP? MCP stands for Model Context Protocol, an open standard designed to allow AI agents to connect with and interact with external data sources, applications, and tools in real time. In this guide, we'll setup a [simple MCP server](https://github.com/modelcontextprotocol/servers/) that allows your AI to read files and search the internet.

**DISCLAIMER: Running ANY MCP SERVER gives it full access to your system. Their scripts will be able to modify and make changes to your files. Be sure to only run servers you trust!**

1. First, [download the latest version of KoboldCpp here](https://github.com/LostRuins/koboldcpp/releases/latest). **Pick the correct version for your OS and GPU**.
2. (Skip this step if you already have necessary dependencies) MCP Servers are often Python uvx or Node.JS based. For this example you'll need to install Node.JS (for NPX). You can grab it from [https://nodejs.org](https://nodejs.org) or follow the [Claude Desktop docs here](https://modelcontextprotocol.io/docs/develop/connect-local-servers) for more details. The rest of the guide assumes you have npm/npx installed.
3. KoboldCpp accepts a `mcp.json` config files compatible with Claude Desktop. This file contains all the MCP servers to be started. You can connect both HTTP and STDIO based MCP servers. We'll use the [Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) example server along with [EXA search MCP](https://mcp.exa.ai/mcp), a remote HTTP free MCP server provided by EXA AI. 

Here's the `mcp.json` file template you can use. Change the filesystem path to a folder you want the AI to access (the example uses my Desktop folder, be careful what you let the AI access!). **Remember, you can use any mcp.json file compatible with Claude Desktop** if you have used that before - format is the same. 
```
{
  "mcpServers": {
    "filesystem_mcp": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/Users/your_username/Desktop"
      ]
    },
    "exaone_search_mcp": {
        "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```
Modify and save this file to your PC as `mcp.json`  

3. Grab a capable tool calling model. For this example I recommend using [Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct-GGUF/resolve/main/Qwen3VL-8B-Instruct-Q4_K_M.gguf).  
4. Launch koboldcpp and load the mcp.json and the model.  
<img width="460" height="390" alt="image" src="https://github.com/user-attachments/assets/8d17e8e3-3129-45cc-8ac5-7fa5f30dc746" />

5. Once KoboldCpp is launched, you should see the MCP servers being initialized. Pay attention to any errors that may occur, and ensure they are launched correctly.  
<img width="441" height="70" alt="image" src="https://github.com/user-attachments/assets/3f395c14-548e-47f3-a99b-0fb6a7a04a9a" />  

6. Now launch KoboldAI Lite, open settings and enable tool calling, then fetch the tools, you should see the combined tools from both servers being loaded. You can toggle off or on any tools you want to allow the AI to have.  
<img width="460" height="460" alt="image" src="https://github.com/user-attachments/assets/fcb79717-9452-4811-9f91-0dfd80373fce" />

7. Now, you can ask the AI anything about the files on your desktop! If you enabled "Manually Approve Tools", you'll be asked to approve any tool calls. Otherwise, they will be executed automatically. 
<img width="460" height="172" alt="image" src="https://github.com/user-attachments/assets/78fcc171-fb39-4be2-be8b-0f26c20c28b5" />
<img width="460" height="334" alt="image" src="https://github.com/user-attachments/assets/9ed8875a-627c-4674-8e6f-29bc6b2fc433" />  

8. The AI will pick the appropriate tool to use depending on the scenario, and KoboldCpp will route the request to the correct MCP server  
<img width="600" height="300" alt="image" src="https://github.com/user-attachments/assets/0259fe73-c384-4b05-9347-26cee5c3d4a6" />

9. Need another example server? Try this config for a time conversion MCP server (requires python and uv)
```
{
  "mcpServers": {    
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    }
  }
}
```

10. That's it! For an example on how to [write your own MCP server using FastMCP, check this out](https://github.com/LostRuins/koboldcpp/blob/concedo/examples/demo_mcp.py)

## Music and TTS Voice Cloning
KoboldCpp allows for music generation using AceStep 1.5, and TTS speech generation and voice cloning using Qwen3TTS. In this guide, we'll do both. If you have not yet downloaded or setup KoboldCpp before, check out earlier guides in the [previous section](https://github.com/LostRuins/koboldcpp/wiki#basic-text-model-usage-for-chatgpt-refugees-text-generation-system-prompts-memory).

### AceStep 1.5 Music Generation
For music generation, we'll need 4 files (AceStep LM, diffusion, embedder and VAE which are found at https://huggingface.co/koboldcpp/music/tree/main). However, it's easier to simply load from a kcppt template, so [grab and load this template](https://huggingface.co/koboldcpp/music/resolve/main/ace-step-sftturbo-6GB-1.7B.kcppt) which will auto download everything you need.

Once loaded, launch KoboldCpp MusicUI at [http://localhost:5001/musicui](http://localhost:5001/musicui)

Now enter a simple caption and optionally some lyrics, or you can have the AI generate lyrics for you (might not be very good). To let the AI plan the song, click the "Plan" button - the AI will fill in or change some of the fields, but you can adjust it again. Feel free to experiment with the optional parameters or let the AI pick them for you and then tweak them as needed. Here's an example with some safe defaults.

Caption used: `A cheerful and playful children's song featuring a friendly, clear male vocals`

Some sample lyrics if you like:
```
[Verse 1]
Little birds, sing along
Dancing around to our favorite song
Little birds, dance with me
Jump and spin, oh so free
Wings together, a happy sound
Let's dance together all around
So let's go row a boat!

[Chorus]
Row, row, row your boat,
Gently down the stream.
Merrily, merrily, merrily, merrily,
Life is but a dream.

[Instrumental Break]

[Chorus]
Row, row, row your boat,
Gently down the stream.
Merrily, merrily, merrily, merrily,
Life is but a dream.

[Outro]
```
<img width="392" height="609" alt="image" src="https://github.com/user-attachments/assets/ecd018ce-422a-4013-8ccd-1d3324fd0eda" />

Now, once your song plan is ready, click "Generate". The song will appear in the right tab when it is ready, then you can playback or download it!  

https://github.com/user-attachments/assets/e6b76278-4ace-415d-9f27-d81bde5c265d

### Qwen3TTS Voice Cloning and Voice Design
For Qwen3TTS text to speech, you can pick between two models models.   
- [Qwen3TTS VoiceDesign](https://huggingface.co/koboldcpp/tts/resolve/main/Qwen3-TTS-12Hz-1.7B-VoiceDesign-Q8_0.gguf) - This model allows you to create speech based on a text instruction describing the speaker.  
- [Qwen3TTS Base](https://huggingface.co/koboldcpp/tts/resolve/main/Qwen3-TTS-12Hz-1.7B-Base-q8_0.gguf) - This model allows you to clone the voice of a speaker based on a short audio clip.  
- For both, you will also need a [Qwen3TTSTokenizer](https://huggingface.co/koboldcpp/tts/resolve/main/qwen3-tts-tokenizer-q8_0.gguf)  

Load them into the Audio tab, for the TTS model and TTS wav tokenizer.  
<img width="481" height="215" alt="image" src="https://github.com/user-attachments/assets/9f86c74d-389e-4055-81bd-fea77af6632a" />

If you are using the Qwen3TTS Base for **voice cloning**, don't forget to set the folder containing your .wav file samples as well! Each sample .wav file should be between 5 to 10 seconds long.  

<img width="462" height="48" alt="image" src="https://github.com/user-attachments/assets/f97ce7c4-37bd-46cf-8712-401d0e74a3e2" />

Launch KoboldCpp and open MusicUI at [http://localhost:5001/musicui](http://localhost:5001/musicui), then go to the TTS tab. If you are using VoiceDesign, you can input a custom instruction, followed by the text you want narrated. If you are using voice cloning, you cannot use an instruction, but you can pick the voice you want to clone.

<img width="400" height="254" alt="image" src="https://github.com/user-attachments/assets/346ed31a-e1e9-4cb5-8ef4-d03b43f23691" />

https://github.com/user-attachments/assets/5e3a8c24-9f37-49ef-9e3a-f82cbdde681e

For API usage, you can [refer to TTS documentation here](http://lite.koboldai.net/api#/api%2Fextra/post_api_extra_tts).

## Co-writing a novel with the AI

## Using the KoboldCpp and OpenAI Compatible API via a python script

More Guides Coming soon

---

### Useful Links and References  
[Latest KoboldCpp Release for Windows](https://github.com/LostRuins/koboldcpp/releases/latest)  
[KoboldCpp repo and Readme](https://github.com/LostRuins/koboldcpp)  
[Github Discussion Forum](https://github.com/LostRuins/koboldcpp/discussions) and [Github Issues list](https://github.com/LostRuins/koboldcpp/issues?q=)  
[koboldcpp.net - Community Website](https://koboldcpp.net)  

### Other established resources  
[Local LLM guide from /lmg/, with good beginner models](https://rentry.org/local_LLM_guide)  
[SillyTavern documentation regarding KoboldAI](https://docs.sillytavern.app/usage/api-connections/koboldcpp/)  
[PygmalionAI documentation regarding KoboldAI](https://docs.pygmalion.chat/en/backend/kobold-cpp)  
[KoboldAI Discord Server](https://koboldai.org/discord)  
Also check out /lmg/, r/KoboldAI and r/LocalLLaMA/  

### Misc. Guides  
[Installing KoboldCpp on Android via Termux](https://www.reddit.com/r/KoboldAI/comments/14uxmsn/guide_how_install_koboldcpp_in_android_via_termux/)  
[Installing KoboldCpp on Linux with GPU](https://www.reddit.com/r/LocalLLaMA/comments/13q6u9e/koboldcpp_linux_with_gpu_guide/)  
[Building KoboldCpp CUDA on Linux](https://www.reddit.com/r/LocalLLaMA/comments/14faz1d/building_koboldcpp_cuda_on_linux/)  
[Simple Windows Guide to getting started with KoboldCpp](https://www.reddit.com/r/singularity/comments/144th3k/incredibly_simple_guide_to_run_language_models/)  
[Simplified LLAMA Guide](https://rentry.org/TESFT-LLaMa#koboldcpp-windows)  
[Compiling on Windows, A quick guide](https://github.com/LostRuins/koboldcpp/issues/664)  
[Guide to Using the API](https://www.reddit.com/r/LocalLLaMA/comments/1hx8gid/a_beginners_guide_to_llm_scripting_using_python/)  
[Extracting PDFs for KoboldCpp](https://github.com/LostRuins/koboldcpp/discussions/2244)  

### Notable Forks (They may have special features)  
https://github.com/henk717/koboldcpp  
https://github.com/ycros/koboldcpp  
https://github.com/YellowRoseCx/koboldcpp-rocm  
https://github.com/0cc4m/koboldcpp  
https://github.com/SammCheese/koboldcpp  
https://github.com/Nexesenex/croco.cpp  
https://github.com/esolithe/esobold  