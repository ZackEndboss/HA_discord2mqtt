
# Home Assistant Add-on: Borgmatic
![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]

![Current version][version]

Based on [BorgBackup by yeah (Jan)](https://github.com/yeah/hassio-borg_backup/tree/master/borg_backup)

## Summary

This Add-on backup the contents of `/backup` to a remote [Borg Backup](https://www.borgbackup.org/) server.
The Pre-Version of this addon is using borg only - in second step it will be transform into borgmatic

## Installation

Add this repository's URL as an Add-on repo to your Hassio via Supervisor → Add-on store → Repositories.

## Configuration

The following configuration options are available:

```yaml
user: u123456
host: u123456.your-storagebox.de
port: 23
path: ./borg/my-hassio-server
archive: hassio
passphrase: a secret passphrase
prune_options: '--keep-daily=8 --keep-weekly=5 --keep-monthly=13'
```

## First run

When the Add-On runs for the first time, it will display an SSH public key like this:

```
[15:15:00] INFO: A public/private key pair was generated for you.
[15:15:00] NOTICE: Please use this public key on the backup server:
[15:15:00] NOTICE: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHRHnaf0uiRPxVYKJ8PcfK5GJLz/omuZYS5627v1+U0i hassio
[15:15:00] INFO: Trying to initialize the Borg repository.
```

You will have to **copy this key** to the server's `./ssh/authorized_keys` file.


## Usage

Run this Add-on whenever you would like to upload your backups to the Borg server. Here's an automation that achieves this:

```yaml
- alias: Upload snapshots to Borg
  id: upload_snapshots_to_borg
  trigger:
  - platform: time_pattern
    hours: '5'
    minutes: '0'
    seconds: '0'
  action:
  - service: hassio.addon_start
    data:
      # your add-on identifier will differ from this one
      # find it as part of the add-on URL in
      # Supervisor -> Add-ons
      addon: abcdef01_borg_backup
```

Please note that this Add-on does not trigger Hassio snapshots. You will have to do this manually or create an automation for it like so:

```yaml
- alias: Create Snapshot
  id: create_snapshot
  trigger:
  - platform: time_pattern
    hours: '3'
    minutes: '0'
    seconds: '0'
  action:
  - service: hassio.snapshot_full
```

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[version]: https://img.shields.io/badge/version-v1.0.2-blue.svg