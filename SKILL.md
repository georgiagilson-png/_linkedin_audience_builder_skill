---
name: linkedin-audience-builder
description: >
  Creates a saved LinkedIn audience in Campaign Manager via the LinkedIn Ads API.
  Use this skill whenever the user wants to build, create, save, or set up a LinkedIn
  audience — even if they don't say "API" or "skill". Triggers on requests like
  "create an audience for me on LinkedIn", "save this audience to LinkedIn",
  "build a LinkedIn saved audience", "set up targeting in LinkedIn Campaign Manager",
  or any time the user provides audience criteria (job titles, skills, seniorities,
  industries, etc.) and wants it saved to a LinkedIn ad account.
---

# LinkedIn Audience Builder

Create a saved audience in LinkedIn Campaign Manager using the Ads API.

## What you need from the user

Before building the audience, confirm you have:

1. **Audience name** -- what to call it in Campaign Manager
2. **Ad account** -- which account to save it to (see account list below)
3. **Location targeting** -- always ask which countries, regions, or cities to target (Profile Location and/or IP Location). Do not proceed without this.
4. **Targeting criteria** -- any combination of:
   - Job Titles (current)
   - Member Skills
   - Job Seniorities
   - Job Functions
   - Company Industries
   - Years of Experience
   - Member Age
   - Profile Location / IP Location
   - Company Size
   - Company Names (employer targeting)
   - Degrees / Fields of Study
   - Member Groups
   - Member Interests
   - Company Growth Rate
   - Company Revenue
   - Company Category (Fortune 50/100/500 etc.)

If anything is missing, ask before proceeding.

## Available ad accounts

| Account Name | Account ID |
|---|---|
| SEON | 507770895 |
| SEON (secondary) | 513954232 |
| Acuity Analytics | 504764976 |
| Aiven Oy | 504034043 |
| Learnosity | 506893206 |
| Ververica | 507880404 |
| Media Forty Two | 510472640 |

## Step 1: Resolve URNs for all criteria

Use the `mcp__linkedin-audience__search_targeting_entities` tool to look up URNs for each targeting value. Run searches in parallel where possible.

Facet name mappings:
- Job Titles → `titles`
- Member Skills → `skills`
- Job Seniorities → use `mcp__linkedin-audience__get_facet_entities` with facet `seniorities`
- Job Functions → use `mcp__linkedin-audience__get_facet_entities` with facet `jobFunctions`
- Company Industries → `industries`
- Profile Location → `profileLocations`
- IP Location → `ipLocations`
- Company Size → use `mcp__linkedin-audience__get_facet_entities` with facet `staffCountRanges`
- Years of Experience → use `mcp__linkedin-audience__get_facet_entities` with facet `yearsOfExperienceRanges`
- Member Age → use `mcp__linkedin-audience__get_facet_entities` with facet `ageRanges`
- Degrees → `degrees`
- Fields of Study → `fieldsOfStudy`
- Employer (current) → `employers`
- Employer (all) → `employersAll`
- Groups → `groups`
- Interests → `interests`
- Company Growth Rate → use `mcp__linkedin-audience__get_facet_entities` with facet `growthRate`
- Company Revenue → use `mcp__linkedin-audience__get_facet_entities` with facet `revenue`
- Company Category → use `mcp__linkedin-audience__get_facet_entities` with facet `companyCategory`

**LinkedIn skills limit:** Member Skills facet is capped at 100 values. If more than 100 skills are provided, deduplicate and trim to 100, noting which were dropped.

Always pick the closest exact match. If a search returns no match, note it and skip rather than using an approximate.

## Step 2: Build the targeting criteria payload

Structure criteria as AND across facets, OR within a facet:

```json
{
  "targetingCriteria": {
    "include": {
      "and": [
        {
          "or": {
            "urn:li:adTargetingFacet:titles": [
              "urn:li:title:153",
              "urn:li:title:68"
            ]
          }
        },
        {
          "or": {
            "urn:li:adTargetingFacet:skills": [
              "urn:li:skill:1184",
              "urn:li:skill:1245"
            ]
          }
        },
        {
          "or": {
            "urn:li:adTargetingFacet:seniorities": [
              "urn:li:seniority:6",
              "urn:li:seniority:7",
              "urn:li:seniority:8"
            ]
          }
        }
      ]
    }
  }
}
```

Each AND block contains exactly one facet with its OR list of URNs.

## Step 3: Confirm all criteria with the user before implementing

Before making any API calls, present a full summary of every resolved value grouped by facet, and ask the user to confirm. Format it clearly, for example:

---
**Please review and confirm the following targeting before I create the campaign:**

**Job Titles (41)**
- Chief Technology Officer (urn:li:title:153)
- VP of Engineering (urn:li:title:68)
- ...

**Member Skills (99)**
- Python (urn:li:skill:1184)
- ...

**Seniorities**
- Director, VP, CXO, Owner, Partner

**Job Functions**
- Information Technology, Engineering

**Industries**
- Computer Software, IT Services, Computer Networking

**Locations**
- United Kingdom (urn:li:geo:101165590)

**Years of Experience**
- 5 years, 6 years, ... *(note any API limits)*

**Age Ranges**
- 35-54, 55+

**Campaign name:** Agent Fleet | Retargeting | C
**Account:** Acuity Analytics
**Campaign Group:** Agent Fleet

Shall I proceed?

---

Do not call the API until the user confirms. If they request any changes, update the criteria and show the summary again.

## Step 4: Apply targeting or output for manual entry

> **API limitation:** LinkedIn's "Saved Audiences" (Plan > Audiences in Campaign Manager) does **not** have a public API endpoint. This is a confirmed gap -- even with `rw_ads` scope, there is no `POST /savedAudiences` or equivalent endpoint available in LinkedIn's public Marketing API.

**Two options depending on user need:**

**Option A -- Apply directly to a campaign (API-supported):**
```bash
curl -s -X POST "https://api.linkedin.com/v2/adCampaignsV2" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -d '{
    "account": "urn:li:sponsoredAccount:ACCOUNT_ID",
    "name": "CAMPAIGN_NAME",
    "status": "DRAFT",
    "type": "SPONSORED_UPDATES",
    "costType": "CPM",
    "targetingCriteria": { ... }
  }'
```

**Option B -- Output for manual entry in Campaign Manager:**
Present the full resolved criteria list (display names + URNs grouped by facet) so the user can paste them into Campaign Manager under Plan > Audiences > Create audience > Saved audience.

## Step 5: Report back

Report:
- Full resolved targeting criteria, grouped by facet with display names
- Count of values per facet
- Any criteria that could not be resolved (skipped)
- Whether targeting was applied to a campaign (Option A) or output for manual entry (Option B)

If an API call returns an error, show the full error message and suggest checking token expiry (expires 2026-08-17) or account permissions.

## Configuration

The skill reads credentials from environment variables. Set these before use:

```bash
export LINKEDIN_ACCESS_TOKEN="your_token_here"
```

The token expires **2026-08-17**. If it has expired, a new one must be generated via the LinkedIn OAuth flow using:
- Client ID: stored in `~/.claude/linkedin_config` (set up separately)

## Notes

- The `savedAudiences` endpoint requires the `rw_ads` OAuth scope
- Age targeting requires the user to certify they will not use it to discriminate -- confirm this with the user before including age criteria
- Company list / TAL (matched audience segments) require a pre-uploaded segment URN -- only include these if the user explicitly provides a segment name or URN
- Maximum 100 values per skill facet; other facets have no hard limit but LinkedIn recommends keeping total criteria reasonable
