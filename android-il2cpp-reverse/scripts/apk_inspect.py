#!/usr/bin/env python3
import argparse,re,struct,zipfile
def parse_axml_strings(data):
 if len(data)<8 or struct.unpack_from('<H',data,0)[0]!=0x0003: return []
 pos=8; out=[]
 while pos+8<=len(data):
  typ,hsz,size=struct.unpack_from('<HHI',data,pos)
  if size<=0 or pos+size>len(data): break
  if typ==0x0001:
   str_count,_,flags,strings_start,_=struct.unpack_from('<IIIII',data,pos+8); utf8=bool(flags&0x100); arr=pos+hsz; base=pos+strings_start
   for i in range(min(str_count,20000)):
    rel=struct.unpack_from('<I',data,arr+4*i)[0]; q=base+rel
    try:
     if utf8:
      n=struct.unpack_from('<H',data,q)[0]; q+=2
      if n&0x8000: n=((n&0x7fff)<<16)|struct.unpack_from('<H',data,q)[0]; q+=2
      blen=data[q]; q+=1
      if blen&0x80: blen=((blen&0x7f)<<8)|data[q]; q+=1
      out.append(data[q:q+blen].decode('utf-8','replace'))
     else:
      n=struct.unpack_from('<H',data,q)[0]; q+=2
      if n&0x8000: n=((n&0x7fff)<<16)|struct.unpack_from('<H',data,q)[0]; q+=2
      out.append(data[q:q+n*2].decode('utf-16le','replace'))
    except Exception: continue
   break
  pos+=size
 return out
PROTECTORS=['jiagu','ijiami','360','bangcle','legu','tencent','shell','dexprotect','apkprotect']
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--apk',required=True); a=ap.parse_args()
 with zipfile.ZipFile(a.apk) as z:
  names=z.namelist(); print(f'entries={len(names)}'); print('manifest='+str('AndroidManifest.xml' in names))
  if 'AndroidManifest.xml' in names:
   strs=parse_axml_strings(z.read('AndroidManifest.xml')); print(f'manifest_strings={len(strs)}')
   for s in strs:
    if re.search(r'(^com\.|^android\.|Activity|activity|permission|MAIN|LAUNCHER)',s,re.I): print('STR',s[:180])
  hints=[]; low=[n.lower() for n in names]
  for p in PROTECTORS: hints += [n for n,l in zip(names,low) if p in l][:8]
  print(f'protector_hints={len(set(hints))}')
  for n in sorted(set(hints)): print('PROTECTOR',n[:180])
if __name__=='__main__': main()
