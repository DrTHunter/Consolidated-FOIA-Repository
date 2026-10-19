import pymupdf, sys, os, zipfile, re, json
src = os.path.expanduser("~/OneDrive/Desktop")
out = sys.argv[1]
files = ["01-09-2025 LECAC Agenda.pdf","03-13-2025 LECAC Agenda.pdf","11-14-2024 LECAC Agenda.pdf",
 "FOIA.20363.Bluffton_Flock_Camera_Locations.fulfillment.7.6.2026.pdf","20394 (1) (2).pdf"]
stats = {}
for f in files:
    d = pymupdf.open(os.path.join(src,f))
    empty = 0; chars = 0
    with open(os.path.join(out, f+".txt"),"w",encoding="utf-8") as o:
        for i,p in enumerate(d):
            t = p.get_text()
            if len(t.strip())<20: empty+=1
            chars += len(t)
            o.write(f"\n=====PAGE {i+1}=====\n{t}")
    stats[f] = dict(pages=d.page_count, empty_pages=empty, chars=chars)
z = zipfile.ZipFile(os.path.join(src,"2. LE Advise mins Feb 24.docx"))
x = z.read("word/document.xml").decode("utf8")
x = re.sub(r"</w:p>","\n",x); x = re.sub(r"<[^>]+>","",x)
open(os.path.join(out,"minutes.docx.txt"),"w",encoding="utf-8").write(x)
print(json.dumps(stats,indent=1))
