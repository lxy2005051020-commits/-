from pathlib import Path
import csv, json, hashlib, re, xml.etree.ElementTree as ET
import markdown
ROOT=Path(__file__).resolve().parent
md=(ROOT/"第一部分_规则基底.md").read_text(encoding="utf-8")
macro='<div class="flow"><span>战前配置</span><b>→</b><span>战斗结算</span><b>→</b><span>战后状态</span><b>→</b><span>恢复与补充</span><b>→</b><span>再次出征</span></div>'
md=re.sub(r'```mermaid\n.*?\n```', lambda m:macro, md, flags=re.S)
body=markdown.markdown(md,extensions=["tables","fenced_code","toc"])
def embed(m):
    src=m.group(1)
    return '<figure>'+ (ROOT/src).read_text(encoding="utf-8")+'</figure>'
body=re.sub(r'<img[^>]*src="(figures/[^"]+\.svg)"[^>]*/?>', embed, body)
css="""body{margin:0;background:#edf1f6;color:#203047;font:16px/1.85 "Microsoft YaHei","Segoe UI",sans-serif}main{max-width:1060px;margin:30px auto;padding:40px 56px;background:white;border-radius:14px;box-shadow:0 8px 35px #24395410}h1{font-size:29px;line-height:1.5;color:#152c4a}h2{font-size:23px;margin-top:42px;border-left:5px solid #2b6f75;padding-left:14px}h3{font-size:19px;color:#235a65;margin-top:26px}a{color:#17697e;text-decoration:none;overflow-wrap:anywhere}blockquote{margin:20px 0;padding:10px 20px;background:#f0f5fa;border-left:3px solid #9fb5c8}table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.7;margin:20px 0}th{background:#e9f1f7;color:#233e59}td,th{padding:11px 10px;border:1px solid #dce4ed;vertical-align:top}tr:nth-child(even){background:#fafbfd}code{font-family:Consolas,monospace;font-size:.9em;overflow-wrap:anywhere}pre{padding:17px;background:#f3f6f9;overflow-x:auto;white-space:pre-wrap}figure{margin:24px 0}svg{width:100%;height:auto;display:block}.flow{display:flex;align-items:center;gap:9px;justify-content:center;flex-wrap:wrap;background:#f3f7fa;padding:20px}.flow span{background:#e5f0ed;border:1px solid #bfdbd4;padding:7px 12px;border-radius:6px}em{color:#5d6d80;font-size:14px}strong{color:#163e58}.topline{color:#5d6d80;font-size:13px}@media(max-width:800px){main{margin:0;padding:22px 18px;border-radius:0}table{font-size:12px}td,th{padding:7px}}@media print{body{background:white}main{box-shadow:none;margin:0;padding:0}h2,h3{break-after:avoid}figure,tr,pre{break-inside:avoid}a{color:inherit}}"""
html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第一部分：规则基底</title><style>'+css+'</style></head><body><main><div class="topline">三国志·战略版战斗数值拆解 · 第一部分 · 2026-10-18</div>'+body+'</main></body></html>'
(ROOT/"第一部分_规则基底.html").write_text(html,encoding="utf-8")
def readcsv(path):
    with (ROOT/path).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
# Numerical ledger: source assumptions are explicit; validate arithmetic only.
rows=readcsv("data/教学算例_伤兵账本.csv")
t,w=10000,0
for row in rows:
    step=int(row["step"])
    if step==4:
        w=w*9//10
    else:
        loss=int(row["actual_loss"]);t-=loss
        w=min(10000-t,w+loss*9//10)
        actual=min(int(row["nominal_heal"]),w,10000-t)
        assert actual==int(row["actual_heal"])
        t+=actual;w-=actual
    assert (t,w,10000-t-w)==(int(row["t"]),int(row["w"]),int(row["unrecoverable_gap"]))
assert t==9755 and w==0
assert 950-855==95
real=readcsv("data/实战转录_多段急救.csv")
t=int(real[0]["t_after"])
for row in real[1:]:
    t+=int(row["delta_t"]);assert t==int(row["t_after"])
assert t==3893 and 4368-t==475
selected=readcsv("data/研究重放表_选定两行.csv")
assert len(selected)==2
assert [int(r["actual_recovery"]) for r in selected]==[465,0]
assert [int(r["wounded_pool_before"]) for r in selected]==[465,0]
assert int(selected[1]["missing_troops_before"])==53
for row in selected:
    assert int(row["post_troops"])-int(row["pre_troops"])==int(row["actual_recovery"])
manifest=json.loads((ROOT/"source_manifest.json").read_text(encoding="utf-8"))
source_checks=[]
for item in manifest["sources"]:
    data=(ROOT/item["local"]).read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    source_checks.append({"id":item["id"],"file":item["local"],"git_blob_sha_matches":blob==item["blob_sha"],"expected":item["blob_sha"],"actual":blob})
assert all(s["git_blob_sha_matches"] for s in source_checks),source_checks
source_rows=readcsv("sources/D01_STAGE13_B1_ROUND4_REPLAY_VALIDATION.csv")
assert len(source_rows)==4542,len(source_rows)
for chosen in selected:
    matches=[r for r in source_rows if all(r[k]==chosen[k] for k in ["battle_id","source_file","round","event_key","unit_name"])]
    assert len(matches)==1 and matches[0]==chosen
figs=list((ROOT/"figures").glob("*.svg"))
assert len(figs)==2
for path in figs:ET.parse(path)
assert html.count("<svg ")==2 and '<img ' not in html
assert len(re.findall(r"^## 1\.[1-4] ",(ROOT/"第一部分_规则基底.md").read_text(encoding="utf-8"),re.M))==4
assert "TODO" not in md and "待补" not in md
report={"status":"PASS","checked_date":"2026-10-18","source_snapshots":len(source_checks),"git_blob_sha_all_match":True,"full_research_replay_rows":len(source_rows),"selected_replay_rows_exact_match":2,"constructed_ledger_steps":len(rows),"transcribed_case_net_loss":475,"constructed_final_troops":9755,"constructed_timing_difference":95,"svg_xml_valid":2,"html_svg_embedded":2,"raw_report_rescan_performed":False,"repository_test_suite_run":False,"visual_browser_check":"not_run_by_this_script","sources":source_checks}
(ROOT/"交付检查.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="sources"},ensure_ascii=False))
