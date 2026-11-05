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
