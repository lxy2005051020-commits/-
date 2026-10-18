# 690090 FIRST_STRIKE / 先攻 — Mechanism Contract

> Research Status: **FROZEN**  
> Freeze Date: **2026-09-23**  
> Runtime Status: **NOT_INTEGRATED / SKELETON_ONLY legacy behavior must not be treated as authority**  
> Question Ledger: **Q1-Q17 CLOSED**  
> Unified Falsification Audit: **PASSED**  
> Canonical Battle-Report Corpus: **9,969 reports**

本文件是 690090「先攻」当前研究侧 P0 机制权威。旧 `states/functional/minimum_usable/690090_FIRST_STRIKE.md` 仅保留为历史兼容入口，不再是 current authority。

本合同只冻结**外部可观察游戏行为**。排序元组、状态对象、计数器、队列容器、内部 flag 等均不得反向宣称为官方服务器实现。

---

## 1. Scope

690090「先攻」是作用于自然战斗回合 **Primary Action Slot** 排序的功能性增益状态。

本合同覆盖：

- 先攻与普通 / 遇袭的行动优先层关系；
- 同层速度与同速仲裁；
- 回合排序快照；
- 重复施加与非叠加；
- 生命周期、自然到期；
- 来源依赖型与独立施加型先攻；
- 暂时抑制 / 恢复；
- 当前常规驱散边界；
- 震慑、缴械、计穷与行动槽位的关系；
- 准备战法交互；
- Primary Action Slot 与槽内派生动作的作用域边界。

---

## 2. Terminology

### Primary Action Slot

每个自然战斗回合中武将的常规行动窗口。战报中以：

```text
cfg=723  行动回合
cfg=175  开始行动
```

作为核心可观察标志。

### In-Slot Sub-Action

发生在 Primary Action Slot 内部或由其触发的事件，例如：

```text
主动战法
准备完成后的发动
普通攻击
连击
突击
反击
被动 / 指挥响应
伤害反应
```

### Effective Speed

武将在行动排序时用于**同一行动优先层内部比较**的最终有效速度值。其具体计算公式属于速度系统机制，不在 690090 合同内定义。

### Round Snapshot

自然战斗回合首个武将开始行动之前已经建立、随后在本回合内不因先攻状态中途变化而重新排序的 Primary Action Order。

---

## 3. Core Semantics

```text
FIRST_STRIKE
= Primary Action Slot ordering state
!= speed numeric bonus
```

拥有有效先攻的单位进入高于普通单位的行动优先层。

先攻本身不表现为已观察到的速度属性数值增加，也不重新排序已经进入行动槽位后的技能、攻击、追击、反击等派生事件。

在行动排序意义上，先攻表现为二元状态：

```text
Effective First Strike = Yes / No
```

没有观察到 Level 2 / Level 3 等多倍先攻优先级。

---

## 4. Primary Action Ordering Contract

跨层关系：

```text
纯先攻层 > 普通层 > 纯遇袭层
```

当前全库跨层审计未发现有效普通层单位越过有效纯先攻单位的真实反例。

速度只在**同一行动优先层内部**进行比较。先攻不是 `Speed + N`，也不得抽象成“速度加无穷大”的官方机制陈述。

---

## 5. First Strike × Ambush / 遇袭

当前项目权威规则：

```text
先攻 + 遇袭 = 普通行动层
```

且与两种状态的施加先后顺序无关。

该条证据 provenance：

```text
PROJECT_AUTHORITATIVE_RULE / USER_CONFIRMED_RULE
```

统一证伪审计中找到 12 例先攻与遇袭共存战报，没有发现与该规则冲突的案例；这不改变其原始 provenance。

本条只冻结**可观察行动层结果**，不冻结内部是“两个状态同时保留后抵消”还是其他存储实现。

---

## 6. Same-Layer Ordering

同一行动优先层内部按以下确定性顺序仲裁：

```text
1. Effective Speed：高者先
2. 完全同速且跨阵营：攻方 > 守方
3. 完全同速且同阵营：主将 > 副将1 > 副将2
```

不得使用随机 shuffle 作为同速 Tie-break。

其中同速跨阵营与同阵营阵位规则 provenance：

```text
USER_CONFIRMED_RULE / PROJECT_AUTHORITATIVE_RULE
```

现有语料未发现明显冲突，但真实玩家底层有效速度精确相等样本极少，因此不得伪装成大规模 Class-A 实证。

---

## 7. Round Snapshot Timing

每个自然战斗回合的 Primary Action Order 在该回合首个武将依次执行前已经建立。

一旦建立，本回合行动顺序不会因为以下先攻状态变化而重新计算：

```text
中途获得先攻
中途失去先攻
中途暂时抑制先攻
来源死亡导致先攻终止
自然到期
```

因此：

- 中途获得先攻不会在当前回合插队；
- 中途失去 / 抑制先攻不会在当前回合掉位；
- 对排序的首次可观察影响出现在后续重新建立行动顺序时。

该结论不声明服务器内部一定存在某个具体 `action_queue` 数组。

---

## 8. Application Conflict / Non-Stacking

若目标当前已存在先攻，后续再次施加先攻会发生同类效果冲突并失败。

已观察特征：

```text
cfg=23
“身上已存在同等或更强的「先攻」效果”
```

冻结规则：

```text
已有先攻
→ 后续同类先攻施加失败
→ 不创建第二实例
→ 不增加层数
→ 不刷新剩余持续时间
→ 不覆盖原先攻
```

统一证伪审计覆盖 628 例重复施加判定，未发现成功叠加 / 刷新反例。

---

## 9. Lifecycle

标称持续 `N` 回合的先攻，其可观察生命周期以目标武将自身 `cfg=175 开始行动` 节点计量。

规则：

```text
若先攻在本回合目标 cfg=175 之前成功施加
→ 本回合该 cfg=175 计入一次生命周期

若先攻在本回合目标 cfg=175 之后成功施加
→ 本回合不计
→ 下一次目标 cfg=175 才计第一次
```

该模型覆盖准备阶段施加、行动前施加、行动中 / 行动后施加。

不冻结任何“内部 remaining_rounds 整数变量”的实现假设。

---

## 10. Natural Expiration

最后一个有效回合的可观察时序：

```text
Round Start / Action Order 建立时先攻仍有效
→ 武将按先攻顺位进入 Primary Action Slot
→ cfg=723 行动回合
→ cfg=175 开始行动
→ 先攻自然到期 / 效果已消失
```

因此状态本身在当前行动开始窗口已经注销，但当前回合行动顺位不会回溯重排。

准确表述是：

> 状态注销后，对行动排序的首次可观察影响发生在下一次重新建立行动顺序时。

不是“状态继续存活到下一回合”。

---

## 11. Source Dependency

先攻来源必须区分两类可观察生命周期。

### Type S — Source-Dependent

代表：

```text
工神
国士将风
```

来源持续存在是效果继续维持的条件。

```text
来源阵亡
→ 对应友军先攻立即消失
→ 当前回合既定顺位不重排
→ 后续排序不再获得该来源先攻
```

### Type I — Independently Maintained After Application

代表：

```text
白马义从
八门金锁阵
```

先攻成功施加后，其后续可观察生命周期不依赖施加者继续存活。

```text
施加者后续阵亡
→ 不撤销目标已成功获得的先攻
→ 该先攻继续按自身生命周期演进
```

这是一条行为分类，不声明内部对象模型。

---

## 12. Suppression / Recovery

特定机制可使先攻暂时失效。

已观察事件：

```text
cfg=204  「先攻」暂时失效
cfg=205  「先攻」继续生效
```

冻结规则：

- 被抑制期间，先攻不参与后续新回合排序的先攻层提升；
- 抑制解除时，若原先攻生命周期仍有效，可无需重新施加而继续生效；
- 抑制期间生命周期继续按原规则消耗；
- 若原生命周期已在抑制期间结束，则解除抑制后不再恢复。

该规则描述可观察恢复行为，不声明内部 `disabled=true`。

---

## 13. Current-Scope Dispel Boundary

在当前已审计版本和常规【驱散】机制中，先攻未被观察到作为可移除对象。

直接审计：

```text
明确命中先攻持有者的常规驱散 = 26
先攻被移除                     = 0
```

因此冻结范围仅为：

> 当前已观察常规驱散不移除先攻。

未来若出现明确“移除功能性状态 / 专门移除先攻”的新机制，属于 `OUTSIDE CURRENT OBSERVED SCOPE`，不得用本条预先否定。

---

## 14. Control Interaction

先攻排序权与行动执行许可是两个可观察层次。

### 震慑

直接核心证据：

```text
293 个 FirstStrike + Stun 存活样本
293 / 293 保留 cfg=723
293 / 293 保留 cfg=175
293 / 293 在槽位内触发 cfg=44 无法行动
控制导致槽位被删除 = 0
```

因此：

```text
先攻决定何时轮到武将
震慑决定轮到后能否执行具体动作
```

### 缴械 / 计穷

已观察样本同样保留 Primary Action Slot，并在槽位内部限制相应动作类型。

本合同不把未专项核验的其他控制自动扩展成同一已证事实。

---

## 15. Preparation Skill Interaction

准备开始与准备完成后的正式发动均发生在武将自身 Primary Action Slot 内。

因此先攻通过提前整个行动槽位，间接提前：

```text
开始准备
或
下一有效行动槽位中的准备完成 / 正式发动
```

全库审计：

```text
准备开始样本 = 8,820
准备完成发动 = 4,221
槽位外准备开始 / 完成真实反例 = 0
```

对于【后发先至】：

```text
准备开始时先攻已成功施加
→ 后续准备被控制打断
→ 已成功施加的先攻不级联回滚
```

63 个对应打断样本未观察到先攻随准备回滚。

只能表述为“已观察生命周期行为相互独立”，不得宣称服务器内部一定是两个独立对象。

---

## 16. Action Scope Boundary

先攻冻结作用域为：

```text
自然战斗回合 Primary Action Slot 排序
```

当前 9,969 份已审计语料中：

- 未观察到真实玩家同一武将实体在同一自然回合获得第二个独立 `cfg=723` Primary Action Slot；
- 连击、突击、反击等均表现为槽位内部或触发事件内部派生行为；
- Round 0 中即使先攻已经施加，也未观察到先攻改变 Round 0 后续技能执行顺序。

这是一条**当前语料零观测边界**，不是对所有未来版本的永恒不存在声明。

---

## 17. Evidence Provenance

| 机制区域 | Evidence Source | Freeze Basis |
|---|---|---|
| 基础作用域 / 跨层 / 同层速度 | `OBSERVED_BATTLE_REPORT` | 全库排序与槽位审计 |
| 先攻 × 遇袭 | `PROJECT_AUTHORITATIVE_RULE / USER_CONFIRMED_RULE` | 规则确认 + 现有语料冲突搜索 |
| 精确同速 Tie-break | `USER_CONFIRMED_RULE / PROJECT_AUTHORITATIVE_RULE` | 规则确认；现有语料覆盖有限 |
| Round Snapshot | `OBSERVED_BATTLE_REPORT` | Gain/Loss/Suppression/Source-Death 反例池 |
| Non-Stacking | `OBSERVED_BATTLE_REPORT` | 628 例 cfg=23 重复施加拒绝 |
| Lifecycle / Expiration | `OBSERVED_BATTLE_REPORT` | 3,365 条自然失效轨迹 |
| Source Dependency | `OBSERVED_BATTLE_REPORT` | Type S / Type I 来源死亡对照 |
| Suppression / Recovery | `OBSERVED_BATTLE_REPORT` | 313 cfg=204 / 42 cfg=205 + 生命周期追踪 |
| Current-Scope Dispel | `CURRENT_SCOPE_NEGATIVE_AUDIT` | 26 命中 / 0 移除 |
| Control | `OBSERVED_BATTLE_REPORT` | 293 个先攻+震慑直接样本 |
| Preparation | `OBSERVED_BATTLE_REPORT` | 8,820 starts / 4,221 completions / 63 interrupts |
| Round 0 Boundary | `OBSERVED_BATTLE_REPORT` | 9,969 Round 0 execution traces |

---

## 18. Unknown / Outside Current Observed Scope

以下不阻塞当前 Freeze：

1. 未来版本可能新增的战斗中复活 / 重返战场；
2. 未来明确针对功能性状态的特殊移除机制；
3. 当前未观察到的第二个独立 Primary Action Slot；
4. 当前未观察到的回合外交替插入型完整行动窗口；
5. 未来具有特殊覆盖 / 强度规则的新型先攻来源。

这些项目只在未来真实机制出现时重新打开对应边界，不得作为当前 Runtime 自由发挥的许可。

---

## 19. Non-Normative Abstract Ordering Model

以下仅用于表达合同语义，不声明服务器内部实现：

```text
resolve tier:
    FS only        -> FIRST_STRIKE
    Ambush only    -> AMBUSH
    both / neither -> NORMAL

order within battle round:
    priority tier
    -> effective speed
    -> attacker / defender tie-break
    -> formation slot tie-break
```

生命周期行为示意：

```text
At target cfg=175 Action Start:
    if this is the final valid lifecycle step:
        First Strike expires
        current frozen round order is not recalculated

Then:
    action permission / in-slot execution proceeds under current control state
```

---

## 20. Freeze Decision

Unified Falsification Audit 覆盖：

```text
Eligible Battle Reports        = 9,969
Combat Rounds Audited          = 46,143
Primary Action Slots Audited   = 233,855
First Strike Action Instances  = 40,170
Audited Falsification Clauses  = 15
True Counterexamples           = 0
Core Blocking Ambiguities      = 0
Evidence Provenance Violations = 0
```

最终判定：

```text
690090 FIRST_STRIKE
RESEARCH STATUS             = FROZEN
QUESTION LEDGER             = Q1-Q17 CLOSED
UNIFIED FALSIFICATION AUDIT = PASSED
BATTLE-REPORT SCAN          = TERMINATED
QUESTION EXPANSION          = TERMINATED
RUNTIME STATUS              = NOT_INTEGRATED / legacy SKELETON_ONLY
NEXT OWNER                  = STAGE11 RUNTIME INTEGRATION DESIGN
```

Research Freeze 不表示 Runtime 已正确实现。旧 Runtime 中任何与本合同冲突的排序或同速随机逻辑，均属于后续 Runtime Integration Design / Implementation 的工程欠账，不得反向修改本合同。
