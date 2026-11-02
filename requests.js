// FOIA request tracker. Edit this file by hand; build.py does not touch it.
// Privacy rule: requesters appear as first name + last initial only. No emails,
// street addresses, or phone numbers. Town staff are named by role.
//
// no:     the Town's request number, or null until it is known
// status: "filed" | "paused" | "fulfilled" | "closed"
// log:    [date, what happened], oldest first
window.FOIA_REQUESTS = [
  {
    no: null,
    requester: "Julie M.",
    filed: "2026-07-06",
    dept: "Engineering / Traffic / Safety",
    scope: "Entire Town of Bluffton, every street and shopping center",
    asked: [
      "All contracts and information on every Flock camera installed around town.",
      "Which meetings and agendas the Flock cameras were discussed in."
    ],
    status: "filed",
    log: [
      ["2026-07-06", "Filed through the Town's online FOIA form."]
    ]
  },
  {
    no: null,
    requester: "Trent H.",
    filed: "2026-07-21",
    dept: "Bluffton Police Department",
    scope: "Entire Town of Bluffton",
    asked: [
      "The Police Chief's emails with the Flock sales team, looking for free trials or grant funding that bypassed Town approval.",
      "The Town's formal ordinance authorizing the cameras, or a statement that none exists."
    ],
    status: "paused",
    log: [
      ["2026-07-21", "Filed through the Town's online FOIA form."],
      ["2026-07-22", "Town's PIO acknowledged the request and asked for a date range for the IT search. FOIA clock stopped until a range is given. Staff time over 2 hours is billed under the fee schedule."],
      ["2026-07-22", "Requester narrowed it to emails between the Police Chief (or the designated Flock contact) and the Flock representative over the past 365 days."]
    ]
  },
  {
    no: null,
    requester: "Trent H.",
    filed: "2026-11-02",
    dept: "Town Clerk / Mayor and Town Council",
    scope: "Flock Safety communications",
    asked: [
      "All emails, with attachments, between the Mayor or any Town Council member and anyone at Flock Safety (including any @flocksafety.com address), January 1, 2017 to present, as complete threads in electronic format.",
      "Any withheld or redacted record to cite its specific § 30-4-40 exemption, with nonexempt portions released."
    ],
    status: "filed",
    log: [
      ["2026-11-02", "Filed through the Town's online FOIA form, with an offer to meet the Mayor or Council before publishing."]
    ]
  },
  {
    no: null,
    requester: "Trent H.",
    filed: "2026-11-02",
    dept: "Finance (filed under Town Clerk / Mayor and Town Council)",
    scope: "Flock Safety invoices and payments",
    asked: [
      "All invoices from Flock Safety (Flock Group, Inc.) to the Town, January 1, 2017 to present.",
      "The matching payment records (purchase orders, check or ACH records, general ledger entries) showing the fund, department, and account code each payment was charged to."
    ],
    status: "filed",
    log: [
      ["2026-11-02", "Filed through the Town's online FOIA form."]
    ]
  }
];
