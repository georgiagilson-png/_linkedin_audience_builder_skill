# LinkedIn Audience Builder Skill

A Claude Code skill that creates saved audiences in LinkedIn Campaign Manager via the LinkedIn Ads API.

## What it does

Given an audience name and targeting criteria in plain language, this skill:
1. Resolves all targeting values (job titles, skills, seniorities, etc.) to LinkedIn URNs
2. Builds the correct `targetingCriteria` payload structure
3. POSTs to the LinkedIn Ads API to save the audience to your chosen ad account
4. Confirms success and reports the new audience ID

## Supported targeting criteria

- Job Titles (current)
- Member Skills (max 100)
- Job Seniorities
- Job Functions
- Company Industries
- Years of Experience
- Member Age
- Profile Location / IP Location
- Company Size
- Employer (current or all)
- Degrees / Fields of Study
- Member Groups
- Member Interests
- Company Growth Rate
- Company Revenue
- Company Category (Fortune 50/100/500)

## Setup

### 1. Set your LinkedIn access token

```bash
export LINKEDIN_ACCESS_TOKEN="your_token_here"
```

The token must have the `rw_ads` OAuth scope. Tokens expire -- check with your LinkedIn App admin for renewal.

### 2. Install the skill in Claude Code

Copy `SKILL.md` into your Claude skills directory, or install via the `.skill` package if available.

### 3. Use it

Just tell Claude what you want:

> "Create a saved audience called 'Finance Leaders Q3' in the SEON account targeting CFOs, CTOs, and VPs in the Capital Markets and Banking industries with 8+ years experience."

Claude will handle the rest.

## Manual use (script)

You can also use the helper script directly:

```bash
python scripts/create_audience.py \
  --account-id 507770895 \
  --name "My Audience" \
  --criteria path/to/criteria.json
```

The `criteria.json` should follow the LinkedIn `targetingCriteria` format (see SKILL.md for the structure).

## Ad accounts

| Account Name | Account ID |
|---|---|
| SEON | 507770895 |
| SEON (secondary) | 513954232 |
| Acuity Analytics | 504764976 |
| Aiven Oy | 504034043 |
| Learnosity | 506893206 |
| Ververica | 507880404 |
| Media Forty Two | 510472640 |

## Notes

- Age targeting requires certifying non-discriminatory use per LinkedIn's policy
- Company list / TAL segments require a pre-uploaded matched audience URN
- Token expiry: check the API details file for the current expiry date
