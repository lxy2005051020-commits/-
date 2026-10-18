# 690101 EXHAUSTION / 计穷 — Mechanism Contract

> Contract Version: **v0.2-frozen**
> Research Status: **FROZEN**
> Runtime Status: **NOT_INTEGRATED / NOT FROZEN TO CONTRACT**
> Project Stage: **Stage12**
> Research Wave: **Wave 4**
> Freeze Date: **2026-09-26**

## 1. Authority and evidence policy

This file is the canonical research authority for 690101 EXHAUSTION / 计穷.

Evidence labels:
- OBSERVED: directly supported by battle-report event flow.
- CROSS_AUTHORITY: inherited from another frozen mechanism contract.
- PROJECT_DEFAULT: engineering/governance choice for an unobservable boundary.
- UNOBSERVABLE: cannot be discriminated from available battle reports.
- BOUNDED_UNKNOWN: unresolved edge that does not alter the frozen core model.

Runtime code is not game-mechanism evidence.

## 2. Core semantic

If EXHAUSTION is effective on a unit, that unit cannot activate ACTIVE_SKILL at an eligible Active-Skill admission point.

EXHAUSTION is a skill-permission control. It is not equivalent to STUN, DISARM, or a generic cannot-act state.

## 3. Scope matrix

| Behavior / category | Frozen disposition |
|---|---|
| ACTIVE_SKILL | BLOCKED while EXHAUSTION is effective |
| BASIC_ATTACK | NOT blocked by EXHAUSTION itself |
| Standard ASSAULT after a legal Basic Attack | NOT blocked by EXHAUSTION itself |
| PASSIVE | NOT blocked by EXHAUSTION itself |
| COMMAND | NOT blocked by EXHAUSTION itself |
| Preparation Active Skill | governed by Sections 7–9 |
| Exotic/nested skill categories | only blocked when they constitute a new ACTIVE_SKILL admission; otherwise non-claim |

## 4. Observable Active-Skill admission — EXH-ACT-01

Observed topology:

    effective EXHAUSTION
      -> cfg230 execute EXHAUSTION effect
      -> cfg45 unable to activate Active Skill
      -> no observable ACTIVE_SKILL activation

The block is holder-level/global in the observable log. Multiple equipped Active Skills do not produce one independent cfg45 per skill.

The contract does not assert whether internal candidate enumeration occurs before the block.

## 5. Zero-active-skill silent path — EXH-ACT-02

If the holder has no relevant Active Skill candidate at the observable action point, EXHAUSTION does not require a synthetic cfg230/cfg45 broadcast merely because the state exists.

The final audit found the observed zero-active path to be silent and to continue through the natural action flow.

## 6. Natural action continuation — EXH-ACT-03

EXHAUSTION does not consume the holder's natural action opportunity.

After Active-Skill admission is blocked, a legal Basic Attack may still occur unless another mechanic independently blocks it, such as DISARM, STUN, death, invalid actor state, or battle finalization.

EXHAUSTION itself must not be used as the reason to cancel a legal Basic Attack.

## 7. Standard Assault boundary — EXH-ASSAULT-01

A standard Assault Skill triggered from a legal Basic Attack remains eligible while EXHAUSTION is effective.

This does not authorize generalization to recursive or converted skill systems that create a new independent ACTIVE_SKILL admission.

## 8. Preparation start and interruption

### EXH-PREP-01 — preparation start

While EXHAUSTION is effective, a preparation Active Skill cannot reach observable START_PREPARATION.

Observed result:

    effective EXHAUSTION
      -> cfg230
      -> cfg45
      -> no cfg36 START_PREPARATION

No claim is made about hidden activation RNG consumption.

### EXH-PREP-02 — mid-preparation interrupt

If EXHAUSTION becomes effective while the unit owns an active PREPARING Active-Skill state, that preparation is immediately interrupted.

Observed topology:

    cfg21 EXHAUSTION becomes effective
      -> cfg191 preparation interrupted

The old preparation does not remain queued and does not automatically resume after EXHAUSTION ends.

### EXH-PREP-03 — restart after interruption

After an EXHAUSTION-interrupted preparation, later removal or expiry of EXHAUSTION does not restore previous preparation progress.

A future successful preparation must enter a new observable cfg36 START_PREPARATION event.

## 9. Preparation reduction / skip — EXH-PREP-04

Observed zero-preparation paths such as Wei Yan / 奇兵间道 do not bypass EXHAUSTION.

Normal observed skip-preparation path:

    cfg96 preparation-time effect
      -> cfg241 reduce preparation time
      -> cfg7 Active-Skill activation

When EXHAUSTION is already effective at the relevant admission point, the observed path is:

    cfg230
      -> cfg45
      -> no observable cfg241
      -> no cfg36
      -> no cfg7 Active-Skill activation

This freezes the behavioral result, not hidden server call order.

## 10. Already-activated skill boundary — EXH-INFLIGHT-01

EXHAUSTION does not retroactively cancel an Active-Skill instance that has already reached observable activation at cfg7.

For observed normal child-effect chains, the current activated instance is not rolled back when EXHAUSTION becomes effective during resolution.

At the same time:
- independent PREPARING skills on the holder are immediately interrupted by cfg191;
- future independent ACTIVE_SKILL admissions are blocked by EXHAUSTION.

A nested mechanic that constitutes a genuinely new independent ACTIVE_SKILL admission must still pass the EXHAUSTION permission boundary.

## 11. Lifecycle / removal boundary

### EXH-LIFE-01

Once EXHAUSTION becomes effective, its preparation-interrupt consequence is immediate. It does not wait for the holder's next natural action.

### EXH-LIFE-02

After EXHAUSTION ceases to be effective, future eligible Active-Skill admission points are no longer blocked by this state.

Bounded unknown:
- if the Active-Skill phase was already passed because of EXHAUSTION and the state is removed later in the same natural action, whether that already-passed phase is retroactively reopened is not established.

Runtime must not present retroactive reopening as evidence-backed behavior.

## 12. Insight interaction

690089 INSIGHT is the cross-state authority.

Inherited frozen rules:
- effective INSIGHT plus incoming EXHAUSTION -> protected-control admission is rejected;
- existing EXHAUSTION plus INSIGHT becomes effective -> EXHAUSTION is PRESENT_BUT_SUPPRESSED;
- while suppressed, EXHAUSTION does not block Active-Skill admission.

PRESENT_BUT_SUPPRESSED Active-Skill success is not an EXHAUSTION counterexample.

## 13. Cross-control observable ordering

### EXHAUSTION + DISARM

When both permissions are reached in the same natural action, the final audit observed Active-Skill permission block cfg45 before Basic-Attack permission block cfg46.

### STUN + EXHAUSTION

When STUN removes the natural action opportunity, the Active-Skill admission point may never be reached. EXHAUSTION must not manufacture a new action phase after STUN has preempted the action.

## 14. Observable event mapping

| cfg | Observed meaning |
|---:|---|
| 21 | EXHAUSTION admitted/applied |
| 22 | EXHAUSTION expiry/removal where observed |
| 230 | EXHAUSTION execution/check observable |
| 45 | unable to activate Active Skill |
| 36 | preparation Active Skill starts preparation |
| 191 | preparation interrupted |
| 241 | preparation-time reduction |
| 7 | observable skill activation |
| 9 | Basic Attack |

These cfg identifiers are evidence mappings, not mandatory Runtime enum values.

## 15. RNG boundary

Whether Active-Skill activation RNG is consumed while EXHAUSTION blocks admission is UNOBSERVABLE from the battle-report corpus.

The contract requires neither no-RNG-consumption nor mandatory-RNG-consumption. Any Runtime choice requires explicit project governance unless stronger authority appears.

## 16. Model disposition

Eliminated as observable behavior models:
- M3 post-RNG-success-only EXHAUSTION gate;
- M4 post-observable-activation EXHAUSTION gate;
- P2 release-only preparation model;
- P4 preparation-start snapshot immunity;
- SP2 observable skip modifier before EXHAUSTION block;
- SP4 skip-preparation override bypasses EXHAUSTION;
- AR2 continuous permission recheck that cancels the current activated skill.

Preserved bounded distinctions:
- M1 vs M2 internal candidate-selection / permission-node distinction;
- hidden RNG consumption;
- same-action retroactive phase reopening after removal;
- exotic nested mechanics that create a new ACTIVE_SKILL admission.

## 17. Runtime obligations

A conforming Stage12 implementation must satisfy:
1. Active-Skill admission consults effective EXHAUSTION.
2. EXHAUSTION becoming effective can asynchronously interrupt existing preparation.
3. Interrupted preparation does not automatically resume.
4. EXHAUSTION itself does not suppress legal Basic Attack.
5. Standard post-Basic-Attack Assault remains reachable.
6. An already activated Active-Skill instance is not retroactively rolled back.
7. Preparation-reduction/skip mechanics do not bypass EXHAUSTION.
8. INSIGHT rejection/suppression authority is honored.
9. Internal RNG ordering is not presented as evidence-backed unless separately governed.

## 18. Non-goals and bounded unknowns

This contract does not own global preparation taxonomy, every possible preparation-interrupting state, INSIGHT lifecycle internals, global RNG semantics, STUN semantics, DISARM semantics, or all exotic recursive skill semantics.

Preserved boundaries:
- B-EXH-01 hidden activation RNG consumption;
- B-EXH-02 M1 vs M2 internal admission-node distinction;
- B-EXH-03 same-action reopening after EXHAUSTION removal;
- B-EXH-04 exotic nested effects creating a new independent ACTIVE_SKILL admission;
- B-EXH-05 native 100%-base-rate ordinary Active discriminator unavailable.

These do not block Research Freeze.

## 19. Freeze basis

Final adversarial audit baseline:
- structured battle reports audited: 23,002;
- observed EXHAUSTION executions: 18,487;
- verified true Active-Skill counterexamples: 0;
- unresolved anomalies: 0;
- independent freeze review: PASS.

## 20. Final statement

    690101 EXHAUSTION / 计穷
    RESEARCH STATUS      = FROZEN
    MECHANISM CONTRACT   = v0.2-frozen
    ADVERSARIAL AUDIT    = PASS
    FREEZE AUDIT         = PASS
    RUNTIME STATUS       = NOT_INTEGRATED / NOT FROZEN
    NEXT                 = STAGE12 CONTRACT-ALIGNED RUNTIME DESIGN
