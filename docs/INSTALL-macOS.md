# macOS 安装说明

本说明适用于 Apple Silicon（M 系列芯片）Mac。建议使用较新的 macOS，训练建议至少 16 GB 统一内存。具体系统兼容性仍受 PyTorch 等第三方包限制；Intel Mac 暂不在本版验证范围。

希望让 AI 协助安装或复用已有环境，可复制 [README 中的 macOS 环境准备提示词](../README.md#用-ai-帮你准备-macos-环境)。AI 应先检查实际解释器、依赖和路径，再选择复用或新建。

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

  "$TIDE_RUNTIME/bin/python" -c 'import importlib.metadata as m; import platform, sys, torch, cv2, av, serial, h5py, accelerate; print("CPU:", platform.machine()); print("Python:", sys.executable); print("LeRobot:", m.version("lerobot")); print("PyTorch:", torch.__version__); print("MPS:", torch.backends.mps.is_available())'
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

ACT 训练前需准备 ResNet18 预训练权重。请按下方检查命令，将权重下载并验证到应用实际使用的缓存。

本版默认 ACT 使用 `ResNet18_Weights.IMAGENET1K_V1`。软件未收到 `TORCH_HOME` 覆盖时，使用 `~/Library/Application Support/EmbodyData/unified-runtime/torch-cache`，权重文件位于其 `hub/checkpoints` 下。请让 AI 在这个缓存位置准备并验证权重，不要只放在终端默认的 `~/.cache/torch`。已有 `TORCH_HOME` / `HF_HOME` 时，应先核对软件进程实际使用的位置，不能仅以当前终端的下载成功作为依据。

SmolVLA 需要额外依赖和两组指定版本的权重。计划使用时，在同一环境安装依赖，然后完成第 8 节的检查和权重下载。

```bash
"$HOME/Library/Application Support/EmbodyData/unified-runtime/lerobot-0.6.0/bin/python" -m pip install 'lerobot[smolvla]==0.6.0'
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

## 7. 复用已有环境

统一入口为 `$HOME/Library/Application Support/EmbodyData/unified-runtime/lerobot-0.6.0/bin/python`。已有 Apple Silicon 原生 Python 3.12 venv 或 Conda 环境可在完整验证后，通过符号链接接入该入口的环境根目录。AI 应先确认目标包含可运行的 `bin/python`，依赖版本匹配，并检查路径链接和原目录用途。入口已存在时，先核对再处理。

Finder 启动的应用通常具有不同于交互式终端的环境。仅在终端激活环境、修改 shell 配置或设置 `TORCH_HOME` / `HF_HOME`，不能证明 Finder 应用使用了相同配置。优先通过上述入口接入，随后重启应用，核对实际 Sidecar 进程与缓存路径。

旧 Sidecar 路径、前缀参数、工作目录及 `TIDE_COLLECTOR_AGENT_EXECUTABLE` / `SO101_RUNTIME_EXECUTABLE` 覆盖项也需要检查。环境、Sidecar、校准、数据和模型路径都应使用当前 Mac 的有效路径。由 Windows 复制过来的配置若包含盘符路径，应通过软件重新选择或导入对应资源。

## 8. 应用环境检查和 ACT 权重

先打开一次 `.app` 释放随包 Sidecar，再完全退出。以下命令在 zsh 中执行，所有带空格的路径都保留双引号。

```bash
TIDE_RUNTIME="$HOME/Library/Application Support/EmbodyData/unified-runtime/lerobot-0.6.0"
TIDE_SIDECAR="$HOME/Library/Application Support/EmbodyData/sidecar"
TIDE_CHECK="$(mktemp -t tide-check-environment)"
curl --fail --location 'https://raw.githubusercontent.com/Allentide/Tide-workstation/main/tools/check_environment.py' -o "$TIDE_CHECK"
"$TIDE_RUNTIME/bin/python" "$TIDE_CHECK" --sidecar-root "$TIDE_SIDECAR"
```

确认下载 ACT 权重后执行以下命令。检查脚本从当前 Sidecar 读取缓存规则，因此复用符号链接环境时也能按真实目录准备权重。

```bash
"$TIDE_RUNTIME/bin/python" "$TIDE_CHECK" --sidecar-root "$TIDE_SIDECAR" --download-act
"$TIDE_RUNTIME/bin/python" "$TIDE_SIDECAR/scripts/collector-agent" training-capabilities
```

选择 SmolVLA 并安装其依赖后，可经授权下载产品锁定的两组完整权重，再做本地缓存检查。下载可能达到数 GB。

```bash
"$TIDE_RUNTIME/bin/python" "$TIDE_CHECK" --sidecar-root "$TIDE_SIDECAR" --download-smolvla
"$TIDE_RUNTIME/bin/python" "$TIDE_CHECK" --sidecar-root "$TIDE_SIDECAR" --smolvla
```

脚本验证 Python 和依赖、LeRobot 采集/训练/推理入口导入、实际加速设备张量运算、默认 AV1 视频编码解码、ACT 权重校验加载以及 `pip check`。相机和机械臂由用户后续在软件中连接。检查结果为 `FAIL` 时先处理具体错误。

Apple GPU 是否实际参与训练或推理，还要核对任务日志中的最终 `device`。当前启动配置可能请求 CUDA，LeRobot 0.6 在该设备不可用时会结合策略配置重新选择设备。`MPS: True` 说明 MPS 可用，实际模型前向/反向与运行性能需要任务验证。

## 9. 全流程验收

让 AI 核对 Finder 启动的软件使用了上述解释器和缓存，再由用户确认硬件操作。

1. 完成相机权限、设备组、校准和遥操作验证，保存一个短 Episode 并成功回放视频和关节数据。
2. 用该 Episode 执行 ACT 冒烟训练，例如 100 步、Batch size 1、数据加载进程 0，确认 Loss 更新和最终检查点生成。记录训练日志中的实际 `device`。
3. 在模型库查看该检查点，核对相机字段、完整模型处理器文件和本机校准。少量数据得到的冒烟模型行为可能无意义，实际执行需用户确认场地及急停条件。
4. 经用户确认后完成短推理和手动停止，检查实际推理设备、推理数据集保存与硬件释放。

脚本全通过仅代表环境检查完成。Apple Silicon 真机的采集、训练和推理需分别验收。当前文档更新在 Windows 上验证了检查脚本，macOS 执行结果仍需目标 Mac 确认。
