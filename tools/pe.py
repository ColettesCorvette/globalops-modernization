import struct, sys
def info(p):
    d=open(p,'rb').read()
    e=struct.unpack_from('<I',d,0x3c)[0]
    machine,nsec=struct.unpack_from('<HH',d,e+4)
    opt=e+24
    magic=struct.unpack_from('<H',d,opt)[0]
    chars=struct.unpack_from('<H',d,e+22)[0]
    dllchar=struct.unpack_from('<H',d,opt+70)[0]
    sizeopt=struct.unpack_from('<H',d,e+20)[0]
    secs=[]
    off=opt+sizeopt
    for i in range(nsec):
        name=d[off:off+8].rstrip(b'\0').decode('latin1')
        vsz,va,rsz,ro=struct.unpack_from('<IIII',d,off+8)
        secs.append((name,vsz,rsz))
        off+=40
    print(f"{p}")
    print(f"  machine=0x{machine:x} magic=0x{magic:x} chars=0x{chars:04x} LARGE_ADDRESS_AWARE={'OUI' if chars&0x20 else 'non'}")
    print(f"  dllcharacteristics=0x{dllchar:04x} (DEP={'oui' if dllchar&0x100 else 'non'}, ASLR={'oui' if dllchar&0x40 else 'non'})")
    print("  sections: " + ", ".join(f"{n}({rsz})" for n,v,rsz in secs))
for p in sys.argv[1:]:
    try: info(p)
    except Exception as ex: print(p,"ERR",ex)
