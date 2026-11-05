# Tide Workstation

<img src="assets/logo.png" width="128" alt="Tide Workstation 机械臂图标">

这是我开发的机械臂数据采集软件，免费分享给想要学习具身智能的爱好者朋友们。

从连接机械臂、采集演示数据，到回放检查、训练和运行模型，在一个桌面工作站里完成。

**[下载 Windows 应用](https://github.com/Allentide/Tide-workstation/releases/tag/v1.0.0-windows-preview.84) · [Windows 安装说明](docs/INSTALL-Windows.md) · [下载 macOS 应用](https://github.com/Allentide/Tide-workstation/releases) · [安装说明](docs/INSTALL-macOS.md) · [使用说明](docs/USAGE.md) · [反馈问题](https://github.com/Allentide/Tide-workstation/issues)**

## 主要功能

- 设备配置：发现主从臂串口、添加相机、保存设备组。
- 校准与遥操作：调用 LeRobot 0.6.0 官方 SO-101 校准和控制流程。
- 数据采集：创建采集任务、实时预览、按 Episode 录制演示。
- 数据集管理：导入、回放、检查与标注数据。
- 模型训练：配置 ACT / SmolVLA 训练任务，查看进度与日志。
- 模型运行：管理本地模型，在已配置的设备组上进行推理验证。

## Windows 快速开始

1. 下载 Windows x64 预览包，完整解压，运行 `data_collector_workstation.exe`。
2. 按 [Windows 安装说明](docs/INSTALL-Windows.md)准备 Python 3.12、LeRobot 0.6.0 与 PyTorch 环境。
3. 进入本地模式，完成设备配置、校准和遥操作后开始采集。

## 用 AI 帮你准备 Windows 环境

将下面整段提示词复制给 AI。具备本机终端权限的 AI 可以在你授权后执行安装。使用普通聊天 AI 时，让它逐步给出 PowerShell 命令，你执行后把结果发回。

```text
请帮我在这台 Windows 10/11 x64 电脑上准备 Tide Workstation 的运行环境，让我能在软件中连接 SO-101 主从臂和相机、采集数据、训练 ACT 并运行模型推理。

先阅读该软件的 Windows 安装说明，以其中锁定的版本为准：
https://github.com/Allentide/Tide-workstation/blob/main/docs/INSTALL-Windows.md
如果无法访问，请让我粘贴文档内容后继续。

请按以下顺序处理：
1. 检查 Windows 版本、x64 架构、Python 3.12、GPU/驱动、可用磁盘空间及下述标准目录中的环境，给我简短结果。只按软件要求准备标准环境，不迁移、修改或适配其他项目的环境。
2. 当前版本使用 Python 3.12、LeRobot 0.6.0、PyTorch 2.11.0 和 torchvision 0.26.0，其他依赖按安装说明准备。标准目录中已有兼容环境时验证并补齐；不存在时创建。不兼容时先说明原因，未经同意不要删除重建。安装前告诉我下载内容、预计空间及目标目录。
3. 环境固定使用软件可自动发现的位置：%LOCALAPPDATA%\EmbodyData\unified-runtime\lerobot-0.6.0。PowerShell 中请通过 $env:LOCALAPPDATA 解析当前用户路径。软件解压位置可自由选择，不把环境放进随时可能被替换的应用目录。
4. 始终用目标环境的 Scripts\python.exe -m pip 安装依赖。仅从安装说明给出的 CUDA 12.8 或 CPU 构建中选择，不擅自升级版本，并实际检查 torch.cuda.is_available()。GPU 条件不足时说明影响，让我选择后续方案。
5. 按安装说明补齐相机、串口、视频读写和训练依赖。collector-agent 是 Tide Workstation 随包交付的自有组件，检查应用包中的 sidecar 模块与启动入口即可。安装说明中的第三方依赖由你协助准备。
6. 默认先完成 ACT 环境。核对已安装 LeRobot 0.6.0 的 ACTConfig；本版默认使用 resnet18 和 ResNet18_Weights.IMAGENET1K_V1。在得到我的下载授权后，准备到 %LOCALAPPDATA%\EmbodyData\unified-runtime\torch-cache（TORCH_HOME）下的 hub\checkpoints。检查已有 TORCH_HOME 是否会改变软件的实际缓存位置，不仅验证终端的默认缓存。SmolVLA 的依赖和权重等我明确选择使用时再准备，训练进程使用离线 Hugging Face 缓存，不能只凭“联网正常”判定权重已就绪。
7. 逐项执行验证，报告 Python 的实际路径、各依赖版本、CUDA 可用性、相机/串口模块导入结果、视频依赖及权重状态，并确认软件能够发现环境。
8. 安装或验证失败时先检查具体错误，再修复。保留已有环境、设备配置、校准文件、采集数据和模型。连接机械臂、启动力矩或运行推理前，先等我确认设备已准备好。

如果你有本机执行能力，在我的授权范围内直接处理。如果你只能提供文字，每次给我一个步骤的 PowerShell 命令，等待执行结果后再继续。最后列出已验证通过的项目和仍需我在软件中验证的步骤。
```

环境检查完成后，按“设备配置 → 采集 → 数据集管理 → 本地训练 → 模型库”的顺序使用软件。真实设备采集、训练和推理的完成情况需要分别验证。

## macOS 如何开始

1. 在 Releases 下载 `Tide-workstation-macOS-preview.83.zip`，解压后将 `.app` 拖到“应用程序”。
2. 按[安装说明](docs/INSTALL-macOS.md)安装 Python 3.12 与 LeRobot 0.6.0 环境，不需要 Conda、Flutter 或 Xcode 编译工程。
3. 打开软件，进入本地模式，依次完成设备配置、校准、遥操作验证和数据采集。

macOS 预览版面向 Apple Silicon Mac。应用二进制架构以 Release 说明为准；本文的训练运行时安装命令仅面向 Apple Silicon，未完成 Intel Mac 的端到端验证。

本地采集不需要云端账号。云端功能需要另行配置兼容服务端，本仓库不提供公共云服务。

## 用 AI 帮你准备 macOS 环境

适用于 Apple Silicon（M 系列芯片）Mac。将下面整段复制给 AI：有本机终端权限时可授权执行；普通聊天 AI 会逐步给出命令，由你在“终端”执行并反馈结果。

```text
请帮我在这台 Apple Silicon Mac 上准备 Tide Workstation 的标准运行环境，用于 SO-Arm101（SO-101）主从臂遥操作数据采集、回放和标注，以及 ACT 模型训练和推理。

先阅读本软件的 macOS 安装说明，以其中指定的依赖版本和目录为准：
https://github.com/Allentide/Tide-workstation/blob/main/docs/INSTALL-macOS.md
如果无法访问，请让我粘贴文档内容后继续，不要凭记忆换用其他版本。

请按以下顺序处理：
1. 检查 macOS 版本、芯片、当前进程架构、Homebrew、Python 3.12 和可用磁盘空间。确认使用 arm64 原生环境；若是 Intel Mac 或 Rosetta 下的 x86_64 环境，先说明本安装方案不适用，不混装两种架构。
2. 不使用 Conda，不修改其他项目的环境。按需准备 Homebrew、其要求的 Command Line Tools 和 Homebrew Python 3.12；不需要 Flutter 或完整 Xcode 来编译本应用。安装前列出下载内容、预计空间和目标目录，获得授权后再执行。不要修改全局 Python 指向或卸载现有环境。
3. 虚拟环境固定放在 "$HOME/Library/Application Support/EmbodyData/unified-runtime/lerobot-0.6.0"。所有带空格的路径必须加引号，用当前用户的 $HOME，不写死开发者用户名。仅在环境不存在时创建；已存在则检查其中的 Python 版本和依赖，不直接覆盖、删除或重建。
4. 始终使用目标环境的 bin/python -m pip 安装。按说明准备 Python 3.12、LeRobot 0.6.0、torch 2.11.0、torchvision 0.26.0，以及 OpenCV、相机枚举、Feetech、pyserial、PyAV、accelerate 等依赖。使用 macOS 原生 PyTorch，不使用 CUDA wheel，不擅自升级锁定版本。运行 pip check，发现冲突先解释具体原因。
5. collector-agent / Sidecar 已随 .app 交付，不另找同名第三方包安装，也不要求下载工程源码。软件首次启动会释放自有 Sidecar；使用标准目录里的 Python 运行它。不要把 Python 路径填进用于 collector-agent 可执行入口的环境变量，不依赖终端激活状态来让 Finder 启动的软件找到环境。
6. 先验证基础环境：报告 sys.executable、Python 架构和版本、LeRobot/PyTorch/torchvision 版本；验证 cv2、cv2_enumerate_cameras、serial、av、h5py、accelerate 及 SO101Follower 能否导入。检查 torch.backends.mps.is_available()，并尝试在 MPS 上创建一个小张量和完成运算。若为 False 或运算失败，报告实际错误，不能宣称 Apple GPU 已可用。模块能导入不等于真实硬件已通过测试。
7. 默认准备 ACT。核对本机 LeRobot 0.6.0 ACTConfig 的视觉骨干及权重，本版默认是 resnet18 / ResNet18_Weights.IMAGENET1K_V1。获授权后把权重下载到 "$HOME/Library/Application Support/EmbodyData/unified-runtime/torch-cache"（TORCH_HOME）下的 hub/checkpoints，并验证缓存可加载。检查已有 TORCH_HOME 是否改变实际位置；不要只下载到默认 ~/.cache/torch，也不要改成随机初始化来绕过缺失权重。
8. 只有我选择 SmolVLA 时，才安装说明中的额外依赖，下载文档指定 revision 的 lerobot/smolvla_base 和 HuggingFaceTB/SmolVLM2-500M-Video-Instruct。默认 Hugging Face 缓存位于 "$HOME/Library/Application Support/EmbodyData/huggingface-cache/hub"，保留下载工具生成的缓存结构。检查已有 HF_HOME 是否改变实际位置，完成后按指定 revision 以 local_files_only=True 验证。不要把“网络可以访问模型网站”当成离线权重验证通过。
9. 如果我已有训练好的 ACT/SmolVLA 模型，指导我在“模型库 → 导入本地模型”选择完整 pretrained_model 目录。它应包含 config.json、model.safetensors、policy_preprocessor.json、policy_postprocessor.json 及处理器引用的其他文件。基础预训练权重不等于已经学会具体任务的模型；推理前需要核对主从臂配置、相机名称和模型输入。
10. 完成后让我重新打开 .app，进入本地模式，核对软件是否识别标准环境。由我处理 macOS 相机权限；RealSense 不属于这份 USB/UVC 基础环境。说明下一步“设备配置 → 校准 → 遥操作验证 → 采集 → 数据回放和标注 → 本地训练 → 模型库推理”。未经我明确确认，不自动启动校准、遥操作、采集或模型推理。

发生错误时根据具体输出排查，不删除设备配置、校准、数据集或模型，不关闭 macOS 安全保护。出现 OpenCV/PyAV 的 AVFoundation 重复类警告时单独记录，不直接删除动态库，也不把警告当成验证通过。

如果你能执行本机命令，在授权范围内直接处理；否则每次只给我一步可复制的 zsh 命令，等我反馈结果再继续。最后分别列出“环境已验证”“权重已验证”“仍需软件/真实硬件验证”，不要把安装完成说成全流程已验收。
```

采集、回放和标注不需要预训练模型权重。训练和推理需要各自对应的依赖、权重或完整任务模型；可先准备基础采集环境，再按需准备模型。

## 发布内容

此仓库当前用于分发**编译好的应用和文档**，暂不公开完整工程源码，也不声明为开源授权项目。

应用包含运行必需的 Sidecar 组件；下载包不包含 Python 虚拟环境、第三方训练环境、预训练权重、个人设备配置、采集数据、构建缓存或开发仓库历史。第三方组件仍遵循各自许可。软件免费提供给具身智能爱好者学习使用。

本次发布为预览版，已在开发机完成构建和包结构检查；全新 Windows / Mac 的端到端安装与真实硬件验收仍待完成。请参阅各平台的安装说明。

## 反馈

请在 Issues 描述复现步骤，附上操作系统版本、处理器或显卡型号、应用版本和错误日志片段。分享日志前请移除账号凭据和个人信息。
