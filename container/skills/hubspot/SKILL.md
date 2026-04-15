---
name: hubspot
description: HubSpot CRM skill — manage contacts, deals, pipelines, sequences, and reporting. Use when working with HubSpot data, automating CRM tasks, building sequences, analyzing pipeline health, or troubleshooting HubSpot workflows.
---

# HubSpot CRM Skill

Manage contacts, deals, sequences, and pipeline reporting in HubSpot.

---

## What This Skill Does

- **Contact management** — find, create, update, segment contacts
- **Deal pipeline** — move deals, update stages, flag stale deals
- **Sequences** — build, audit, and optimize email sequences
- **Reporting** — pipeline health, conversion rates, revenue forecasting
- **Automation** — workflows, property updates, notifications
- **Cleanup** — duplicates, missing data, dead contacts

---

## HubSpot API Access

Credentials should be in environment variables:
```
HUBSPOT_ACCESS_TOKEN=your_private_app_token
```

Base URL: `https://api.hubapi.com`

Key endpoints:
- Contacts: `GET/POST /crm/v3/objects/contacts`
- Deals: `GET/POST /crm/v3/objects/deals`
- Companies: `GET/POST /crm/v3/objects/companies`
- Pipelines: `GET /crm/v3/pipelines/deals`
- Engagements: `GET /crm/v3/objects/notes`

---

## Common Tasks

### Find a contact
```bash
curl "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"email","operator":"EQ","value":"email@example.com"}]}]}'
```

### List deals in a stage
```bash
curl "https://api.hubapi.com/crm/v3/objects/deals/search" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"dealstage","operator":"EQ","value":"STAGE_ID"}]}],"properties":["dealname","amount","closedate","hubspot_owner_id"]}'
```

### Update a deal stage
```bash
curl -X PATCH "https://api.hubapi.com/crm/v3/objects/deals/DEAL_ID" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"dealstage":"new_stage_id"}}'
```

---

## Pipeline Health Report

When asked for pipeline health, output:
1. **Total pipeline value** by stage
2. **Stale deals** — no activity in 14+ days
3. **Close date overdue** — past expected close
4. **Win rate** — closed won vs closed lost (last 30 days)
5. **Top 5 deals by value**

---

## Sequence Audit

When auditing a sequence:
1. Check open rates by step (flag steps below 30%)
2. Check reply rates (flag if step 1 reply rate < 5%)
3. Check bounce/unsubscribe spikes
4. Recommend subject line rewrites for underperforming steps
5. Check send time distribution

---

## Output Format

Always present data in clean tables. For action items, use numbered list. Flag urgent items (stale deals, overdue closes) in bold.

---

## Rules

- Never delete contacts or deals without explicit confirmation
- Always confirm before bulk updates (more than 10 records)
- When API credentials are missing, tell the user exactly which env var to set
