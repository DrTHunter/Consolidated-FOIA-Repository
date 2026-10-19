import json, os, re, sys, shutil
import pymupdf
sys.path.insert(0, os.path.dirname(__file__))
from content import POINTS, STORY, FAIR, NEXT

S = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
DESK = os.path.expanduser("~/OneDrive/Desktop")
os.makedirs(os.path.join(OUT, "docs"), exist_ok=True)

# Secret to black out (a camera password found in the records). Never commit it.
PASSWORD = os.environ["FLOCK_REDACT_TERM"]
REDACT = "[REDACTED]"

def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()

# ---- email corpus ----
corpus = {r["file"][:4]: r for r in json.load(open(os.path.join(S, "corpus.json"), encoding="utf8"))}
sub_ids = re.findall(r"^######## \[(\d{4})\.pdf\]", open(os.path.join(S, "substantive.txt"), encoding="utf8").read(), re.M)

WARN = re.compile(r"WARNING!\s*This email originated.*?content is\s*safe\.", re.S)
DISC = re.compile(r"Disclaimer from Town of Bluffton:.*?original\s*message\.", re.S)
SPACED = re.compile(r"^(\S ){5,}")
def clean(t):
    t = WARN.sub("", t); t = DISC.sub("", t)
    t = re.sub(r"This email was sent to .*?(any\s*time\.|Policy)", "", t, flags=re.S)
    lines = []
    for l in t.split("\n"):
        s = l.strip()
        if SPACED.match(s) or s.startswith("Archived:") or s.startswith("Monday, July 27, 2026"):
            continue
        lines.append(l.rstrip())
    t = "\n".join(lines)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

def date_of(d):
    return f"{d[2:6]}-{d[6:8]}-{d[8:10]}" if d.startswith("D:") else ""

docs = {}
def add_email(i):
    r = corpus[i]
    t = clean(r["body"]).replace(PASSWORD, REDACT)
    if i == "0681":  # officer roster: strip phone numbers
        t = re.sub(r"\b\d{3}-\d{3}-\d{4}\b", "[phone]", t)
    subj = re.sub(r"_", ":", r["subject"]) if r["subject"] else "(no subject)"
    docs["e" + i] = dict(kind="Email", src=f"FOIA 20394 · item {i}", title=r["subject"] or "(no subject)",
                         frm=r["frm"].replace("  ", " "), date=date_of(r["sent"]), text=t, pdf=None)

for i in sub_ids:
    add_email(i)

def txt(name):
    return open(os.path.join(S, "txt", name), encoding="utf8").read()
def page_clean(t):
    t = re.sub(r"=====PAGE \d+=====\n", "", t)
    return re.sub(r"[ \t]+\n", "\n", t).strip()

docs["a2024-11-14"] = dict(kind="Agenda", src="LECAC agenda", title="LECAC meeting agenda, Nov 14, 2024", frm="Town of Bluffton", date="2024-11-14", text=page_clean(txt("11-14-2024 LECAC Agenda.pdf.txt")), pdf="11-14-2024 LECAC Agenda.pdf")
docs["a2025-01-09"] = dict(kind="Agenda", src="LECAC agenda", title="LECAC meeting agenda, Jan 9, 2025", frm="Town of Bluffton", date="2025-01-09", text=page_clean(txt("01-09-2025 LECAC Agenda.pdf.txt")), pdf="01-09-2025 LECAC Agenda.pdf")
docs["a2025-03-13"] = dict(kind="Agenda", src="LECAC agenda", title="LECAC meeting agenda, Mar 13, 2025", frm="Town of Bluffton", date="2025-03-13", text=page_clean(txt("03-13-2025 LECAC Agenda.pdf.txt")), pdf="03-13-2025 LECAC Agenda.pdf")
docs["f20363"] = dict(kind="FOIA response", src="FOIA 20363", title="Bluffton Flock camera locations (50 sites)", frm="Town of Bluffton", date="2026-07-06", text=page_clean(txt("FOIA.20363.Bluffton_Flock_Camera_Locations.fulfillment.7.6.2026.pdf.txt")), pdf="FOIA.20363.Bluffton_Flock_Camera_Locations.fulfillment.7.6.2026.pdf")
m = txt("minutes.docx.txt")
m = m.replace("(38 Wiregrass Way, Bluffton, SC 29910)", "(address removed)")
for k in ["Members present:", "Members Not Present:", "Staff Present:", "Michael Frazier called", "Public Comment:", "Old Business:", "New Business:", "Discussion:", "A motion to adjourn", "The next scheduled", "Sergeant Matt Ferrelli"]:
    m = m.replace(k, "\n\n" + k)
m = re.sub(r"\s*-(?=[A-Z])", "\n- ", m)
m = re.sub(r"[ \t]{2,}", " ", m).strip()
docs["m2024-02-08"] = dict(kind="Minutes", src="LECAC minutes", title="LECAC meeting minutes, Feb 8, 2024", frm="Town of Bluffton", date="2024-02-08", text=m, pdf=None)

# ---- cites ----
cited = set()
def check(cites, where):
    bad = 0
    for d, q in cites:
        if d not in docs:
            add_email(d[1:]) if d.startswith("e") else None
        if d not in docs:
            print("MISSING DOC", d, where); bad += 1; continue
        cited.add(d)
        if q and norm(q) not in norm(docs[d]["text"]):
            print("QUOTE NOT FOUND", where, d, repr(q)); bad += 1
    return bad
bad = 0
for p in POINTS: bad += check(p["cites"], p["id"])
for c in STORY:
    for e in c["entries"]: bad += check(e[2], c["id"] + " " + e[0])
for f in FAIR: bad += check(f[1], "fair")
print("problems:", bad, "cited docs:", len(cited), "total docs:", len(docs))

# ---- PDFs for cited docs (redacted where needed) ----
total = 0
for d in sorted(cited):
    doc = docs[d]
    if d.startswith("e"):
        srcp = os.path.join(S, "emails", d[1:] + ".pdf")
        name = f"FOIA20394-item{d[1:]}.pdf"
    elif doc["pdf"]:
        srcp = os.path.join(DESK, doc["pdf"]); name = doc["pdf"].replace(" ", "_")
    else:
        continue
    dst = os.path.join(OUT, "docs", name)
    if d in ("e0232", "e0681"):
        pdf = pymupdf.open(srcp)
        for pg in pdf:
            terms = [PASSWORD] if d == "e0232" else sorted(set(re.findall(r"\b\d{3}-\d{3}-\d{4}\b", pg.get_text())))
            for term in terms:
                for rect in pg.search_for(term):
                    pg.add_redact_annot(rect, fill=(0, 0, 0))
            pg.apply_redactions()
        pdf.save(dst, garbage=3, deflate=True)
        chk = pymupdf.open(dst)
        alltext = "".join(p.get_text() for p in chk)
        assert PASSWORD not in alltext
        if d == "e0681": assert not re.search(r"\b\d{3}-\d{3}-\d{4}\b", alltext), "phones remain"
    else:
        shutil.copyfile(srcp, dst)
    doc["pdf"] = "docs/" + name
    total += os.path.getsize(dst)
for d, doc in docs.items():
    if d not in cited and not (doc["pdf"] or "").startswith("docs/"):
        doc["pdf"] = None
print("pdf MB", round(total / 1e6, 1))

data = dict(points=POINTS, story=STORY, fair=FAIR, next=NEXT, docs=docs)
with open(os.path.join(OUT, "data.js"), "w", encoding="utf8") as f:
    f.write("window.FLOCK=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";")
print("data.js KB", os.path.getsize(os.path.join(OUT, "data.js")) // 1024)
