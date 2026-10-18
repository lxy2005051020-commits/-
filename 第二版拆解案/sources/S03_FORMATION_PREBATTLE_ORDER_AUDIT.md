# 准备阶段阵法与兵种发动顺序专项重审报告 (Formation Pre-Battle Order Reconciled Audit V2)

> **Document Status**: `AUTHORITATIVE_RESEARCH_AUDIT`  
> **Governance Stage**: Stage14 Formation F0-R Final User Decision & Research Closure  
> **Audited Dataset**: 43,000 战报 JSON 语料库，基于确定性文件排序 `sorted(...)[:5000]` 扫描前 5,000 份战报全量微事件流  
> **Reproduction Tool**: `Stage14_Formation_Skill_Research/tools/audit_prebattle_macro_order_v2.py`  
> **Machine-Readable Evidence**:  
>   - 全量事件明细: `Stage14_Formation_Skill_Research/02_Evidence/prebattle_macro_order_evidence_v2.csv` (80,293 行)  
>   - 审计汇总与配对 ID 清单: `Stage14_Formation_Skill_Research/02_Evidence/formation_troop_paired_report_ids_v2.json`  
>   - 边界测试夹具与回归套件: `Stage14_Formation_Skill_Research/02_Evidence/test_fixtures/prebattle_order_test_fixtures.json` (7/7 用例 100% 通过)  
> **Battle Baseline**: Battle main `9f038afa2be0c92ab88ef8719fb660f89ea3027e`  
> **Research PR #18 历史研究基线（非当前 HEAD）**: `869db60db08e34030a692c2cbbfb8925da0e9ec5`  
> **Date**: 2026-10-12  

---

## 1. 历史审计重审与证据溯源核实

在 Stage14-0 早期报告 `Stage14_Troop_Skill_Research/02_Evidence/audits/TROOP_PREBATTLE_ORDER_AUDIT.md` 中，曾提出假设性的“宏观阶段严格全序（PASSIVE $\to$ FORMATION $\to$ TROOP $\to$ COMMAND）”。

### 1.1 真实战报实证结论 (Empirical Truth)
实证表明，**真实游戏战报中绝不能将 `FORMATION -> TROOP` 的全局全序推演为全战法类型的四阶段全局定序**。在全场跨武将维度上：
- `PASSIVE -> FORMATION`: 有效样本 1,636 份，逆序 370 份。
- `FORMATION -> TROOP`: 有效样本 1,314 份，严格正序 1,314 份 (100.0%)，逆序 0 份 (`EMPIRICALLY_CONFIRMED_GAMEPLAY`)。
- `TROOP -> COMMAND`: 有效样本 2,132 份，逆序 1,294 份。
原因在于游戏客户端准备阶段战法触发是以 **武将准备阶段实时速度（Speed Order）** 主导行动循环，而非简单的大类分块。因此：
`EMPIRICAL_PREBATTLE_GLOBAL_FOUR_PHASE_ORDER = NOT_SUPPORTED`。

### 1.2 模拟器 V1 用户批准规则 (RULE-01)
用户最终批准模拟器 V1 运行规则：
`SIMULATOR_V1_PREBATTLE_ORDER = USER_APPROVED_IMPLEMENTATION_RULE`
即模拟器必须按照全局四阶段调度：
$$\text{PASSIVE} \longrightarrow \text{FORMATION} \longrightarrow \text{TROOP} \longrightarrow \text{COMMAND}$$
真实游戏研究结论和模拟器 V1 执行规则可以不同，但不得互相冒充。

### 1.3 样本量与 Taxonomy 覆盖说明
- 样本内实际观察到的独立技能名称为 **245 个**（已记录在 `tools/g0_skills_list.json`）。
- 代码 Taxonomy 集合收录了 **255 个** 技能名称（包含拓印阵法变体如【拓·锋矢阵】、【拓·三势阵】以及【虎卫军】、【鱼鳞阵】等 10 个未在前 5,000 份样本中触发的合法官方技能）。
- 全量 80,293 行事件中，`UNKNOWN` 技能数为 **0**。

---

## 2. 确定性扫描与全量事件全序复核数据

使用独立提交的正式复现脚本 `Stage14_Formation_Skill_Research/tools/audit_prebattle_macro_order_v2.py` 执行全量复核：

### 2.1 统计结果 (Empirical Verification)
- **扫描战报总数**: 5,000 份 (确定性文件排序)
- **包含准备阶段 (Group 0) 有效战报**: 4,976 份
- **排除数量与原因**: 24 份 (全部为战报缺失 Group 0，数据损坏为 0)
- **同场同时包含 FORMATION 与 TROOP 的有效战报总数**: **1,314 份**
- **严格满足 $\max(\text{FORMATION.seq}) < \min(\text{TROOP.seq})$ 的样本数**: **1,314 份 (100.0%)**
- **全局逆序反例数**: **0 份 (0.0%)**
- **同武将 (team, actor) 同时携带阵法与兵种样本数**: **523 组**，逆序数为 **0 (100.0% 正序)**
- **跨阵营双方同时携带阵法战报数 (Cross-Team Dual Formation)**: **475 份**
- **单阵法战报数**: 1,362 份
- **零阵法战报数**: 3,139 份
- **同侧单队同时携带 $\ge 2$ 个阵法违规数**: **0 份 (0.0%)**

### 2.2 相邻大类时序关系统计 (Adjacent Macro Relations)

| 检验维度 | 比较阶段关系 | 有效配对样本数 | 正序样本数 | 逆序样本数 | 裁决结论 |
|---|---|:---:|:---:|:---:|:---:|
| **全场跨武将** | **`PASSIVE -> FORMATION`** | 1,636 | 1,266 | 370 | **`NOT_GLOBAL_ORDER`** (由武将速度主导) |
| **全场跨武将** | **`FORMATION -> TROOP`** | 1,314 | 1,314 | **0** | **`GLOBAL_STRICT_ORDER` (100.0%)** |
| **全场跨武将** | **`TROOP -> COMMAND`** | 2,132 | 838 | 1,294 | **`NOT_GLOBAL_ORDER`** (由武将速度主导) |
| **同武将内部** | **`PASSIVE -> FORMATION`** | 350 | 158 | 192 | **`SLOT_OR_SPEED_DEPENDENT`** (受槽位/战法子类影响) |
| **同武将内部** | **`FORMATION -> TROOP`** | 523 | 523 | **0** | **`INTRA_HERO_STRICT_ORDER` (100.0%)** |
| **同武将内部** | **`TROOP -> COMMAND`** | 2,234 | 1,535 | 699 | **`SLOT_OR_SPEED_DEPENDENT`** (受槽位/战法子类影响) |

---

## 3. 发动日志顺序 vs 效果真实提交时点的解耦判定

### 3.1 核心裁决结论
1. **阵法早于兵种的不可逆性 (`BOUNDED_CONFIRMED`)**:
   - 在任何游戏机制与日志表现中，阵法阶段调度与效果挂载必须先于兵种战法。
2. **模拟器 V1 四阶段调度与微观排序 (RULE-01 & RULE-04)**:
   - 模拟器 V1 严格执行被动 $\to$ 阵法 $\to$ 兵种 $\to$ 指挥四阶段调度。
   - 同一阶段内武将按速度降序；双方同速时，用户批准规则 `EQUAL_SPEED_TIEBREAKER = ATTACKER_FIRST` 优先执行进攻方（严禁假定 `my = attacker`，通过 Context 明确判定）。官方真实同速定序保持 `OPEN`。
3. **双军阵法独立性 (`BOUNDED_CONFIRMED`)**:
   - 当双方队伍均有阵法发动时（475 份样本），二者各自独立生效、分别追踪所有权。
4. **同队单阵法限制 (RULE-03)**:
   - 4,976 份有效战报中同队双阵法案例为 0。用户批准规则 `TEAM_FORMATION_LIMIT = ONE_PER_TEAM` (`USER_APPROVED_IMPLEMENTATION_RULE`)，限制对象为 `SkillType.FORMATION`，模拟器运行时实施 Fail-Closed 强校验拦截。

