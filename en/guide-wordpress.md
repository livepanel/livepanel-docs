# A WordPress site: from zero to HTTPS

In this guide we open a WordPress site on your domain: the site, WordPress, SSL, mail and automatic backups. About 10 minutes.

**You need:** a server with LivePanel, a domain (e.g. `example.uz`) and access to its DNS.

## 1. Point the domain to the server

In your domain registrar’s panel add two A records:

| Name | Type | Value |
|---|---|---|
| `@` | A | the server IP address |
| `www` | A | the server IP address |

DNS takes from minutes to a few hours to spread. Check: `nslookup example.uz` must show the server IP. Details — [Domains and DNS](dns.md).

## 2. Create the site and WordPress

![CMS and frameworks](../images/wizard-apps.png)

1. **Sites → Create site**.
2. Template: **CMS / Framework → PHP → CMS → WordPress**.
3. Domain: `example.uz`. Site user — **a new user**.
4. On the settings step enter WordPress’s **site name**, **administrator login**, **email** and **password** (at least 12 characters; the panel suggests one). Keep the PHP version or pick the newest.
5. Click **Create site**.

The panel downloads WordPress, creates a MySQL database and sets up `wp-config.php`. At the end you get the admin link (`https://example.uz/wp-admin/`) and the database details — save them. Details — [Installing CMS and frameworks](app-installer.md).

## 3. Get an SSL certificate

![SSL](../images/ssl.png)

1. On the site page open **SSL certificates → New certificate**.
2. Choose **Let’s Encrypt** and turn on **Redirect all HTTP requests to HTTPS**.

The site now opens at `https://example.uz`. In WordPress check under **Settings → General** that both addresses start with `https://`. Details — [SSL certificates](ssl.md).

## 4. Mail (optional)

For an address like `info@example.uz` — **Mail → New domain**, then create a mailbox and add the DNS records (MX, SPF, DKIM, DMARC). Details — [Mail](mail.md).

So that WordPress mail (password resets, orders) arrives, use this mailbox in an SMTP plugin: server — the mail server address, port 587, STARTTLS.

## 5. Automatic backups

1. On the site page open **Backups**.
2. **Automatic backup → Daily**, copies to keep — 7, **Files** and **Databases** ticked.
3. If you can, connect Google Drive or Dropbox in **Settings → Backup servers** and turn sending on for the site.

Details — [Backups](backups.md).

## 6. Speed and security

- **Real cron instead of WP-Cron:** add `define('DISABLE_WP_CRON', true);` to `wp-config.php` and add a task every 5 minutes in the [Scheduler](cron.md): `php /var/www/<user>/data/www/example.uz/wp-cron.php`.
- **Caching:** install Redis in **System → Applications** and use the Redis Object Cache plugin.
- **Large images and plugins:** raise `upload_max_filesize` and `post_max_size` in **Settings → Backend → PHP settings**.
- **Protecting the admin area:** [Login protection](panel-settings.md) and the site’s **request rate limit** cut password-guessing on `wp-admin`; keep WordPress, plugins and themes updated.
- **Virus checks:** use the **Scanning** tile from time to time — [Site security and scanning](site-security.md).
