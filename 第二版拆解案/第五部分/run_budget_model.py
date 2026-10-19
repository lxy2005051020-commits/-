from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import csv,json
ROOT=Path(__file__).resolve().parent
def out(name,rows):
    with (ROOT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def exact(x):return F(str(x))
def packets(c):
    hw=[exact(x) for x in c['hero_weights']];total=sum(hw);q=exact(c['early_share'])
    assert len(hw)==3 and all(h>=0 for h in hw) and total>0 and 0<=q<=1
    assert exact(c['physical'])>=0 and exact(c['strategy'])>=0 and exact(c['fujia_extra'])>=0
    result=[]
    for rnd in range(1,9):
        time=(q if rnd<=4 else 1-q)/4
        for i,h in enumerate(hw):
            for typ,key in [('physical','physical'),('strategy','strategy')]:result.append((rnd,i,typ,exact(c[key])*time*h/total))
    return result
def evaluate(c,pair,r,u):
    assert len(set(pair))==2 and set(pair)<=set(range(3)) and 0<=r<=1 and 0<=u<=1
    ps=packets(c);p=sum(v for _,_,t,v in ps if t=='physical');m=sum(v for _,_,t,v in ps if t=='strategy');covered=sum(v for rnd,h,t,v in ps if rnd<=4 and h in pair)
    old=sum(v*(1-r if t=='physical' else 1) for rnd,h,t,v in ps)+exact(c['fujia_extra'])
    new=sum(v*(1-u if rnd<=4 and h in pair else 1) for rnd,h,t,v in ps)
    delta=new-old;threshold=r*p-u*covered
    assert old==(1-r)*p+m+exact(c['fujia_extra'])
    assert new==p+m-u*covered
    assert delta==threshold-exact(c['fujia_extra'])
    return dict(physical=p,strategy=m,covered=covered,original=old,candidate=new,delta=delta,threshold=threshold)
if __name__=='__main__':
    cfg=json.loads((ROOT/'inputs/预算模型输入.json').read_text(encoding='utf-8'));r=exact(cfg['teng_reduction']);u=exact(cfg['yudi_reduction']);rows=[];events=[];summary=[]
    for c in cfg['cases']:
        vals=[]
        for pair in combinations(range(3),2):
            v=evaluate(c,pair,r,u);vals.append(v)
            row=dict(case=c['id'],场景=c['name'],御敌保护对象='、'.join(cfg['heroes'][i] for i in pair),物理预算=float(v['physical']),谋略预算=float(v['strategy']),前四回合覆盖预算=float(v['covered']),藤甲额外预算=c['fujia_extra'],原配置损失预算=float(v['original']),候选损失预算=float(v['candidate']),候选减原配置=float(v['delta']),火额外交叉点=float(v['threshold']),差值精确分数=str(v['delta']),判定='候选更低' if v['delta']<0 else '原配置更低' if v['delta']>0 else '相同')
            rows.append(row)
            for rnd,h,t,a in packets(c):
                events.append(dict(case=c['id'],保护对象=row['御敌保护对象'],round=rnd,hero=cfg['heroes'][h],damage_type=t,input=float(a),original_after=float(a*(1-r if t=='physical' else 1)),candidate_after=float(a*(1-u if rnd<=4 and h in pair else 1)),note='M1人工输入预算；不含原配置额外F，不是真实战报重放'))
        summary.append(dict(case=c['id'],场景=c['name'],原配置损失预算=float(vals[0]['original']),候选最小损失预算=float(min(v['candidate'] for v in vals)),候选最大损失预算=float(max(v['candidate'] for v in vals)),候选减原配置最小=float(min(v['delta'] for v in vals)),候选减原配置最大=float(max(v['delta'] for v in vals))))
    out('受控预算_目标组合结果.csv',rows);out('受控预算_输入与分段结算.csv',events);out('受控预算_场景汇总.csv',summary)
    frontier=[]
    for q in [0.2,0.5,0.8,1.0]:
        for i in range(101):
            p=F(i,100);threshold=r*p-u*exact(q)*F(2,3)
            frontier.append(dict(physical_share=float(p),early_share=q,uniform_covered_share=float(exact(q)*F(2,3)),fujia_extra_threshold_per_1000=float(threshold*1000),note='均匀受伤，三种保护对象等价；负阈值表示F=0已偏向候选'))
    out('受控预算_交叉点曲线.csv',frontier)
    (ROOT/'qa/预算执行.json').write_text(json.dumps(dict(model='M1',cases=len(cfg['cases']),pair_combinations=len(rows),fraction_arithmetic=True,packet_rows=len(events),frontier_rows=len(frontier),scope=cfg['assumptions']),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))
