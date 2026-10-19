"""M2: deterministic cleanse timing gates; no battle or probability simulation."""
from pathlib import Path
from itertools import product
import csv,json
ROOT=Path(__file__).resolve().parent

def simulate(initial,man_available,man_target,cao_available,cao_target,late,extra):
    # Only one dispellable, non-expiring abstract debuff on Xiahou.
    # initial=0: inherited at t=0; initial=1: newly applied at t=20.
    active=initial==0
    events=[]
    def record(t,action):
        events.append(dict(time=t,action=action,debuff_active=active))
    record(0,'inherited' if active else 'no_inherited')
    if extra and man_available and man_target:
        active=False;record(10,'man_cleanse')
    record(19,'before_enemy_action')
    if initial==1:
        active=True;record(20,'enemy_new_debuff')
    record(29,'before_cao_action')
    if cao_available and cao_target:
        active=False;record(30,'cao_cleanse')
    if late:
        active=True;record(35,'enemy_reapplies')
    record(39,'before_xiahou_action')
    return events

def run():
    rows=[];ledger=[]
    for idx,bits in enumerate(product([0,1],repeat=6),1):
        keys=['new_after_man','man_available','man_selects_xiahou','cao_available','cao_covers_xiahou','late_reapply']
        inputs=dict(zip(keys,bits));record=dict(branch=idx,**inputs)
        for variant,extra in [('A',False),('C',True)]:
            events=simulate(*bits,extra)
            for t,label in [(19,'before_enemy'),(29,'before_cao'),(39,'before_xiahou')]:
                record[f'{variant}_{label}_blocked']=int(next(e['debuff_active'] for e in events if e['time']==t))
            ledger.extend(dict(branch=idx,variant=variant,**e) for e in events)
        rows.append(record)
    for name,rr in [('净化时序_64组配对结果.csv',rows),('净化时序_逐节点账本.csv',ledger)]:
        with (ROOT/'data'/name).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
    metadata=dict(model='M2',paired_inputs=64,variants=['A','C'],probability_weights=None,
        time_order={'0':'inherited state','10':'Man cleanse opportunity','19':'before enemy action','20':'enemy new debuff','29':'before Cao action','30':'Cao cleanse opportunity','35':'optional enemy reapplication','39':'before Xiahou action'},
        assumptions=['single dispellable debuff, no expiry in window','opportunities and targets are exogenous gates','all 64 binary combinations enumerated without weights','no troops, healing, counterattacks or source restoration simulation','availability incorporates action eligibility, actual activation and cooldown as appropriate','same input sequence for A and C; adding a gate does not model removing Feigong healing'],
        excluded=['probability estimates','current-game implementation claim','win rate','net troop loss','full battle results'])
    (ROOT/'inputs/净化时序假设.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    print('M2: 64 paired inputs; node ledger:',len(ledger))

if __name__=='__main__':run()
