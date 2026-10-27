#!/usr/bin/env python3
"""Build 80 benign standalone variants and assert hand-specified ground truth."""
from pathlib import Path
import json,os,shutil,subprocess,sys
BASE=Path(__file__).resolve().parents[1]
COMPILER=os.environ.get('CC','gcc')
if not shutil.which(COMPILER):
    raise SystemExit(f'Compiler not found: {COMPILER}. Install GCC/MinGW or set CC.')
OUT=BASE/'build'/'native'
OUT.mkdir(parents=True,exist_ok=True)
data=json.loads((BASE/'ground_truth_manifest.json').read_text(encoding='utf8'))
num=0; fails=[]
for item in data:
    sid=item['id']
    for variant in ('original','mutant'):
        exe=OUT/f'{sid}_{variant}'
        cmd=[COMPILER,'-std=c11','-O0','-fno-inline','-fno-lto','-fno-omit-frame-pointer','-Wall','-Wextra',str(BASE/'src'/f'{sid}_{variant}.c'),str(BASE/'tools'/'runner.c'),'-o',str(exe)]
        p=subprocess.run(cmd,text=True,capture_output=True)
        if p.returncode: raise SystemExit(f'BUILD FAILED {sid} {variant}\n{p.stdout}\n{p.stderr}')
        for test in item['tests']:
            args=[str(test[x]) for x in ('a','b','c')]
            p=subprocess.run([str(exe),*args],capture_output=True,text=True,timeout=3)
            got=p.stdout.strip()
            want=str(test[variant])
            num+=1
            if p.returncode!=0 or got!=want:
                fails.append(f'{sid}/{variant} {args}: expected {want}, got {got}; rc={p.returncode}')
print(f'Functions: {len(data)} | Variant builds: {len(data)*2} | Test assertions: {num}')
print('Discriminating mutations:',sum(any(t['original']!=t['mutant'] for t in s['tests']) for s in data))
if fails:
    print('FAILED:',*fails,sep='\n  ')
    sys.exit(1)
print('PASS: all hand-authored ground-truth assertions matched.')
