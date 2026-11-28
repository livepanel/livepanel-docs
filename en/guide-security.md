# Security checklist

The panel’s tools for protecting the server and sites — in one place. Go through this list after installing the panel.

## Panel and accounts

- [ ] **Change the `liveadmin` password** and do not use it anywhere else — [Panel settings and security](panel-settings.md).
- [ ] **Turn on two-factor sign-in (2FA)** and keep the recovery codes somewhere safe.
- [ ] **Enter a recovery email** — for a forgotten password and important notifications.
- [ ] **Set up login protection:** attempts, block duration; add your own IP to the allowlist.
- [ ] **Install fail2ban** (**System → Applications**) — it protects SSH, FTP and mail from password guessing.
- [ ] **Give the panel a trusted certificate** or open it by a domain — [Panel address and SSL](panel-access.md).
- [ ] Give every customer **a separate account** with only the permissions they need — [Users, roles and limits](users.md).
- [ ] Disable or delete accounts you no longer need; look through the [activity log](api-tokens.md) from time to time.
- [ ] Create API tokens with the fewest scopes and a short term; revoke the ones you do not need — [API v2 reference](api-reference.md).

## Server

- [ ] **Turn the firewall on** and keep only the ports you need — [Firewall](firewall.md).
- [ ] Stop services you do not use (e.g. mail, if not needed) — [System services](services.md).
- [ ] Give outside database access only to exact IPs, never `%` — [Databases](databases.md).
- [ ] Turn SSH on only for the accounts that need it.
- [ ] Keep the panel on the new version: turn on **Automatic updates** or press the **Update** button at the top; keep the license active — [Updates and notifications](updates-notifications.md).

## Sites

- [ ] **SSL** and the **HTTPS redirect** for every site — [SSL certificates](ssl.md).
- [ ] Create every site under **its own Linux user** — if one site is hacked, the others stay safe.
- [ ] Close internal and test sites **by IP** or with a **login and password** — [Site security and scanning](site-security.md).
- [ ] With many bots, turn on the **request rate limit** — [Site settings](site-settings.md).
- [ ] Install **ClamAV** and scan the sites from time to time.
- [ ] Keep PHP `display_errors` off on production sites.
- [ ] Keep the CMS, plugins and libraries updated.

## Backups

- [ ] **Automatic backups** for every important site — [Backups](backups.md).
- [ ] Send copies **outside the server** too (Google Drive or Dropbox).
- [ ] **Test a restore** from time to time — a backup you cannot restore is worthless.

## If a site is hacked

1. **Disable** the site for a while or close it by IP.
2. Find the malicious files with **Scanning** and quarantine them.
3. Look through the **activity log** and **logs** to find how they got in.
4. Restore from a clean backup.
5. Change every password: panel, FTP/SSH, database, CMS administrator, API tokens.
6. Update the CMS and plugins, then enable the site.
