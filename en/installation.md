# Installation

LivePanel is installed on a clean server with one command, usually in 5–10 minutes.

## Requirements

| | Minimum | Recommended |
|---|---|---|
| Operating system | **Ubuntu 22.04 LTS**, freshly installed | Ubuntu 22.04 LTS |
| CPU | 1 vCPU, x86_64 | 2 vCPU or more |
| Memory | 1 GB | 2 GB or more |
| Disk | 10 GB | 20 GB or more (SSD) |
| Access | root or sudo | — |
| Network | a public IP address | — |

Ports that must be open: **80** and **443** (sites and Let’s Encrypt), **6563** (the panel), **22** (SSH). For mail also 25, 465, 587, 993 and 995.

> The server must not have another panel (cPanel, Plesk, ISPmanager, etc.) or existing Nginx/Apache configuration. A clean server is the most reliable way to a smooth installation.

## 1. Connect to the server

Connect from your computer over SSH (PowerShell or PuTTY on Windows, Terminal on macOS and Linux):

```bash
ssh root@SERVER_IP
```

## 2. Run the installer

```bash
curl -fsSL https://livepanel.uz/install.sh | sudo bash
```

The script runs these steps and shows each one on the screen:

1. downloads the LivePanel package and **checks its signature and checksum**;
2. installs the panel;
3. installs Nginx and PHP 8.1-FPM;
4. installs MySQL 8 and phpMyAdmin;
5. installs the FTP/SFTP server (ProFTPD);
6. installs the Let’s Encrypt client (certbot) and Node.js LTS;
7. starts the hosting agent.

## 3. Save the sign-in details

At the end you see:

```text
LivePanel is ready

  Address:   https://SERVER_IP:6563
  Login:     liveadmin
  Password:  ************

  Save this password now: it is shown only once and is not stored.
```

**Save the password right away** — it is shown only once and is not kept on the server. If it is lost, set a new one on the server:

```bash
livepanel passwd liveadmin
```

The installation log is in `/var/log/livepanel-install.log`.

## 4. Open the panel

Open `https://SERVER_IP:6563` in the browser. At first the panel uses a certificate it made itself (self-signed), so the browser warns that the connection is not secure — choose **Advanced → Proceed**. Later you can give the panel a trusted certificate or a domain: [Panel address and SSL](panel-access.md).

Sign in as `liveadmin` with the saved password — [First sign-in and the interface](first-login.md).

## Removing the panel

To remove LivePanel and everything it installed, run on the server:

```bash
livepanel remove
```

Other server commands — [Server commands](console.md).

> This also deletes the sites, databases and mail. Make backups of anything you need first.

## Troubleshooting

- **“Ubuntu 22.04 LTS is required”** — another OS is installed. Reinstall the server with Ubuntu 22.04.
- **The panel does not open** — port 6563 may be closed in your provider’s external firewall. Open it in the provider’s control panel.
- **The installation stopped** — check the end of `/var/log/livepanel-install.log` and run the command again.
