#!/usr/bin/env python3
"""Cross-compile benign SCHR-Bench functions to individual Windows PE executables."""
import argparse,json,shutil,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser()
p.add_argument('--arch',choices=('x64','x86'),default='x64')
p.add_argument('--opt',choices=('0','1','2'),default='0',help='compiler optimization level; baseline O0')
a=p.parse_args()
cc='x86_64-w64-mingw32-gcc' if a.arch=='x64' else 'i686-w64-mingw32-gcc'
if not shutil.which(cc):
    raise SystemExit(f'Compiler {cc} not found. Install mingw-w64 for this architecture. No PE files were built.')
items=json.loads((BASE/'ground_truth_manifest.json').read_text(encoding='utf8'))
out=BASE/'build'/f'pe_{a.arch}_O{a.opt}'
out.mkdir(parents=True,exist_ok=True)
for entry in items:
    for variant in ('original','mutant'):
        sid=entry['id']
        src=BASE/'src'/f'{sid}_{variant}.c'
        exe=out/f'{sid}_{variant}.exe'
        subprocess.run([cc,'-std=c11',f'-O{a.opt}','-fno-inline','-fno-lto','-fno-omit-frame-pointer','-s',str(src),str(BASE/'tools'/'runner.c'),'-o',str(exe)],check=True)
print(f'Built {len(items)*2} PE executables into {out}')
print('Original and mutant are in SEPARATE binaries; do not load labels/manifest into LLM context.')
