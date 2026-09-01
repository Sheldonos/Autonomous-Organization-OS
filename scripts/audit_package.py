#!/usr/bin/env python3
from __future__ import annotations
import pathlib,re,json,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
SKIP_PARTS={'source_archives','source_archive','source_505','.git'}
SECRET_PATTERNS=[re.compile(r'\bsk-[A-Za-z0-9_-]{20,}\b'),re.compile(r'\bgh[pousr]_[A-Za-z0-9]{20,}\b'),re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),re.compile(r'\bAKIA[0-9A-Z]{16}\b')]
def main():
 errors=[];warnings=[];files=0
 for p in ROOT.rglob('*'):
  if any(x in SKIP_PARTS for x in p.parts):continue
  if p.is_dir():
   if p.name=='__pycache__':errors.append(f'cache directory present: {p.relative_to(ROOT)}')
   continue
  files+=1
  if p.suffix=='.pyc':errors.append(f'pyc present: {p.relative_to(ROOT)}');continue
  if p.stat().st_size>3_000_000:continue
  try:txt=p.read_text(errors='ignore')
  except Exception:continue
  for rx in SECRET_PATTERNS:
   if rx.search(txt):errors.append(f'possible embedded secret: {p.relative_to(ROOT)} pattern={rx.pattern}')
 # Market/provenance boundaries must be explicit, not hidden.
 mr=(ROOT/'market/MARKET_READINESS.md').read_text()
 if 'license' not in mr.lower() or 'deployment' not in mr.lower(): errors.append('market readiness missing deployment/license boundaries')
 # Generated runtime core should compile.
 import py_compile
 for p in list((ROOT/'runtime').glob('*.py'))+list((ROOT/'scripts').glob('*.py'))+[ROOT/'aos.py']:
  try:py_compile.compile(str(p),doraise=True,cfile='/tmp/faos-audit.pyc')
  except Exception as e:errors.append(f'compile failed {p.relative_to(ROOT)}: {e}')
 result={'status':'PASS' if not errors else 'FAIL','files_scanned':files,'errors':errors,'warnings':warnings};print(json.dumps(result,indent=2));return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(main())
