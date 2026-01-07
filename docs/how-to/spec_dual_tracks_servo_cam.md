# 双线路与泛化统一 Spec（练习套路 + 通用伺服优化）

## 1. 概述 (Overview)
- **目标**：将项目沿“两条路线”并行推进——“工程师练习套路（以利乐柔性机夹爪驱动凸轮为例）”与“通用伺服电机曲线优化工具（电子凸轮）”——并抽象共享核心库，避免重复维护与长期分支漂移。
- **方法**：单仓多包结构，保留主干（main），以目录拆分模块（core/recipes/servo_opt）；所有开发通过短期特性分支完成并合并回主干。

## 2. 架构与目录 (Architecture)
### 2.1 核心层 (Core)
共享的基础设施，位于 `src/core`。
- **Units**: 统一秒/度/mm 与互转（参考 [helper.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/helper.py)）。
- **Spline**: 统一样条接口与评估/导数/jerk（参考并收敛 [polynomial.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/polynomial.py)）。
- **Kinematics**: 机构模型与符号/数值通道（参考 [mechanism.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/mechanism.py)）。
- **Trajectory**: 曲线 + 时间标定；采样、插值与 re-timing。
- **Plotting**: 无 GUI 依赖的绘图工具，保留 `show` 参数（默认 `False`）。
- **IO/Config**: CSV/YAML/JSON 读取与路径管理，移除硬编码。

### 2.2 练习套路 (Recipes)
具体的工程实例，位于 `src/recipes`。
- **Cam Jaw**: 利乐柔性机夹爪驱动凸轮练习的脚本、数据与测试；贯通“数据→样条→机构触点→整机四联图”。

### 2.3 伺服优化工具 (Servo Opt)
通用的优化工具，位于 `src/servo_opt`。
- **Model**: 电子凸轮与轨迹建模，ServoModel（电机参数）。
- **Solvers**: SciPy（起步）、CasADi/Pyomo（选配）适配层。
- **Sim**: 仿真评估（速度/加速度/jerk/能耗/扭矩）。
- **Export**: 位置-时间表与路点导出，适配设备采样率/插补方式。

## 3. 核心抽象 (Core Abstractions)
- **SplineCurve**: 提供 `evaluate`/`vel`/`acc`/`jerk` 接口；支持 knot 参数化与时间缩放；保证 C1/C2/C3 连续性与边界条件。
- **ElectronicCam**: 以多段样条定义电子凸轮位移-时间曲线；支持重标定与段间约束对齐。
- **Trajectory**: 统一采样、插值与 re-timing；满足速度/加速度/jerk 上限。
- **MechanismModel**: 机构几何与解析表达式；输出位移/速度/加速度；支持符号/数值双实现。
- **ServoModel**: 电机参数与负载模型（转矩常数、惯量、摩擦/粘性、驱动上限）。
- **Objective/Constraint**: 目标函数与约束模块化（jerk、能耗/扭矩、跟踪误差、多目标加权；边界、速度/加速度/jerk、扭矩、周期/同步、机械干涉）。

## 4. 功能模块详情 (Functional Tracks)

### 4.1 通用伺服电子凸轮 (Servo Opt)
- **问题建模**：决策变量为样条 knot 位置/时间或基函数系数；可选全局时间缩放。
- **目标函数**：加权和（例如 $w_{jerk}\int jerk^2 + w_{energy}\int \tau \cdot \omega + w_{track}\int error^2$）。
- **约束集**：位置、速度/加速度/jerk、扭矩上限；周期/同步；机械限位/干涉。
- **数值方法**：起步用 SciPy minimize + 非线性约束；进阶用 CasADi（自动微分、配点/多相）或 Pyomo（复杂约束管理）。
- **时间再标定**：先确定几何曲线，再优化时间分配以满足上限与驱动约束。
- **求解策略**：多起点随机化、分层优化（先可行后优化）、单位归一化与合理初值。

### 4.2 夹爪驱动凸轮练习 (Recipes - Cam Jaw)
- **主题**：数据到图（P/V/A/J 四联图）；样条入门（knot_info 连续性约束）；机构融合（滑块-摇杆触点与位移）；整机拼接（阶段边界对齐）。
- **验收**：统一单位与容差（例如 1e-3）；关键特征位置对齐；测试可重入、路径无关、无 GUI 依赖。
- **实现**：依赖 core 的 `SplineCurve`/`MechanismModel`/`plotting`；输出 PNG 与 CSV 到 `data/plots`、`data/outputs`。

## 5. 工程实施计划 (Implementation Plan)

### 5.1 阶段 0: 准备工作 (Preparation)
**目标**：建立工程基准，解耦核心代码。
1.  **工程化与依赖管理**：
    - 在项目根创建 `pyproject.toml`，声明依赖与可选特性。
    - 基础依赖：`numpy`、`scipy`（优化）、`sympy`（符号）、`matplotlib`（绘图，默认 `show=False`）。
    - 可选扩展：`tetracamthon[servo]`（CasADi/Pyomo 等进阶求解器）。
2.  **物理目录结构重构**：
    - 在 `src` 下建立 `core`/`recipes`/`servo_opt` 三目录骨架。
3.  **核心代码解耦与迁移**：
    - **样条**：将 [polynomial.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/polynomial.py) 收敛为 `SplineCurve` 接口（`src/core/spline.py`），补齐 evaluate/vel/acc/jerk。
    - **机构**：将 [mechanism.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/mechanism.py) 提炼为 `MechanismModel` 抽象（`src/core/mechanism.py`），统一符号/数值双通道。
    - **单位与工具**：将 [helper.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/helper.py) 拆分为 `src/core/units.py` 等基础工具。
    - **遗留策略**：旧实现保留在 `src/tetracamthon/**` 作为只读参考，文档中保留链接，新代码通过核心层接口使用。

### 5.2 阶段 1: 核心迁移与测试分层 (Migration & Testing)
**目标**：完成代码迁移，确保测试通过。
1.  **测试目录重构**：
    - `tests/core`：覆盖 units、SplineCurve、Trajectory、MechanismModel。
        - [test_polynomial.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_polynomial.py) → `tests/core/test_spline_curve.py`
        - [test_mechanism.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_mechanism.py) → `tests/core/test_mechanism_model.py`
    - `tests/recipes/cam_jaw`：覆盖数据处理与机构融合。
        - [test_stage.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_stage.py) → `tests/recipes/cam_jaw/test_cam_jaw_stages.py`
        - [test_read_data.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_read_data.py) → `tests/recipes/cam_jaw/test_cam_jaw_pipeline.py`
    - `tests/servo_opt`：覆盖模型与求解器。
2.  **Conftest 分层**：
    - 根层 `tests/conftest.py`：设置 `MPLCONFIGDIR`，提供路径 fixture。
    - 子层 `tests/core/conftest.py`、`tests/recipes/cam_jaw/conftest.py` 等初始化专用 fixture。
3.  **验证**：
    - 运行分层测试，确保迁移后功能无损。
    - 确认 `plotting` 模块在测试中默认不显示窗口 (`show=False`)。

### 5.3 阶段 2: 并行执行策略 (Parallel Execution)
**策略**：在核心层（Core）稳定并通过测试后，练习套路（Recipes）与伺服优化（Servo Opt）可并行推进。
- **闸门条件**：
  - `tests/core` 全绿，确保 SplineCurve/MechanismModel 接口稳定。
  - `plotting` 模块默认 `show=False`，支持 CI 自动化。

#### 任务 A: 旧功能再现 (Recipes - Baseline)
**目标**：用新架构跑通现有数据，建立可验证基线。
1.  **最小闭环**：在 `recipes/cam_jaw` 编写脚本，实现“读数据 → 样条重建 → 机构触点 → 四联图/CSV 输出”。
2.  **验收标准**：产物与 `data/plots` 下的历史黄金图表/数据一致（数值容差 1e-3）。

#### 任务 B: 优化 MVP (Servo Opt - Prototype)
**目标**：实现时间再标定（Re-timing）原型。
1.  **可行性问题**：给定几何样条与 v/a/jerk 上限，优化段时间分配。
2.  **验证**：使用 SciPy minimize 求解，输出优化后的轨迹并检查约束满足度。

### 5.4 阶段 3: 双线迭代与扩展 (Iteration)
- **Recipes**: 扩展更多测试用例，覆盖边界条件与异常处理。
- **Servo Opt**: 引入 CasADi/Pyomo 适配层，支持复杂约束与多目标优化。

## 6. 数据与配置管理 (Data & Config)
- **路径**：统一 `data/{inputs,outputs,plots}`，以仓库根为基准，禁止绝对路径。
- **配置**：YAML/JSON 承载单位、约束、采样率、电机参数与输出路径。
- **可复现**：固定随机种子；输入文件版本/快照；必要时用 LFS 或 DVC 管理大文件。

## 7. 测试与质量保障 (QA)
- **分层测试**：严格区分 `tests/core`、`tests/recipes`、`tests/servo_opt`。
- **数值断言**：统一容差（如 1e-3）与单位（秒/度/mm）。
- **属性测试**：验证连续性（C1/C2/C3）、单调性、周期性。
- **CI 与运行**：
    - 推荐以 `PYTHONPATH=src` 运行 pytest。
    - 路径过滤：改动特定模块时只跑对应 tests 子树。
    - 无 GUI：CI 环境仅生成文件并做数值校验。

## 8. 分支与 CI 工作流 (Workflow)
- **主干可发布**：main 始终可编译、可测试。
- **特性分支**：feature/xxxx 小步开发，频繁同步。
- **PR 审查**：必须通过 lint/类型检查/单元测试。

## 9. 客户案例与展示 (Showcase)
- **标杆案例**：TetraPak A3-Flex 的曲线与机构数据。
- **展示内容**：优化前后对比（jerk、能耗、峰值扭矩、误差）。
- **输出物料**：PNG 图、CSV 轨迹、复现脚本。
