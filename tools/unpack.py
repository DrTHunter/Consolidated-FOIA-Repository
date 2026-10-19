import pymupdf, os, sys, json, re
d = pymupdf.open(os.path.expanduser('~/OneDrive/Desktop/20394 (1) (2).pdf'))
out = sys.argv[1]
meta = []
for x in range(1, d.xref_length()):
    if d.xref_get_key(x,'Type')[1] != '/FileSpec': continue
    obj = d.xref_object(x)
    name = d.xref_get_key(x,'UF')[1] or d.xref_get_key(x,'F')[1]
    ef = d.xref_get_key(x,'EF/F')[1]
    efx = int(ef.split()[0])
    ci = d.xref_get_key(x,'CI')
    cimeta = {}
    if ci[0]=='xref':
        cx=int(ci[1].split()[0]); cimeta = d.xref_object(cx)
    elif ci[0]=='dict': cimeta = ci[1]
    data = d.xref_stream(efx)
    idx = len(meta)
    fn = f"{idx:04d}.pdf"
    open(os.path.join(out, fn),'wb').write(data)
    meta.append(dict(i=idx, file=fn, name=name, size=len(data), ci=str(cimeta)))
json.dump(meta, open(os.path.join(out,'..','meta.json'),'w'), indent=0)
print(len(meta)); print(meta[0]); print(meta[500])
