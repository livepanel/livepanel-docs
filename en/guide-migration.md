# Moving a site from another host

In this guide we move a PHP + MySQL site from another host or panel (cPanel, ISPmanager, Plesk and others) to LivePanel — without taking the site down.

## 1. Take a copy from the old host

1. **Files:** download the site folder (`public_html`, `httpdocs` or similar) as a **ZIP or tar.gz** archive.
2. **Database:** in phpMyAdmin use **Export → SQL** (or `mysqldump`) — a `.sql` or `.sql.gz` file.
3. Note the database name, user and table prefix from the site’s config file (`wp-config.php` in WordPress, `.env` in Laravel).

## 2. Create the site in LivePanel

1. **Sites → Create site → PHP**.
2. Domain — the same as the old site. Pick the **PHP version** the old host used, or the closest one.
3. Turn on the **Database** card to create a MySQL database, or create it later in **Databases**. Save the password.

The domain still points to the old server — that is fine: visitors keep seeing the old site until the new one is ready.

## 3. Upload the files

![File manager](../images/files.png)

1. Open the **Files** tile and go into `www/<domain>`.
2. Delete the panel’s starter `index.php` / `index.html`.
3. Upload the archive (up to 2 GB) and **Extract** it into this folder.
4. If the files stayed in a folder inside the archive (e.g. `public_html/`), move them one level up.

For large sites FTP/SFTP is handier — [FTP, SFTP and SSH](ftp-ssh.md).

## 4. Import the database

![Import](../images/database-import.png)

1. **Databases** → your database’s menu → **Import (.sql)**.
2. Choose the `.sql` or `.sql.gz` file (up to 2 GB).

`DEFINER`s from the other server are cleaned automatically, and views and triggers move to the new database user. Details — [Databases](databases.md).

## 5. Update the settings

Write the new database details in the site’s config file:

| | Value |
|---|---|
| Host | `localhost` |
| Database name, user, password | the ones created in step 2 |

- **WordPress:** `wp-config.php` → `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`.
- **Laravel:** `.env` → `DB_*`; then `php artisan config:clear` in the [Terminal](terminal.md).

> In **Laravel and Symfony** projects only the `public/` folder may be open to visitors. For that, create the site in step 2 with **CMS / Framework → PHP → Framework → Laravel** (or Symfony) — the panel sets the web root to the project’s `public/` folder. Then replace the installed sample project with your files (`.env` and `storage/` too).

## 6. Check before switching DNS

Add a temporary line to your computer’s `hosts` file (Windows: `C:\Windows\System32\drivers\etc\hosts`, macOS/Linux: `/etc/hosts`):

```text
NEW_SERVER_IP  example.uz www.example.uz
```

Open `http://example.uz` in the browser and check that the site works on the new server. On errors — **Logs → Error log**. When done, remove the line from `hosts`.

## 7. Switch DNS to the new server

1. Change the domain’s A records (`@` and `www`) to the new server IP.
2. Wait for it to spread (up to a few hours). If new orders or comments land on the old site meanwhile, you may need to move the database once more — if you can, put the old site into “maintenance” mode during the move.
3. When DNS points to the new server — get an [SSL certificate](ssl.md).
4. Turn on [automatic backups](backups.md).

## 8. Mail

Mailboxes on the old host do not move by themselves. Create the mailboxes on the new server ([Mail](mail.md)), change the MX record, and drag old messages from one mailbox to the other over IMAP in a mail app.

Keep the old host for a week or two — close it once you are sure everything works.
