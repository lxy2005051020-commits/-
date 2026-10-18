# Rebellion Mechanism Contract

Status ID: `690077`  
Official Name: `叛逃`  
English Name: `REBELLION`  
Status: `FROZEN`  
Freeze Date: `2026-09-06`  
Reference Family Contract: [`methodology/CONTINUOUS_DAMAGE_FAMILY_BASELINE.md`](../../../methodology/CONTINUOUS_DAMAGE_FAMILY_BASELINE.md)  
Family Freeze Audit: [`methodology/CONTINUOUS_DAMAGE_FAMILY_FREEZE_AUDIT.md`](../../../methodology/CONTINUOUS_DAMAGE_FAMILY_FREEZE_AUDIT.md)  
State Freeze Audit: [`FINAL_FREEZE_AUDIT.md`](FINAL_FREEZE_AUDIT.md)  

---

## 1. Metadata & Classification

```yaml
State_ID: 690077
Official_Name: 叛逃
English_Name: REBELLION
Category: CONTINUOUS_DAMAGE
DamageType: DYNAMIC (WEAPON / STRATEGY)
DamageSourceType: CONTINUOUS
BaseDamageFamily: DYNAMIC (WEAPON / STRATEGY)
Subfamilies:
  Weapon_Route: WEAPON_CONTINUOUS_DAMAGE_SUBFAMILY
  Strategy_Route: STRATEGY_CONTINUOUS_DAMAGE_SUBFAMILY
Confidence: HIGH_CONFIDENCE
Evidence: O + B + I
ExactNumericFormula: FORMULA_RESEARCH_OUT_OF_SCOPE
Contract_Status: FROZEN
```

- `[O]` 官方客户端多语言配置 `Global.LangId[690077]` 明确定义为：“持续性状态，拥有该状态的武将行动时将受到伤害”。官方直接施加战法描述均明确声明其伤害“受武力或智力最高一项影响，无视防御”。
- `[B]` 实战战报库（4,271 份战报样本、15,300+ 次有效 Tick）证实：叛逃在行动开始窗口结算；统率与智力防御被完全绕过（99 场跨不同防御目标完全同伤）；根据施加期属性最高项动态分流进入兵刃或谋略路线，分别受对应增减伤调控并与相反减伤形成交叉否定。
- `[I]` 属于 `CONTINUOUS_DAMAGE` 家族，完全继承持续伤害家族通用基线；并依据施加期路线分别继承 `WEAPON_CONTINUOUS_DAMAGE` 与 `STRATEGY_CONTINUOUS_DAMAGE` 子家族规则。

---

## 2. Application

```yaml
Predicate: DEFINED_BY_SOURCE_SKILL_OR_EFFECT
Target: UNIT
Application_Log: "「叛逃」效果已施加 (cfg_id 21)"
```

- **施加前提与判定**:
  - 叛逃自身不定义来源战法的发动概率、准备回合、判定目标或前置生效条件；
  - 全部施加逻辑由来源战法独立判定并驱动；
  - 来源技能成功触发并施加叛逃时，在目标实体上建立叛逃状态实例。
- **官方直接施加战法配置全清单 (15 项)**:
  - 武力倾向来源:【威谋靡亢】(20227),【狮子奋迅】(20038),【猛虎之吼】(20138),【拓·威谋靡亢】(20978),【拓·狮子奋迅】(20979),【拓·猛虎之吼】(20980)
  - 智力倾向来源:【十面埋伏】(20005),【围师必阙】(20078),【镇压黄巾】(10014),【拓·十面埋伏】(20975),【拓·镇压黄巾】(20981)
  - 多状态/其它来源:【妖术】(20025),【拓·妖术】(20976),【毒气】(30026),【叛逃】(40032)

---

## 3. Trigger Node & Frequency

```yaml
Node: TARGET_ACTION_START
Max_Per_Combat_Round_Per_Entity: 1
Execution_Log: "执行来自【战法】的「叛逃」效果 (cfg_id 96)"
Damage_Log_Normal: "损失了兵力 (cfg_id 26)"
Damage_Log_Display_Observation: "损失了兵力 (cfg_id 213, 橙色字，暴击展示层记录)"
```

- **触发窗口**: 状态持有者在大回合中的行动开始节点（`TARGET_ACTION_START`）。
- **执行顺序**: 先于武将本回合的主动战法、普通攻击判定，以及“无法行动”等行动中止流程。
- **触发频率**: 每个实体在每个战斗大回合（Combat Round）中最多触发 1 次叛逃伤害结算。15,300+ 次实战执行窗口检验无 off-node 反例。

---

## 4. Duration & Lifecycle

```yaml
Unit: COMBAT_ROUND
Value: DECLARED_BY_SOURCE_SKILL
First_Tick: NEXT_VALID_TARGET_ACTION_START
Expiration: AFTER_DECLARED_DURATION_COMPLETES
Expiration_Log: "「叛逃」效果已消失 (cfg_id 22)"
```

- **生命周期规则**:
  - 持续时间采用战斗大回合（`COMBAT_ROUND`）计数。
  - 声明 `N` 回合的叛逃，正常生命周期内最多产生 `N` 次行动开始伤害结算机会。
  - 若在目标本回合行动前施加，首跳可在同回合行动开始时触发；若在行动后施加，首跳顺延至下一回合行动开始。
  - 到期后状态在目标后续行动开始时自然移除（`cfg_id 22`），不产生第 `N+1` 次跳伤。

---

## 5. Attribution

```yaml
Source_Unit: CURRENT_EFFECTIVE_INSTANCE_SOURCE
Source_Skill: CURRENT_EFFECTIVE_INSTANCE_SKILL
Target_Unit: STATE_OWNER
```

- 当前有效叛逃实例的伤害归属，始终为施加该实例的武将与战法。
- 若发生同名叛逃刷新/覆盖，来源武将与来源战法立即替换为新施加实例的来源。
- 来源武将阵亡后，既有叛逃实例依然归属于原来源武将与技能，直至自然耗尽或被净化。

---

## 6. Instance & Reapplication (Refresh & Overwrite)

```yaml
Effective_Instance_Limit: 1
Same_Source_Reapplication: REFRESH_AND_OVERWRITE
Cross_Source_Reapplication: REFRESH_AND_OVERWRITE
Refresh_Log: "「叛逃」效果已刷新 (cfg_id 25)"

On_Refresh:
  Replace_Source_Unit: true
  Replace_Source_Skill: true
  Reset_Duration: true
  Replace_Application_Context: true
  Replace_Effect_Potency: true
  Redetermine_Dynamic_Route: true
```

- **单一有效实例约束**: 目标武将身上永远只允许存在 1 个有效叛逃实例，不存在同来源或跨来源的并行共存与多重独立跳伤。
- **完全覆盖重置规则 `[U]`**:
  - 无论是相同来源再次发动，还是其他武将施加叛逃，一旦成功施加，均触发刷新覆盖（`cfg_id 25`）。
  - 刷新发生时，重置持续时间为新战法声明的完整回合数，并完整替换来源武将、来源技能、施加期属性快照、伤害强度及伤害路线分流。
  - 不存在“高强度保护拒绝低强度刷新”的特殊机制。

---

## 7. Dynamic Route Determination & Attribute Scaling (核心特异合同)

```yaml
Route_Evaluation_Timing: LOCKED_AT_APPLICATION
Source_Attribute_Evaluation:
  Context: APPLICATION_TIME_EFFECTIVE_ATTRIBUTES
  Condition:
    If Source Effective Base ATK > Source Effective Base INT: WEAPON_ROUTE
    If Source Effective Base INT > Source Effective Base ATK: STRATEGY_ROUTE
    If Source Effective Base ATK == Source Effective Base INT: DETERMINISTIC_DEFAULT_ROUTE (ATK priority / Skill base type fallback)

Runtime_Changes_After_Application:
  Recalculate_Existing_Instance: false
  Reroute_Existing_Instance: false

Refresh:
  Policy: REDETERMINE_FROM_REFRESHED_APPLICATION_CONTEXT
  Replace_Previous_Route: true

Internal_Storage_Model: INTERNAL_IMPLEMENTATION_UNRESOLVED / NON_BLOCKING
```

- **外部行为合同**:
  - 叛逃成功施加或刷新时，读取施加者当时的有效属性（`APPLICATION_TIME_EFFECTIVE_ATTRIBUTES`），比较武力与智力的高低，确立该实例归入 `WEAPON_ROUTE` 还是 `STRATEGY_ROUTE`。
  - 确定路线后，该有效实例的驱动属性与伤害子家族即行固化（`LOCKED_AT_APPLICATION`）。
  - 施加后运行期属性变动（如被夺魂挟魄吸取、士气波动、受击掉兵）**绝不追溯重算或逆转既有实例的驱动路线**。
  - 刷新时，依据刷新时刻的新属性上下文重新比对并覆盖旧路线。
- **底层实现解耦**:
  - 引擎底层是“施加时固化路线枚举”还是“保存双属性快照在 Tick 时比对”，属于内部实现细节（`INTERNAL_IMPLEMENTATION_UNRESOLVED`），不阻断外部行为合同冻结。

---

## 8. Ignore Defense Stat Boundary (无视防御边界合同)

实战战报（Case 1, Case 2, Case 5）严密确立了“无视防御”的精确作用边界：

```yaml
Defense_Stat_Mitigation:
  Target_DEF_Stat (统率防御): BYPASSED [CONFIRMED, B]
  Target_INT_DEF_Stat (智力防御): BYPASSED [CONFIRMED, B]
  Evidence: 全库 99 组朱儁跨目标完全同伤案例，不同统率/智力武将受损完全一致

Damage_Reductions_Mitigation:
  Generic_Damage_Reductions: NOT_BYPASSED [CONFIRMED, B] (御敌屏障等通用减伤正常削减叛逃伤害)
  Route_Specific_Damage_Reductions:
    Weapon_Route:
      Weapon_Damage_Reduction: NOT_BYPASSED [CONFIRMED, B] (受暂避其锋等兵刃减伤削减，如法正 -72.18% 减伤受损 787 vs 郝昭 1370)
      Strategy_Damage_Reduction: BYPASSED_IGNORED [CONFIRMED, B] (谋略减伤对武力叛逃完全无效，如吕蒙 -73.49% 谋略减伤受损 1459 未衰减)
    Strategy_Route:
      Strategy_Damage_Reduction: NOT_BYPASSED [CONFIRMED, B] (受谋略减伤削减，司马懿易伤 vs 典韦减伤以 99.38% 比值吻合度调控)
      Weapon_Damage_Reduction: BYPASSED_IGNORED [CONFIRMED, B] (兵刃减伤对智力叛逃完全无效，典韦 -38.62% 藤甲兵减伤被完全忽略)
```

- **防御属性完全绕过**: “无视防御”仅指绕过目标的**统率防御与智力防御属性值**。
- **百分比增减伤严格适用**: 百分比伤害减免、易伤与增伤修饰符**不属于防御属性**，严格按所属路线参与计算。

---

## 9. Damage Family Modifier Compatibility Matrix

### 9.1 Weapon Route Subfamily Compatibility (武力路线)
```yaml
Weapon_Damage_Increase: APPLIES / LOCKED_AT_APPLICATION
Weapon_Damage_Reduction: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Increase: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Reduction: APPLIES / LOCKED_AT_APPLICATION
Weapon_Damage_Taken_Increase: APPLIES / LOCKED_AT_APPLICATION
Weapon_Damage_Taken_Reduction: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Taken_Increase: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Taken_Reduction: APPLIES / LOCKED_AT_APPLICATION

Strategy_Damage_Modifiers: DOES_NOT_APPLY (IGNORED)
```

### 9.2 Strategy Route Subfamily Compatibility (智力路线)
```yaml
Strategy_Damage_Increase: APPLIES / LOCKED_AT_APPLICATION
Strategy_Damage_Reduction: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Increase: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Reduction: APPLIES / LOCKED_AT_APPLICATION
Strategy_Damage_Taken_Increase: APPLIES / LOCKED_AT_APPLICATION
Strategy_Damage_Taken_Reduction: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Taken_Increase: APPLIES / LOCKED_AT_APPLICATION
Generic_Damage_Taken_Reduction: APPLIES / LOCKED_AT_APPLICATION

Weapon_Damage_Modifiers: DOES_NOT_APPLY (IGNORED)
```

---

## 10. Crit Family Compatibility (会心与奇谋双路线分流)

```yaml
Weapon_Route:
  Physical_Crit (会心):
    Participation: APPLIES
    Runtime_Policy: LOCKED_AT_APPLICATION
    Evidence: B (Case 4: 吕玲绮【狮子奋迅】cfg_id 34 会心判定，跳字 cfg_id 213 结算双倍伤害)
  Strategy_Crit (奇谋):
    Participation: DOES_NOT_APPLY

Strategy_Route:
  Strategy_Crit (奇谋):
    Participation: APPLIES
    Runtime_Policy: LOCKED_AT_APPLICATION
    Evidence: B (Case 3: 程昱【十面埋伏】+【太平道法】cfg_id 32 奇谋判定，跳字 cfg_id 213 结算双倍伤害)
  Physical_Crit (会心):
    Participation: DOES_NOT_APPLY
```

- **暴击体系分流**:
  - 武力路线叛逃继承兵刃持续伤害子家族规则：参与**会心**，不参与奇谋。
  - 智力路线叛逃继承谋略持续伤害子家族规则：参与**奇谋**，不参与会心。
- **判定与锁定窗口**:
  - 暴击判定严格在战法施加/刷新瞬间完成（`cfg_id: 34` / `cfg_id: 32`），结果锁定于实例中；
  - 行动开始 Tick 结算时，以暴击专用扣减日志（`cfg_id: 213`）打出翻倍跳伤，不在 Tick 触发期二次 ROLL 暴击。

---

## 11. Dynamic Runtime Checks (Trigger-Time Gates)

```yaml
Source_Weakness: DYNAMIC_CHECK_AT_TRIGGER
Target_Evasion: DYNAMIC_CHECK_AT_TRIGGER
Target_Barrier: DYNAMIC_CHECK_AT_TRIGGER
```

以下机制属于触发期动态判定（`DYNAMIC_CHECK_AT_TRIGGER`），与施加期快照严格分离：
- **来源虚弱**: 若来源武将在 Tick 结算瞬间处于虚弱状态，本跳伤害归零/无效。
- **目标规避**: 若目标武将在 Tick 结算瞬间规避判定成功，本跳伤害被规避。
- **目标抵御**: 若目标武将在 Tick 结算瞬间存在抵御状态，吸收本跳伤害并按抵御自身规则扣减层数。

---

## 12. Source Death

```yaml
Existing_Rebellion: PERSISTS_UNTIL_NORMAL_EXPIRATION_OR_REMOVAL
Attribution: REMAINS_WITH_CURRENT_EFFECTIVE_INSTANCE
```

- 来源武将阵亡后，其之前成功施加给敌方的叛逃状态不被自动清除。
- 状态继续在宿主后续行动开始时正常结算跳伤，伤害归属仍记为已阵亡的来源武将与战法。

---

## 13. Target Death

```yaml
Policy: GLOBAL_DEATH_HARD_TERMINATION
On_Target_Death:
  Clear_All_States: true
  Abort_Remaining_Resolution: true
  Reject_Future_Application: true
Dead_Target_Rejection_Log: "已经死亡，无法获得「叛逃」效果 (cfg_id 149)"
```

遵循项目全局死亡硬终止基线：目标阵亡立即移除全部状态并终止行动开始结算，死后拒绝新的叛逃施加。

---

## 14. Control Interaction

```yaml
Stun: DOES_NOT_SUPPRESS_REBELLION_TRIGGER
Disarm: DOES_NOT_SUPPRESS_REBELLION_TRIGGER
Silence: DOES_NOT_SUPPRESS_REBELLION_TRIGGER
Insight: DOES_NOT_IMMUNIZE_REBELLION
Confusion: DOES_NOT_REDIRECT_OR_CANCEL_EXISTING_TICK
```

- **震慑/无法行动**: 控制状态可阻止目标武将后续的主动行动与普攻，但绝不取消或压制已进入 `TARGET_ACTION_START` 阶段的叛逃伤害结算。
- **缴械/计穷**: 仅限制普攻/主动技能，与叛逃结算完全无关。
- **洞察**: 仅免疫控制类状态，不免疫持续伤害类状态。
- **混乱**: 混乱对已挂载叛逃的既有跳伤无重定向影响。

---

## 15. Removal / Cleanse

```yaml
Purify: REMOVES_IMMEDIATELY
Removal_Log: "「叛逃」效果已消失 (cfg_id 22)"
```

- 净化类技能（如刮骨疗毒、净化等）命中目标并清除负面状态时，叛逃状态立即被彻底移除。
- 移除后后续大回合不再产生叛逃伤害结算。

---

## 16. Special Modifiers Policy (Unresolved Non-Blocking)

```yaml
Special_Modifiers_Policy:
  Defense_Pierce: UNRESOLVED_NON_BLOCKING
  Reduction_Pierce: UNRESOLVED_NON_BLOCKING
  Vigilance: UNRESOLVED_NON_BLOCKING
  Limited_Count_Protection: UNRESOLVED_NON_BLOCKING
  First_Hit_Only_Protection: UNRESOLVED_NON_BLOCKING
```

此类特殊机制需要专门独立战报实证，不阻塞叛逃机制合同冻结。

---

## 17. External Systems & Identity Boundary

```yaml
External_Observers: 【一举歼灭】等
Identity_Boundary: STRICTLY_CONFINED_TO_STATUS_ID_690077
```

- **外部观察者**: 如战法检测负面状态标签，属于 `EXTERNAL_SYSTEM_OBSERVES_STATE`，单向读取叛逃状态，叛逃内部无外部技能特异逻辑。
- **身份边界**: 严格限定于官方状态 ID `690077`，排除任何非该 ID 的同名或类似文本效果。

---

## 18. Formula Research Deferred

```yaml
ExactNumericFormula: FORMULA_RESEARCH_OUT_OF_SCOPE
Formula_Status: DEFERRED
```

本合同仅冻结状态机制可观察行为（判定时点、驱动属性分流、增减伤适配矩阵、无视防御边界、暴击体系、生命周期），精确数值计算公式（系数、浮动、取整）与机制解耦，列入 `FORMULA_RESEARCH_OUT_OF_SCOPE`，不阻塞机制冻结。

---

## 19. Final Freeze Verdict

```text
================================================================================
FINAL MECHANISM FREEZE VERDICT:
State ID: 690077
Official Name: 叛逃
English Name: REBELLION
Category: CONTINUOUS_DAMAGE / DYNAMIC (WEAPON / STRATEGY)
Status: FROZEN
Freeze Date: 2026-09-06
Verification: PASSED ALL FREEZE GATES
================================================================================
```
