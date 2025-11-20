Tetracamthon 重构预发布说明
=========================

项目简介
--------

Tetracamthon 是一个面向 Tetra Pak A3 Flex/CompactFlex 无菌灌装机的机构反向工程与驱动凸轮曲线重建项目。它基于公开资料的曲线数据与机械机构参数，使用分段多项式样条与符号计算重建关键工位的 PVAJ（位置、速度、加速度、加加速度）曲线，并生成虚拟凸轮设计参考。

背景与动机
----------

作者自 2012 年起持续研究 A3 Flex 的机构与曲线。在 2019 年重新启动本项目，目标是：

- 用工程化方法重建关键曲线，验证对行业有价值的问题求解能力；
- 将零散研究沉淀为可复现的脚本与文档，形成可扩展的工具集；
- 为后续在 FreeCAD 等 CAD/CAE 环境中的插件化设计打下算法基础。

功能概述
--------

- 读取并修正公开的 A3 Flex 右/左 York 与 Jaw 加速度数据，积分得到 PVAJ 曲线（`src/a3flex/read_data.py`）。
- 可视化多条曲线并自动标注峰值/零点等关键特征（`src/a3flex/draw_data.py`）。
- 基于分段多项式样条构建各阶段的 PVAJ 曲线，满足插值、光滑度与周期性约束（`src/tetracamthon/polynomial.py`）。
- 建模滑块-摇杆机构，推导 O4–O2、AO2 等几何与运动关系，连接各阶段边界条件（`src/tetracamthon/mechanism.py`）。
- 以阶段组织完整工艺：Climbing Back、Clamping Bottom、Waiting Lock、Shaking Hand（两类）、Pulling Tube、Waiting Knife、Throwing Pack（`src/tetracamthon/stage.py`）。
- 支持不同包装规格（如 `1000SQ`、`330SQ`）的参数化计算（`src/tetracamthon/package.py`）。

代码结构
--------

- `src/a3flex/`：数据读取与 PVAJ 计算、曲线可视化。
  - `read_data.py`：读取加速度 CSV，积分/差分得到 PVAJ；支持左右侧与相对曲线。
  - `draw_data.py`：在四联子图上绘制曲线并标注关键点。
- `src/tetracamthon/`：核心样条与机构建模。
  - `polynomial.py`：样条系统，构建分段多项式、插值/光滑度/周期性方程并求解系数。
  - `stage.py`：按工位阶段组织曲线与约束，负责阶段之间的边界衔接。
  - `mechanism.py`：滑块-摇杆等机构几何与运动学推导，提供边界条件与连接量。
  - `package.py`：包装规格参数（尺寸、速度、工艺时序）。
  - `helper.py`：通用工具与持久化缓存；当前使用本地 `data/*.pkl` 缓存中间结果。
  - `knot_info/*.csv`：各阶段的关键节点定义（节点角度、PVAJ 值、光滑度、分段阶数）。
- `tests/`：以 `pytest` 为主的单元/集成测试，覆盖样条、阶段、机构、数据绘制等模块。
- `docs/`：项目文档与参考资料（含中文部分），用于展示与记录。

数据来源与示例图
----------------

- 参考数据来自 MSC Adams 2010 欧洲用户大会公开资料第 56 页，包含 A3 Flex 的 York/Jaw 加速度曲线：

  .. figure:: ./plots/01_one_slide_of_Tetra_Pak_in_Using_Adams_in_university_courses_&_research_involving_Kinematics_&_Dynamics.png
     :alt: Adams 2010 公开曲线截图

- 积分后得到的 PVAJ 总览（721 点采样）：

  .. image:: ./plots/Tetra_Pak_A3_flex_Curves_with_721_points.png
     :alt: Tetra_Pak_A3_flex_Curves_with_721_points
     :align: center

快速开始
--------

- 安装依赖：

  - Python 3.7+，推荐使用虚拟环境
  - 依赖列表见 `requirements.txt`（使用 SymPy、NumPy、SciPy、Matplotlib、NetworkX、scikit-image 等）

- 数据可视化示例：

  - 打开 `src/a3flex/tetra_pak_a3_flex_cam_acc_data_721.csv`，调用 `plot_dynamic_subplots` 绘制四联子图并标注关键点。

- 阶段样条与机构分析：

  - 各阶段的关键节点定义位于 `src/tetracamthon/knot_info/*.csv`，样条的构建与求解在 `src/tetracamthon/polynomial.py` 与 `src/tetracamthon/stage.py` 中完成。

测试与验证
----------

- 测试位于 `tests/`，覆盖：

  - 多项式样条的方程与系数求解（`tests/test_polynomial.py`）
  - 阶段曲线构建与可视化（`tests/test_stage.py`）
  - 机构几何与速度关系（`tests/test_mechanism.py`）
  - 包装规格与生产节拍计算（`tests/test_package.py`）

- 注：早期测试使用了作者本地的绝对路径，后续重构将统一为相对路径与可配置目录，确保开箱即用。

核心算法要点
------------

- 分段多项式样条：在每个节点处满足插值值（P/V/A/J）、两侧光滑度阶、周期性约束，整体使用 SymPy 求解系数并生成表达式（含各阶导）。
- 机构学连接：通过 Forward/Backward 推导滑块-摇杆的几何与运动关系，将机构边界量（如 `r_O4O2`、`x_AO2`、`y_AO2`）转换为阶段样条的边界约束，实现工艺阶段的连续衔接。

重构计划（草案）
----------------

- 路径与缓存：移除硬编码绝对路径，改为相对路径与配置项；统一缓存目录到 `./data`，并提供环境变量或配置文件设置。
- 包装与依赖：修复 `setup.py` 的打包参数，移除 `requirements.txt` 中对自身包的引用；完善版本与发布流程。
- API 设计：收敛样条与机构模块的公共接口，提供更稳定的 Python API 与示例。
- 测试与文档：将测试用例改造为路径无关、可在 CI 环境运行；补充中文/英文使用说明与示例。
- 可视化与导出：统一绘图接口与输出目录，支持导出 PNG/SVG 与数据文件。

许可证
------

本项目采用开源许可证（见 `LICENSE`）。项目涉及的第三方资料与图像归原作者与机构所有，仅用于学术研究与工程学习交流。

更新记录
--------

- 2020-01-08：整理并格式化初版 README。
- 2020-08-29：刷新以 721 点采样的 A3 曲线示例。
- 2025-11-20：重构预发布说明（中文），补充模块结构与重构计划。