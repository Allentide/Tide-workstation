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
1. 检查现有 Python、虚拟环境、PyTorch、LeRobot、GPU 和可用磁盘空间，先给我简短的检查结果。优先复用版本兼容且能被软件发现的环境，保留已有项目和数据。
2. 当前版本使用 Python 3.12 和 LeRobot 0.6.0，PyTorch 按安装说明选择。已有环境可用时直接验证，缺少依赖时补齐。安装前告诉我将下载哪些内容、预计空间及目标目录。
3. 新建环境使用软件可自动发现的位置：%LOCALAPPDATA%\EmbodyData\unified-runtime\lerobot-0.6.0。PowerShell 中请通过 $env:LOCALAPPDATA 解析当前用户路径。软件解压位置可自由选择。复用其他位置的环境时，先确认 Tide Workstation 确实可以发现它。
4. 始终用目标环境的 Scripts\python.exe -m pip 安装依赖。根据当前硬件和驱动选择兼容的 PyTorch 构建，并实际检查 torch.cuda.is_available()。GPU 条件不足时说明影响，让我选择后续方案。
5. 按安装说明补齐相机、串口、视频读写和训练依赖。collector-agent 是 Tide Workstation 随包交付的自有组件，检查应用包中的 sidecar 模块与启动入口即可。安装说明中的第三方依赖由你协助准备。
6. 默认先完成 ACT 环境。查明当前 ACT 配置实际需要的预训练视觉骨干权重，在得到我的下载授权后准备到该运行环境使用的缓存中。SmolVLA 的依赖和权重等我明确选择使用时再准备。
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

## 发布内容

此仓库当前用于分发**编译好的应用和文档**，暂不公开完整工程源码，也不声明为开源授权项目。

应用包含运行必需的 Sidecar 组件；下载包不包含 Python 虚拟环境、第三方训练环境、预训练权重、个人设备配置、采集数据、构建缓存或开发仓库历史。第三方组件仍遵循各自许可。软件免费提供给具身智能爱好者学习使用。

本次发布为预览版，已在开发机完成构建和包结构检查；全新 Windows / Mac 的端到端安装与真实硬件验收仍待完成。请参阅各平台的安装说明。

## 反馈

请在 Issues 描述复现步骤，附上操作系统版本、处理器或显卡型号、应用版本和错误日志片段。分享日志前请移除账号凭据和个人信息。
