# Windows 安装与运行

适用于 Windows 10/11 x64。下载 Releases 中的 `Tide-workstation-Windows-x64-preview.84.zip`，完整解压到有写入权限的目录，运行 `data_collector_workstation.exe`。请保留同目录的 DLL 和 `data` 文件夹。

## 发布内容

程序使用机械臂 Logo，窗口和任务栏图标采用同一图案。软件包含 Flutter 桌面程序、视频播放组件，以及 TideWorkstation 自有的 collector-agent Python 模块和启动脚本。应用通过发现的 Python 环境运行随包 Sidecar。

第三方 Python、LeRobot、PyTorch 和模型权重需要单独准备。以下命令面向新建的 Python 3.12 环境，在 PowerShell 中执行。Python 环境位于当前用户目录，软件解压位置可自行选择。

## 1. 安装 Python 3.12

已有 Python 3.12 时可直接验证。

```powershell
winget install --exact --id Python.Python.3.12
```

重新打开 PowerShell，验证版本。

```powershell
py -3.12 --version
```

## 2. 创建第三方运行环境

以下目录属于应用自动查找的路径。已有该环境时保留目录，跳过创建命令，直接验证其中的依赖。

```powershell
$runtime = Join-Path $env:LOCALAPPDATA 'EmbodyData\unified-runtime\lerobot-0.6.0'
if (Test-Path $runtime) { throw '目标环境已存在，请按下方已有环境说明检查后复用' }
py -3.12 -m venv $runtime
if ($LASTEXITCODE -ne 0) { throw '创建环境失败，请先处理错误' }
$python = Join-Path $runtime 'Scripts\python.exe'
& $python -m pip install --upgrade pip setuptools wheel
```

## 3. 安装 PyTorch 和 LeRobot

以下 PyTorch CUDA 12.8 wheel 用于兼容的 NVIDIA GPU。硬件驱动由用户管理，PyTorch wheel 提供其需要的 CUDA 用户态运行库。

```powershell
& $python -m pip install torch==2.11.0 torchvision==0.26.0 --index-url https://download.pytorch.org/whl/cu128
& $python -m pip install 'lerobot[core_scripts,dataset,training,feetech,deepdiff-dep]==0.6.0' 'opencv-python==4.13.0.92' 'cv2-enumerate-cameras==1.3.3' 'rerun-sdk==0.33.1' 'h5py>=3.10,<4' 'PyYAML>=6,<7' 'websockets>=13,<16'
```

使用 CPU 时，将上面的 PyTorch 安装命令替换为以下命令。CPU 训练和推理的速度取决于硬件与模型规模。

```powershell
& $python -m pip install torch==2.11.0 torchvision==0.26.0 --index-url https://download.pytorch.org/whl/cpu
```

需要 SmolVLA 时，额外安装其依赖，并准备对应预训练权重。

```powershell
& $python -m pip install 'lerobot[smolvla]==0.6.0'
```

验证安装。

```powershell
& $python -c "import importlib.metadata as m; import cv2, cv2_enumerate_cameras, serial, torch, h5py, websockets; from lerobot.cameras.opencv import OpenCVCameraConfig; from lerobot.robots.so_follower.so_follower import SO101Follower; print('LeRobot:', m.version('lerobot')); print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('OpenCV:', cv2.__version__)"
```

ACT 和 SmolVLA 需要提前准备权重。训练与推理使用产品指定缓存，SmolVLA 以本地缓存模式检查指定 revision。请完成下方的应用环境检查和权重准备步骤。

## 4. 启动软件

运行解压目录中的 `data_collector_workstation.exe`，选择本地模式，完成设备配置、校准与遥操作，再开始采集。软件会查找上述运行环境，并运行随包 collector-agent。采集、训练和模型推理都使用该环境。

如果系统提示缺少 `VCRUNTIME140.dll` 或 `MSVCP140.dll`，安装 Microsoft Visual C++ 2015–2022 Redistributable x64。

```powershell
winget install --exact --id Microsoft.VCRedist.2015+.x64
```

下载包附有 `SHA256SUMS-Windows.txt`。可通过以下命令核验压缩包哈希。

```powershell
Get-FileHash .\Tide-workstation-Windows-x64-preview.84.zip -Algorithm SHA256
```

## 验证范围

此包为 Windows x64 预览构建。发布时执行构建产物与资源完整性检查、针对性自动化测试和压缩包校验。全新 Windows 电脑上的安装、真实设备采集、训练和推理全流程仍需进一步验收。

## 已有环境和路径接入

可复制 [README 中的 AI 提示词](../README.md#用-ai-处理-windows-运行环境)，让 AI 检查并接入已有环境。

当前自动发现的统一入口是 `%LOCALAPPDATA%\EmbodyData\unified-runtime\lerobot-0.6.0\Scripts\python.exe`。已验证兼容的 Windows venv 可通过目录 Junction 接入。入口已存在时，先确认其用途和依赖，再决定如何处理。

Windows Conda 环境通常把 `python.exe` 放在环境根目录，当前发现代码查找 `Scripts\python.exe`。AI 应检查真实布局，再选择合适方式。对于这种 Conda 布局，建议在约定入口创建独立 Python 3.12 venv。将 Conda 根目录直接链接到入口无法满足当前路径要求。

采集、训练和推理的默认配置共用环境发现逻辑。旧配置中的 Sidecar 可执行路径、前缀参数、工作目录，以及 `TIDE_COLLECTOR_AGENT_EXECUTABLE` / `SO101_RUNTIME_EXECUTABLE` 覆盖项可能改变实际入口。升级用户需要由 AI 核对这些设置。确认环境后完全退出再启动应用，让常驻进程使用新配置。

## 应用环境检查和 ACT 权重

先完整解压并打开一次软件，让应用释放随包 Sidecar，再完全退出。随后在 PowerShell 执行以下命令。检查脚本读取随包 Sidecar 的缓存计算函数，支持目录链接后的实际路径。

```powershell
$runtime = Join-Path $env:LOCALAPPDATA 'EmbodyData\unified-runtime\lerobot-0.6.0'
$python = Join-Path $runtime 'Scripts\python.exe'
$sidecar = Join-Path $env:LOCALAPPDATA 'EmbodyData\sidecar'
$check = Join-Path $env:TEMP 'tide-check-environment.py'
Invoke-WebRequest 'https://raw.githubusercontent.com/Allentide/Tide-workstation/main/tools/check_environment.py' -OutFile $check
& $python $check --sidecar-root $sidecar
```

首次检查可能报告缺少 ACT 权重。确认联网下载后执行下一条命令，它会将当前 ACT 默认的 ResNet18 权重放到应用实际使用的缓存，并校验和加载该文件。

```powershell
& $python $check --sidecar-root $sidecar --download-act
& $python (Join-Path $sidecar 'scripts\collector-agent') training-capabilities
```

选择 SmolVLA 并安装其依赖后，可经授权下载产品锁定的两组完整权重，再做本地缓存检查。下载可能达到数 GB。

```powershell
& $python $check --sidecar-root $sidecar --download-smolvla
& $python $check --sidecar-root $sidecar --smolvla
```

脚本检查 Python/依赖版本、三个 LeRobot 入口的导入、加速设备张量运算、默认 AV1 视频编码解码，以及 ACT 缓存和依赖冲突。它仅在临时目录写入测试视频，`--download-act` 明确开启权重下载。每个 `FAIL` 都需要处理后重跑。

普通新建环境的 Torch 缓存通常在 `%LOCALAPPDATA%\EmbodyData\unified-runtime\torch-cache`。目录链接和既有 `TORCH_HOME` / `HF_HOME` 会影响真实缓存位置，以脚本输出和软件进程环境为准。脚本通过后，仍需核对软件日志或 Sidecar 进程实际使用的 Python 与该脚本一致。

## 全流程验收

让 AI 逐项记录结果，由用户确认硬件动作后执行。

1. 软件重启后，核对 Sidecar 解释器、版本、缓存和权重，与环境检查输出一致。
2. 连接设备并采集一个短 Episode，正常保存 Session，能在数据集页面回放相机画面和关节数据。
3. 使用该 Episode 新建 ACT 冒烟训练，例如 100 步、Batch size 1、数据加载进程 0，确认实际 Loss 日志和最终 `pretrained_model` 文件。此参数仅用于验证流程。
4. 从模型库选择刚生成的模型，先核对相机字段、完整检查点、设备组与校准状态。使用少量数据得到的冒烟模型行为可能无意义，实际机器人执行需用户确认场地和急停条件。
5. 经用户确认后完成一次短推理和手动停止，核对模型加载设备、记录数据保存、设备释放结果。

环境脚本全通过仅代表环境检查完成。完成上述软件和硬件步骤后，才能记录该电脑全流程通过。
