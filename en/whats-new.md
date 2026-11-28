# What’s new

LivePanel checks for a new version every 6 hours and when an administrator signs in; it installs automatically or with the **Update** button — [Updates and notifications](updates-notifications.md). The version number is the date and time (UTC): `YYYY.MM.DD.HHMM`. The current version is shown at the bottom of the panel menu. This page lists the latest changes, newest first.

## 2026.11.28.1534 — Automatic updates setting

- **Settings → Automatic updates**: accepting updates automatically can be turned on or off. It is off by default.
- When off, a new version shows the notice `{version} Update available` with an **Update** button at the top right of the screen; the panel updates when you press it — [Updates and notifications](updates-notifications.md).

## 2026.11.26.1641 — Web firewall (WAF) and wildcard SSL with outside DNS

- **Web application firewall (WAF)** — ModSecurity + OWASP CRS per site: block or detect-only mode, WordPress/Drupal/Nextcloud exclusions, the list of stopped requests and switching a false-positive rule off in one click — [Site security](site-security.md#web-application-firewall-waf).
- **Wildcard SSL works with the DNS elsewhere too**: one `_acme-challenge` NS record at the registrar is enough, and the panel shows the exact record — [SSL certificates](ssl.md#wildcard-certificate-premium).
- API v2: `GET /sites/waf`, and the `waf`, `waf_app`, `waf_skip` site settings.

## 2026.11.26.1605 — Site statistics

- The **visitor report** (GoAccess) opens again: before, the page kept showing the loading spinner. The report still opens isolated from the panel (sandbox) — [Statistics](statistics.md).

## 2026.11.26.1523 — Wildcard SSL and DNSSEC

- **Wildcard SSL (Premium)** — one Let’s Encrypt certificate for the domain and all its subdomains (`example.uz` + `*.example.uz`). The panel adds and removes the check TXT record in the DNS zone itself; the certificate renews by itself — [SSL certificates](ssl.md#wildcard-certificate-premium).
- **DNSSEC** — the zone is signed and the panel shows the DS record for the registrar — [Domains and DNS](dns.md#dnssec).
- API v2: `wildcard` in `POST /sites/ssl`, the `dnssec` action of `POST /dns` — [API v2](api-reference.md).

## 2026.11.26.0718 — License protection

- A Free key cannot replace an active Premium license (`409 license_not_better`); within a plan the longer key stays.
- The “activate with a code” path, which never worked, is gone: paid keys arrive by themselves after payment — [License and plans](license.md#how-license-keys-are-protected).
- livepanel.uz hands a key only to the server that owns the license.

## 2026.11.25 — API v2

- **API v2 (Premium)**: almost everything the panel does, through the API — sites, files, databases, DNS, mail, FTP, cron, backups, Git, accounts, limits, branding and the server. 13 areas, each with “read” and “write” permissions — [API tokens](api-tokens.md), [API v2 reference](api-reference.md).
- PHP, Node.js and Bash examples and an OpenAPI file: [openapi.json](https://wiki.livepanel.uz/openapi.json). To hand the docs to an AI, every page has a “Copy for AI” button and a `.md` link.
- File manager: creating a folder that exists answers `file_exists`; uploads replace a file with `overwrite=1`.
- Backup storage sign-in (Google Drive, Dropbox) returns only to the panel’s own address.
