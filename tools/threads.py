import json,sys,os,re,collections
S=sys.argv[1]
c=json.load(open(os.path.join(S,'corpus.json'),encoding='utf8'))
WARN=re.compile(r"WARNING!\s*This email originated.*?content is safe\.",re.S)
def norm(s):
    s=re.sub(r'^((re|fw|fwd|out of office[^r]*re)[:_]\s*)+','',s.strip(),flags=re.I)
    return s.lower()
mkt_from={'Flock Safety Daily Digest','Google Calendar','Flock Safety','Flock','Flock Safety Events','Customer Education at Flock','Dunning No-Reply','Flock Safety Do-not-reply','Flock Billing'}
groups=collections.defaultdict(list)
for r in c:
    groups[norm(r['subject'])].append(r)
keep=[]
for k,rs in groups.items():
    rs.sort(key=lambda r:len(r['body']))
    best=rs[-1]
    keep.append((min(r['sent'] for r in rs),k,best,[r['file'] for r in rs]))
keep.sort()
sub=open(os.path.join(S,'substantive.txt'),'w',encoding='utf8')
mk=open(os.path.join(S,'marketing.txt'),'w',encoding='utf8')
n=0
for sent,k,b,files in keep:
    body=WARN.sub('',b['body'])
    body=re.sub(r'Archived: .*?\n','',body)
    body=re.sub(r'\n\s*\n+','\n',body)
    is_mkt = b['frm'] in mkt_from or k.startswith(('invitation_','updated invitation','accepted_','declined_','canceled','synced invitation'))
    out = mk if is_mkt else sub
    out.write(f"\n\n######## [{b['file']}] (+{len(files)-1} dupes: {','.join(files[:6])}) {sent} | {b['frm']} | {b['subject']}\n{body}")
    if not is_mkt: n+=len(body)
print(len(keep), n)
