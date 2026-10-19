import pymupdf, os, sys, json, re
S = sys.argv[1]
meta = json.load(open(os.path.join(S,'meta.json')))
def parse_ci(s):
    r={}
    for k,v in re.findall(r'/(\w)\((.*?)\)(?=/\w|>>)', s): r[k]=v
    m=re.search(r'/6 (\d+)',s); r['6']=m.group(1) if m else '0'
    return r
corpus=[]; imgonly=0
for m in meta:
    ci=parse_ci(m['ci'])
    p=os.path.join(S,'emails',m['file'])
    rec=dict(i=m['i'],file=m['file'],subject=ci.get('3',''),frm=ci.get('2',''),to=ci.get('8',''),cc=ci.get('9',''),sent=ci.get('4',''),natt=ci.get('6','0'),body='',atts=[])
    try:
        d=pymupdf.open(p)
        rec['pages']=d.page_count
        rec['body']="\n".join(pg.get_text() for pg in d)
        for j in range(d.embfile_count()):
            info=d.embfile_info(j); nm=info['filename']; data=d.embfile_get(j)
            ext=os.path.splitext(nm)[1].lower()
            afn=f"{m['i']:04d}_{j}{ext}"
            open(os.path.join(S,'att',afn),'wb').write(data)
            txt=''
            if ext in ('.pdf','.docx','.xlsx','.pptx','.txt','.csv','.htm','.html','.eml','.msg') :
                try:
                    if ext in ('.txt','.csv','.htm','.html'): txt=data.decode('utf8','ignore')
                    else:
                        ad=pymupdf.open(stream=data, filetype=ext[1:] if ext!='.msg' else None)
                        txt="\n".join(pg.get_text() for pg in ad)
                except Exception as e: txt=f'[unreadable {e}]'
            rec['atts'].append(dict(name=nm,file=afn,size=len(data),text=txt))
    except Exception as e:
        rec['err']=str(e)
    corpus.append(rec)
json.dump(corpus, open(os.path.join(S,'corpus.json'),'w',encoding='utf8'))
import collections
print(len(corpus), sum(len(r['atts']) for r in corpus))
print(collections.Counter(os.path.splitext(a['name'])[1].lower() for r in corpus for a in r['atts']).most_common())
print(collections.Counter(r['frm'] for r in corpus).most_common(40))
