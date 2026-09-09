import struct,sys
def rva2off(secs,rva):
    for va,vsz,ro,rsz in secs:
        if va<=rva<va+max(vsz,rsz): return ro+(rva-va)
    return None
def imports(p):
    d=open(p,'rb').read(); e=struct.unpack_from('<I',d,0x3c)[0]
    nsec=struct.unpack_from('<H',d,e+6)[0]; sizeopt=struct.unpack_from('<H',d,e+20)[0]
    opt=e+24; off=opt+sizeopt; secs=[]
    for i in range(nsec):
        vsz,va,rsz,ro=struct.unpack_from('<IIII',d,off+8); secs.append((va,vsz,ro,rsz)); off+=40
    idir=struct.unpack_from('<I',d,opt+104)[0]
    o=rva2off(secs,idir); res=[]
    while True:
        oft,ts,fc,namerva,fthunk=struct.unpack_from('<IIIII',d,o)
        if namerva==0: break
        no=rva2off(secs,namerva); res.append(d[no:d.index(b'\0',no)].decode('latin1'))
        o+=20
    return res
for p in sys.argv[1:]:
    print(p.split('/')[-1]+":", ", ".join(sorted(imports(p),key=str.lower)))
