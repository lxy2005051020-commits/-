# Research Authority Index

Gameplay Truth Owner = Research Repository.
Battle code != evidence. Runtime result != empirical proof.
There is one current authority for each mechanism; historical records cannot override it.

## Current baseline — 2026-10-05

```text
Research FROZEN = 40 / 40 official-state mechanisms
DSTS9-B02 CLOSED
B1 FROZEN
B2 FROZEN
B2.5 CLOSED
B3 ordinary treatment core FROZEN
690221 Active + DOT CLOSED
690099 6% inclusive CLOSED

Stage14 Troop Foundation = FROZEN
Stage14 Troop Skill Set = ACTIVE / PARTIAL
Stage14 Batch01-04 Baselines = FROZEN (7 skills; extensions remain open)
Stage14 Jinfan = BOUNDED_FROZEN / FORMULA_PLACEHOLDERS
Stage14 Hu Wei = USER_PROVISIONAL_MODEL / RUNTIME_BASELINE_ENABLED
Stage14 Xian Deng = USER_FIT_MODEL / RUNTIME_BASELINE_ENABLED / GAMEPLAY_DETAILS_OPEN
Stage14 Xie Fan = BOUNDED_FROZEN / FINE_LINEAGE_OPEN
Stage14 Xiang Bing = DEFERRED BY USER
Stage14 Formation F0 = BOUNDED_FROZEN / MERGED_PR18 / Battle F0-I-A merged-main CI PASS
Stage14 F1 Feng Shi Zhen Lv10 = BATTLE_MAIN_MERGED / CI_2267_PASS / EVIDENCE_BOUNDED
```

## Canonical navigation

- [State contracts](STATE_MECHANICS_INDEX.md)
- [Research maturity](STATE_COMPLETION_MATRIX.md)
- [Stage9 shared execution-right/death contract](stage9_core_arbitration/core_arbitration_v2/STAGE9_EXECUTION_RIGHT_AND_DEATH_SCOPE_CONTRACT.md)
- [Stage9 finalization contract](stage9_core_arbitration/core_arbitration_v2/STAGE9_BATTLE_FINALIZATION_BARRIER_CONTRACT.md)
- [690085 Counterattack](stage9_core_arbitration/core_arbitration_v2/STAGE9_COUNTERATTACK_MECHANICS_FREEZE_RECORD.md)
- [690086 Distribution](stage9_core_arbitration/core_arbitration_v2/STAGE9_DISTRIBUTION_MECHANICS_FREEZE_RECORD.md)
- [690097 Chain Link](stage9_core_arbitration/core_arbitration_v2/STAGE9_CHAIN_MECHANICS_FREEZE_RECORD.md)
- [690106 Taunt](stage9_core_arbitration/core_arbitration_v2/STAGE9_TAUNT_MECHANICS_FREEZE_RECORD.md)
- [Damage formula V1 candidate/provenance](formulas/NORMAL_ATTACK_FORMULA_V1.md)
- [Strategy V1 model boundary](formulas/STRATEGY_DAMAGE_FORMULA_V1.md)
- [Current damage modifiers](STAGE13_B2_DAMAGE_MODIFIER_MECHANISM_CONTRACT.md)
- [Recovery formula families](B3_Recovery_Research/00_Governance/RECOVERY_FORMULA_FAMILY_INDEX.md)
- [Recovery core contract](STAGE13_B3_RECOVERY_FORMULA_MECHANISM_CONTRACT.md)
- [Stage13 research ledger](STAGE13_RESEARCH_GAP_LEDGER.md)
- [Wounded troops](STAGE13_B1_WOUNDED_TROOP_MECHANISM_CONTRACT.md)
- [Full damage closure](STAGE13_FULL_DAMAGE_CLOSURE_VERDICT.md)
- [Stage14 troop foundation contract](Stage14_Troop_Skill_Research/00_Governance/TROOP_SKILL_IDENTITY_AND_PROVIDER_LIFECYCLE_CONTRACT.md)
- [Stage14 troop question ledger](Stage14_Troop_Skill_Research/00_Governance/TROOP_SKILL_QUESTION_LEDGER.md)
- [Stage14 existing troop prebattle order evidence audit](Stage14_Troop_Skill_Research/02_Evidence/audits/TROOP_PREBATTLE_ORDER_AUDIT.md)
- [Stage14 Formation F0 historical research plan](Stage14_Formation_Skill_Research/00_Governance/FORMATION_F0_RESEARCH_PLAN.md)
- [Stage14 Formation F0 bounded readiness audit](Stage14_Formation_Skill_Research/00_Governance/FORMATION_F0_READINESS_AUDIT.md)
- [Stage14 Formation foundation authoritative contract](Stage14_Formation_Skill_Research/00_Governance/FORMATION_FOUNDATION_CONTRACT.md)
- [Stage14 F1 Feng Shi Zhen contract](Stage14_Formation_Skill_Research/01_Skills/FENG_SHI_ZHEN_RESEARCH_CONTRACT.md)
- [Stage14 F1 preintegration handoff](Stage14_Formation_Skill_Research/00_Governance/F1_FENG_SHI_ZHEN_PREINTEGRATION_READINESS.md)
- [Stage14 Round3B user-confirmed integration record](Stage14_Troop_Skill_Research/00_Governance/ROUND3B_USER_CONFIRMED_RULE_INTEGRATION.md)
- [Stage14 Batch01-04 bounded baseline freeze](Stage14_Troop_Skill_Research/00_Governance/STAGE14_BATCH01_04_BASELINE_FREEZE.md)
- [Stage14 Jinfan bounded mechanism contract](Stage14_Troop_Skill_Research/01_Skills/锦帆军/JIN_FAN_JUN_MECHANISM_CONTRACT.md)
- [Stage14 Hu Wei provisional contract](Stage14_Troop_Skill_Research/01_Skills/虎卫军/HU_WEI_JUN_PROVISIONAL_CONTRACT.md)
- [Stage14 Xian Deng user-fit contract](Stage14_Troop_Skill_Research/01_Skills/先登死士/XIAN_DENG_SI_SHI_USER_FIT_CONTRACT.md)
- [Stage14 Xie Fan bounded contract](Stage14_Troop_Skill_Research/01_Skills/解烦卫/XIE_FAN_WEI_MECHANISM_CONTRACT.md)
- [Methodology](methodology/RESEARCH_PROTOCOL.md)
- [Evidence standard](methodology/EVIDENCE_STANDARD.md)
- [Official catalog](catalogs/official_state_catalog_v1/OFFICIAL_STATE_CATALOG_V1.md)
- [Stage9 evidence/tools](stage9_core_arbitration/core_arbitration_v2/evidence/MANIFEST.md)
- [Migration ledger](governance/CROSS_REPO_RESEARCH_MIGRATION_2026-10-04.md)

## Stage14 authority notes

The following Stage14 troop rules are now canonical:

1. Special-troop conversion occurs during PRE_BATTLE.
2. Special troops inherit their declared base troop restraint family.
3. Later preparation-stage skills read the already-updated current state from earlier preparation effects.
4. Provider identity is holder-bound; Provider and team Target domain are separate concepts.
5. Temporary Provider invalidation and Provider death are separate lifecycle events.

Seven Batch01-04 skill baselines are additionally frozen by `MC-STAGE14-TROOP-BATCH01-04-BASELINE-01`. Explicit extension questions remain open exactly where that contract lists them. Skill-specific storage/battery behavior and all other unfrozen trigger/target/formula questions remain outside the shared foundation freeze.

Existing states/functional/{cleave,damage_share,combo,guard} and states/control/confusion contracts remain canonical. Their imported Stage9 snapshots are historical / superseded.
V1 damage formula documents preserve candidate provenance, not an independent claim of official source recovery; later B2/B2.5 authorities retain their scoped precedence.

## 2026-10-13 Formation authority update

Research F0 PR #18 -> main `abd654a907019a16a61adefee97663b25b073dd2`; Battle F0-I-A PR #66 -> main `2238186848fee6c89a9e688174f2fe64d382c1a0`. [Battle merged-main CI](https://github.com/lxy2005051020-commits/sgs-v2-battle-system/actions/runs/38278028436) PASS (2239 pytest; Stage13-D1 + Qingzhou independent audits). F1 is ready for independent implementation, **not** already installed. F0 four-phase order is a user-approved simulator V1 choice despite contrary empirical preparation logs. Provider death removal is a user-approved behavior; client proof remains OPEN.

## Stage14 F1 authority update — 2026-10-13 (supersedes F0 handoff status above)

Battle [F1 PR #68](https://github.com/lxy2005051020-commits/sgs-v2-battle-system/pull/68) merged at `975b44e67f7d1bfbb6a46fd12be6895e3c8a7cb4`; [F1 merged-main CI #38280765590](https://github.com/lxy2005051020-commits/sgs-v2-battle-system/actions/runs/38280765590) **SUCCESS** (2267/2267 tests; demo, Stage13-D1 and Qingzhou audits PASS). The Lv10 Feng Shi Zhen `20066` Runtime is **implemented on main**, not merely ready for implementation. Authoritative research remains the [F1 contract](Stage14_Formation_Skill_Research/01_Skills/FENG_SHI_ZHEN_RESEARCH_CONTRACT.md); [Battle implementation and independent CI record](https://github.com/lxy2005051020-commits/sgs-v2-battle-system/blob/main/stages/stage14/FENG_SHI_ZHEN_INTEGRATION.md). Lv1–9 and official client timing/provider-death evidence stay open. The four prebattle scheduling/death/exclusivity/speed priorities are user-approved **simulator V1 choices**, not historical-client factual findings.

## 2026-10-14 Nine-formation cross-repo canonical identity audit

**Authoritative follow-up**: [FORMATION_CROSS_REPO_ID_AUDIT_2026-10-14](Stage14_Formation_Skill_Research/00_Governance/FORMATION_CROSS_REPO_ID_AUDIT_2026-10-14.md). Current Battle main (audit baseline `2105a6a10f8d570ef40550cbe94b487142f4f5e6`) contains nine formation registrations, including the newly completed Yu Lin base-rate reactions and Yan Xing non-scaling transfers. **Eight of nine Runtime IDs differ from the historical Research FORMATION_CATALOG_V1 IDs**, which remains an explicitly versioned historical source, not a proven universal alias map. Client ID namespace reconciliation remains `OPEN`. User-approved, non-client-frozen Gameplay and deferred attribute scaling remain source-scoped; full client Gameplay freeze cannot be inferred from engineering CI.
