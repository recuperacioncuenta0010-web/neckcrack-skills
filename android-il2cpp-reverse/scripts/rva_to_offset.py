#!/usr/bin/env python3
import argparse, struct
PT_LOAD=1
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--elf',required=True); ap.add_argument('--rva',required=True); a=ap.parse_args()
 rva=int(a.rva,0)
 data=open(a.elf,'rb').read(64)
 if data[:4]!=b'\x7fELF': raise SystemExit('not ELF')
 if data[4]!=2: raise SystemExit('only ELF64 supported')
 if data[5]!=1: raise SystemExit('only little-endian supported')
 e_phoff=struct.unpack_from('<Q',data,0x20)[0]; e_phentsize=struct.unpack_from('<H',data,0x36)[0]; e_phnum=struct.unpack_from('<H',data,0x38)[0]
 with open(a.elf,'rb') as f:
  f.seek(e_phoff)
  for _ in range(e_phnum):
   ph=f.read(e_phentsize)
   if len(ph)<e_phentsize: break
   if struct.unpack_from('<I',ph,0)[0]!=PT_LOAD: continue
   p_offset,p_vaddr,p_paddr,p_filesz,p_memsz=struct.unpack_from('<QQQQQ',ph,8)
   if p_vaddr<=rva<p_vaddr+p_filesz:
    off=p_offset+(rva-p_vaddr); print(f'rva=0x{rva:x} file_offset=0x{off:x} segment=0x{p_vaddr:x}-0x{p_vaddr+p_filesz:x}'); return
 print(f'rva=0x{rva:x} mapping not found')
if __name__=='__main__': main()
