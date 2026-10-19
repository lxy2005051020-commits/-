# 第五部分：三类环境配置尝试

正文：`第五部分_三类环境配置尝试.md`，可阅读 PDF、HTML。

本版保留旧交付，新增三套九槽配置、控制类型区分、满宠先攻净化的时序分支，以及三配置×三压力的实战验收表。没有执行完整战斗模拟或新增真实试配战报；不提供候选胜率。

- A：原藤甲＋非攻；B：曹操藤甲换御敌；C：满宠非攻换刮骨。
- M1：防护预算，5种人工输入×3组保护对象。数值不是实际兵力。
- M2：净化时序，6项二元前提的64组配对，不赋予概率。可用性与目标均为外生门禁，不模拟发动随机、治疗或反击。
- sources保留前版冻结材料；inputs/本轮来源校验.json冻结本版来源。旧来源清单中的旧绝对路径仅用于追踪出处。
- 与第四部分的衔接说明.md保留前文口径纠正，未覆盖用户修改的前四部分。

重建（在本目录使用已安装依赖的 Python）：

```powershell
python run_budget_model.py
python run_control_windows.py
python audit_report_anchors.py
python build_document.py
python verify_delivery.py
```

prepare_revision.py是一次性初始化记录，渲染脚本已经完成适配，**无需再次运行初始化**。requirements.txt列出原版绘制依赖。本机未找到pdftoppm，本版沿用PyMuPDF渲染，qa包含七页PNG与视觉复核记录。package_delivery.py核对ZIP CRC和内容哈希；校验报告有明确的验证范围。
