# 690082 EVASION / 规避 Mechanism Contract

State ID: `690082`  
Official Name: `规避`  
English Name: `EVASION`  
Category: `FUNCTIONAL_STATE`  
Status: `FROZEN`  
Freeze Date: `2026-09-17`  
Evidence Maturity: `HIGH_CONFIDENCE`  

本合同冻结的是官方战报能够稳定确认的外部行为；不宣称复原官方源码内部函数、对象、计数器或PRNG实现。

---

## 1. Identity & Classification

* **State ID**: `690082`
* **Official Name**: `规避`
* **English Name**: `EVASION`
* **Official Category**: `FUNCTIONAL_STATE`
* **Engineering Taxonomy (Optional)**: `DEFENSIVE_EVASION`（*注：ENGINEERING TAXONOMY，仅作工程分类，非官方战报分类*）
* **Dispel / Cleanse Eligibility**: `NOT ESTABLISHED BY CURRENT 690082 RESEARCH`（*当前规避专项研究未建立驱散/净化协议规则，不预设未实证规则*）

---

## 2. Core Effect

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **可观察协议规则**：
  * 当受击目标持有生效中的规避状态面对具有规避资格的伤害实例时，进行规避裁决；
  * **规避成功**：战报输出 `cfg 135`（`[目标]处于规避状态，本次伤害无效`），该次伤害实例造成的伤害值与对应兵损结算严格为 **0**；
  * **规避失败**：战报输出 `cfg 134`（`[目标]规避失败`），该伤害实例继续向下执行后续结算；
  * *边界约束*：本条只管辖单次伤害实例无效化；禁止引申为“不触发所有受伤派生”或“不扣减其他状态”（抵御保留规则单独由第 7 节管辖）。

---

## 3. Eligible Damage Classes

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **已确证具备规避资格的伤害分类与实证范围**：
  1. **普通攻击**：普通攻击直接兵刃伤害；
  2. **战法直接伤害**：在官方战报中已实际观察到的主动战法、突击战法、被动战法、指挥战法造成的直接物理或谋略伤害实例；
  3. **持续性伤害（DOT Tick）**：溃逃、中毒、灼烧、水攻、沙暴、叛逃六大类状态按回合结算的独立 Tick；
  4. **普通攻击派生「群攻」副目标伤害**：普通攻击触发群攻后，对副目标造成的溅射伤害（*严格限定为普通攻击派生的群攻*）；
  5. **官方日志明确标记为「反击」的伤害**：仅限定于专项研究中实际观察并确认的来源：
     * 【后发制人】
     * 【气凌三军】
     * 【青州兵】
     * 【三里而还】
     * 【还击】
     * （*禁止将缺乏有效重叠样本的【梦中弑臣】或未纳入本专项研究的【千里驰援】列为已证实来源*）。

---

## 4. Non-Evasion Boundaries

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **确证不进入规避的伤害实例（范围严格受限于已实证来源）**：
  1. **【连环计】「铁索连环」反馈传导伤害**：
     * 铁索连环传递给连接目标的反馈伤害，战报中未观察到 `cfg 134/135` 判定，直接结算兵损；
     * *严格限定*：仅指【连环计】「铁索连环」机制，禁止无证据推广至所有抽象反馈机制。
  2. **标准分担 / 代承伤害（Share Target）**：
     * 承担者为原目标分担/代承伤害时，承担者身上不出现 `cfg 134/135` 规避判定，直接扣减对应分担兵损；
     * *强证据来源*：【严阵以待】、【校胜帷幄】；
     * *一致性支持来源*：【闭月】、【庐江上甲】、【护卫】；
     * *严格限定*：仅限上述实证分担来源的承担端，禁止加入未经检验的来源。

---

## 5. Adjudication Granularity

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **裁决粒度可观察行为**：
  * **多受击目标**：群体伤害作用于多个目标时，每个持有规避的目标按目标分别独立输出裁决；
  * **同目标多个 Damage Instance**：同一次行动内对同一目标的多次伤害结算（如多段战法 Hit、普攻随后追加装备特技【踩踏】伤害），按伤害实例分别独立输出裁决；
  * **持续性状态（DOT）**：同一 DOT 状态在不同回合产生的独立 Tick，按独立 Tick 分别独立输出裁决；
  * *表述约束*：禁止使用“底层 RNG 独立”等不可观察实现词汇，仅记录事件流独立性。

---

## 6. Sure-Hit Interaction

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **「必中」交互规则**：
  * 当伤害来源方具有明确生效的「必中」状态，且受击目标持有明确生效的「规避」状态时：
    * 战报中**未观察到 `cfg 134`（规避失败）或 `cfg 135`（规避成功）**；
    * 伤害实例直接进入伤害结算；
  * *表述约束*：禁止在官方协议层表述为“服务端 skip_evasion_check()”。

---

## 7. Barrier Ordering

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **「规避」与「抵御」共存时的可观察判定顺序与事件链**：
  1. **规避失败链路**：
     $$\text{cfg 134 (规避失败)} \longrightarrow \text{cfg 96 (执行抵御)} \longrightarrow \text{伤害结果为 0} \longrightarrow \{\text{cfg 757 抵御次数下降} \lor \text{cfg 22 抵御消失}\}$$
  2. **规避成功链路**：
     $$\text{cfg 135 (规避成功，本次伤害无效)} \longrightarrow \text{伤害结果为 0}$$
     后续受击闭环实证：目标当前持有的抵御层数未被消费，在后续受击中依然完整保留并正常抵御。

---

## 8. Lifecycle

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **生命周期推进、生效与注销锚点**：
  1. **Mid-Round 施加即时生效**：在回合中途施加规避后，同回合内在持有者下一次行动之前受到可规避伤害，规避状态立即实际生效并参与裁决；
  2. **推进单位与自然失效（Natural Removal Hook）**：规避状态的持续周期严格与**持有者自身行动周期（Holder Action Cycle）**对齐，自然移除事件在决定性样本中稳定锚定于**持有者自身行动开始（Holder Action Start）**时刻；
  3. **到期回合临界受击窗口**：在到期回合中，持有者自身行动开始前受到可规避伤害，规避依然具有裁决资格；行动开始后注销，随后的受击不再拥有该规避；
  4. **Post-Owner-Action 施加顺延**：在持有者本回合行动结束后施加的规避，已经完成的当前行动不消耗新状态的持续周期，其有效性顺延至后续行动周期；
  5. **SOURCE-DEPENDENT EARLY REMOVAL（来源依赖型提前移除）**：
     * 特定来源依赖型规避，已观察到在来源方死亡后提前移除；
     * *当前强确证来源*：【金丹秘术】（左慈阵亡后规避提前被注销）；
     * *范围限定*：仅限已证实来源，禁止推广为所有 690082 规避的通用行为；
  6. *表述约束*：禁止在合同中定义内部 counter 或递减变量。

---

## 9. Different-Source Coexistence

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **概念定位**：`SOURCE-SCOPED INDEPENDENT CONTRIBUTION / LIFECYCLE SEMANTICS`（来源级独立贡献与生命周期语义）
* **规则事实**：
  * 来自不同战法来源的规避效果可同时作用于同一武将并各自提供规避贡献；
  * 某一来源到期失效时，仅移除该来源自身的贡献，其他来源贡献继续保留并正常生效（继续触发 `cfg 134/135`）；其余来源在后续到达各自的到期锚点时再独立移除；
  * **可观察日志协议**：
    * 某来源贡献移除时：触发 `cfg 22`（对应规避效果消失）；
    * 若其他规避贡献仍存在：常见触发 `cfg 302`（总规避率下降后仍非零）；
    * 若最后贡献归零：常见触发 `cfg 139`（总规避率降至 0）；
  * *禁止事项*：禁止宣称官方底层必然创建了多个“独立 Modifier Object”或“内部状态对象”。

---

## 10. Same-Source Reapplication

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **战法级分化实证表现（Source-Specific Observed Behavior）**：
  1. **【兴云布雨】（同源追加独立贡献）**：
     * 同源重复触发时，可在原贡献存续期间增加新的规避贡献（总规避率按非线性规则进一步提高）；
     * 旧贡献保持原到期边界，新贡献拥有后续独立的移除边界，战报中可观察到两阶段分别输出移除日志（`cfg 302/139/22`）；
  2. **兵书【灵巧】（同源数值不刷新/持续时间延续）**：
     * 重入触发时输出 `cfg 25`（状态已存在），总规避率不增加；
     * 状态跨过原自然到期边界后继续有效，表现为 **Value-Unchanged Refresh / Continuation**；
     * *边界声明*：【灵巧】最后一次刷新后的精确终末 Expiry 公式未由完整自然终结样本直接观察闭环，但不阻塞当前可观察行为的实现；
  3. *表述约束*：禁止断言“由官方底层配置字段决定”，仅记录已观察到的战法级行为。

---

## 11. Probability Composition

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **规则命名**：`COMPLEMENT-PRODUCT COMPOSITION FORMULA`（互补乘积组合公式）
* **数值组合关系**：
  $$P_{\text{total}} = 1 - \prod_{i=1}^{n} (1 - P_i)$$
* **精度与边界声明**：
  * 官方战报 UI 日志中所有规避率均显示为两位百分比小数；
  * 底层内部计算时的中间浮点/定点精度以及具体舍入步骤属于 `UNOBSERVABLE`；
  * *禁止事项*：禁止将“Round Half-Up”或“每一步步进舍入两位”写为官方事实。

---

## 12. RNG Observability Boundary

* **Authority Level**: `OFFICIAL / EMPIRICALLY SUPPORTED FACT`
* **裁决暴露事实**：
  * 对实际进入规避裁决的 Damage Instance，官方战报对外**必然且仅暴露一个最终裁决日志（`cfg 134` 或 `cfg 135`）**；
  * 未观察到逐来源分别输出 `cfg 134/135`；
  * `cfg 134` 与 `cfg 135` 的日志结构仅包含武将名称，**完全不绑定战法来源**；
  * 当前战报未发现能够可靠绑定到具体规避裁决的 roll / seed / threshold 等显式字段；
  * 引擎内部到底是使用 $P_{\text{total}}$ 抽样一次（One Aggregate Roll），还是按来源隐式短路抽样（Hidden Multi-Roll），在战报协议中属于严格的 **`UNOBSERVABLE`**，禁止作为官方事实，允许作为模拟器工程兼容实现选择（Engineering Choice）。

---

## 13. Clean Evidence Matrix

| Q | 机制项 (Mechanism) | 正式判定 (Formal Verdict) | 权威级别 (Evidence Level) | 决定性经验证据链 (Decisive Evidence) | 严格实证范围 (Scope Limitation) |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **Q1** | 成功规避效果 | 伤害无效，兵损 0 | HIGH_CONFIDENCE | 战报 `cfg 135` 紧随其后的兵力结算值稳定为 `0` | 通用规避语义 |
| **Q2** | 战法直接伤害资格 | 可进入规避 | HIGH_CONFIDENCE | 主动/突击/被动/指挥直接伤害均稳定触发 `cfg 134/135` | 战报中已观察到的直接伤害 |
| **Q3** | DOT 持续伤害资格 | 逐 Tick 重新裁决 | HIGH_CONFIDENCE | 6 类 DOT 在回合开始 Tick 时稳定触发 `cfg 134/135` | 溃逃/中毒/灼烧/水攻/沙暴/叛逃 |
| **Q4** | 跨 Tick 独立裁决 | 独立判定 | HIGH_CONFIDENCE | 同一武将身上同一 DOT，相邻回合 Tick 出现失败与成功交替 | 同一 DOT 跨回合 Tick |
| **Q5** | 群体伤害多目标 | 按目标分别裁决 | HIGH_CONFIDENCE | 战法作用于 2~3 人时，战报为各目标分别输出独立 134/135 | 群体伤害多目标场景 |
| **Q6** | 同技能多段 Hit | 按实例分别裁决 | HIGH_CONFIDENCE | 多段技能（如神机妙算、暗藏玄机）每段 Hit 均有独立 134/135 | 同技能内多个 Damage Instance |
| **Q7** | 普攻派生群攻 | 具有规避资格 | HIGH_CONFIDENCE | 普攻触发群攻后，溅射副目标稳定产生独立 `cfg 134/135` | 仅限普通攻击派生群攻 |
| **Q8** | 反击伤害资格 | 具有规避资格 | HIGH_CONFIDENCE | 后发制人、气凌三军、青州兵等反击触发时稳定产生 134/135 | 仅限已实证的 5 种反击来源 |
| **Q9** | 连环计铁索反馈 | 不进入规避 | HIGH_CONFIDENCE | 【连环计】传导伤害直接触发扣血，全库无 134/135 伴随 | 仅限【连环计】「铁索连环」 |
| **Q10** | 标准分担代承 | 不进入规避 | HIGH_CONFIDENCE | 【严阵以待】、【校胜帷幄】等分担受击直接扣血，承担端无 134/135 | 仅限已实证的分担战法 |
| **Q11** | 必中交互穿透 | 穿透且无日志 | HIGH_CONFIDENCE | 必中存在时，直接结算伤害，战报中 134/135 发生数为 0 | 攻击方必中生效期 |
| **Q12** | 规避与抵御顺序 | 规避先于抵御；成功保留抵御 | HIGH_CONFIDENCE | 失败：`134 -> 96 -> 757/22`；成功：`135` 后后续受击仍可抵御 | 规避与抵御共存受击 |
| **Q13** | 生命周期推进与注销 | 即时生效；Holder 行动开始注销；源死早退 | HIGH_CONFIDENCE | 自然移除稳定锚定 Holder Action Start；金丹秘术左慈阵亡后提前移除 | 生命周期与自然到期规则 |
| **Q14** | 多来源共存与注销 | 独立贡献；阶梯式注销 | HIGH_CONFIDENCE | 某源到期触发 cfg 22/302，其他源存续期仍可成功规避，归零见 cfg 139 | 跨来源多贡献场景 |
| **Q15** | 同源重入差异 | 兴云追加新贡献；灵巧续期总值不变 | HIGH_CONFIDENCE | 兴云布雨两阶段注销闭环；灵巧触发 `cfg 25` 且跨原到期点存活 | 仅限【兴云布雨】与【灵巧】 |
| **Q16** | 概率非线性合成 | 互补乘积组合公式 | HIGH_CONFIDENCE | 多层叠加与注销战报显示数值与 $1-\prod(1-P_i)$ 达到 100% 拟合 | 规避贡献可观察数值组合 |
| **Q17** | 裁决可观察性 | 单一聚合裁决；无来源归因；无 RNG 暴露 | HIGH_CONFIDENCE | 多来源受击下多判定反例数为 0；战报中未发现显式 roll/seed 字段 | 战报协议表现层 |

---

## 14. Non-Blocking Implementation Guidance

为确保三国志战略版战斗模拟器（Runtime）实现与本合同 100% 兼容，提供以下工程实现指南（*注：本节属于 ENGINEERING INTERPRETATION，用于指导代码实现，不代表官方底层源码事实*）：

1. **概率合成与抽样**：
   * 在受击裁决管道中，推荐先遍历受击者当前生效的所有规避来源计算复合总概率：
     $$P_{\text{total}} = 1 - \prod_{i=1}^{n} (1 - P_i)$$
   * 随后执行单次随机数抽样：若 $\text{rand}() < P_{\text{total}}$，则判定规避成功并输出 `cfg 135`，将当前伤害实例的值置为 0；否则判定规避失败并输出 `cfg 134`。
   * 该单次抽样方案在数学期望与外部日志协议上与官方行为完全等价，具备最佳的工程性能与清晰度。
2. **时序管道（Execution Order）**：
   * 目标解析（援护重定向锁定 actualTarget） $\longrightarrow$
   * 规避裁决（若必中有效则直接跳过规避；若无必中则执行规避裁决） $\longrightarrow$
   * 抵御裁决（若规避成功则直接跳过抵御且不扣减抵御层数；若规避失败且目标有抵御，则消费抵御免除伤害） $\longrightarrow$
   * 伤害数值结算与分担派生。
3. **生命周期对齐**：
   * 规避状态内部应记录来源标识（Source ID）、规避率数值（Value）以及剩余有效行动周期（Action Turns）；
   * 在武将回合开始并正式执行行动（Action Start）事件时，扣减其持有的规避状态剩余行动周期，当周期耗尽时触发移除逻辑（输出 `cfg 22` 与相应 `cfg 302/139`）。
