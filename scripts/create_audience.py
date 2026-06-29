#!/usr/bin/env python3
"""
LinkedIn Saved Audience Creator
Builds and POSTs a saved audience to the LinkedIn Ads API.

Usage:
    python create_audience.py --account-id 507770895 --name "My Audience" --criteria criteria.json

The criteria.json should follow the LinkedIn targetingCriteria format:
{
  "include": {
    "and": [
      { "or": { "urn:li:adTargetingFacet:titles": ["urn:li:title:153"] } },
      { "or": { "urn:li:adTargetingFacet:skills": ["urn:li:skill:1184"] } }
    ]
  }
}
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


LINKEDIN_API_BASE = "https://api.linkedin.com/v2"


def create_saved_audience(account_id: str, name: str, targeting_criteria: dict, access_token: str) -> dict:
    payload = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "name": name,
        "targetingCriteria": targeting_criteria,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{LINKEDIN_API_BASE}/savedAudiences",
        data=data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return {"status": resp.status, "body": json.loads(body) if body else {}}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"status": e.code, "error": body}


def main():
    parser = argparse.ArgumentParser(description="Create a LinkedIn saved audience")
    parser.add_argument("--account-id", required=True, help="LinkedIn ad account ID (numeric)")
    parser.add_argument("--name", required=True, help="Audience name")
    parser.add_argument("--criteria", required=True, help="Path to targeting criteria JSON file")
    parser.add_argument("--token", help="Access token (defaults to LINKEDIN_ACCESS_TOKEN env var)")
    args = parser.parse_args()

    access_token = args.token or os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        print("ERROR: No access token provided. Set LINKEDIN_ACCESS_TOKEN or use --token.")
        sys.exit(1)

    with open(args.criteria) as f:
        targeting_criteria = json.load(f)

    result = create_saved_audience(args.account_id, args.name, targeting_criteria, access_token)

    if result.get("status") in (200, 201):
        print(json.dumps(result["body"], indent=2))
        print(f"\nSuccess! Audience created with ID: {result['body'].get('id', 'unknown')}")
    else:
        print(f"ERROR (HTTP {result.get('status')}):")
        print(result.get("error", result))
        sys.exit(1)


if __name__ == "__main__":
    main()
