# 双线路与泛化统一 Spec（练习套路 + 通用伺服优化）

## 概述
- 目标：将项目沿“两条路线”并行推进——“工程师练习套路（以利乐柔性机夹爪驱动凸轮为例）”与“通用伺服电机曲线优化工具（电子凸轮）”——并抽象共享核心库，避免重复维护与长期分支漂移。
- 方法：单仓多包结构，保留主干（main），以目录拆分模块（core/recipes/servo_opt）；所有开发通过短期特性分支完成并合并回主干。

## 架构与目录
- 核心层（共享）：`src/core`
  - units 与转换：统一秒/度/mm 与互转（参考 [helper.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/helper.py)）
  - spline/插值：统一样条接口与评估/导数/jerk（参考并收敛 [polynomial.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/polynomial.py)）
  - kinematics：机构模型与符号/数值通道（参考 [mechanism.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/mechanism.py)）
  - trajectory：曲线 + 时间标定；采样、插值与 re-timing
  - plotting：无 GUI 依赖的绘图工具，保留 show 参数
  - io/config：CSV/YAML/JSON 读取与路径管理，移除硬编码
- 练习套路：`src/recipes`
  - cam_jaw：利乐柔性机夹爪驱动凸轮练习的脚本、数据与测试；贯通“数据→样条→机构触点→整机四联图”
- 伺服优化工具：`src/servo_opt`
  - model：电子凸轮与轨迹建模，ServoModel（电机参数）
  - solvers：SciPy（起步）、CasADi/Pyomo（选配）适配层
  - sim：仿真评估（速度/加速度/jerk/能耗/扭矩）
  - export：位置-时间表与路点导出，适配设备采样率/插补方式

## 核心抽象
- SplineCurve：evaluate/vel/acc/jerk；knot 参数化与时间缩放；C1/C2/C3 连续性与边界条件
- ElectronicCam：以多段样条定义电子凸轮位移-时间曲线；支持重标定与段间约束对齐
- Trajectory：统一采样、插值与 re-timing；满足速度/加速度/jerk 上限
- MechanismModel：机构几何与解析表达式；输出位移/速度/加速度；支持符号/数值双实现
- ServoModel：电机参数与负载模型（转矩常数、惯量、摩擦/粘性、驱动上限）
- Objective/Constraint：目标函数与约束模块化（jerk、能耗/扭矩、跟踪误差、多目标加权；边界、速度/加速度/jerk、扭矩、周期/同步、机械干涉）

## 优化策略（通用伺服电子凸轮）
- 问题建模：决策为样条 knot 位置/时间或基函数系数；可选全局时间缩放
- 目标函数：加权和（例如 w_jerk∫jerk² + w_energy∫τ·ω + w_track∫误差²）
- 约束集：位置、速度/加速度/jerk、扭矩上限；周期/同步；机械限位/干涉
- 数值方法：起步用 SciPy minimize + 非线性约束；进阶用 CasADi（自动微分、配点/多相）或 Pyomo（复杂约束管理）
- 时间再标定：先确定几何曲线，再优化时间分配以满足上限与驱动约束
- 求解策略：多起点随机化、分层优化（先可行后优化）、单位归一化与合理初值

## 练习套路（夹爪驱动凸轮）
- 主题：数据到图（P/V/A/J 四联图）；样条入门（knot_info 连续性约束）；机构融合（滑块-摇杆触点与位移）；整机拼接（阶段边界对齐）
- 验收：统一单位与容差（例如 1e-3）；关键特征位置对齐；测试可重入、路径无关、无 GUI 依赖
- 实现：依赖 core 的 SplineCurve/MechanismModel/plotting；输出 PNG 与 CSV 到 data/plots、data/outputs

## 数据与配置管理
- 路径：统一 data/{inputs,outputs,plots}，以仓库根为基准，禁止绝对路径
- 配置：YAML/JSON 承载单位、约束、采样率、电机参数与输出路径
- 可复现：固定随机种子；输入文件版本/快照；必要时用 LFS 或 DVC 管理大文件

## 测试与质量保障
- 分层测试：`tests/core`、`tests/recipes`、`tests/servo_opt`
- 数值断言：统一容差与单位；性质测试（连续性、单调性、周期性）
- 基准与回归：优化器收敛时间与结果质量（jerk、能耗、峰值扭矩）；黄金数据与结果对比
- 日志与审计：结构化 logging 替代 print；关键事件可被测试捕获与断言；记录配置与版本用于结果追溯

## API 与使用体验
- 稳定接口：core 暴露少量稳定类与函数；recipes/servo_opt 仅依赖 core
- 计算与绘图分离：计算函数只返回数据；绘图由 plotting 控制 show（默认 false）
- CLI/脚本：最小命令/脚本贯通“数据→样条→优化→导出”
- 文档与示例：docs 中提供“快速开始”“练习教程”“优化工具使用说明”（参考 [refactor_recommendation.md](file:///Users/quzheng/Projects/tetracamthon/docs/how-to/refactor_recommendation.md)）

## 客户案例与展示
- 标杆案例：保留并强化 TetraPak A3-Flex 的曲线与机构数据作为“可验证客户案例”
- 展示内容：输入与处理、样条重建、机构融合、优化前后对比（jerk、能耗、峰值扭矩、误差）、位置指令/路点导出与采样策略
- 输出物料：PNG 图、CSV 轨迹、伺服路点表；复现脚本一键生成；日志含版本、配置与输入快照

## 测试目录重构（recipes 与 servo_opt 对齐）
- 目标结构
  - tests/core：覆盖 units、SplineCurve、Trajectory、MechanismModel、plotting 的纯计算与接口
  - tests/recipes/cam_jaw：覆盖“数据→样条→机构触点→四联图”的贯通线与阶段断言
  - tests/servo_opt：覆盖模型建模、求解器适配、re‑timing、指标度量（jerk、能耗、峰值扭矩）
  - tests/fixtures：测试用轻量输入与公共配置
- 迁移映射（现有文件）
  - [test_polynomial.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_polynomial.py) → tests/core/test_spline_curve.py
  - [test_mechanism.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_mechanism.py) → tests/core/test_mechanism_model.py
  - [test_stage.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_stage.py) → tests/recipes/cam_jaw/test_cam_jaw_stages.py
  - [test_read_data.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_read_data.py) + [test_draw_data.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_draw_data.py) → tests/recipes/cam_jaw/test_cam_jaw_pipeline.py
  - [test_package.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_package.py) → tests/recipes/cam_jaw/test_package_profiles.py（或合并为集成用例）
  - 将 [tested_Tetra_Pak_A3_flex_Curves_with_721_points.png](file:///Users/quzheng/Projects/tetracamthon/tests/tested_Tetra_Pak_A3_flex_Curves_with_721_points.png) 移出 tests 根，转移到 data/plots 或作为测试生成产物
- 路径与资源管理
  - 小体量 CSV 放入 tests/fixtures/inputs；较大/共享数据放 data/inputs（必要时用 LFS/DVC）
  - 测试产物写入 tmp_path 或 data/outputs/test/<run_id>；对图像只做生成与关键数据断言，不逐像素比对
  - 统一用 Path(__file__).resolve() 组合项目根 + 相对目录，禁止硬编码绝对路径
- conftest 分层与职责
  - 根层 tests/conftest.py：设置 MPLCONFIGDIR；提供 project_root、data_path、src_path 的实用 fixture；注册 markers（slow、solver、integration）
  - tests/core/conftest.py：最小样本 fixture（样条 knots、机构参数）
  - tests/recipes/cam_jaw/conftest.py：721 点数据路径、knot_info CSV、JawOnYork/TracingOfPointA 组合 fixture
  - tests/servo_opt/conftest.py：ServoModel 参数与优化配置示例（速度/加速度/jerk/扭矩上限）
- 断言与 markers
  - 数值容差统一（如 1e‑3），单位一致（秒/度/mm）
  - 属性测试：连续性（C1/C2/C3）、单调性、周期性、边界条件一致性
  - 优化器度量：jerk 积分、能耗（τ·ω）、峰值扭矩、跟踪误差；过程指标（迭代次数、收敛时间）
  - markers：slow（耗时）、solver（外部优化器）、integration（跨模块贯通线）
- CI 与运行
  - 推荐以 PYTHONPATH=src 运行 pytest，确保新结构导入清晰
  - 路径过滤：改动 core/recipes/servo_opt 时只跑对应 tests 子树，缩短反馈周期
  - 无 GUI：plotting 默认 show=False，CI 仅生成文件并做数值校验
- 过渡期兼容
  - 首批迁移仅重命名与分层，不改内部逻辑，保证快速通过
  - 第二步将旧 conftest 中的专用 fixture 拆分到 recipes 层；core 层补最小样本
  - 如核心代码迁移到 src/core，临时在根 conftest 中提供别名导入适配，避免测试大面积失效
- 执行步骤（建议）
  - 创建分层目录：tests/core、tests/recipes/cam_jaw、tests/servo_opt、tests/fixtures
  - 批量 git mv 按上述映射迁移测试文件
  - 移动或生成图像输出到 data/plots 或 tmp 路径，替换断言为数值/存在性检查
  - 分层 conftest 初始化；调整导入与容差断言；确保 plotting 使用 show=False

## 分支与 CI 工作流
- 主干可发布：main 始终可编译、可测试、可发布
- 特性分支：feature/xxxx 小步开发，最长 1–2 周；频繁与 main 同步
- PR 审查：必须通过 lint/类型检查/单元测试；路径过滤只跑相关模块测试
- 版本与发布：在 main 打 tag（语义化版本）；servo 适配用 extras（如 tetracamthon[servo]）

## 里程碑与行动
- 第1–2周：抽象 core（SplineCurve/ElectronicCam/Trajectory/MechanismModel/units/plotting/io）；清理绝对路径与配置读取；保持现有测试通过（参考 [test_mechanism.py](file:///Users/quzheng/Projects/tetracamthon/tests/test_mechanism.py)）
- 第3–4周：完成 cam_jaw 练习首批脚本与测试；贯通“数据→样条→机构触点→四联图”；搭建 CI、测试标记与日志体系
- 第5–6周：servo_opt MVP（SciPy 优化、基础约束与目标、示例问题）；导出轨迹与指令
- 第7–8周：引入 CasADi/Pyomo 适配，扩展约束与多目标；完善仿真与性能基准
- 持续：优化性能与鲁棒性；更多设备案例与文档

## 落地建议（立即执行）
- 在 `src` 下建立 `core/recipes/servo_opt` 三目录骨架
- 将绘图逻辑迁入 core.plotting，计算函数只返回数据（参考 [mechanism.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/mechanism.py) 的 show 设计）
- 将 [polynomial.py](file:///Users/quzheng/Projects/tetracamthon/src/tetracamthon/polynomial.py) 收敛成 SplineCurve 接口，补齐 vel/acc/jerk
- 在 `recipes/cam_jaw` 写最小贯通脚本：读数据→样条→机构触点→四联图与 CSV 输出
- 在 `servo_opt` 写最小示例：给定速度/加速度/jerk 上限，优化 knot 时间，输出轨迹并测试验收

## 遗留代码封存策略
- 保留 `src/tetracamthon/**` 作为过时实现的借鉴来源；在新核心层（src/core）、示例层（src/recipes）与优化层（src/servo_opt）完成后进行封存。
- 新结构开发期间，参考旧实现的算法与测试，但不在旧路径继续扩展功能。
- 完成迁移后：
  - 标注遗留目录为只读参考，不纳入新的 CI 流程；
  - 在文档中保留到遗留实现的链接，用于教学与对照；
  - 记录接口与行为差异的变更说明，便于回溯与维护。
