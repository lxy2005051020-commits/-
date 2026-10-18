# 690079 RECUPERATION (休整) Official Mechanism Contract
# 《三国志·战略版》官方状态机制合同

Status ID: `690079`
Official Name: `休整`
Internal Name: `RECUPERATION`
Category: `PERIODIC_RECOVERY_STATE` (周期性行动前恢复状态)
Family: `RECOVERY` (恢复效果家族)
Contract Status: `✅ RE-FROZEN`
Freeze Date: `2026-09-06`
Final Audit Reference: [`FINAL_FREEZE_AUDIT_V2.md`](FINAL_FREEZE_AUDIT_V2.md)
Errata Audit Reference: [`POST_REFREEZE_CONTRACT_ERRATA_AUDIT.md`](POST_REFREEZE_CONTRACT_ERRATA_AUDIT.md)
Authoritative Sources: `[O + B + I + U]`

---

## 0. Version & Audit History (版本与审计沿革)

- `aa03f2c`: 初版错误冻结（存在数据目录冲突、过度断言触发频次与未证明公式、将失效时钟阻断错误降级）。
- `601f092`: 依据 `POST_FREEZE_CORRECTIVE_AUDIT.md` 正式 Reopen，重开休整状态机制研究。
- `4036e20`: Round 3 建立外部通用基线 `SOURCE_SKILL_DEACTIVATION_LIFECYCLE_BASELINE` 并完成适用性初审。
- `20d692b`: 全局基线冻结后证据分母纠偏重审，完成三维样本解耦与时钟分类硬化。
- `FINAL_FREEZE_AUDIT_V2.md`: 澄清金丹秘术全场持续并撤销直接时钟实证，通过全局基线继承完全闭合时钟阻断，通过全部 20 项反例攻击与门禁，正式授予 `✅ RE-FROZEN`。
- `POST_REFREEZE_CONTRACT_ERRATA_AUDIT.md`: 非实质性合同勘误，明确有限回合与全场持续生命周期分支，解耦指挥来源阵亡可观测行为与系统归属。

---

## 1. Identity & Classification (状态标识与分类)

```yaml
Identity:
  Status_ID: 690079
  Official_Name: 休整
  Internal_Name: RECUPERATION
  Category: PERIODIC_RECOVERY_STATE
  Family: RECOVERY
  Client_Text: "使自身或友军获得休整状态，自身行动时有概率/必然恢复一定兵力"
  Evidence: "[O + B]"
  Confidence: CONFIRMED
```

---

## 2. Application & Instance Model (施加与实例模型)

```yaml
Application:
  Source_Skills:
    - 乘敌不虞 (20042, 主动, 2回合, 受智力影响)
    - 金丹秘术 (20054, 指挥, 战斗第3回合起持续到战斗结束, 受智力影响)
    - 镇扼防拒 (20189, 指挥, 1回合, 受智力影响)
    - 拓·镇扼防拒 (20478, 指挥, 1回合, 受智力影响)
    - 江东眷影 (20574, 缘分/阵法, 前3回合, 固定50%)
    - 婴城自守 (22026, 主动, 1回合, 固定31%不标智力)
    - 诈降 (24011, 指挥, 第2-4回合共3回合, 受智力影响)
    - 自愈 (24053, 被动, 战斗全程, 固定50%)
    - 安营扎寨 (24136, 被动, 战斗全程, 固定62.5%)
    - 诈死赴蜀 (24143, 指挥, 第2-4回合共3回合, 受智力影响)
    - 整备 (29614, 主动, 2回合, 固定40%)
  External_Recovery_Modifiers:
    - 才辩机捷 (20224, 被动, 提升休整和急救恢复量15%->30%, 自身修饰符)
  Target_Entity: 自身 / 友军单体 / 友军群体 / 我军主将
  Initial_Duration: 由施加战法显式定义 (如金丹秘术/自愈全场, 乘敌不虞 2回合, 婴城自守 1回合, 诈降 3回合)
  Event_Protocol: cfg_21 (<Hero>的「休整」效果已施加)

Instance_Model:
  Limit: SINGLE_SHARED_INSTANCE (单个实体全局同一时刻最多维持 1 个有效休整状态)
  Same_Source_Reapplication: REFRESH_AND_OVERWRITE (重置持续时间并覆盖实例参数)
  Cross_Skill_Reapplication: REFRESH_AND_OVERWRITE (后施加战法完全取代旧战法来源、技能与参数，无论强弱)
  Field_Level_Refresh:
    Replace_Source_Unit: true (CONFIRMED [B])
    Replace_Source_Skill: true (CONFIRMED [B])
    Reset_Duration: true (CONFIRMED [B])
    Replace_Treatment_Rate: true (CONFIRMED [B])
    Replace_Attribute_Context: true (CONFIRMED [B])
    Replace_Potency_Model: true (CONFIRMED [B])
    Replace_Recovery_Modifier_Context: true (CONFIRMED [U])
  Evidence: "[B + U]"
  Confidence: CONFIRMED
```

---

## 3. Trigger Architecture & Timing (触发架构与时序)

```yaml
Trigger:
  Trigger_Node: TARGET_ACTION_START (目标武将自身行动开始窗口，位于 cfg_175 与 cfg_9 之间)
  Trigger_Frequency:
    Reachable_Official_Combat:
      Observed_Max: MAX_1_PER_ENTITY_PER_COMBAT_ROUND
      Evidence: "[B]"
      Confidence: CONFIRMED
    Additional_Target_Action_Start:
      Status: UNRESOLVED_NON_BLOCKING
      Current_Reachability: NO_KNOWN_OFFICIAL_GENERATOR

First_Tick_Timing:
  Action_Before_Application:
    Rule: ELIGIBLE_IN_SAME_ROUND (施加发生在目标本回合行动之前，当回合行动开始立即触发首跳)
    Evidence: "[B]" (1,859 / 1,859 例当回合触发，100.0%)
  Action_After_Application:
    Rule: ELIGIBLE_IN_NEXT_ROUND (施加发生在目标本回合行动之后，首跳延至下一回合自身行动开始)
    Catch_Up_Tick: PROHIBITED (严格禁止回合末补跳或事后追偿)
    Evidence: "[B]" (4,265 / 4,265 例延至下回合，100.0%)
  Confidence: CONFIRMED

Duration_And_Expiration:
  Duration_Policy: SOURCE_SKILL_DEFINED

  Finite_N_Round_Instance:
    Duration_Unit: N_ROUNDS
    Enabled_Recovery_Opportunity: TARGET_ACTION_START
    Scheduled_Lifecycle: CONTINUES_DURING_TEMPORARY_INACTIVE (由全局战斗大回合推进，失效不挂起)
    Suppressed_Opportunity: LOST_WITHOUT_CATCH_UP (失效期间跳过的行动机会永久丢失)
    Suppression_Extends_Duration: false (失效不顺延持续时间)
    Natural_Expiration: AT_SOURCE_DEFINED_NOMINAL_EXPIRY (第 N+1 回合目标行动开始窗口进行到期检查)
    Observed_Expiration_Protocol: cfg_22 (<Hero>的「休整」效果已消失)
    Evidence: "[B + I]" (2,594 次自然到期实证，100% 吻合)
    Confidence: CONFIRMED

  Until_Battle_End_Instance:
    Example:
      - 金丹秘术 (20054)
      - 自愈 (24053)
      - 安营扎寨 (24136)
    Natural_N_Round_Expiration: NOT_APPLICABLE
    Termination: GOVERNED_BY_SOURCE_SKILL_LIFECYCLE / BATTLE_END / CONFIRMED_EXTERNAL_TERMINATION
    Evidence: "[O + B]"
    Confidence: CONFIRMED
```

---

## 4. Potency Architecture (恢复强度架构)

休整状态的恢复强度采取**施加期上下文快照锁定**与**触发期动态输入解耦**的架构：

```yaml
Potency_Architecture:
  Recovery_Potency:
    Defined_By_Source_Skill: true
    Skill_May_Use_Source_Attributes: true (部分来源受智力加成，部分来源为固定比例)
    Application_Context: LOCKED_AT_APPLICATION (依据 [U])
    Exact_Mathematical_Formula: FORMULA_RESEARCH_OUT_OF_SCOPE

  Application_Time_Inputs (LOCKED_AT_APPLICATION [B + U]):
    - Source_Base_Attributes:
        Source_INT: LOCKED_AT_APPLICATION (CONFIRMED [B], 左慈智力受挫降32.1%治疗量严格恒定290)
        Other_Attributes: LOCKED_AT_APPLICATION (CONFIRMED [U])
    - Treatment_Rate_Parameter: LOCKED_AT_APPLICATION (CONFIRMED [B])
    - Recovery_Modifiers:
        Source_Side_Modifier (造成治疗提升/降低): LOCKED_AT_APPLICATION (CONFIRMED [U])
        Target_Side_Modifier (受到治疗提升/降低): LOCKED_AT_APPLICATION (CONFIRMED [U])
        Recuperation_Specific_Modifier (如才辩机捷): LOCKED_AT_APPLICATION (CONFIRMED [U])
    Runtime_Changes_Recalculate: false (存续期间外部属性或修饰符变化不追溯修改已有实例)
    On_Successful_Refresh: REBUILD_FROM_REFRESH_TIME_CONTEXT (刷新成功时依据新时刻重新构建)

  Trigger_Time_Dynamic_Inputs (DYNAMIC_AT_RECOVERY_RESOLUTION [B]):
    - Target_Alive: 目标武将必须存活，阵亡武将立即终止状态机，绝不结算
    - Wounded_Troops_Cap: 实际恢复量动态受当前伤兵上限截断，Actual = min(NominalPotency, WoundedTroops)
    - Healing_Prevention: 目标处于禁疗状态时动态拦截，派发 cfg_129 削减恢复兵力至 0，状态不移除
    Evidence: "[B]"
    Confidence: CONFIRMED
```

---

## 5. Control, Lifecycle & Interaction Rules (控制、生命周期与交互规则)

```yaml
Control_Interactions:
  Stun (震慑): DOES_NOT_SUPPRESS (CONFIRMED [B], 348 例全正常触发)
  Disarm (缴械): DOES_NOT_SUPPRESS (CONFIRMED [B], 614 例全正常触发)
  Silence (计穷): DOES_NOT_SUPPRESS (CONFIRMED [B], 235 例全正常触发)
  Confusion (混乱): DOES_NOT_SUPPRESS (CONFIRMED [B], 428 例全正常触发)
  Weakness (虚弱): DOES_NOT_SUPPRESS (CONFIRMED [B], 192 例全正常触发)
  Summary: 5 大行动限制状态 1,817 次样本 100% 正常执行休整结算，零压制。

Death_Interactions:
  Active_Source_Death:
    Behavior: PERSISTS
    Evidence: "[B]"
    Confidence: CONFIRMED
    Description: 主动战法施加者阵亡后，友军身上挂载的休整持续生效至自然到期 (9 例确证)

  Command_Source_Death:
    Observable_Behavior: ASSOCIATED_RECUPERATION_REMOVED_ON_COMMAND_SOURCE_DEATH
    Event_Protocol: cfg_22
    Evidence: "[B]"
    Confidence: CONFIRMED
    State_Internal_Rule: NONE_OBSERVED (休整内部无特殊生命监听逻辑)
    System_Ownership: EXTERNAL_COMMAND_AURA_LIFECYCLE
    System_Ownership_Evidence: "[I]"
    Implementation_Blocking_For_Recuperation: false

  Target_Death:
    Behavior: HARD_TERMINATION
    Evidence: "[B]"
    Confidence: CONFIRMED
    Description: 目标阵亡立即清理所有挂载状态

Source_Skill_Deactivation (伪报 / 军心动摇):
  Interaction_Type: EXTERNAL_SYSTEM_INTERACTION
  State_Internal_Ownership: false (休整自身不维护伪报逻辑，被动响应外部系统门控)
  Active_Sourced: NOT_APPLICABLE (主动战法施加后无中途失效机制)
  Command_Passive_Sourced:
    Temporary_Inactive_Event: cfg_204 (<Hero>的「休整」暂时失效)
    Resume_Event: cfg_205 (<Hero>的「休整」继续生效)
    During_Inactive:
      Runtime_Execution: SUPPRESSED (CONFIRMED [B], 83 例自愈/金丹秘术失效窗口实测 100% 抑制)
      Duration_Clock: CLOCK_CONTINUES (CONFIRMED [B + I], 继承自已冻结全局基线 methodology/SOURCE_SKILL_DEACTIVATION_LIFECYCLE_BASELINE.md)
      Missed_Opportunity: LOST_WITHOUT_CATCH_UP (CONFIRMED [B + I], 恢复后不追偿失效期遗漏跳血)

Removal_Interactions:
  Negative_Cleanse: DOES_NOT_REMOVE (CONFIRMED [B], 净化/草船借箭/刮骨疗毒不清除增益休整)
  Positive_Dispel: UNRESOLVED_NON_BLOCKING_EXTERNAL_DEPENDENCY (被动响应外部驱散系统)

State_Ordering_With_DOT:
  Resolution_Window: 同一行动开始窗口 (TARGET_ACTION_START)
  Observed_Behavior: 既有休整在DOT前 (893 例)，亦有DOT在休整前 (506 例)
  Policy: UNRESOLVED_NON_BLOCKING (排除严格 FIFO 与固定分类，属于底层调度实现细节，不阻断状态机制)
```

---

## 6. Formula Status (公式研究范围声明)

- **微观公式归类**: 智力属性向治疗数值映射的非线性公式常数、受智力加成的非线性系数曲线、微观整除与伪随机截断算法正式归入 `FORMULA_RESEARCH_OUT_OF_SCOPE`。
- **机制层边界**: 机制合同严格界定状态的生命周期、刷新覆盖、动态门禁截断与控制交互，不包含未经验证的推测公式。

---

## 7. Reopen Conditions (重新激活重审条件)

本合同已通过 `FINAL_FREEZE_AUDIT_V2.md` 与 `POST_REFREEZE_CONTRACT_ERRATA_AUDIT.md` 审核并冻结。未来仅在满足以下排他性条件之一时允许重开：
1. 官方发布全新资料、官方答疑或技能重做，与本合同发生直接规则冲突；
2. 战报库中发现可稳定复现的核心机制反例（如失效期间时钟真实发生顺延暂停）；
3. 官方推出可在单回合赋予武将多次完整行动开始节点的全新机制，且产生休整多次结算；
4. 来源战法暂时失效全局基线被新的系统级反例推翻；
5. 底层战报解析器被证实存在实体归属或协议解析的系统性结构错误。
