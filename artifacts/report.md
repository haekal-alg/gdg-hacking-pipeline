# Vulnerability Report

**Title:** SQL Injection Authentication Bypass in /login
**Target:** https://vulnbank.org/login
**Severity:** Critical
**Reported by:** Muhammad Haekal
**Date:** 2026-07-18

## Summary

The `/login` endpoint builds its database query directly from the username and password fields instead of treating them as safe values. Sending `admin'--` as the username logs in without checking the password at all. This isn't a one-off: fuzzing 10 similar payloads against both fields found 11 out of 20 that work.

## Steps to Reproduce

1. Send a POST request to `/login` with this body: `{"username": "admin'--", "password": "anything"}`.
2. The response comes back `200 OK` with a valid login token, for an account we never had the password for.
3. Run `scripts/exploit.py` to see this confirmed automatically. It tries every payload in `payloads.txt` against both fields and reports which ones work. See `artifacts/exploit_results_20260718_073154.txt`.

## Impact

Anyone can log in as an existing user without a real password. Some payloads always land on the same account (`admin'--` gets account `8570375411` every time); others land on a different account each run since the query has no fixed order. Either way, the attacker gets a valid logged-in session for free.

## Recommendation

Use parameterized queries instead of building SQL from raw input, e.g. `cursor.execute("SELECT * FROM users WHERE username = %s", (username,))`. Add rate limiting to `/login` so this can't be automated at scale.

## Evidence

- `artifacts/nmap_output_20260718_072916.txt`: recon scan, four open ports
- `artifacts/gobuster_output_20260718_072916.txt`: recon scan, confirms `/login` exists
- `artifacts/exploit_results_20260718_073154.txt`: fuzz results, 11/20 payloads worked
- Reproduce it directly:
  ```
  curl -s -X POST https://vulnbank.org/login -H "Content-Type: application/json" -d "{\"username\": \"admin'--\", \"password\": \"anything\"}"
  ```
