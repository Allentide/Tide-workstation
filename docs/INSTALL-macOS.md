# macOS 安装说明

本说明适用于 Apple Silicon（M 系列芯片）Mac。建议使用较新的 macOS，训练建议至少 16 GB 统一内存。具体系统兼容性仍受 PyTorch 等第三方包限制；Intel Mac 暂不在本版验证范围。

希望让 AI 协助安装，可复制 [README 中的 macOS 环境准备提示词](../README.md#用-ai-帮你准备-macos-环境)。提示词按本说明的标准目录和版本执行，不适配其他项目的环境。

## 1. 下载应用

从 [Releases](https://github.com/Allentide/Tide-workstation/releases) 下载 `Tide-workstation-macOS-preview.83.zip`，双击解压，将 `data_collector_workstation.app` 拖到“应用程序”。不要下载 GitHub 自动生成的 `Source code.zip`，它只有发布文档。

此预览版未做 Apple Developer ID 公证。若 macOS 阻止打开，确认文件来自本仓库并校验下载后，可在“系统设置 → 隐私与安全性”使用系统提供的“仍要打开”。无需关闭系统整体安全检查。

## 2. 安装一次运行环境

软件包已自带 collector-agent / Sidecar。新用户仅需安装第三方运行环境，不需要源码、不需要单独安装 collector-agent，也不需要 Flutter。

先按 [Homebrew 官方说明](https://brew.sh/)安装 Homebrew；安装完成后打开新终端，确认 `brew --version` 可执行。

下面命令使用 Homebrew Python 3.12 创建独立环境，不使用 Conda。首次安装需要联网下载依赖，可能耗时较长。若终端已激活其他虚拟环境，请先退出该环境再执行。

```bash
(
  set -e
  brew install python@3.12

  TIDE_RUNTIME="$HOME/Library/Application Support/EmbodyData/unified-runtime/lerobot-0.6.0"
  TIDE_PYTHON="$(brew --prefix python@3.12)/bin/python3.12"

  "$TIDE_PYTHON" -c 'import platform; assert platform.machine() == "arm64", "请使用 Apple Silicon 原生终端与 Homebrew Python"'
  if [ ! -x "$TIDE_RUNTIME/bin/python" ]; then
    "$TIDE_PYTHON" -m venv "$TIDE_RUNTIME"
  fi

  "$TIDE_RUNTIME/bin/python" -m pip install --upgrade pip setuptools wheel
  "$TIDE_RUNTIME/bin/python" -m pip install \
    "torch==2.11.0" "torchvision==0.26.0" \
    "lerobot[core_scripts,dataset,training,feetech]==0.6.0" \
    "accelerate" "opencv-python==4.13.0.92" \
    "cv2-enumerate-cameras==1.3.3" \
    "h5py>=3.10,<4" "numpy>=2.0,<2.3" \
    "PyYAML>=6,<7" "websockets>=13,<16" \
    "rerun-sdk==0.33.1" "pyserial>=3.5,<4"

  "$TIDE_RUNTIME/bin/python" -c 'import platform, sys, torch, lerobot, cv2, av, serial, h5py, accelerate; print("CPU:", platform.machine()); print("Python:", sys.executable); print("LeRobot:", lerobot.__version__); print("PyTorch:", torch.__version__); print("MPS:", torch.backends.mps.is_available())'
)
```

成功时应显示 `arm64`、LeRobot `0.6.0` 和环境内的 Python 路径。`MPS: True` 表示可使用 Apple GPU；若为 False，先检查系统与 PyTorch 支持情况。不要在 Mac 上安装 CUDA 版 PyTorch。

以后从 Finder 打开软件即可，应用会查找上面的固定用户环境路径，无需每次手动激活。需要终端排查时可执行：

```bash
source "$HOME/Library/Application Support/EmbodyData/unified-runtime/lerobot-0.6.0/bin/activate"
```

以上依赖安装方式沿用开发机配置，尚未在全新 Mac 上完成验证。OpenCV 与 PyAV 在 macOS 上可能出现 `AVFFrameReceiver` 重复加载警告；开发机训练曾在该警告后继续推进，但不能据此保证所有设备稳定。遇到真实崩溃请附错误栈反馈，不要直接删除动态库。

## 3. 首次启动与权限

打开 `.app`，进入本地模式。首次访问相机时允许系统相机权限；若拒绝，可在“系统设置 → 隐私与安全性 → 相机”修改后重新打开软件。

SO-101 主从臂通过 USB 连接，串口一般显示为 `/dev/cu.*`。发现不到串口时检查数据线、USB 集线器和转接芯片对应的 macOS 驱动。基础安装面向 USB/UVC 相机，RealSense 的 macOS 驱动和 SDK 未包含在基础安装范围。

## 4. 训练所需权重

ACT 首次训练可能需要联网下载 ResNet18 预训练权重。此发布包没有附带权重，也不承诺首次启动断网可训练。

本版默认 ACT 使用 `ResNet18_Weights.IMAGENET1K_V1`。软件未收到 `TORCH_HOME` 覆盖时，使用 `~/Library/Application Support/EmbodyData/unified-runtime/torch-cache`，权重文件位于其 `hub/checkpoints` 下。请让 AI 在这个缓存位置准备并验证权重，不要只放在终端默认的 `~/.cache/torch`。已有 `TORCH_HOME` / `HF_HOME` 时，应先核对软件进程实际使用的位置，不能仅以当前终端的下载成功作为依据。

SmolVLA 还需要额外依赖和两组指定版本的权重。计划使用时，在同一环境执行：

```bash
source "$HOME/Library/Application Support/EmbodyData/unified-runtime/lerobot-0.6.0/bin/activate"
python -m pip install 'lerobot[smolvla]==0.6.0'
python - <<'PY'
from pathlib import Path
from huggingface_hub import snapshot_download

cache = Path.home() / "Library/Application Support/EmbodyData/huggingface-cache/hub"
for repo, revision in [
    ("lerobot/smolvla_base", "c83c3163b8ca9b7e67c509fffd9121e66cb96205"),
    ("HuggingFaceTB/SmolVLM2-500M-Video-Instruct", "7b375e1b73b11138ff12fe22c8f2822d8fe03467"),
]:
    snapshot_download(repo_id=repo, revision=revision, cache_dir=str(cache))
print("SmolVLA 权重下载完成")
PY
```

这是用户主动联网下载步骤，需要足够磁盘空间；权重许可见各模型页面。软件的 SmolVLA 预检查使用本地缓存，缺少权重时会报错。

## 5. 更新与数据位置

更新前先结束采集、训练和推理，再按 `Command + Q` 完全退出软件，替换“应用程序”中的 `.app`。保留以下用户目录：

- `~/Library/Preferences/com.ioai.dataCollectorWorkstation.plist`：设备组等偏好配置。
- `~/Library/Application Support/com.ioai.dataCollectorWorkstation/lerobot/calibration/`：机械臂校准文件。
- `~/Library/Application Support/EmbodyData/`：运行环境、Sidecar 与缓存。
- `~/Documents/recordings/`、`~/Documents/models/`、`~/Documents/training_state/`：默认采集、模型及训练状态目录。

不要通过删除这些目录解决升级问题。若设备列表暂时为空，先完全退出再重开，确认当前运行的是新版本。

## 6. 校验下载

Release 提供 `SHA256SUMS.txt`。将它与 ZIP 放在同一目录后执行：

```bash
shasum -a 256 -c SHA256SUMS.txt
```

输出 `OK` 表示下载文件与发布校验值一致。
