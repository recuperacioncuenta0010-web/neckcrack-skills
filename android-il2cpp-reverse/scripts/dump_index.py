#!/usr/bin/env python3
import argparse, re
CLASS_RE=re.compile(r'^\s*(?:public|private|protected|internal)?\s*(?:sealed\s+|static\s+|abstract\s+)?(?:class|struct|interface|enum)\s+([^\s:<]+)')
NS_RE=re.compile(r'^\s*namespace\s+([^\s{]+)')
DLL_RE=re.compile(r'^\s*//\s*(?:Dll|Assembly)\s*:\s*(.+)$')
FIELD_RE=re.compile(r'^\s*(?:public|private|protected|internal)\s+.*;\s*//\s*0x([0-9a-fA-F]+)\s*$')
METHOD_RE=re.compile(r'^\s*(?:public|private|protected|internal|static|virtual|override|abstract|sealed|extern|new|partial|unsafe|readonly)\b[^;{}]*?\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*;\s*//\s*0x([0-9a-fA-F]+)')
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--dump',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
 image=''; ns=''; cur='?'; n=0
 with open(a.dump,encoding='utf-8',errors='replace') as f, open(a.out,'w',encoding='utf-8') as w:
  w.write('kind\timage\tnamespace\tclass\tname\toffset\tsignature\n')
  for line in f:
   s=line.strip()
   m=DLL_RE.match(s)
   if m: image=m.group(1).strip()
   m=NS_RE.match(s)
   if m: ns=m.group(1).strip()
   m=CLASS_RE.match(line)
   if m: cur=m.group(1)
   m=FIELD_RE.match(line)
   if m:
    decl=s.rsplit(';',1)[0].strip(); nm=re.search(r'([A-Za-z_][A-Za-z0-9_]*)\s*$',decl); name=nm.group(1) if nm else '?'
    off=int(m.group(1),16); w.write(f'field\t{image}\t{ns}\t{cur}\t{name}\t0x{off:x}\t{decl}\n'); n+=1; continue
   m=METHOD_RE.match(line)
   if m:
    name=m.group(1); off=int(m.group(2),16); sig=s.split('//',1)[0].strip()
    w.write(f'method\t{image}\t{ns}\t{cur}\t{name}\t0x{off:x}\t{sig}\n'); n+=1
 print(f'indexed={n} out={a.out}')
if __name__=='__main__': main()
