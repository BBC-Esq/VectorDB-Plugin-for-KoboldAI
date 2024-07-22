# KoboldCpp Preset Options and Parameter Compatibility

| Preset Option | Compatible Parameters | Incompatible Parameters | Notes |
|---------------|----------------------|-------------------------|-------|
| Use OpenBLAS | Most general parameters | `--usecublas`, `--usevulkan`, `--useclblast`, `--lowvram`, `--mmq`, `--rowsplit`, `--gpulayers`, `--tensor_split`, `--noavx2` | Default option for CPU-only systems |
| Use CLBlast | `--useclblast`, `--gpulayers` | `--usecublas`, `--usevulkan`, `--noblas`, `--lowvram`, `--mmq`, `--rowsplit`, `--noavx2` | Must specify exactly 2 arguments for platform ID and device ID |
| Use CuBLAS | `--usecublas`, `--gpulayers`, `--tensor_split`, `--lowvram`, `--mmq`, `--rowsplit` | `--usevulkan`, `--useclblast`, `--noblas`, `--noavx2` | Best option for NVIDIA GPUs |
| Use Vulkan | `--usevulkan`, `--gpulayers`, `--tensor_split` | `--usecublas`, `--useclblast`, `--noblas`, `--lowvram`, `--mmq`, `--noavx2` | Compatible with a wide range of GPUs |
| Use No BLAS | `--noblas` | `--usecublas`, `--usevulkan`, `--useclblast`, `--lowvram`, `--mmq`, `--rowsplit`, `--gpulayers`, `--tensor_split` | Slowest option, but most compatible |
| CLBlast NoAVX2 (Old CPU) | Same as "Use CLBlast" | Same as "Use CLBlast" | Automatically sets `--noavx2` |
| Vulkan NoAVX2 (Old CPU) | Same as "Use Vulkan" | Same as "Use Vulkan" | Automatically sets `--noavx2` |
| NoAVX2 Mode (Old CPU) | Most general parameters | `--usecublas`, `--usevulkan`, `--useclblast` | Automatically sets `--noavx2` |
| Failsafe Mode (Old CPU) | Basic parameters only | `--usecublas`, `--usevulkan`, `--useclblast`, `--lowvram`, `--mmq`, `--rowsplit`, `--gpulayers`, `--tensor_split` | Automatically sets `--noavx2`, `--noblas`, and `--nommap` |

> Notes:
> - The `--gpulayers` option is only available for Vulkan, CLBlast, and CuBLAS modes.
> - The `--tensor_split` option is only available for CuBLAS and Vulkan modes.
> - The `--lowvram`, `--mmq`, and `--rowsplit` options are only available for CuBLAS mode.

## Kobold AI - Menu Options by Binary

| Menu Option                  | koboldcpp_nocuda.exe | koboldcpp.exe | koboldcpp_oldcpu.exe | koboldcpp_cu12.exe |
|------------------------------|:--------------------:|:-------------:|:--------------------:|:------------------:|
| Use OpenBLAS                 |          ✓           |       ✓       |          (no AVX2)            |         ✓          |
| Use CLBlast                  |          ✓           |       ✓       |          ✓           |         ✓          |
| Use CuBLAS                   |                      |       ✓ (CUDA 11)       |          ✓ (CUDA 11)           |         ✓ (CUDA 12)          |
| Use Vulkan                   |          ✓           |       ✓       |          ✓           |         ✓          |
| Use No BLAS                  |          ✓           |       ✓       |          ✓           |         ✓          |
| CLBlast NoAVX2 (Old CPU)     |          ✓           |       ✓       |          ✓           |         ✓          |
| Vulkan NoAVX2 (Old CPU)      |          ✓           |       ✓       |          ✓           |         ✓          |
| NoAVX2 Mode (Old CPU)        |          ✓           |       ✓       |          ✓           |         ✓          |
| Failsafe Mode (Old CPU)      |          ✓           |       ✓       |          ✓           |         ✓          |

## Kobold AI - Binary Details

| DLL Files                    | koboldcpp_nocuda.exe | koboldcpp.exe | koboldcpp_oldcpu.exe | koboldcpp_cu12.exe |
|------------------------------|:--------------------:|:-------------:|:--------------------:|:------------------:|
| OpenCL.dll                   |          ✓           |       ✓       |          ✓           |         ✓          |
| koboldcpp_default.dll        |          ✓           |       ✓       |          ✓           |         ✓          |
| koboldcpp_openblas.dll       |          ✓           |       ✓       |                      |         ✓          |
| koboldcpp_failsafe.dll       |          ✓           |       ✓       |          ✓           |         ✓          |
| koboldcpp_noavx2.dll         |          ✓           |       ✓       |          ✓           |         ✓          |
| libopenblas.dll              |          ✓           |       ✓       |                      |         ✓          |
| koboldcpp_clblast.dll        |          ✓           |       ✓       |          ✓           |         ✓          |
| koboldcpp_clblast_noavx2.dll |          ✓           |       ✓       |          ✓           |         ✓          |
| koboldcpp_vulkan_noavx2.dll  |          ✓           |       ✓       |          ✓           |         ✓          |
| clblast.dll                  |          ✓           |       ✓       |          ✓           |         ✓          |
| koboldcpp_vulkan.dll         |          ✓           |       ✓       |          ✓           |         ✓          |
| vulkan-1.dll                 |          ✓           |       ✓       |          ✓           |         ✓          |
| koboldcpp_cublas.dll         |                      |       ✓       |          ✓           |         ✓          |
| cublas64_11.dll              |                      |       ✓       |          ✓           |                    |
| cublasLt64_11.dll            |                      |       ✓       |          ✓           |                    |
| cudart64_110.dll             |                      |       ✓       |          ✓           |                    |
| cublas64_12.dll              |                      |               |                      |         ✓          |
| cublasLt64_12.dll            |                      |               |                      |         ✓          |
| cudart64_12.dll              |                      |               |                      |         ✓          |
| msvcp140.dll                 |                      |       ✓       |          ✓           |         ✓          |
| msvcp140_codecvt_ids.dll     |                      |       ✓       |          ✓           |         ✓          |
| vcruntime140.dll             |                      |       ✓       |          ✓           |         ✓          |
| vcruntime140_1.dll           |                      |       ✓       |          ✓           |         ✓          |

## KoboldAI Misc.

| Mode                      | Required DLLs                                                                               |
|---------------------------|----------------------------------------------------------------------------------------------|
| **Default/No acceleration**| koboldcpp_default.dll                                                                        |
| **OpenBLAS**              | koboldcpp_openblas.dll<br>libopenblas.dll (must exist alongside)                             |
| **CLBlast**               | koboldcpp_clblast.dll<br>clblast.dll (must exist alongside)<br>OpenCL.dll (implied by Makefile's use of OpenCL.lib) |
| **CuBLAS (NVIDIA GPU acceleration)**| koboldcpp_cublas.dll<br>cuda.dll<br>cublas.dll<br>cudart.dll<br>cublasLt.dll           |
| **HipBLAS (AMD GPU acceleration)**| koboldcpp_hipblas.dll<br>Additional AMD ROCm libraries (not explicitly listed in Makefile) |
| **Vulkan**                | koboldcpp_vulkan.dll<br>vulkan-1.dll                                                         |
| **NoAVX2 variants (for older CPUs)**| koboldcpp_noavx2.dll<br>koboldcpp_clblast_noavx2.dll (requires same dependencies as CLBlast)<br>koboldcpp_vulkan_noavx2.dll (requires same dependency as Vulkan) |
| **Failsafe mode**         | koboldcpp_failsafe.dll                                                                       |


# Kobold AI API Documentation

## Required Arguments

- `--model [filename]`: Model file to load.
- `--port [portnumber]`: Port to listen on.
- You can use the foregoing as "positional" arguments but just using the flags makes things more uniform.

## Optional Arguments

- `--config [filename]`: Load settings from a `.kcpps` file. Other arguments will be ignored.
- `--noavx2`: Do not use AVX2 instructions; enables a slower compatibility mode for older devices.
- `--nommap`: If set, do not use `mmap` to load newer models.
- `--usemlock`: For Apple systems. Forces the system to keep the model in RAM rather than swapping or compressing. On systems with limited RAM, setting `--usemlock` can prevent frequent memory swapping and improve performance. Disabled by default.
- `--skiplauncher`: Doesn't display or use the GUI launcher.
- `--quiet`: Enable quiet mode, which hides generation inputs and outputs in the terminal. Quiet mode is automatically enabled when running a horde worker.
- `--onready [shell command]`: An optional shell command to execute after the model has been loaded.
  - This is an advanced parameter intended for script or command line usage. You can pass a terminal command (e.g., start a Python script) to be executed after Koboldcpp has finished loading. This runs as a subprocess and can be useful for starting Cloudflare tunnels, displaying URLs, etc.
  - Example: `--onready "python script.py"` runs the specified Python script after the model is loaded.
- `--threads [number]`: Specifies the number of CPU threads to use for text generation.
  - If a number is not specified a default value is calculated.
    - If CPU core count > 1: Uses half the physical cores, with a minimum of 3 and maximum of (physical cores - 1)
    - For systems with 1 core: Uses 1 thread.
  - Intel CPU Specific: For Intel processors, the maximum default is capped at 8 threads to avoid using efficiency cores
  - Usage: `--threads [number]`
    - Note: If not specified, the program uses the calculated default value

## --usecublas

The `--usecublas` argument enables GPU acceleration using CuBLAS (for NVIDIA GPUs) or hipBLAS (for AMD GPUs). For hipBLAS binaries, check the YellowRoseCx ROCm fork.

### Usage:

- `--usecublas [lowvram|normal] [main GPU ID] [mmq] [rowsplit]`
- Example: `--usecublas lowvram 0 mmq rowsplit`

### Optional Parameters:

- `lowvram` or `normal`
  - `lowvram`: Prevents offloading to the GPU the KV layers. Suitable for GPUs with limited memory.
  - `normal`: Default mode.
- `main GPU ID`: A number (e.g. 0, 1, 2, or 3) selecting a specific GPU. If not specified, all available GPUs will be used.
- `mmq`: Uses “quantized matrix multiplication” during prompt processing instead of cuBLAS. This is slightly faster and uses slightly less memory for Q4_0, but is slower for K-quants. Generally, cuBLAS is faster but uses slightly more VRAM.
- `rowsplit`: If multiple GPUs are being used, splitting occurs by “rows” instead of “layers,” which can be beneficial on some older GPUs.

### Unique Features:

- Can use `--flashattention`, which can be faster and more memory efficient.
  - If `--flashattention` is used `--quantkv [level]` can also be used but “context shifting” will be disabled. Here, level 0=f16, 1=q8, 2=q4.

## --usevulkan

Enables GPU acceleration using Vulkan, which is compatible with a broader range of GPUs and iGPUs. See more info at [Vulkan GPU Info](https://vulkan.gpuinfo.org/).

### Optional Parameter:

- `Device ID`: An integer specifying which GPU device to use. If not provided, it defaults to the first available Vulkan-compatible GPU.

### Usage:

- `--usevulkan [Device ID]`
- Example: `--usevulkan 0`

## Using Multiple GPUs

The program first determines how many layers are computed on the GPU(s) based on `--gpulayers`. Those layers are split according to the `--tensor_split` parameter. Layers not offloaded will be computed on the CPU. It is possible to specify `--usecublas`, `--usevulkan`, or `--useclblast` and not specify `--gpulayers`, in which case the prompt processing will occur on the GPU(s) but the per-token inference will not.

### Not Specifying GPU IDs:

- By default, if no GPU IDs are specified after `--usecublas` or `--usevulkan`, all compatible GPUs will be used and layers will be distributed equally.
  - NOTE: This can be bad if the GPUs are different sizes.
- Use `--tensor_split` to control the ratio, e.g., `--tensor_split 4 1` for an 80%/20% split on two GPUs.
- The number of values in `--tensor_split` should match the total number of available GPUs.

### Specifying a Single GPU ID:

- Don't use `--tensor_split`. However, you can still use `--gpulayers`.

### Specifying Some GPUs and Offloading Layers to Those GPUs:

- If some (but not all) GPU IDs are provided after `--usecublas` or `--usevulkan`, only those GPUs will be used for layer offloading.
- Use `--tensor_split` to control the distribution ratio among the specified GPUs.
- The number of values in `--tensor_split` should match the number of GPUs selected.
  - Example: With four GPUs available but only specifying the last two with `--usecublas 2 3`, using `--tensor_split 1 1` would offload an equal amount of layers to the third and fourth GPUs but none to the first two.

### Specifying Some GPUs to Process Layers While Allowing Other GPUs for Prompt Processing:

- Use `--usecublas` or `--usevulkan` without specifying the GPU Ids, which makes available all GPUs for prompt processing.
- Only assign layers to certain GPUs.  Example: Using `--usecublas` and `--tensor_split 5 0 3 2` will offload 50% of the layers to the first GPU, 30% to the third, and 20% to the fourth.  However, the second GPU will still be available for other processing that doesn't require layers of the model.

### Usage with `--useclblast`:

- `--gpulayers` is supported by `--useclblast` but `--tensor_split` is not.

## --useclblast

Enables GPU acceleration using CLBlast, based on OpenCL. Compatible with a wide range of GPUs including NVIDIA, AMD, Intel, and Intel iGPUs. More info can be found at [CLBlast README](https://github.com/CNugteren/CLBlast/blob/master/README.md).

### Required Arguments:

- `Platform ID`: An integer between 0 and 8 (inclusive).
- `Device ID`: An integer between 0 and 8 (inclusive).

### Usage:

- `--useclblast [Platform ID] [Device ID]`
  - Platform ID: An integer between 0 and 8 (inclusive).
  - Device ID: An integer between 0 and 8 (inclusive).
- Both arguments are required.
- Example: `--useclblast 1 0`
  - The API instructions are unclear whether more than one compatible device can be specified. In any event, `--tensor_split` cannot be used.

## OpenBLAS:

- Only used by CPU, not GPU.
- Enabled in Windows by default, but other platforms require a separate installation.

## BLAS Configuration

All BLAS acceleration (including OpenBLAS) can be disabled using `--noblas` or `--blasbatchsize -1`. Setting to -1 disables BLAS mode but retains other benefits like GPU offload.

### --blasbatchsize

Sets the batch size used in BLAS processing.

- Default: 512
- Options: -1, 32, 64, 128, 256, 512, 1024, 2048

### --blasthreads

Specifies the number of threads to use during BLAS processing.

- If not specified, it uses the same value as `--threads`.
- If left blank, it will automatically set to a value slightly less than the CPU count.
- Recommendation: When running with full GPU offload, setting it to 1 thread may be sufficient.

## Samplers in KoboldCpp

Samplers determine how the AI selects the next token from a list of possible tokens. There are various samplers with different properties, but generally, you will only need a few.

### Sampler Order:

- Controls the sequence in which samplers are applied to the list of token candidates when choosing the next token.
- Hardcoded into the source code as `[6,0,1,3,4,2,5]` to avoid poor outputs (0 = Top K  1 = Top P, 2 = Typical P, 3 = Top A, 4 = Min P, 5 = Temperature, 6 = TFS) 
- Don't change.

### Good Default Settings:

- `top_p`: 0.92
- `rep_pen`: 1.1
- `Temperature`: 0.7
- Leave everything else disabled by default

### Sampler Descriptions:

1. **Top-K**: 
   - Parameter: `top_k`
   - Function: Limits the number of possible words to the top K most likely options, removing everything else.
   - Usage: Can be used with Top-P. Set value to 0 to disable its effect.
2. **Top-A**: 
   - Parameter: `top_a`
   - Function: Alternative to Top-P. Removes all tokens with a softmax probability less than `top_a * m^2` where `m` is the maximum softmax probability.
   - Usage: Set value to 0 to disable its effect.
3. **Top-P**: 
   - Parameter: `top_p`
   - Function: Discards unlikely text during sampling. Considers words with the highest cumulative probabilities summing up to P.
   - Effect: Low values make the text predictable by removing uncommon tokens.
   - Usage: Set value to 1 to disable its effect.
4. **TFS (Top-Filter Sampling)**: 
   - Parameter: `tfs`
   - Function: Alternative to Top-P. Removes the least probable words from consideration, using second-order derivatives.
   - Benefit: Can improve the quality and coherence of generated text.
5. **Typical**: 
   - Parameter: `typical_p`
   - Function: Selects words randomly with equal probability.
   - Effect: Produces more diverse but potentially less coherent text.
   - Usage: Set value to 1 to disable its effect.
6. **Temperature**: 
   - Parameter: `temperature`
   - Function: Controls the randomness of the output by scaling probabilities without removing options.
   - Effect: Lower values produce more logical, less creative text.
7. **Repetition Penalty**: 
   - Parameter: `rep_pen`
   - Function: Applies a penalty to reduce the usage of recently used words, making the output less repetitive.

## --contextsize

- Controls the memory allocated for maximum context size. Adjust this if you need more RAM for larger contexts.
- Default: 4096
- Supported Values:
  - 256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 12288, 16384, 24576, 32768, 49152, 65536, 98304, 131072
- Warning: Use values outside the supported range at your own risk.

### Usage:

- `--contextsize [Value]`
- Example: `--contextsize 8192` allocates memory for a context size of 8192.

## Context Shifting

Context Shifting is a better version of Smart Context that only works for GGUF models. This feature utilizes KV cache shifting to automatically remove old tokens from context and add new ones without requiring any reprocessing. It is on by default. To disable Context Shifting, use the flag `--noshift`.

## Streaming

KoboldCpp now supports a variety of streaming options. Kobold Lite UI supports streaming out of the box, which can be toggled in Kobold Lite settings. Note: the `--stream` parameter is now deprecated and should not be used.

### Streaming Methods:

1. **Polled-Streaming (Recommended)**:
   - Default Method: Used by the Kobold Lite UI.
   - Mechanism: Polls for updates on the `/api/extra/generate/check` endpoint every second.
   - Advantages: Relatively fast and simple to use.
   - Drawback: Some may find it a bit "chunky" as it does not update instantaneously for every single token.
2. **Pseudo-Streaming**:
   - Status: An older method no longer recommended due to performance overheads.
   - Usage with Kobold Lite: Enable streaming and append `&streamamount=x` to the end of the Lite URL, where `x` is the number of tokens per request.
   - Drawback: Has a negative performance impact.
3. **SSE (True Streaming)**:
   - Supported by: A few third-party clients such as SillyTavern and Agnaistic, available only via the API.
   - Mechanism: Provides instantaneous per-token updates.
   - Requirements: Requires a persistent connection and special handling on the client side with SSE support.
   - Usage: This mode is not used in Lite or the main KoboldAI client. It uses a different API endpoint, so configure it from your third-party client according to their provided instructions.
