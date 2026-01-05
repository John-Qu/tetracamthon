# 2026 年重构咨询

## 我以 Readme.rst 为基础来问我做过什么，还可以做什么

这是我在2019年做的项目 `/Users/quzheng/Projects/tetracamthon/README.rst` 说明，现在打算重构（refactor) 一下，用软件工程最佳实践的方式。请你通读整个项目文件夹，理解我当年做了什么，怎么做的。请先帮我用中文重写一下这个readme文件，当作是重构的一个预发布稿。

### GPT-5-high 回答我

**项目总览**
- 这是一个针对 Tetra Pak A3 Flex/CompactFlex 灌装机的机构反向工程与驱动凸轮曲线重建项目。它将公开的 York/Jaw 加速度曲线数据积分成 PVAJ（位置/速度/加速度/加加速度），并通过分段多项式样条与机构学约束重建机器各阶段的运动曲线。
- 数据侧从公开资料中提取并做轻度修正，然后生成右/左、相对曲线；算法侧以“阶段”为单位串联整机工艺（摇手、拉管、等待、夹底、回程、抛包），并用滑块-摇杆机构建立几何与运动学连接。
- 你在 2019 年做的主要工作包括：数据采集与清洗、数值积分与可视化、分段样条建模与求解、机构学推导、阶段边界条件的自动衔接，以及参数化的包装规格支持。

**关键模块**
- 数据与可视化
  - `src/a3flex/read_data.py:7` 读取 CSV 加速度数据（右/左、相对曲线），积分/差分得到 PVAJ。
  - `src/a3flex/draw_data.py:327` 绘制四联子图（位置/速度/加速度/加加速度），并自动标注峰值与零点特征。
- 样条与阶段
  - `src/tetracamthon/polynomial.py:197` 样条系统：分段多项式、插值/光滑度/周期性约束，SymPy 求解系数。
  - `src/tetracamthon/stage.py:223` 各阶段（ClampingBottom 等）按 knot_info CSV 定义关键点与光滑度，生成整段 PVAJ。
  - `src/tetracamthon/profile.py:8` 组合多个阶段形成 YorkProfile，并提供整体可视化与分析。
- 机构与参数
  - `src/tetracamthon/mechanism.py:150` 滑块-摇杆机构（Forward/Backward），推导 `r_O4O2`、`x_AO2`、`y_AO2` 等量并与样条边界衔接。
  - `src/tetracamthon/package.py:77` 包装参数（`1000SQ`、`330SQ` 等）与生产节拍（8000 pph）下的时序与速度计算。
- 测试与文档
  - `tests/` 覆盖样条、阶段、机构、数据绘制、包装参数等。
  - `docs/` 存放说明文档与参考资料（含中文分区）。

**已识别的技术债与重构要点**
- 绝对路径硬编码
  - `src/tetracamthon/helper.py:29`、`src/tetracamthon/polynomial_spline.py:446`、`src/tetracamthon/polynomial.py:512` 等处使用了作者本机路径；测试 `tests/conftest.py:10` 也使用绝对路径。这会阻碍跨环境运行。
- 打包与依赖
  - `setup.py:11` 使用了 `package=find_packages(...)`，应为 `packages=find_packages(...)`。
  - `requirements.txt:5` 依赖中包含 `tetracamthon~=1.0` 的自引用，容易导致安装冲突。
- 统一的输出与缓存
  - `data/*.pkl` 用于缓存解与中间结果，但路径与策略需要统一并可配置。
- API 与示例
  - 可将阶段构建、机构连接、绘图导出统一为稳定 API，并附带最简示例脚本。

**中文预发布 README**
- 我已将 `README.rst` 重写为中文的预发布稿，并替换了原文件内容。新结构包括：项目简介、背景与动机、功能概述、代码结构、数据来源与示例图、快速开始、测试与验证、核心算法要点、重构计划（草案）、许可证与更新记录。你可直接在仓库查看：`/Users/quzheng/Projects/tetracamthon/README.rst`。

以下为新 README 的核心内容摘录（完整内容已写入文件）：
- 项目简介：面向 A3 Flex/CompactFlex 的反向工程与凸轮曲线重建，分段样条 + 机构学 + 数据可视化。
- 功能概述：
  - 读取与修正 York/Jaw 加速度数据并生成 PVAJ（`src/a3flex/read_data.py:7`）。
  - 绘制四联子图并标注关键特征（`src/a3flex/draw_data.py:327`）。
  - 构建满足插值/光滑度/周期性的阶段样条（`src/tetracamthon/polynomial.py:267`、`src/tetracamthon/stage.py`）。
  - 滑块-摇杆几何/运动关系接入阶段边界（`src/tetracamthon/mechanism.py:219`、`src/tetracamthon/mechanism.py:291`）。
  - 包装规格参数化支持与生产时序计算（`src/tetracamthon/package.py:95`）。
- 快速开始：
  - 安装依赖 `requirements.txt`（SymPy、NumPy、SciPy、Matplotlib、NetworkX、scikit-image）。
  - 运行绘图示例：用 `plot_dynamic_subplots` 对 `tetra_pak_a3_flex_cam_acc_data_721.csv` 出图。
  - 阶段样条：`src/tetracamthon/knot_info/*.csv` 定义关键节点；在 `polynomial.py` / `stage.py` 构建并求解。
- 测试与验证：
  - `tests/test_polynomial.py`、`tests/test_stage.py`、`tests/test_mechanism.py`、`tests/test_package.py`。
  - 说明后续将把绝对路径改造为相对路径与配置目录。
- 重构计划（草案）：
  - 移除绝对路径、统一缓存目录与配置；修复打包参数与依赖自引用；收敛 API；测试改 CI 友好；统一绘图导出。

如果你希望，我可以在下一步直接按上述重构计划开始改造：清理绝对路径、修复 `setup.py` 与依赖、统一缓存目录与导出路径、为阶段与机构模块加一个简洁的示例入口，并把测试用例改造为路径无关。你也可以告诉我优先级（例如先修 `setup.py` 和路径问题，再跑一次测试）。

## 如果为了做成务实工程师套路案例

这个项目是我 2019年年中做的，现在是 2026 年 1 月 5 日，我希望用当下工具和手段重构这个项目，让它成为一个独立的工程师练手项目，迁移 Thomas 和 Hunt 在 The Pragmatic Programmer 中指出的方法，实践一个务实的机械工程师所能做到的程度。把它做成我的一个个人案例，让同行能拍案叫绝，让年轻人能上手打一遍套路来学习老工程师的做法和思路。带着这个目的，来重构这个项目，你有什么建议？

### GPT-5-high 回答
          
**总体目标**
- 把项目升级为一个“独立工程师的练手经典案例”：从数据到机构、从样条到整机曲线，形成一套可复现、可扩展、可教学的完整工程闭环。
- 迁移务实主义的工程实践：可读、可测、可发布、可维护；拥抱自动化、强调反馈、避免重复、消除硬编码；让新人能“打一遍套路”，同行能看出专业度。

**重构路线图**
- 快速获益（1周）
  - 移除硬编码绝对路径，统一数据/缓存到仓库 data 目录。
  - 修复打包配置与依赖自引用，确保本地安装与测试顺畅。
  - 整理一个最小 CLI/脚本入口，跑通一条从数据到 PVAJ 可视化的“贯通线”（Tracer Bullet）。
- 工程化（2–4周）
  - 统一配置源：使用环境变量 + TOML/YAML 配置（如 config/engine.yaml）。
  - 结构化日志与缓存：标准 logging，分级日志；持久化采用统一路径策略；为耗时求解做结果缓存（哈希化参数 -> 结果）。
  - 类型与风格：加入 Ruff/Black/isort/mypy + pre-commit，保证代码质量与一致性。
  - 测试与覆盖率：pytest 参数化 + 资源路径无关；增加金样（golden）数据与性质测试（如平滑度、周期性约束）。
  - CI/CD：GitHub Actions 跑 lint/测试，发布文档与示例工件；引入依赖缓存加速。
- 产品化（2–3周）
  - CLI 与示例：提供 tcam 命令（数据绘图、阶段求解、整机曲线）；示例场景 330SQ/1000SQ/不同产能。
  - 文档与教程：用 MkDocs Material/Mermaid 统一文档；“一条龙”教学路线：从数据到整机曲线的 5 个练习。
  - 数据与大文件管理：用 DVC 或 Git LFS 管控 CSV/图像；确保版本可追溯与空间友好。
- 扩展与稳定（持续）
  - 数值稳健性：单位统一、归一化策略、求解容差与失败回退；SymPy 求解性能优化（分块求解、初值策略）。
  - 插件化：阶段与机构的接口统一，支持“加新工艺/替换机构/换包装规格”的可插拔。
  - 版本与发布：语义化版本，CHANGELOG，发布到 PyPI（可选）。

**你当前代码的具体改进建议**
- 路径与缓存
  - 把所有绝对路径替换为相对项目根的 data 目录，并提供统一函数生成路径。
    - 参考文件： [helper.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/helper.py#L29-L74)、[polynomial_spline.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/polynomial_spline.py#L446-L461)、[polynomial.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/polynomial.py#L355-L396)。
- 打包与依赖
  - 修复 setup 参数名：package -> packages；移除 requirements 中对自身包的自引用，避免安装循环。
    - 参考文件： [setup.py](file:///Users/quzheng/Projects/tetracamthon/setup.py)、[requirements.txt](file:///Users/quzheng/Projects/tetracamthon/requirements.txt)。
- 测试可移植性
  - tests/conftest.py 使用了本机绝对路径，改为相对路径 + 测试资源 fixture。用 pathlib.Path(__file__).resolve() 组合出路径。
    - 参考文件： [conftest.py](file:///Users/quzheng/Projects/tetracamthon/tests/conftest.py#L10-L15)。
- 接口与演示
  - main.py 当前为空，建议提供一个示例入口：读取 721 点数据 -> 生成 PVAJ 四联图 -> 保存到 plots；或生成某一阶段样条并绘图。
    - 参考文件： [draw_data.py](file:///Users/quzheng/Projects/tetracamthon/src/a3flex/draw_data.py#L327-L361)、[profile.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/profile.py#L209-L221)。

**已经准备好的“快速获益”改动预览**
- 我为以下文件准备了改动预览（不会自动生效）。请在 IDE 中“Review and Accept”以应用修改：
  - 修复打包配置
    - setup.py：将 package 改为 packages，避免打包失败
  - 移除依赖自引用
    - requirements.txt：删除 tetracamthon~=1.0
  - 统一缓存路径
    - helper.py：新增 data_path 函数，Memory 与通用存取改为使用仓库根 data
    - polynomial_spline.py：保存/加载 pieces 改为使用 helper.data_path
- 接受后，后续我可以继续批量清理 tests 与阶段 CSV 路径的硬编码。

**工程化实践（结合《程序员修炼之道》的迁移）**
- Tracer Bullet（贯通线）
  - 先打通“一条完整业务线”：读数据 -> PVAJ 可视化 -> 一个阶段样条求解 -> 整机曲线拼接 -> 导出图与数据。以此为基线迭代，始终可运行。
- DRY 与正交性
  - 路径生成、保存/加载、绘图导出统一公共辅助；阶段构建使用统一抽象，避免每个阶段重复样板。
- 设计即测试
  - 样条约束（插值/光滑度/周期性）用性质测试覆盖；机构边界关系用符号求解 + 数值案例双重验证。
- 自动化
  - pre-commit 自动格式化与静态检查；CI 自动跑测试、生成文档与示例图；版本标注与 CHANGELOG 自动更新。
- 可逆决策与尽量延迟
  - 文档系统先用 MkDocs（修改成本小），如需后续迁移再评估；数据管理先用 LFS，后期再看 DVC 是否需要。
- 知识资产与教练式教程
  - 用“练手剧本”把复杂问题拆成 5 个渐进练习：数据 -> 可视化 -> 样条 -> 机构连接 -> 整机曲线；每个练习都有输入、目标、验收条件。

**教学“套路”设计（可直接用于新人带教）**
- 路线 A：数据到图
  - 任务：用 721 点数据生成四联图，标注关键峰值/零点；验收：生成 PNG，关键点标注位置正确。
- 路线 B：最小样条
  - 任务：根据 knot_info CSV 构建某阶段样条，满足插值和光滑度，导出 P/V/A 曲线；验收：约束等式数=变量数，曲线连续。
- 路线 C：机构边界融合
  - 任务：用滑块-摇杆关系，把机构量 `r_O4O2`、`x_AO2` 融入阶段边界，算出触碰时刻与位移；验收：与单元测试给定数值在容差范围内。
- 路线 D：整机拼接
  - 任务：用 StagesConnector 拼接各阶段，输出完整 YorkProfile；验收：阶段边界位置/速度连续，周期性满足。
- 路线 E：参数化与探索
  - 任务：更换包装 330SQ/1000SQ、调整产能，观察曲线变化；验收：脚本可重入，输出结果命名规范。

**风险与兼容**
- 大文件与外链图：建议本仓库保存必要的示意图，超大图交由 LFS/DVC 管理。
- 数值稳定性：SymPy 求解复杂时需分块、做初值引导与容差控制；必要时用 SciPy 替代部分符号求解。
- 系统路径：彻底移除本机绝对路径（已开始）；统一用 pathlib 与相对根。

**下一步行动**
- 请先在 IDE 中“Review and Accept”我提供的 4 个改动预览，它们会：
  - 修复打包参数
  - 清理自引用依赖
  - 统一缓存路径到项目 data 目录
- 我将按路线图继续：
  - 第二批清理 tests 与阶段 CSV 的绝对路径
  - 增加最小 CLI/脚本入口贯通一条完整业务线
  - 引入 pre-commit、Ruff/Black/mypy 与 GitHub Actions

如果你更倾向先定一个“练手剧本”的具体清单，我也可以直接输出一套 5 个练习的任务书与验收标准，并同时准备对应的示例脚本骨架。只要你点头，我就开始。