# Updates and notifications

## Automatic updates

Updates are managed in **Settings → Automatic updates** (administrator only).

- **Accept updates automatically** — when on, the panel updates itself as soon as a new version is out.
- **Schedule**: when on, you choose when updates are checked and installed — every day or every 2–7 days, hour and minutes (AM/PM). The time is in the server’s time zone; the section shows the server’s current time and the next update time.
- **What’s new**: the button in the update notice and the list in the section show what changed in the versions not installed yet.
- It is **off by default**: when a new version is out, the notice `{version} Update available` with an **Update** button appears at the top right of the screen. Pressing it updates the panel and reopens the page in the new version. The notice stays until you update; once the panel is on the latest version it goes away.
- The section also shows the installed version and the available update, with an **Update** button too.

How it works:

- The server checks for a new version **every 6 hours**. A check also starts when an administrator signs in to the panel.
- The new version is downloaded from livepanel.uz and its **digital signature** and checksum are verified — an unsigned or altered package is never installed.
- After installing, the panel checks that it works; if there is a problem, it **rolls back to the previous version automatically** and shows “The update failed”.
- Sites keep working during the update.

The current version is shown at the bottom of the sign-in page and of the left menu (e.g. `2026.11.25`).

To check for a new version right away, run on the server:

```bash
systemctl start livepanel-update.service
```

> Updates work while the license is active.

## Email notifications

The panel emails you about important events from **push@livepanel.uz**. Messages go to the account’s **recovery email** ([Panel settings and security](panel-settings.md)) in the language the user chose in the panel. The same event is not mailed again and again.

| Event | To |
|---|---|
| Sign-in to the account from a new IP address | the account owner |
| The disk is more than 90% full | the administrator |
| A server service stopped (Nginx, MySQL, PHP-FPM and others) | the administrator |
| An SSL certificate has less than 14 days left | the site owner and the administrator |
| An account was blocked for its RAM limit | the account owner and the administrator |

If no mail arrives, check that the recovery email is set and look in the Spam folder.
