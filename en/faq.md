# FAQ and troubleshooting

## The panel

**The panel does not open.**
Check the services on the server: `systemctl status livepanel livepanel-agent`. Check that port 6563 is open in the provider’s external firewall. The panel’s own firewall never closes SSH and the panel port.

**I forgot the administrator password.**
With a recovery email set — **Forgot your password?** on the sign-in page. Otherwise, over SSH on the server: `passwd liveadmin`.

**My IP address is blocked.**
The block lifts by itself after a few minutes. If it is urgent, sign in from another IP (e.g. mobile internet), unblock yourself in **Settings → Login protection** and add your IP to the allowlist.

**I lost my phone and have no 2FA code.**
Enter one of the recovery codes. If you do not have them either, an administrator disables 2FA for the account in **Users**.

**“License expired” / “License is bound to another server”.**
[License and plans](license.md) — renew it or move the license to the new server.

## Sites

**The site does not open, says “site not found” or opens another site.**
Check that the domain’s A record points to the server IP: `nslookup example.uz`. DNS changes can take a few hours to spread.

**403 Forbidden.**
The site is disabled, the IP is blocked in **Site access**, or the folder has no index page (`index.php` / `index.html`).

**500 or 502 error.**
Open **Logs → Error log** (PHP) or **Application log** (Node.js, Python) — the cause is there. 502 means the application is not running or listens on another port.

**Large files cannot be uploaded to PHP.**
Raise `upload_max_filesize` and `post_max_size` in **Settings → Backend → PHP settings**.

**The SSL certificate was not issued.**
[SSL certificates](ssl.md) → “If the certificate is not issued”.

**Moving a site to another server.**
On the old server send a backup to Google Drive or Dropbox, connect the same storage on the new server, bring the copy in with **Get to server** and restore it — [Backups](backups.md). Or download the copy and upload it to the new server.

## Mail

**Mail does not reach Gmail.**
The provider may block outgoing port 25 — the panel warns about it. Contact the provider.

**Mail lands in spam.**
Check the SPF, DKIM and DMARC records and the server’s PTR (reverse DNS) record — [Mail](mail.md).

## Disk and resources

**The disk is full.**
**Files → Disk statistics** shows the largest folders and files. Clean up old backups, logs and caches; lower the number of copies kept by the automatic backup.

**The account got a “RAM block”.**
The sites went over the RAM limit. Raise the limit or optimize the site, then edit the account and turn on **Account active** — [Users, roles and limits](users.md).

## Removing the panel

On the server: `livepanel-uninstall`. This also deletes the sites, databases and mail — make backups first.

## Help

If you did not find an answer, contact us through the details on livepanel.uz. Include the panel version, the error text and the relevant log lines.
