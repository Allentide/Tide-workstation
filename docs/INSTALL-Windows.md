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
py -3.12 -m venv $runtime
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

ACT 使用的视觉骨干权重和 SmolVLA 权重会占用额外磁盘空间。首次训练前需确保相应权重已经准备好，或网络能够访问权重来源。

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
