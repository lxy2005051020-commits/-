# 690102 DISARM / 缴械 — Mechanism Contract

> Research Status: **FROZEN**  
> Freeze Date: **2026-09-24**  
> Runtime Status: **SKELETON_ONLY / NOT RUNTIME-FROZEN**  
> Full-Corpus Adversarial Falsification: **SURVIVED**  
> Independent Freeze Readiness Audit: **PASSED**  
> Canonical Corpus: **19,941 battle reports / 455,796 cfg9 NormalAttack events**

本文件是 690102「缴械 / DISARM」当前研究侧 P0 机制权威。旧 `states/control/minimum_usable/690102_DISARM.md` 已 SUPERSEDED，仅保留为历史入口。

本合同只冻结**外部可观察游戏行为**。状态容器、缓存、内部对象、随机函数、队列、计数器等不得反向宣称为官方服务器实现。

---

## 1. Canonical terminology

### DISARM_PRESENT

目标已接受一个可观察的 690102 状态，且尚未通过 `cfg22` 退出。

典型进入：

```text
cfg21  「缴械」效果已施加
```

典型退出：

```text
cfg22  「缴械」效果已消失
```

`PRESENT` 只表示状态在册，不等价于“本次普通攻击必定阻断”。

### DISARM_AVAILABLE

`DISARM_PRESENT` 且当前未处于显式暂时失效状态。

```text
cfg204  「缴械」暂时失效
cfg205  「缴械」继续生效
```

### Admission Relevance

针对**每个具体 NormalAttack admission** 的瞬态上下文谓词，不是持久状态字段。

常规直接施加已观察到可在同一行动 / 因果链的后续 admission 中产生作用。反弹 / 代理施加存在非统一时序，见 B02。

### Per-Admission Effect Evaluation

当状态在册、可用且对当前 admission 相关时，本次普通攻击仍进行该次效果求值。

```text
BLOCK:
cfg230 执行缴械
→ cfg46 无法普通攻击
→ 本次攻击不产生 cfg9

NO_BLOCK:
例如 cfg229 效果因几率没有生效
→ 本次攻击可以继续
→ DISARM 不因此退出
→ 后续 NormalAttack admission 可再次求值
```

### Behavioral Masking

上游机制使 NormalAttack admission 根本不可达时，DISARM 的阻断行为暂时不可观察。

典型 STUN：

```text
cfg96 执行震慑
→ cfg44 无法行动
```

这不等于 DISARM 被移除或挂起。

---

## 2. Observable admission model

```text
NormalAttack Attempt
        │
        ▼
Is NormalAttack admission reachable?
   NO ─────> BEHAVIORAL_MASKING
   YES
        ▼
Is DISARM PRESENT?
   NO ─────> ALLOW
   YES
        ▼
Is DISARM SUSPENDED?
   YES ────> ALLOW
   NO
        ▼
Is DISARM relevant to THIS admission now?
   NO ─────> ALLOW
   UNKNOWN -> preserve boundary / unresolved
   YES
        ▼
Per-Admission Effect Evaluation
   BLOCK    -> cfg230 -> cfg46 -> no cfg9
   NO_BLOCK -> e.g. cfg229 -> attack may continue
```

后续 admission 不继承 Action Start 或上一击的冻结结果。

---

## 3. D01 — Action Opportunity Preservation

DISARM 自身不剥夺单位正常 Action Opportunity。

若行动被 STUN 等其他机制阻断，该阻断不归因于 DISARM。

---

## 4. D02 — Active Skill Independence

DISARM 不直接禁止已观察的普通主动战法发动，包括：

```text
Instant Active Skill
Prepared Active Skill preparation
Prepared Active Skill later execution
```

本条不外推至所有战法内部数值、概率或特殊条件。

---

## 5. D03 — Standard NormalAttack Permission

对于当前语料中已观察的标准 NormalAttack family，当 admission 节点可达时，当前 DISARM 上下文接受实时准入求值。

若同一次 admission 实际执行：

```text
cfg230
→ cfg46
```

则该次普通攻击在 `cfg9` 前被拒绝。

合法 NO_BLOCK，例如：

```text
cfg229
→ cfg9 may continue
```

不会移除 DISARM。

当前 observed standard NormalAttack families：

```text
Natural Primary NormalAttack
Combo #2
王元姬【垂心万物】生成标准普攻
SP马超【威武并昭】生成标准普攻
```

---

## 6. D04 — Per-Admission Live / JIT Evaluation

普通攻击权限不在 Action Start 时永久锁定。

同一行动内后续 admission 实时反映：

```text
Presence
Availability
Admission Relevance
Per-Admission Effect Evaluation
```

因此同一在册 DISARM 可以出现：

```text
Attack #1 → cfg229 → NO_BLOCK
Attack #2 → cfg230 + cfg46 → BLOCK
```

而无需状态删除后重新施加。

---

## 7. D05 — Combo #2 Re-Admission

690081 COMBO 第二击是新的标准 NormalAttack admission。

```text
First NormalAttack denied
→ Combo checkpoint not reached
→ no Combo #2

First NormalAttack executes
→ Combo #2 generated
→ Combo #2 independently re-enters current DISARM evaluation
```

---

## 8. D06 — Counterattack Boundary

依据 690085 Frozen Authority：

```text
Counterattack
NormalAttackIdentity = false
```

已观察的标准 Counterattack 不被 DISARM 作为标准 NormalAttack 直接阻断。

本条不外推到所有反应技能、被动技能或兵刃伤害。

---

## 9. D07 — Assault / Pursuit Causal Dependency

已观察 Assault / Pursuit opportunity 依赖宿主 NormalAttack 成功进入后续流程。

```text
Host NormalAttack BLOCK
→ downstream Assault opportunity absent

Host NormalAttack executes
→ downstream Assault logic can become reachable
```

是否在 Assault node 内部另有一个冗余 DISARM gate 未建立，见 B01。

---

## 10. D08 — Application Effective Timing

### D08-A Ordinary Direct Application

已观察常规直接 DISARM application 可在同一行动 / 因果链的后续 eligible NormalAttack admission 中变得 relevant。

这不表示每次 admission 必然 BLOCK；`cfg229` 仍是合法 NO_BLOCK。

### D08-B Reflected / Proxy Application

`cfg21` 不普遍等价于“对所有来源上下文立即 admission-relevant”。

已观察：

```text
6273894:
cfg21
→ same-action NormalAttack allowed
→ later action blocked

6286726:
reflected/proxy context
→ immediate blocking behavior
```

确切 discriminator = **UNKNOWN**，不得虚构固定 `NEXT_TURN_START` 偏移。

---

## 11. D09 — Natural Expiration

已观察 generic natural DISARM expiry 发生于持有者自身：

```text
Action-Start Maintenance Window
```

一旦 `cfg22` removal 已发生，后续 admission 不再继承该已到期 DISARM。

本条不定义官方内部 duration counter。

---

## 12. D10 — Explicit Removal

既有 DISARM 被显式合法清除并产生 `cfg22` 后，同一行动内之后的 eligible NormalAttack admission 可以立即反映 `DISARM_ABSENT`，无需等待下一回合。

---

## 13. D11 — Suspension / Resume

已观察协议：

```text
PRESENT + AVAILABLE
  → cfg204
PRESENT + SUSPENDED
  → cfg205
PRESENT + AVAILABLE
```

SUSPENDED 期间不阻断观察到的相关攻击。

`cfg205` 后无需 fresh `cfg21`，此前既有状态可再次参与后续 admission evaluation；恢复不等于下一击必然 BLOCK，普通 NO_BLOCK 仍适用。

---

## 14. D12 — Source Death

施加源死亡本身不是已建立 DISARM 的 generic removal trigger。

已观察：

```text
source dies
→ battle continues
→ target later acts
→ existing DISARM remains behaviorally relevant
```

之后仍可自然到期、被净化或被挂起。

---

## 15. D13 — cfg23 Reapplication Rejection

严格条件合同：

当 incoming DISARM attempt 实际产生：

```text
cfg23
「身上已存在同等或更强的缴械效果」
```

则：

```text
incoming attempt rejected
no accepted cfg21 for that attempt
no observable source takeover
no latent automatic activation after existing state disappears
```

本条不定义 hypothetical verified stronger incoming DISARM。

---

## 16. D14 — cfg23-Rejected Application Does Not Refresh

实际触发 `cfg23` 的 reapplication 未观察到刷新或延长当前已接受 DISARM 的生命周期。

本条仅适用于 `cfg23`-rejected reapplication。

---

## 17. D15 — Multiple Accepted DISARM

### D15-A Ordinary ACTIVE Domain

在严格审计普通域中，existing accepted DISARM 仍在册期间，没有观察到第二个 concurrent accepted DISARM `cfg21`。

### D15-B SUSPENDED Domain

```text
existing DISARM PRESENT + SUSPENDED
→ incoming second DISARM
```

严格 model-separating opportunity = 0，因此状态保持：

```text
UNOBSERVED
```

不得把 ordinary ACTIVE domain 的零案例外推到该边界，也不得宣称官方只有一个物理状态槽。

---

## 18. D16 — Conflict Priority Boundary

`cfg23` 的可观察语义支持：

```text
Existing does not lose the observed comparison against Incoming
```

严格观察到五组 specific bidirectional rejection pairs：

```text
出其不意 ↔ 精练策数
白衣渡江 ↔ 传檄宣威
出其不意 ↔ 奋突
高橹连营 ↔ 机鉴先识
威震华夏 ↔ 奋突
```

这些具体 pair 与 equal conflict priority 相容。

不得推导全局同阶、传递等价或完整优先级类。

Verified stronger replacement = **UNOBSERVED**，见 B03。

---

## 19. D17 — Cross-Control Composition

当前范围严格限定：

```text
DISARM × STUN
DISARM × CONFUSION
```

### STUN

```text
cfg96 执行震慑
→ cfg44 无法行动
```

STUN 可以令 NormalAttack admission 不可达，从而行为遮蔽 DISARM，但不会自动 remove / suspend DISARM。

STUN 不再阻断行动且 DISARM 仍存在时，后续 NormalAttack admission 可再次到达 DISARM evaluation。

### CONFUSION

CONFUSION 改变 target-selection semantics；DISARM 控制 NormalAttack admission。

DISARM 若在前级阻断，后续普通攻击 target-selection node 不可达。

---

## 20. D18 — Cross-Control Lifecycle Independence

在已审计 `DISARM × STUN` 与 `DISARM × CONFUSION` 语境中，观察到一个状态退出而另一个继续存在。

STUN 行为遮蔽期间，DISARM observable lifecycle 仍继续推进。

本条不证明所有控制拥有独立物理槽。

---

## 21. D19 — Special Generated Standard NormalAttack

当前 canonical corpus 中观察到两个特殊 standard-`cfg9` generator family：

```text
王元姬【垂心万物】
SP马超【威武并昭】
```

两者均与标准 JIT DISARM admission model 一致：

```text
generated NormalAttack attempt
→ DISARM BLOCK
→ cfg230
→ cfg46
→ no generated cfg9
```

未被该次 DISARM 阻断时，可执行 generated `cfg9`。

因此 Natural/Combo-only Gate 已被拒绝。未来未知 generator 属于 B05。

---

## 22. D20 — Guard Target Redirection

已观察【援护】序列中：

```text
initial NormalAttack
→ cfg143 援护
→ target redirected
```

重定向不构成发起者的第二个独立 NormalAttack admission。

本条仅覆盖已观察【援护】机制。

---

## 23. D21 — Duel Boundary

【天下无双】决斗使用 `cfg177` 专用序列。

观察到：

```text
cfg204
DISARM temporarily ineffective

→ cfg177 duel sequence

→ cfg205
DISARM available again
```

决斗结束以后，later ordinary NormalAttack 再次按普通规则 evaluate resumed DISARM。

决斗内部每一击是否仍执行冗余内部 DISARM query = **UNOBSERVABLE**，见 B04。

---

## 24. Boundary Ledger

| Boundary | Status | Frozen bounded statement |
|---|---|---|
| B01 Assault redundant internal gate | UNOBSERVABLE / NOT ESTABLISHED | 只冻结 host-NA causal suppression；内部冗余 gate 不作结论 |
| B02 Reflection/proxy admission timing | UNKNOWN | 反弹/代理 `cfg21` 不保证统一即时 relevant；判别器未知 |
| B03 Stronger replacement | UNOBSERVED | 无 strict stronger incoming case；replace/override/coexist/reject 均不预判 |
| B04 Duel internal per-strike query | UNOBSERVABLE | 只冻结 cfg204→cfg177→cfg205 宏观边界 |
| B05 Future generated NA families | OUTSIDE CURRENT CORPUS | 新 generator 必须独立验证 |

这些边界**不阻塞 Research Freeze**，也不是 Runtime 自由发挥许可。

---

## 25. Evidence provenance

关键黄金证据：

```text
D04: 2240204, 2133575, 2100191
D05: 2240204, 2135148, 2207508
D06: 2487293, 2197506, 2244444
D07: 1481645, 1481613, 2135148
D08-B: 6273894, 6286726
D09: 1481642 + corpus aggregate
D10: 1775640
D11: 2133575, 2484837
D12: 1481644, 2098327
D17/D18: 1481642, 2202663
D19: 2203070, 2136573 + SP马超 strict corpus
D20: 2202432
D21: 2484837
```

Final audit baseline：

```text
Battle Reports                     = 19,941
Executed cfg9 NormalAttack Events  = 455,796
cfg230 DISARM Execution Events     = 45,462
Core True Counterexamples          = 0
D15-B Strict Opportunities         = 0 / UNOBSERVED
Contract Mutation                  = 0
```

---

## 26. Freeze decision

```text
690102 DISARM
RESEARCH STATUS                    = FROZEN
MECHANISM CONTRACT                 = v0.4
FULL-CORPUS FALSIFICATION          = SURVIVED
INDEPENDENT FREEZE READINESS AUDIT = PASSED
TRUE COUNTEREXAMPLES               = 0
BOUNDARIES PRESERVED               = B01-B05
RUNTIME STATUS                     = SKELETON_ONLY / NOT FROZEN
NEXT OWNER                         = STAGE11 RUNTIME INTEGRATION DESIGN
```

Research Freeze 不表示 Runtime 已正确实现。任何 legacy runtime 行为只可作为后续工程待核对项，不得反向修改本合同。
