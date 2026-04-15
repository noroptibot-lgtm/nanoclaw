---
name: norwegian-writer
description: "Write flawless, natural Norwegian bokmål using correct æ, ø, å and native phrasing. Use this skill whenever the user asks for anything in Norwegian, including emails, ads, captions, contracts, replies to clients, website copy, SMS, or translations into Norwegian. Use it even when the user only switches into Norwegian mid-conversation, types a Norwegian word, or asks how to say something in Norwegian. Never write nynorsk. Never substitute ae/oe/aa for æ/ø/å. Never write Norwegian that sounds translated."
---

# Norwegian Writer

Your job is to produce Norwegian text that a native speaker from Oslo would write themselves. No translation smell. No anglicisms. Correct spelling, correct æ ø å, correct word order, correct register.

## Hard rules

1. **Always use æ, ø, å.** Never ae, oe, aa. Never a, o. If you cannot type them, stop and fix your output.
2. **Always write bokmål. Never nynorsk.** If the user asks for nynorsk, refuse and offer bokmål instead. Do not mix nynorsk forms ("eg", "ikkje", "kva", "kjem") into bokmål text.
3. **Never invent words.** If you are not 100% sure a word exists in Norwegian, check `references/common-mistakes.md` or pick a word you know.
4. **Never word-for-word translate from English.** Rewrite the idea in Norwegian. English idioms do not survive translation.
5. **No em dashes.** Norwegian uses commas, periods, parentheses, or colons.
6. **Match register to channel.** SMS to a customer is not the same as a service contract. See "Register" below.

## Workflow for any Norwegian request

1. Read the request. Identify: channel (email, SMS, ad, contract, caption), audience (customer, supplier, B2B, B2C), and dialect (bokmål default).
2. Draft in Norwegian directly. Do not draft in English first and translate.
3. Run the self-check (below) before sending output.
4. If the request is a translation, read the English source twice, then write the Norwegian version as if you were the original author.

## Self-check before every output

Before you finish, walk this list:

- Every æ, ø, å is present where it belongs. No ae/oe/aa.
- No English word order leaking through ("jeg har vært i Oslo i 5 år" not "jeg har vært i Oslo for 5 år").
- "Å" vs "og" is correct. "Å" goes before infinitive. "Og" connects two things.
- "De" / "dem" / "deres" used correctly. "De" is subject. "Dem" is object.
- "Sin/sitt/sine" refers back to the subject of the same clause, not someone else.
- No double definite ("den bilen" → usually just "bilen", unless you are pointing).
- Compound words are written as ONE word. "Lammelår" not "lamme lår". "Kundeservice" not "kunde service". This is the most common mistake. See `references/compound-words.md`.
- Numbers, dates, currency in Norwegian format: 1 500 kr, 12.04.2026, kl. 14.30.
- Punctuation: comma before "men", "for", "så" when they join two main clauses. No Oxford comma.

If anything fails, fix it before you output.

## Register guide

| Channel | Tone | Example opener |
|---|---|---|
| Cold email B2B | Direct, polite, no fluff | "Hei [navn], jeg så at..." |
| Customer SMS | Short, warm, first name | "Hei Anders, takk for..." |
| Service contract | Formal, precise, third person OK | "Kunden forplikter seg til..." |
| Ad copy / hook | Conversational, native slang OK | "Slik fikser du..." |
| Reply to complaint | Calm, ownership, no excuses | "Hei, beklager at..." |
| Website body copy | Clear, second person ("du") | "Du får..." |

Norwegians are informal. Use "du", not "De". "De" as polite form is dead. Last names alone feel cold. First names are standard, even with strangers in business.

## When to load reference files

- **Compound words / særskriving doubts** → read `references/compound-words.md`. This is the single biggest error category. If you are writing any noun phrase with two parts, check.
- **Common mistakes (anglicisms, false friends, og/å, da/når, enda/ennå)** → read `references/common-mistakes.md`.
- **Business / contract / legal phrasing** → read `references/business-phrases.md`.

Read the file before writing. Do not guess.

## What "natural" means

A native Norwegian writes like this:
- Short sentences. Norwegians do not pile clauses.
- "Jeg" and "du" are fine. Not stiff.
- Ends emails with "Mvh, [navn]" or "Hilsen [navn]". Not "Beste hilsener" (translation smell).
- Says "Hei" not "Hallo" or "Kjære" in 95% of cases. "Kjære" only for very formal letters or people you love.
- Uses "takk" generously. "Tusen takk" is normal, not over the top.
- Says "kanskje" not "muligens" in casual contexts.
- Says "jeg skal" for plans, "jeg kommer til å" for predictions, "jeg vil" for want.

## What translation smell looks like (avoid)

- "Jeg ser frem til å høre fra deg" → too literal. Native: "Jeg håper å høre fra deg" or just "Si fra hvis du lurer på noe."
- "Ikke nøl med å kontakte oss" → translated. Native: "Ta kontakt hvis du har spørsmål."
- "Vi setter pris på din virksomhet" → dead translation. Native: "Takk for at du handler hos oss."
- "Ha en flott dag" → American. Native Norwegians do not say this. End with "Mvh" and stop.

## If you are unsure

Stop. Do not guess. Either:
- Read the relevant reference file.
- Ask the user for the missing context (which dialect, which client, what tone).
- Use a simpler word you know is correct.

A simple correct sentence beats a fancy wrong one every time.
