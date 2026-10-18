# Stage13-B1「伤兵池 / 可恢复容量」机制合同
## STAGE13-B1 WOUNDED TROOP / RECOVERABLE CAPACITY MECHANISM CONTRACT

> **Current Document Status**: `FROZEN` (经独立 Mechanism Contract Freeze Auditor 审计通过)  
> **Stage13-B1 Frozen**: `YES`  
> **Runtime Change Authorized**: `NO` (严禁在此阶段修改 `sgs_v2/battle_core/*`，待全链路研究完成统一授权)  
> **Authority Source**: `STAGE13_B1_ROUND4_UNIFIED_MODEL.md`, `STAGE13_B1_ROUND4_ADVERSARIAL_COUNTEREXAMPLE_AUDIT.md`, `STAGE13_B1_ROUND4_CLOSURE_LEDGER.md`, `STAGE13_B1_ROUND4_DAMAGE_FAMILY_COVERAGE_MATRIX.md`, `STAGE13_B1_ROUND4_REPLAY_VALIDATION.csv`, `STAGE13_B1_CANONICAL_Q1_Q22_RECONCILIATION.md`, `STAGE13_B1_CONTRACT_EVIDENCE_MATRIX.md`, `STAGE13_B1_WOUNDED_TROOP_FREEZE_AUDIT.md`  
> **Freeze Date**: 2026-09-28  

---

## 1. Scope (范围定义)

本机制合同界定“三国志战略版”战斗系统内武将兵力损失后转化为**伤兵池（Wounded Troop Pool / Recoverable Capacity）**、随时间/回合边界衰减、被各类治疗与倒戈吸收消耗、以及在异常状态与边界条件下的完整数学与时序规范。

- **管辖边界 (In-Scope)**:
  1. 兵力扣减转化为伤兵容量的比例与整数量化规则。
  2. 伤兵池的单/多回合衰减机制与时钟触发点。
  3. 实际治疗结算时的硬上限截断：$H_{actual} = \min(H_{nominal}, W, M)$。
  4. 治疗与倒戈吸收对伤兵池的即时扣除与竞争规则。
  5. 伤害家族（兵刃、谋略、DOT）、分担（SHARE）、禁疗（HealingBlock）、阵亡（Defeat）对伤兵池的作用接口。
- **排除边界 (Out-of-Scope / Non-Claims)**:
  1. 增减伤结算公式与攻防系数计算（属于 **Stage13-B2**）。
  2. 治疗基础名义量 $H_{nominal}$ 的属性加成与战法系数计算（如急救、整装待发数值计算，属于 **Stage13-B3**）。
  3. 分摊机制（DISTRIBUTION）伤害结算公式（维持 **Stage9 DSTS9-B02** 挂起状态）。

---

## 2. Authority / Evidence Hierarchy (证据等级分层体系)

为防止将经验外推或工程设计伪装为客观游戏实证，本合同所有规则严格划分为三个法定等级：

- **Tier A — EMPIRICALLY FROZEN RULES (实证冻结规则)**:
  - 具备直接战报数据支撑、明确判别器（Discriminator）验证、通过 113 场战报 4,542 笔全量事件对抗性反例审计，误差 $\Delta = 0$ 且无任何未决反例。
- **Tier B — BOUNDED / PARTIALLY OBSERVED (有界支持 / 部分观察)**:
  - 真实战报中已观察到该现象，但因战报环境均为复合受击，缺乏纯净单段截断样本，实证空间被收敛在一个较窄的数学界限内（如 $[0.88, 0.92]$）。
  - 合同严格限定其适用范围与置信边界，不得宣称“全称闭环证明”。
- **Tier C — CANONICAL RUNTIME DEFAULTS (规范运行时默认值)**:
  - 在当前战报集合中无法直接经验测量（如武将阵亡后不再有恢复探针），或属于单回合实证规则在多回合递推中的自然状态机外推。
  - 为确保模拟器 Runtime 具备确定性执行能力而设定的标准默认规范。严禁在对外报告中宣称为“官方解包或实证事实”。

---

## 3. Terminology (标准术语表)

- **$T_{max}$ (Max Troops)**: 武将初始最大兵力（标准环境为 10000）。
- **$T_{current}$ (Current Troops)**: 武将当前存活兵力，$T_{current} \in [0, T_{max}]$。
- **$M$ (Missing Troops / 缺兵量)**: 武将当前缺损兵力，$M = T_{max} - T_{current}$。
- **$W$ (Wounded Troops / 伤兵池)**: 武将内部累加器，表示当前最大可被恢复的伤兵数量。
- **$\Delta T$ (Actual Troop Loss / 实际损兵)**: 某次物理扣血结算中武将实际扣减的兵力。
- **$H_{nominal}$ (Nominal Recovery / 名义恢复量)**: 治疗或倒戈战法根据智力/武力/技能系数计算出的理论恢复数值。
- **$H_{actual}$ (Actual Recovery / 实际恢复量)**: 战报最终体现的实际加血数值。
- **Round Transition**: 回合结束至下一回合开始之间的时钟切换阶段。
- **Action Boundary**: 同一回合内武将行动开始与结束的瞬时边界。

---

## 4. State Variables (状态机变量定义)

每个战斗单元（Unit）独立维护以下状态：

```text
UnitState {
    max_troops: int,         // T_max >= 0
    current_troops: int,     // 0 <= T_current <= T_max
    wounded_pool: int,       // 0 <= W <= (T_max - T_current)
    is_defeated: bool,       // T_current == 0
    is_healing_blocked: bool // 禁疗状态标志位
}
```

---

## 5. Wounded Generation (伤兵生成规则) — Tier A

- **规则编号**: `Rule-A1 (Generation Ratio)`
- **触发时机**: 武将受到任意实际兵力扣减（$\Delta T > 0$）事件后立即触发。
- **数学公式**:
  $$\Delta W = \lfloor 0.90 \times \Delta T \rfloor$$
  $$W_{new} = \min(M_{new}, W_{old} + \Delta W)$$
- **实证支持**:
  - 在连续比例空间 $r \in [0.850, 0.950]$（步长 0.001，共 101 点）上全量扫描，$r = 0.900$ 展现出全局唯一精度峰值（Unique Discrete Peak）。
  - 在 0.75, 0.80, 0.85, 0.90, 1.00 离散对照检验中，0.90 达到 30/32（93.75%）精确匹配，其余模型精确匹配数均为 0/32。
  - 113 战报 4,542 笔重放中，预测容量作为上限违例数为 0（0 Over-Prediction Errors）。

---

## 6. Integerization (整数量化与逐笔独立性) — Tier A

- **规则编号**: `Rule-A2 (Event-Local Integerization)`
- **取整函数**: 严格采用向下取整（Floor / Truncation toward zero）。
- **复合事件规则**:
  当一次技能/普攻造成多段伤害，或同一结算窗口触发多笔伤害时，整数量化**严格在每一笔独立损兵事件发生时局部即时执行**，严禁将多次伤害累加后再取整：
  $$\Delta W_{total} = \sum_{i=1}^{k} \lfloor 0.90 \times \Delta T_i \rfloor \neq \lfloor 0.90 \times \sum_{i=1}^{k} \Delta T_i \rfloor$$
- **反例攻击与实证锚点**:
  - 战报 6319219 陆逊受击 $\Delta T_1 = 78, \Delta T_2 = 78$：
    - 逐笔取整：$\lfloor 78 \times 0.90 \rfloor + \lfloor 78 \times 0.90 \rfloor = 70 + 70 = 140$。
    - 合并取整：$\lfloor (78 + 78) \times 0.90 \rfloor = \lfloor 156 \times 0.90 \rfloor = 141$。
    - 实际恢复上限测得恰为 **140**（合并假说被确凿证伪）。
  - 战报 101740 张飞两次受击各损兵 487，测得伤兵容量为 $438 + 438 = 876$，而非 $\lfloor 974 \times 0.90 \rfloor = 877$。
  - 多段受击判别样本中，逐笔向下取整达到 5/12 精确匹配，合并取整精确匹配数为 0/12。

---

## 7. Recovery Capacity Clamp (恢复容量截断) — Tier A

- **规则编号**: `Rule-A3 (Recovery Clamp)`
- **触发时机**: 执行任意治疗、急救、整装待发或倒戈吸收时。
- **数学公式**:
  $$H_{actual} = \begin{cases} 0, & \text{if } is\_healing\_blocked = \text{true} \\ \min(H_{nominal}, W, M), & \text{if } is\_healing\_blocked = \text{false} \end{cases}$$
- **实证支持**:
  - 证伪了 $RecoverableCapacity = MissingTroops$ 假说（Round 2 确凿证伪）。
  - 在全量重放中，观察到 1,323 笔样本精确截断于预测伤兵容量 $W$（EXACT_CAPACITY_CLAMP）。

---

## 8. Recovery Consumption (恢复容量即时扣减) — Tier A

- **规则编号**: `Rule-A4 (Recovery Consumption)`
- **触发时机**: 恢复量生效并加回武将当前兵力后立即扣除池内可用伤兵。
- **数学公式**:
  $$W_{new} = \max(0, W_{old} - H_{actual})$$
  $$T_{current, new} = T_{current, old} + H_{actual}$$
  $$M_{new} = T_{max} - T_{current, new}$$
- **实证支持**:
  - 战报 6319219 周泰：G0 阶段触发【合军聚众】恢复 465 兵力（完全耗尽当时伤兵池 $W=465$）；后续紧随触发【锦帆百翎】造成 141 兵刃伤害本应倒戈恢复 62 兵力，但实际恢复量直接为 **0**。证实治疗即时扣减池容量至 0，无延迟释放。

---

## 9. Round Transition Decay (回合过渡衰减) — Tier A / Tier C 分层

- **规则编号**: `Rule-A5 (One-Round Transition Decay)` — **Tier A**
  - **触发时机**: 回合切换阶段（Round $t \rightarrow t+1$）。
  - **单回合衰减公式**:
    $$W_{t+1} = \lfloor 0.90 \times W_t \rfloor$$
  - **实证支持**:
    - 10 笔独立纯净跨单回合无受击无治疗样本，实测残存容量与 $\lfloor 0.90 \times W_t \rfloor$ 严格拟合（10/10 样本误差 $\Delta = 0$）。
    - 战报 110931 郭嘉第 1 回合末结余伤兵 532，第 2 回合初实测恢复上限恰好为 $\lfloor 532 \times 0.90 \rfloor = 478$。
- **规则编号**: `Rule-C1 (Multi-Round Iteration Default)` — **Tier C**
  - **多回合连续推演公式**:
    $$W_{t+k} = \lfloor 0.90 \times W_{t+k-1} \rfloor, \quad \forall k \ge 2$$
  - **分层说明**: 113 场战报中不存在“跨 2 回合以上既无受击又无治疗且在第 3 回合出现饱和治疗截断”的纯净判别样本（`tools/search_multi_round_clean.py` 实测返回 0 笔）。多回合递推属于状态机时钟逻辑的自然规范外推（Tier C），严禁标注为 Tier A 实证闭环。

---

## 10. Action Boundary Semantics (行动边界无损性) — Tier A

- **规则编号**: `Rule-A6 (Action Invariance)`
- **语义约束**: 回合内跨武将行动（Action Transitions）、普攻前后、战法发动间隙，未观察到伤兵池衰减（No Action Decay Observed）。在现有实证观测精度下，伤兵池衰减率为 **0**。
- **实证支持**:
  - 15 场战报在不同行动步长（$\Delta Action \in [0, 4]$）下验证，同一回合内早受击与晚受击武将的可恢复容量无递减迹象。衰减时钟仅在回合边界离散脉冲触发。

---

## 11. Damage Family Matrix (伤害家族矩阵)

| 伤害家族 / 子类 | 权威等级 | 伤兵生成规则 | 实证状态 / 边界说明 |
| :--- | :---: | :--- | :--- |
| **WEAPON (普通攻击)** | **Tier A** | $\lfloor 0.90 \times \Delta T \rfloor$ | 30 笔纯净单段截断样本完全拟合，反例搜索 0 违例。 |
| **WEAPON (主动/突击/被动)** | **Tier A** | $\lfloor 0.90 \times \Delta T \rfloor$ | 包含所向披靡、避实击虚等，完全拟合。 |
| **WEAPON (反击/倒戈反伤)** | **Tier A** | $\lfloor 0.90 \times \Delta T \rfloor$ | 包含气凌三军、夏侯惇刚烈，完全拟合。 |
| **DOT (中毒 POISON)** | **Tier A** | $\lfloor 0.90 \times \Delta T \rfloor$ | 战报 108422 确凿测得单段溃逃/中毒损兵生成闭环。 |
| **DOT (溃逃 ESCAPE)** | **Tier A** | $\lfloor 0.90 \times \Delta T \rfloor$ | 同上，实测 $\lfloor 0.90 \times \Delta T \rfloor$ 严格无误。 |
| **STRATEGY (谋略主动/被动)** | **Tier B** | $\lfloor 0.90 \times \Delta T \rfloor$ (有界) | 复合受击数据约束在 $[0.88, 0.92]$，采用 0.90 规范继承。 |
| **DOT (灼烧/水攻/沙暴/叛逃)** | **Tier B** | $\lfloor 0.90 \times \Delta T \rfloor$ (有界) | 复合受击数据无冲突，界限锁定，采用 0.90 规范继承。 |

---

## 12. Share / Distribution Interaction (分担与分摊交互)

- **规则编号**: `Rule-A7 (Share Direct Wounded Generation)` — **Tier A**
  - **机制**: 当友军受到伤害触发【分担】（如周泰【肉身铁壁】）时，伤害在扣减前被拆分：
    - 主受击者按其实际承受扣减损兵入池：$\Delta W_{target} = \lfloor 0.90 \times \Delta T_{target} \rfloor$。
    - 分担者按其实际承担扣减损兵入池：$\Delta W_{sharer} = \lfloor 0.90 \times \Delta T_{sharer} \rfloor$。
  - **实证支持**: 战报 6319219 周泰分担孙权受击损兵 517，周泰自身伤兵池精准入池 465 兵力（$\lfloor 517 \times 0.90 \rfloor = 465$）。
- **规则编号**: `Rule-C2 (Distribution Generic Fallback)` — **Tier C**
  - **机制**: 113 战报库中无分摊（DISTRIBUTION）样本，标记为 `UNOBSERVED`。
  - **禁令**: 严禁依据分担实证关闭 Stage 9 的 `DSTS9-B02` 挂起缺陷。Runtime 规范默认采用通用管线，但保持研究缺陷开放。

---

## 13. HealingBlock Interaction (禁疗交互) — Tier A / Tier B 分层

- **规则编号**: `Rule-A8a (HealingBlock Persistence / HB-P1 机制)` — **Tier A**
  - **机制**: 禁疗状态（HealingBlock）生效期间：
    1. 阻断一切实际恢复执行（$H_{actual} = 0$）。
    2. **伤兵池物理结构绝对不被清空或销毁**（确凿证伪 HB2 清空假说）。
    3. 禁疗状态解除后，残存伤兵池立即可供后续治疗正常吸收。
  - **实证锚点**: 战报 1523835 左慈：第 2 回合受焚辎营垒施加禁疗并受击损失 1603 兵力；自愈恢复被禁疗阻断归 0；第 3 回合初禁疗消失，左慈立即通过自愈恢复 $281 + 13$ 兵力，证实伤兵池在禁疗中持久存活。
- **规则编号**: `Rule-B3 (HealingBlock Period Decay / HB-P2 机制)` — **Tier B**
  - **机制**: 禁疗期间跨回合边界正常发生衰减（$W_{t+1} = \lfloor 0.90 \times W_t \rfloor$）。
  - **实证说明**: 左慈解除禁疗后的实际恢复量（$281 + 13 = 294$）未达到饱和容量截断点（小于衰减后的 1297 与冻结的 1442），经验上无法排除未衰减假设（HB3）。因此，禁疗期间的衰减属于有界继承（Tier B），采用通用回合衰减规则统一处理。

---

## 14. Defeat / Overkill Boundaries (阵亡与过量伤害边界) — Tier C

- **规则编号**: `Rule-C3 (Lethal Overkill Canonical Default)` — **Tier C**
  - **定义**: 当单次伤害名义量 $D > T_{current}$ 时，实际损兵为 $\Delta T = T_{current}$。
  - **生成基准**: 运行时规范默认将实际损兵作为伤兵计算基准：$\Delta W = \lfloor 0.90 \times T_{current} \rfloor$。
  - **经验说明**: 阵亡武将已无法接受恢复探针，其真实底层隐藏池不可经验观测，因此该规则属于规范默认值。
- **规则编号**: `Rule-C4 (Defeat Pool Cleanup)` — **Tier C**
  - **定义**: 武将 $T_{current} = 0$ 判定阵亡后，其关联伤兵池立即执行注销重置：
    $$W \leftarrow 0$$
  - **安全保障**: 防止已被击溃单元在异常战斗逻辑或复活机制未完全定义时产生非法的恢复容量悬挂。

---

## 15. Recovery Formula Boundary (与 Stage13-B3 的权责边界)

本合同与后续治疗数值研究（Stage13-B3）建立坚固的防火墙隔离：

```text
+-----------------------------------------------------------+
| Stage13-B3: 治疗名义量产生管线 (Nominal Recovery Formula)   |
|   H_nominal = f(武将智力, 战法系数, 治疗增幅, 兵力系数...)     |
+-----------------------------------------------------------+
                             |
                             v H_nominal
+-----------------------------------------------------------+
| Stage13-B1: 可恢复容量截断管线 (Recovery Capacity Clamp)     |
|   H_actual = min(H_nominal, WoundedPool, MissingTroops)   |
|   WoundedPool -= H_actual                                 |
+-----------------------------------------------------------+
```

- **严禁越界**: 本合同绝不推导、预测或冻结 $H_{nominal}$ 的生成公式（如“急救公式”、“休整公式”的具体多项式）。本合同只负责在上游输出 $H_{nominal}$ 之后，实施 $W$ 与 $M$ 的双重 Clamp 物理截断。

---

## 16. State Invariants (状态机绝对不变量)

任何运行时实现在任何离散时钟点都必须 100% 满足以下不变量，否则断言失败并抛出异常：

1. **不变量 1 (非负性)**:
   $$W(u) \ge 0, \quad \forall u \in Units$$
2. **不变量 2 (缺兵量天花板约束)**:
   $$W(u) \le M(u) = T_{max}(u) - T_{current}(u), \quad \forall u \in Units$$
3. **不变量 3 (阵亡清零 — 规范安全性约束)**:
   $$T_{current}(u) == 0 \implies W(u) == 0$$
4. **不变量 4 (单调消耗性)**:
   在无受击损兵的任意操作窗口中，单次恢复后必然满足：
   $$W_{after} = W_{before} - H_{actual}$$
5. **不变量 5 (衰减单调不增性)**:
   在回合切换中，若无受击损兵，必有：
   $$W_{t+1} \le W_t$$

---

## 17. Canonical Event Ordering (标准战斗管线时序)

回合过渡内部的标准离散时钟事件顺序如下：

```text
[Round Start Boundary (回合开始边界)]
    |-- 1. [规范默认子时序 (Tier C)] 触发回合切换衰减: 对所有存活武将执行 W = floor(0.90 * W)
    |-- 2. 状态机生命周期更新 (持续回合结算、禁疗/状态倒计时递减)
    |-- 3. 准备阶段被动/指挥恢复结算 (执行 H_actual = min(H_nominal, W, M); W -= H_actual)
    v
[Action Execution Loop (武将行动循环)]
    |-- A. 行动开始 (Action Start, 伤兵池 0 衰减)
    |-- B. 伤害计算与扣血 (Damage Pipeline)
    |       |-- 扣减当前兵力: T_current -= DeltaT
    |       |-- 伤兵池逐笔入池: W = min(M, W + floor(0.90 * DeltaT))
    |-- C. 分担/反弹扣血 (Share Pipeline)
    |       |-- 分担者扣血: T_sharer -= DeltaT_share
    |       |-- 分担者入池: W_sharer = min(M_sharer, W_sharer + floor(0.90 * DeltaT_share))
    |-- D. 恢复结算 (Recovery Pipeline / 倒戈 / 急救 / 主动治疗)
    |       |-- 计算 H_nominal (B3 管线)
    |       |-- 实施容量截断: H_actual = min(H_nominal, W, M)
    |       |-- 兵力增加: T_current += H_actual
    |       |-- 伤兵池消耗: W = max(0, W - H_actual)
    |-- E. 阵亡检测: 若 T_current == 0，执行 W = 0
    |-- F. 行动结束 (Action End, 伤兵池 0 衰减)
    v
[Round End Boundary (回合结束边界)]
    |-- 暂存当前 W，等待下一回合开始边界触发衰减
```

*注意：回合开始边界内部各子步骤（衰减、状态过期、准备阶段恢复）的精确子次序在宏观战报中表现为原子时钟切换，其具体实现顺序属于 **Tier C Canonical Runtime Default**。*

---

## 18. Empirically Frozen Rules (实证冻结规则清单 — Tier A)

以下规则通过了全部实证与独立审计，正式冻结：

1. **Rule-A1**: 伤兵生成比率严格为 $90\%$（经 $[0.850, 0.950]$ 网格扫描及离散多模型对照确立）。
2. **Rule-A2**: 整数截断严格采用逐笔独立局部向下取整（Event-Local Floor）。
3. **Rule-A3**: 恢复结算严格受限于 $\min(H_{nominal}, W, M)$。
4. **Rule-A4**: 实际恢复即时 $1:1$ 扣减伤兵池累加器。
5. **Rule-A5**: 单次跨回合衰减率严格为 $10\%$（保留 $\lfloor 0.90 \times W \rfloor$）。
6. **Rule-A6**: 回合内行动边界无观察到衰减（No Action Decay Observed）。
7. **Rule-A7**: 兵刃（普通攻击、主动战法、被动/突击战法、反击）完全适用 90% 规则。
8. **Rule-A8**: 中毒（Poison）、溃逃（Escape）DOT 伤害完全适用 90% 规则。
9. **Rule-A9**: 受分担者（SHARE）按自身实际扣减兵力独立生成伤兵。
10. **Rule-A10**: 禁疗状态持久化保留伤兵池（HB-P1 机制，确证不被清空）。
11. **Rule-A11**: 统合共享池核心——常规被动治疗与兵刃倒戈吸血完全共享单一累加器。

---

## 19. Bounded Rules (有界规则清单 — Tier B)

以下规则在复合受击环境中成立，界限明确，但缺少纯净单段截断样本：

1. **Rule-B1 (STRATEGY Damage Wounded Ratio)**:
   - 谋略伤害在所有混合样本中与 90% 表现一致，界限为 $[0.88, 0.92]$。规范继承采用 $0.90$。
2. **Rule-B2 (Other DOT Subclasses)**:
   - 灼烧（Burn）、水攻（Water）、沙暴（Sandstorm）、叛逃（Defection）。规范继承采用 $0.90$。
3. **Rule-B3 (HealingBlock Period Decay / HB-P2)**:
   - 禁疗期间的回合衰减行为（由于解除后样本未达饱和截断，经验上无法排除未衰减），规范继承单回合衰减规则。
4. **Rule-B4 (Extended Recovery Family Pool Sharing)**:
   - 急救（FIRST_AID）、休整（RECUPERATION）与谋略倒戈（STRATEGY_LIFE_STEAL）通过统一恢复管线共享池子，规范继承统合池。

---

## 20. Canonical Runtime Defaults (规范运行时默认值 — Tier C)

以下规则为实现确定性所必需的规范设定，非直接实证事实：

1. **Rule-C1 (Multi-Round Recursive Decay)**:
   - 连续跨 $k$ 回合（$k \ge 2$）按 $W_{t+k} = \lfloor 0.90 \times W_{t+k-1} \rfloor$ 递推。
2. **Rule-C2 (Distribution Damage Wounded Generation)**:
   - 分摊伤害由于战报无样本，默认继承通用扣血伤兵生成逻辑，**但严禁借此关闭 DSTS9-B02**。
3. **Rule-C3 (Lethal Overkill Wounded Base)**:
   - 致死过量伤害以实际损兵 $L = T_{current}$ 作为入池基准。
4. **Rule-C4 (Defeat Pool Cleanup)**:
   - 阵亡单元伤兵池强制注销归 0。
5. **Rule-C5 (Round Transition Sub-ordering)**:
   - 回合切换内部衰减、状态过期与准备阶段恢复的顺序规范。

---

## 21. Explicit Non-Claims (显式非主张声明)

本合同郑重声明**未证明且不主张**以下内容：

1. **非主张 1**: 未证明【急救】（FIRST_AID）的底层具体名义治疗量计算公式。
2. **非主张 2**: 未证明【休整】（RECUPERATION）的具体名义治疗量计算公式。
3. **非主张 3**: 未证明谋略及常规主动治疗的名义量公式。
4. **非主张 4**: 未证明增伤与减伤的堆叠结算多项式（Stage13-B2 课题）。
5. **非主张 5**: 未证明或关闭 Stage 9 的 `DSTS9-B02` 分摊系统遗留问题。
6. **非主张 6**: 未证明原版游戏在武将阵亡后底层内存池是否仍秘密保留隐式伤兵数值（本合同仅给出规范清零）。
7. **非主张 7**: 未证明致死过量伤害在原版游戏隐藏变量中是否存在超出实际损兵的理论伤兵。
8. **非主张 8**: 未证明战报结算/客户端协议中是否存在独立的伤兵、死兵原始字段（Q15 维持 UNOBSERVED）。

---

## 22. Remaining Research Debts (剩余研究技术债)

1. **Debt-B1-01 (纯净谋略单段截断样本)**:
   - 寻找仅受单笔谋略伤害并在同回合被饱和急救截断的纯净战报，以将 Rule-B1 从 Tier B 升格为 Tier A。
2. **Debt-B1-02 (纯净多回合零伤害截断样本)**:
   - 寻找跨越 2 回合以上无任何伤害与恢复、并在后续回合被饱和治疗截断的战报，以将 Rule-C1 从 Tier C 升格为 Tier A。
3. **Debt-B1-03 (分摊战报实证样本)**:
   - 收集包含分摊技能的真实战报，彻底关闭 DSTS9-B02。
4. **Debt-B1-04 (禁疗期间衰减饱和截断样本)**:
   - 寻找禁疗期间损兵、解除禁疗后发生超饱和治疗截断的战报，以严格区分 HB1 与 HB3。

---

## 23. Runtime Handoff Requirements (运行时移交规范与接口定义)

未来实现 Agent（在全链路 Stage13 冻结并授权后）必须在 `sgs_v2/battle_core/` 中实现以下语义接口，严禁修改当前本轮草案外的代码：

```python
class WoundedTroopPoolProtocol:
    """
    Stage13-B1 运行时标准伤兵池接口规范 (禁止在当前阶段实现)
    """
    
    def on_actual_troop_loss(self, unit_id: str, actual_loss: int) -> int:
        """
        当武将发生实际兵力扣减时调用。
        执行 Rule-A1 与 Rule-A2:
            delta_w = floor(0.90 * actual_loss)
            wounded_pool = min(missing_troops, wounded_pool + delta_w)
        返回新增伤兵量 delta_w。
        """
        ...

    def get_wounded_capacity(self, unit_id: str) -> int:
        """
        获取武将当前最大可恢复容量 (Rule-A3):
            return min(wounded_pool, missing_troops)
        若处于禁疗状态，由上层调用方或本接口判定返回 0。
        """
        ...

    def consume_wounded_capacity(self, unit_id: str, requested_amount: int) -> int:
        """
        执行治疗扣减 (Rule-A4):
            actual_recovery = min(requested_amount, wounded_pool, missing_troops)
            wounded_pool = max(0, wounded_pool - actual_recovery)
            current_troops += actual_recovery
            return actual_recovery
        """
        ...

    def on_round_transition(self, unit_id: str) -> None:
        """
        回合切换时钟触发 (Rule-A5 与 Rule-C1):
            wounded_pool = floor(0.90 * wounded_pool)
        """
        ...

    def on_defeat(self, unit_id: str) -> None:
        """
        武将阵亡回调 (Rule-C4):
            wounded_pool = 0
        """
        ...
```

---

## 24. Evidence Anchors (权威证据锚点索引)

本合同所依据的全部证据均可在全盘扫描数据库及结构化校验 CSV 中准确定位与重放：

- **90% 伤兵生成基准**:
  - `battle_id: 101740, pid: 1008108, group: 1, key: 43`: 曹操受击损兵 1218，伤兵容量实测 1096（$\lfloor 1218 \times 0.90 \rfloor = 1096$）。
  - `battle_id: 104746, pid: 104746, group: 2, key: 67`: 程普受击损兵 653，伤兵容量实测 587（$\lfloor 653 \times 0.90 \rfloor = 587$）。
- **逐笔向下取整 (Event-Local Floor)**:
  - `battle_id: 6319219, pid: 6319219, group: 2, key: 88`: 陆逊连续承受 78 兵刃损兵，容量为 $70 + 70 = 140$（合并取整假说 141 被证伪）。
  - `battle_id: 101740, pid: 1008108, group: 2, key: 52`: 张飞连续承受 487 损兵，容量为 $438 + 438 = 876$（合并假说 877 被证伪）。
- **单回合衰减 10%**:
  - `battle_id: 110931, pid: 110931, group: 1-2, key: 112`: 郭嘉回合末结余 532 伤兵，跨回合后上限实测恰为 478（$\lfloor 532 \times 0.90 \rfloor = 478$）。
- **统合共享池与即时消耗**:
  - `battle_id: 6319219, pid: 6319219, group: 0, key: 33-42`: 周泰合军聚众恢复 465 耗尽池子，后续倒戈即时为 0。
- **禁疗持久化 (HB-P1)**:
  - `battle_id: 1523835, pid: 1523835, group: 2-3, key: 160-130`: 左慈禁疗期间恢复为 0，第 3 回合禁疗解除立即恢复 $281+13$。

---

## 25. Freeze Gate (独立审计冻结最终裁定)

本 Mechanism Contract 经独立 Freeze Auditor 严格审核，所有门禁已全数达成：

- [x] Round 4 与 Round 5 全部产物推送到 `origin/main`。
- [x] 4,542 笔全量事件重放 100% 确定性可复现（Diff 0 字节）。
- [x] 原始 Canonical Q1 ~ Q22 逐条完成恢复与对账，无遗漏无改号。
- [x] Tier A (实证冻结规则)、Tier B (有界支持)、Tier C (规范运行时默认值) 严格物理分层。
- [x] 90% 生成比率经网格扫描与反例审计确立。
- [x] Floor 逐笔取整实证锚点确凿（合并取整被 5 场独立战报证伪）。
- [x] 单回合衰减率 10% 实证锚点确凿（10/10 样本）。
- [x] 多回合衰减显式划分为 Tier C 规范默认值，杜绝冒充 Tier A 实证。
- [x] 行动边界无损性完成严格限定与验证。
- [x] 谋略伤害（STRATEGY）明确标注为 Tier B 有界继承，未被夸大。
- [x] DOT 各子类完成精确分层（中毒/溃逃为 Tier A，其余为 Tier B）。
- [x] 分摊（DISTRIBUTION）保持 UNOBSERVED，未非法关闭 DSTS9-B02。
- [x] 过量伤害（Overkill）与阵亡注销（Defeat）显式标为 Tier C 规范默认值。
- [x] 共享伤兵池假说通过周泰战报独立穿透审计。
- [x] 禁疗持久性 HB-P1 假说通过左慈战报独立穿透审计，HB-P2 准确归为 Tier B。
- [x] 治疗容量（B1）与治疗名义量（B3）划定清晰防火墙。
- [x] 未修改任何运行时代码（`Runtime Change Authorized = NO`）。
- [x] 未激活 Stage13-B2、Stage13-B3 或 Stage13-C。
