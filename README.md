# Consolidated FOIA Repository

What the Town of Bluffton's own records show about its Flock Safety camera network, organized so anyone can follow it.

Open `index.html` in a browser (or turn on GitHub Pages for this repo) to get:

- **The strongest points**: 14 talking points, ranked by how solid the paper trail is.
- **The story, step by step**: seven chapters in date order, April 2023 to July 2026.
- **All records**: a searchable index of 198 records.
- **What to request next**: gaps the next FOIA requests should fill.

Every quote links to its source record, with the quoted words highlighted and a link to the original PDF. "Back to where you were" returns you to the same spot on the page.

## Sources

| Source | What it is |
|---|---|
| FOIA 20394 | Archive of 1,167 emails between Bluffton PD and Flock Safety (April 2023 – July 2026) |
| FOIA 20363 | List of 50 Flock camera locations (July 6, 2026) |
| LECAC agendas | Nov 14, 2024; Jan 9, 2025; Mar 13, 2025 |
| LECAC minutes | Feb 8, 2024 |

`docs/` holds the PDFs of every record cited on the site. The full 490 MB FOIA 20394 package is **not** in this repo.

## Redactions

- A camera system password that the Town emailed to Flock in plain text is blacked out, in both the text and the PDF.
- Officers' phone numbers in the user roster (item 0681) are blacked out.
- A member of the public's street address in the Feb 2024 minutes is removed.

Do not add the unredacted FOIA 20394 package to this repo.

## How it was built

`tools/` has the scripts used to build the site from the FOIA files:

1. `extract.py`, `unpack.py`: pull text from the PDFs and unpack the 1,167 emails from the FOIA 20394 package.
2. `emailtext.py`, `threads.py`: extract each email and collapse duplicate threads.
3. `content.py`: the talking points, story, and citations. Each citation is a record ID plus an exact quote.
4. `build.py`: checks that every quote appears word-for-word in its record, applies the redactions, copies the cited PDFs into `docs/`, and writes `data.js`.

`build.py` reads the password to black out from the `FLOCK_REDACT_TERM` environment variable, so the secret is never stored in this repo. The scripts expect Python 3 with PyMuPDF, and they contain local file paths you will need to adjust.

## Accuracy

Quotes are copied from the records and checked by machine against the source text. The site sticks to what the records say. These records do not include search audit logs, Council minutes, or the signed contract, so they cannot show whether anyone misused the system.
