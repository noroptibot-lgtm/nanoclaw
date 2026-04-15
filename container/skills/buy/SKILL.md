---
name: buy
description: Manage Albert's shopping list in Airtable. Add items, research best prices/links, mark as bought. Reads from and writes to app4vE3ULSqaAterL / tblCbqs9yKbF2180x.
---

# /buy — Shopping List Manager

Airtable shopping list for Albert.

**Base:** app4vE3ULSqaAterL
**Table:** tblCbqs9yKbF2180x
**Fields:**
- Name (fldeSPEyd9ipQZtCw) — item name
- Notes (fldg54gXlgGGXO8eC) — price, link, notes
- Status (fldOMyi2qUTYLDkP2) — Todo / Bought / Skip
- Attachments (fldUyo5hMN5020KAj)

---

## What you do

Parse the input after `/buy`:

**No input / "list"** — show all items with Status=Todo. Format as a numbered list with name + notes.

**"add <item>"** — add a new record to Airtable with Name=item, Status=Todo. Then immediately research it: find the best Norwegian/Nordic source (finn.no, prisjakt.no, amazon.de, komplett.no), best price, and add a short note with the best link + price. Report back.

**"bought <number or name>"** — mark the item as Status=Bought.

**"skip <number or name>"** — mark as Status=Skip.

**"research <number or name>"** — do a deep price/source search for that item. Update the Notes field with best link + price. Report findings.

**"clear"** — show all Bought/Skip items and ask for confirmation before deleting.

---

## Research approach

When researching a purchase:
1. Use WebSearch to find the item + best Norwegian source
2. Check prisjakt.no first for price comparison
3. Note: delivery time, price in NOK, best retailer
4. If it's a supplement/health item, note Norwegian legal status
5. Keep notes short: "Komplett.no — 1299 kr — [url]"

---

## Rules
- Always respond in Norwegian
- No em dashes
- Keep it short and actionable
- If the item seems impulsive or low-priority, say so briefly
