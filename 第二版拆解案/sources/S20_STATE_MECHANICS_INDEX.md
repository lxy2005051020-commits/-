# Official State Mechanics Index

> **2026-10-04 cross-repo reconciliation:** Project Stage numbering is owned by the Battle repository. Research Wave numbering is research-only. Current baseline: Research FROZEN 40 / Runtime FROZEN TO CONTRACT 40 / Strict Complete 40. Full cross-axis view: [STATE_COMPLETION_MATRIX.md](STATE_COMPLETION_MATRIX.md).

本文件只负责状态导航、研究状态与正式合同入口。机制正文以当前 P0 / Freeze Record 为准；旧 `minimum_usable` 文件如果已标 `SUPERSEDED`，只用于历史追踪与旧路径兼容。

## 1. Status vocabulary

```text
FROZEN                           = 当前机制 P0 已冻结
RUNTIME_READY_WITH_RESEARCH_DEBT = 运行时确定、设计不阻塞，但仍有明确实证债务
MINIMUM_USABLE                  = 尚无完整冻结合同的当前最小骨架\nREADY_FOR_FREEZE_AUDIT          = 研究发现与候选合同已完成，等待独立机制合同冻结审计
SUPERSEDED                      = 历史文件，不是 current authority
OPEN                            = 当前仍真实未解决
```

## 2. Persistent States / 持续性状态

| ID | State | Current Status |
|---:|---|---|
| 690072 | 灼烧 BURN | [FROZEN](states/persistent/burn/MECHANISM_CONTRACT.md) |
| 690073 | 水攻 FLOOD | [FROZEN](states/persistent/flood/MECHANISM_CONTRACT.md) |
| 690074 | 中毒 POISON | [FROZEN](states/persistent/poison/MECHANISM_CONTRACT.md) |
| 690075 | 溃逃 ROUT | [FROZEN](states/persistent/rout/MECHANISM_CONTRACT.md) |
| 690076 | 沙暴 SANDSTORM | [FROZEN](states/persistent/sandstorm/MECHANISM_CONTRACT.md) |
| 690077 | 叛逃 REBELLION | [FROZEN](states/persistent/rebellion/MECHANISM_CONTRACT.md) |
| 690078 | 急救 FIRST_AID | [FROZEN](states/persistent/first_aid/MECHANISM_CONTRACT.md) |
| 690079 | 休整 RECUPERATION | [RE-FROZEN](states/persistent/recuperation/MECHANISM_CONTRACT.md) |

## 3. Functional States / 功能性状态

| ID | State | Current Status |
|---:|---|---|
| 690069 | 奇谋 STRATEGY_CRITICAL | ✅ [FROZEN](states/functional/strategy_critical/MECHANISM_CONTRACT.md) — [Project Freeze Ledger](states/functional/strategy_critical/RESEARCH_QUESTION_LEDGER.md) / [Freeze Audit](states/functional/strategy_critical/FREEZE_AUDIT.md)；按显式 Project Decision 镜像 690070；Q26 提供 cfg32/STRATEGY_DIRECT 通道实证；普通攻击若最终 DamageLane 转为 STRATEGY_DIRECT，则可触发奇谋|
| 690070 | 会心 CRITICAL | ✅ [FROZEN](states/functional/critical/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/functional/critical/RESEARCH_QUESTION_LEDGER.md) / [Freeze Audit](states/functional/critical/FREEZE_AUDIT.md)；Q1-Q27 研究阶段完成，Q16 与 Q20-B 保留显式 UNKNOWN；canonical 11,501 战报对抗性审计 Level-A 反例 0|
| 690081 | 连击 COMBO | ✅ [FROZEN](states/functional/combo/MECHANISM_CONTRACT.md) — 独立第二次标准普攻；生命周期、死亡作用域与战斗终结边界已由 RF-P02/P03/P04 收口 |
| 690082 | 规避 EVASION | ✅ [FROZEN](states/functional/evasion/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/functional/evasion/RESEARCH_QUESTION_LEDGER.md) 记录 Q1-Q18 + Q13-B/Q15-B/Q18-B 共 21 轮研究；damage eligibility、lifecycle、multi-source、same-source reapplication、complement-product composition、RNG observability已冻结|
| 690083 | 抵御 RESISTANCE | ✅ [FROZEN](states/functional/resistance/MECHANISM_CONTRACT.md) — Q1-Q17 完成；damage eligibility、EVASION/SURE_HIT ordering、charge consumption、lifecycle、same/cross-source conflict 已冻结；官方状态冲突规则关闭 Old2 跨来源最后阻塞|
| 690084 | 群攻 CLEAVE | ✅ [FROZEN](states/functional/cleave/MECHANISM_CONTRACT.md) — damage layer、state/multi-source、secondary target queue、death/finalization 已收口；旧文件 `690084_SPLASH.md` 仅为 SUPERSEDED 入口 |
| 690085 | 反击 COUNTERATTACK | ✅ [FROZEN](stage9_core_arbitration/core_arbitration_v2/STAGE9_COUNTERATTACK_MECHANICS_FREEZE_RECORD.md) — state skeleton 已 SUPERSEDED |
| 690086 | 分摊 DISTRIBUTION | ✅ [FROZEN](stage9_core_arbitration/core_arbitration_v2/STAGE9_DISTRIBUTION_MECHANICS_FREEZE_RECORD.md) — `DSTS9-B02` CLOSED：主将作为承担者因分摊阵亡时，当前已准入 DistributionTransaction 继续排空，后续承担者与原目标继续提交，事务完成后再进入终战屏障|
| 690087 | 分担 DAMAGE_SHARE | ✅ [FROZEN](states/functional/damage_share/MECHANISM_CONTRACT.md) — integerization、target-death transaction 与作用域均已收口 |
| 690089 | 洞察 INSIGHT | ✅ [FROZEN](states/functional/insight/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/functional/insight/RESEARCH_QUESTION_LEDGER.md) / [Final Falsification](states/functional/insight/FINAL_FALSIFICATION_AUDIT.md) / [Freeze Audit](states/functional/insight/FREEZE_AUDIT.md) / [Freeze Record](states/functional/insight/FREEZE_RECORD.md)；Contract v0.3-frozen；AF01/AF02 preserved；PD-INS-001/002 frozen；690109 cross-contract amendment audit PASS|
| 690090 | 先攻 FIRST_STRIKE | ✅ [FROZEN](states/functional/first_strike/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/functional/first_strike/RESEARCH_QUESTION_LEDGER.md) / [Freeze Audit](states/functional/first_strike/FREEZE_AUDIT.md) / [Freeze Record](states/functional/first_strike/FREEZE_RECORD.md)；Q1-Q17 CLOSED；9,969 战报统一证伪审计 TRUE_COUNTEREXAMPLE=0|
| 690091 | 遇袭 SURPRISE | ✅ [FROZEN](states/functional/surprise/MECHANISM_CONTRACT.md) — [Project Freeze Ledger](states/functional/surprise/RESEARCH_QUESTION_LEDGER.md) / [Mirror Freeze Audit](states/functional/surprise/FREEZE_AUDIT.md) / [Freeze Record](states/functional/surprise/FREEZE_RECORD.md)；按显式 Project Decision 作为 690090 先攻的行动方向镜像：FIRST_STRIKE > NORMAL > SURPRISE；其余共享机制保持一致|
| 690092 | 必中 SURE_HIT | ✅ [FROZEN](states/functional/sure_hit/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/functional/sure_hit/RESEARCH_QUESTION_LEDGER.md)；Q1-Q19 已关闭；damage eligibility 由“可规避 ⇒ 可必中”项目规则与 EVASION frozen matrix 收口；per-DI current-state、Resistance consumption、reapplication/no-refresh、Redirect、Chain/Share topology 与 source-dependent provider lifecycle 已冻结|
| 690093 | 破阵 BREAK_FORMATION | ✅ [FROZEN](states/functional/break_formation/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/functional/break_formation/RESEARCH_QUESTION_LEDGER.md)；Q1-Q14 + Q14-S1 已关闭，Q15 按统一 Direct Damage 工程合同取消；Source-local defense bypass、DOT Application-bound policy、Cleave/Chain parent-derived topology、damage-reduction boundary、multi-source reject/no-refresh 与 target attribute timing 已冻结|
| 690094 | 倒戈 LIFE_STEAL | ✅ [FROZEN](states/functional/life_steal/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/functional/life_steal/RESEARCH_QUESTION_LEDGER.md) / [Freeze Audit](states/functional/life_steal/FREEZE_AUDIT.md)；Stage11 Share assigned-damage basis 已实现|
| 690095 | 攻心 STRATEGY_LIFE_STEAL | ✅ [FROZEN](states/functional/strategy_life_steal/MECHANISM_CONTRACT.md) — [Project Freeze Ledger](states/functional/strategy_life_steal/RESEARCH_QUESTION_LEDGER.md) / [Freeze Audit](states/functional/strategy_life_steal/FREEZE_AUDIT.md)；按显式 Project Decision 镜像 690094；final DamageLane 决定路由；Stage11 Share assigned-damage basis 已镜像实现|
| 690097 | 铁索连环 CHAIN_LINK | ✅ [FROZEN](stage9_core_arbitration/core_arbitration_v2/STAGE9_CHAIN_MECHANICS_FREEZE_RECORD.md) — integerization 已由 RF-P01 冻结；旧 skeleton 已 SUPERSEDED |
| 690098 | 援护 GUARD | ✅ [FROZEN](states/functional/guard/MECHANISM_CONTRACT.md) — target redirect、single pass、slot/lifecycle 已冻结 |
| 690099 | 警戒 ALERT | ✅ [FROZEN](states/functional/alert/MECHANISM_CONTRACT.md) — Independent Grant-Batch + FIFO lifecycle frozen；阈值冻结为 `MaxCarryTroops × 6%`，candidate damage `>=` 阈值即触发，10,000 MaxCarry 下 600 点恰好触发；其余非阻塞 Provider / integration debt 保持显式|
| 690221 | 看破 DAMAGE_REDUCTION_PIERCE | ✅ [FROZEN](states/functional/damage_reduction_pierce/MECHANISM_CONTRACT.md) — Contract v0.4-frozen；Cap-before-pierce + proportional reduction transform frozen；ACTIVE_SKILL 与 DOT/DELAYED 已于 Stage13 authority amendment 关闭为 `SUPPORTED_APPLICABLE`；未覆盖的特殊 command/reaction/counterattack family 仍保持显式 bounded unknown|
| UNRESOLVED | 免疫 IMMUNITY | ✅ [MINIMUM_USABLE](states/functional/minimum_usable/IMMUNITY.md) |
| UNRESOLVED | 穷追 PURSUIT | ✅ [MINIMUM_USABLE](states/functional/minimum_usable/PURSUIT.md) |

## 4. Control States / 控制状态

| ID | State | Current Status |
|---:|---|---|
| 690101 | 计穷 EXHAUSTION | ✅ [FROZEN](states/control/exhaustion/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/control/exhaustion/RESEARCH_QUESTION_LEDGER.md) / [Adversarial Falsification](states/control/exhaustion/ADVERSARIAL_FALSIFICATION_AUDIT.md) / [Freeze Audit](states/control/exhaustion/FREEZE_AUDIT.md) / [Freeze Record](states/control/exhaustion/FREEZE_RECORD.md)；Contract v0.2-frozen；23,002 份结构化战报全库证伪，18,487 次计穷执行，TRUE_COUNTEREXAMPLE=0；准备中 cfg21→cfg191 打断、跳准备不绕过、已发动实例不回滚；B-EXH-01..05 显式保留|
| 690102 | 缴械 DISARM | ✅ [FROZEN](states/control/disarm/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/control/disarm/RESEARCH_QUESTION_LEDGER.md) / [Freeze Audit](states/control/disarm/FREEZE_AUDIT.md) / [Freeze Record](states/control/disarm/FREEZE_RECORD.md)；Contract v0.4；19,941 战报全库对抗性证伪 TRUE_COUNTEREXAMPLE=0；独立 Freeze Readiness PASSED；B01-B05 显式保留|
| 690103 | 混乱 CONFUSION | ✅ [FROZEN](states/control/confusion/MECHANISM_CONTRACT.md) — JIT selector side-constraint suppression；RF-P03 已关闭旧 `CFS9-B01` residual path (`CLOSED AS UNREACHABLE`) |
| 690104 | 虚弱 WEAKNESS | ✅ [FROZEN](states/control/weakness/MECHANISM_CONTRACT.md) — [Freeze Audit](states/control/weakness/FREEZE_AUDIT.md)|
| 690105 | 禁疗 HEALING_BLOCK | ✅ [FROZEN](states/control/healing_block/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/control/healing_block/RESEARCH_QUESTION_LEDGER.md) / [Battle Evidence](states/control/healing_block/BATTLE_REPORT_EVIDENCE.md) / [Freeze Audit](states/control/healing_block/FREEZE_AUDIT.md)；Round 1–5.1 + full-corpus falsification|
| 690106 | 嘲讽 TAUNT | ✅ [FROZEN](stage9_core_arbitration/core_arbitration_v2/STAGE9_TAUNT_MECHANICS_FREEZE_RECORD.md) — selector precedence、lifecycle、source liveness 与 Guard 顺序已冻结；旧 skeleton 已 SUPERSEDED |
| 690107 | 伪报 FALSE_REPORT | ✅ [FROZEN](states/control/false_report/MECHANISM_CONTRACT.md) — [Question Ledger](states/control/false_report/RESEARCH_QUESTION_LEDGER.md) / [Adversarial Falsification](states/control/false_report/ADVERSARIAL_FALSIFICATION_AUDIT.md) / [Freeze Audit](states/control/false_report/FREEZE_AUDIT.md) / [Freeze Record](states/control/false_report/FREEZE_RECORD.md)；Contract v1.0.1-frozen；Provider ownership / Passive+Command suppression / tested Equipment boundary / lifecycle / cleanse / cross-state permissions frozen|
| 690108 | 挑拨 PROVOCATION | ✅ [FROZEN](states/control/provocation/MECHANISM_CONTRACT.md) — [Question Ledger](states/control/provocation/RESEARCH_QUESTION_LEDGER.md) / [Adversarial Falsification](states/control/provocation/ADVERSARIAL_FALSIFICATION_AUDIT.md) / [Freeze Audit](states/control/provocation/FREEZE_AUDIT.md) / [Freeze Record](states/control/provocation/FREEZE_RECORD.md)；Contract v1.0-frozen；target-operation taxonomy / Source admissibility / lifecycle / Taunt-Confusion-Insight-Exhaustion-FalseReport boundaries frozen；bounded unknowns explicit|
| 690109 | 破坏 SABOTAGE | ✅ [FROZEN](states/control/sabotage/MECHANISM_CONTRACT.md) — [Question Ledger](states/control/sabotage/RESEARCH_QUESTION_LEDGER.md) / [Round 3 Commander Audit](states/control/sabotage/ROUND3_COMMANDER_AUDIT.md) / [Freeze Audit](states/control/sabotage/FREEZE_AUDIT.md)；Contract v1.0-frozen；114 战报 final falsification；690089 cross-contract amendment PASS；B-SAB-01..09 explicit/non-blocking|
| 690110 | 捕获 CAPTURE | ✅ [FROZEN](states/control/capture/MECHANISM_CONTRACT.md) — [Question Ledger](states/control/capture/RESEARCH_QUESTION_LEDGER.md) / [Final Falsification](states/control/capture/ADVERSARIAL_FALSIFICATION_AUDIT.md) / [Freeze Audit](states/control/capture/FREEZE_AUDIT.md) / [Freeze Record](states/control/capture/FREEZE_RECORD.md)；Contract v1.0-frozen；counterattack / Active-origin DOT / Insight × Capture discriminators resolved；RST1 Resume + no-replay + source-death independence frozen；Q42/Q44/Q45/Q63 与 Q70-Q74 bounded|
| 690111 | 震慑 STUN | ✅ [FROZEN](states/control/stun/MECHANISM_CONTRACT.md) — [Research Question Ledger](states/control/stun/RESEARCH_QUESTION_LEDGER.md) / [Freeze Audit](states/control/stun/FREEZE_AUDIT.md) / [Freeze Record](states/control/stun/FREEZE_RECORD.md)；Contract v1.2-frozen；Q01-Q23 closed/bounded；11,970 份专项战报对抗性证伪 TRUE_COUNTEREXAMPLE=0；Independent Freeze Readiness PASSED；B01-B05 显式保留|
| 690222 | 威慑 INTIMIDATION | ✅ [FROZEN](states/control/intimidation/MECHANISM_CONTRACT.md) — [Question Ledger](states/control/intimidation/RESEARCH_QUESTION_LEDGER.md) / [Adversarial Falsification](states/control/intimidation/ADVERSARIAL_FALSIFICATION_AUDIT.md) / [Freeze Audit](states/control/intimidation/FREEZE_AUDIT.md) / [Freeze Record](states/control/intimidation/FREEZE_RECORD.md)；Contract v1.0-frozen；single selected Skill Provider suppression / Refresh+Reroll / source Resume preserve-binding / Insight-Gangyi-cleanse boundaries frozen；source-skill counter separated；BU-01..10 explicit|

## 5. Stage 9 shared death/finalization baseline

旧 `TARGET_DEATH → ABORT_REMAINING_ACTION` 与后来的 universal own-open-action exception 都不是 current shared authority。

当前统一模型：

```text
UnitDeathFact != BattleFinalized
already-admitted work follows its owning operation contract
not-yet-admitted future branches require a live admission gate
mechanism-local transaction owns only its own transaction
BattleFinalized occurs at an explicit finalization barrier
```

Authority:

- [STAGE9_EXECUTION_RIGHT_AND_DEATH_SCOPE_CONTRACT.md](stage9_core_arbitration/core_arbitration_v2/STAGE9_EXECUTION_RIGHT_AND_DEATH_SCOPE_CONTRACT.md)
- [STAGE9_BATTLE_FINALIZATION_BARRIER_CONTRACT.md](stage9_core_arbitration/core_arbitration_v2/STAGE9_BATTLE_FINALIZATION_BARRIER_CONTRACT.md)

## 6. Distribution commander-participant boundary

```text
Finding: DSTS9-B02
Mechanism Status: CLOSED
Rule: commander-participant death does not abort the current DistributionTransaction
Settlement: drain remaining participant commits, then commit original target Dtarget
Battle Finalization: after DistributionTransaction completes
Research Debt: NO
Authority Amendment: 2026-10-04
```

Historical corpus absence remains provenance only; it no longer leaves the contract open.


