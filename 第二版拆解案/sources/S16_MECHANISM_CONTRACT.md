# 690107 FALSE_REPORT / 伪报 · Mechanism Contract

> Status: **FROZEN**
>
> Contract Version: **v1.0.1-frozen**
>
> Freeze Date: **2026-09-26**
>
> Runtime Status: **NOT_INTEGRATED**
>
> Research basis: Round 1A → 1G.1, including final adversarial falsification and coverage repair.

## 1. Evidence labels

- **RESEARCH_CONFIRMED**: directly supported by the completed battle-report research program.
- **BOUNDED_UNKNOWN**: not directly observable in the current corpus; must not be promoted into a research fact.
- **PROJECT_DEFAULT**: engineering fallback only; **NOT RESEARCH-DERIVED**.

The contract freezes observable behavior. It does not claim original-game internal classes, pointers, flags, registries, trees, or enum layouts.

## 2. Core observable model

```text
FalseReport application attempt
→ admission resolution
→ rejected OR applied

if applied:
  → suppress confirmed eligible Provider mechanisms
  → tested provider-dependent still-live ongoing effects become temporarily ineffective

while active:
  → other permission systems keep their own semantics
  → equal-strength reapply is rejected / no refresh
  → source death does not remove FalseReport
  → tested cleanse mechanics can remove FalseReport early

on removal / expiry:
  → still-live dependent effects continue functioning again
  → missed trigger windows are not replayed
  → resolved historical facts are not rolled back
```

## 3. Admission contract [RESEARCH_CONFIRMED]

Admission and post-application suppression are distinct observable phases.

### 3.1 Ordinary Insight

Ordinary `690089 INSIGHT` does **not** reject FalseReport. This is a specific observable exception to ordinary Insight protection.

This rule must **not** be generalized to “FalseReport ignores all control immunity”.

### 3.2 Tested special protections

The following tested mechanisms can reject FalseReport when their protection check succeeds:

- 【以逸待劳】
- 【刚毅】

Observed two-stage contrast for 【刚毅】:

```text
protection succeeds
→ FalseReport rejected

protection fails
→ FalseReport applied
→ tested persistent equipment-special effect may then become temporarily ineffective
```

The exact hidden micro-order among unobservable admission checks is not frozen.

## 4. Suppression scope [RESEARCH_CONFIRMED]

### 4.1 Core confirmed SkillType categories

The following core SkillType categories are directly confirmed as suppressible:

- `PASSIVE`
- `COMMAND`

While FalseReport is effective on the relevant Provider, these skills are observably functionally ineffective.

### 4.2 Additional observable suppressible mechanisms

Separately from SkillType classification, the following **tested persistent Equipment Specials** have demonstrated observable FalseReport suppression:

- 踩踏
- 刚毅
- 天公
- 妖气
- 忍让
- 躲闪
- 祝福
- 忠诚
- 集智
- 周旋

This contract does **not** claim that these Equipment Specials are internally implemented as PASSIVE or COMMAND.

For 灵动、援助、无双、雄烈, the relevant observed effects were already consumed, expired, or completed before the tested FalseReport window. No post-lifetime suppression claim is made.

Untested Equipment Special subtypes remain bounded unknowns.

## 5. Provider ownership [RESEARCH_CONFIRMED]

For the tested provider-dependent ongoing categories, observable validity follows the affected **Provider / Skill Owner**, not merely the Effect Holder.

Confirmed directions:

```text
Provider A creates a tested ongoing effect on Holder B/C
Provider A receives FalseReport
→ tested still-live Provider-dependent effect on B/C may become temporarily ineffective
```

and:

```text
Holder B receives FalseReport
Provider A remains effective
→ A-provided tested effect does not become ineffective merely because B is the Holder
```

This has been observed across self, ally, and enemy relationships.

The scope is limited to tested provider-dependent still-live ongoing categories. It is not an unrestricted claim over every possible future effect type.

## 6. Ongoing effect propagation [RESEARCH_CONFIRMED]

Tested provider-dependent ongoing categories include:

- attribute modifiers;
- functional states;
- ally/enemy ongoing states;
- registered triggers / prepared listeners;
- scheduled or periodic ongoing behavior.

During suppression these categories may become observably temporarily ineffective.

For attribute modifiers, tested reports show the active numerical contribution being removed while suppressed and restored when the effect continues.

The research does **not** freeze an internal assertion that a particular memory object stays allocated or mounted.

## 7. Resolved-fact boundary [RESEARCH_CONFIRMED]

FalseReport does not retroactively roll back already resolved historical facts.

Examples include already resolved:

- damage / troop loss;
- recovery;
- resource consumption;
- completed event results.

```text
ONGOING EFFECT
→ may become temporarily ineffective

RESOLVED FACT
→ no retroactive rollback
```

## 8. Skill / action categories not directly suppressed [RESEARCH_CONFIRMED WITH TESTED-SCOPE BOUNDARY]

No FalseReport-linked temporary invalidation was found for the tested standard cases of:

- `ACTIVE`
- `PREPARATION_ACTIVE`
- `ASSAULT`
- `NORMAL_ATTACK`
- standard `FORMATION`
- standard `TROOP`
- `TALENT`

“Not directly suppressed by FalseReport” does not mean “always executable”. Other states still govern their own permissions.

Examples:

- STUN may prevent action.
- DISARM may prevent normal attack.
- EXHAUSTION may prevent Active admission.
- CONFUSION may alter target selection.

## 9. Cross-state permission contract [RESEARCH_CONFIRMED FOR CORE TESTED STATES]

FalseReport participates in **Provider Effectiveness**, not general action admission.

The runtime model must keep these concerns distinct:

- action permission;
- normal-attack permission;
- Active-skill permission;
- Assault admission;
- Provider effectiveness;
- target selection;
- control protection / immunity.

Confirmed cross-state independence covers the tested core combinations with:

- EXHAUSTION;
- STUN;
- DISARM;
- CONFUSION.

No single blanket `controlled = true` semantic is compatible with the frozen contract.

## 10. Lifecycle and reapplication [RESEARCH_CONFIRMED]

### 10.1 Equal-strength same-source reapplication

If an equal-strength FalseReport is already effective, an equal-strength same-source application is rejected.

Observed behavior:

- no refresh;
- no extension;
- no second observable coexisting instance.

### 10.2 Equal-strength different-source reapplication

A second equal-strength FalseReport from another source is likewise rejected while the first remains effective.

### 10.3 Stronger vs weaker FalseReport

**BOUNDED_UNKNOWN**

The current corpus does not contain a directly testable stronger / multi-turn native FalseReport case.

If engineering requires fallback behavior, it must be labeled:

```text
PROJECT_DEFAULT
NOT RESEARCH-DERIVED
```

## 11. Cleanse [RESEARCH_CONFIRMED FOR TESTED REMOVAL MECHANICS]

Tested removal mechanics including 【刮骨疗毒】 and 【净化】 can remove FalseReport early.

Observed removal sequence:

```text
FalseReport disappears
→ surviving suppressed effects continue functioning again
→ attribute contribution returns where applicable
```

This does not assert that every future cleanse mechanic must select FalseReport. Selection rules remain owned by the cleanse mechanism itself.

## 12. Source and holder death [RESEARCH_CONFIRMED AT OBSERVABLE LEVEL]

### 12.1 Source death

FalseReport does not require source survival.

```text
source dies
→ already applied FalseReport remains
→ it ends by its own later removal / expiry behavior
```

### 12.2 Holder death

When the holder dies, the normal future FalseReport expiry / restoration path is no longer observed for that dead holder.

The contract does not claim any specific destructor, garbage collection, memory reclamation, or object-deletion implementation.

## 13. Duration boundary [RESEARCH_CONFIRMED AT OBSERVABLE LEVEL]

For current standard observed FalseReport cases, duration follows a **holder-relative action lifecycle**.

Observed natural removal occurs at the holder-relative lifecycle point shown in the researched timelines unless removed earlier by a tested cleanse mechanic.

The contract deliberately does **not** freeze:

- an internal decrement counter;
- a hidden round-counter formula;
- a universal “covers exactly one complete action turn” abstraction.

Runtime implementation must reproduce the frozen representative report timelines rather than infer a convenient counter model.

## 14. Restoration [RESEARCH_CONFIRMED]

On natural removal or tested cleanse removal, tested still-live dependent effects observably continue functioning again without an observed recast / reacquisition event.

For tested attribute modifiers, the numerical contribution returns symmetrically.

The contract freezes **observable continuation**, not an assertion that the same internal memory object necessarily survived.

If a child effect's own lifetime has already ended, it must not be revived merely because FalseReport ends.

## 15. Missed trigger policy [RESEARCH_CONFIRMED]

If a trigger opportunity occurs while its tested Provider is suppressed:

```text
trigger opportunity occurs
→ opportunity is skipped
→ FalseReport later ends
→ missed opportunity is NOT replayed
```

Restoration is future-only:

- no backfill;
- no replay;
- no retroactive damage;
- no retroactive recovery.

## 16. Observable event ordering [RESEARCH_CONFIRMED]

At the observable log level:

```text
admission succeeds
→ FalseReport applied
→ dependent tested effects temporarily ineffective
→ numerical contribution removed where applicable
```

and:

```text
FalseReport removed / expires
→ surviving tested effects continue functioning
→ numerical contribution restored where applicable
```

Hidden function-level ordering inside admission checks is not frozen.

## 17. Bounded unknown ledger

### B-U01 — Stronger-over-weaker FalseReport
No direct corpus case. **NON-BLOCKING / BOUNDED_UNKNOWN.**

### B-U02 — Unseen future special immunity
Only tested mechanisms are frozen. Future mechanisms require their own evidence. **NON-BLOCKING.**

### B-U03 — Special NPC / scenario-only rules
Out of current standard PvP authority. **NON-BLOCKING.**

### B-U04 — Untested Equipment Special subtypes
Only tested persistent specials are research-confirmed. **NON-BLOCKING.**

If the simulator temporarily generalizes tested persistent-equipment behavior to untested persistent specials, that is a **PROJECT_DEFAULT / NOT RESEARCH-DERIVED** fallback.

## 18. Runtime capability requirements

A conforming Stage12 design must be able to:

1. resolve admission separately from post-application suppression;
2. represent FalseReport as Provider-effectiveness suppression rather than general action denial;
3. determine whether tested ongoing effects depend on an affected Provider;
4. distinguish Effect Holder from Provider;
5. suppress and resume tested still-live dependent ongoing effects without rolling back resolved facts;
6. preserve future-only trigger behavior with no replay;
7. preserve independent STUN / DISARM / EXHAUSTION / CONFUSION semantics;
8. reject equal-strength reapplication without refresh;
9. support tested early removal / cleanse;
10. preserve all BOUNDED_UNKNOWN items as non-research facts.

No specific internal class, pointer, tree, registry, flag, or boolean layout is mandated.

## 19. Forbidden implementations

The following violate the frozen contract:

- implementing FalseReport as STUN;
- implementing FalseReport as DISARM;
- implementing FalseReport as EXHAUSTION;
- blanket-disabling every skill category;
- holder-only blanket invalidation;
- deleting Passive / Command definitions as the semantic meaning of suppression;
- rolling back resolved historical damage or recovery;
- reinitializing / recasting all suppressed skills on removal;
- replaying missed triggers;
- refreshing equal-strength FalseReport duration;
- treating ordinary Insight as a FalseReport rejection;
- treating “ignores Insight” as “ignores all immunity”;
- claiming stronger-over-weaker replacement as research-confirmed;
- claiming all Equipment Specials are suppressed;
- claiming tested Equipment Specials are internally PASSIVE / COMMAND without separate evidence.

## 20. Mandatory contract tests

A later Runtime implementation must include at least the following 30 contract tests:

1. `test_insight_penetration`
2. `test_yiyidailao_rejection`
3. `test_gangyi_success_rejection`
4. `test_gangyi_failure_two_stage`
5. `test_self_passive_suppression`
6. `test_command_ally_cascade`
7. `test_command_enemy_cascade`
8. `test_passive_enemy_cascade`
9. `test_holder_fr_external_provider_intact`
10. `test_active_execution_under_fr`
11. `test_prep_active_start_under_fr`
12. `test_prep_active_complete_under_fr`
13. `test_assault_execution_under_fr`
14. `test_normal_attack_under_fr`
15. `test_formation_intact_under_fr`
16. `test_troop_intact_under_fr`
17. `test_talent_intact_under_fr`
18. `test_persistent_equipment_suppression`
19. `test_equal_strength_reapply_no_refresh`
20. `test_different_source_equal_strength_rejection`
21. `test_cleanse_immediate_resume`
22. `test_source_death_persistence`
23. `test_holder_death_observable_cleanup`
24. `test_missed_trigger_no_replay`
25. `test_resolved_damage_no_rollback`
26. `test_fr_exhaustion_permission_independence`
27. `test_fr_stun_permission_independence`
28. `test_fr_disarm_permission_independence`
29. `test_fr_confusion_targeting_independence`
30. `test_duration_representative_timeline_reproduction`

## 21. Freeze declaration

```text
690107 FALSE_REPORT

Research Status:
FROZEN

Mechanism Contract:
FROZEN
Version: v1.0.1-frozen

Runtime Implementation:
NOT_INTEGRATED

Remaining Bounded Unknowns:
NON-BLOCKING
```

This contract is the research-side authority for Stage12 design. Runtime work must not silently broaden any bounded claim.
