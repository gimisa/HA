# 🛠️ Technical Implementation: Hydro-Québec Automation

This document details the scripts and security configurations required to run the Hivelo peak detection on **HA1**.

## 🔐 1. Yahoo Mail Security Configuration
To allow `check_hq.py` to access the inbox, a standard login is insufficient. You must:
1. Log into your email account security settings.
2. Generate a unique **"App Password"** specifically for this script.
3. Replace the password in the script with this 16-character code.
4. Ensure IMAP access is enabled for the account.

## 🐍 2. Python Engine (`check_hq.py`)
This script uses `imaplib` to scan for emails from "hydroquebec" received today.
* **Mode DRY_RUN:** Set to `True` for testing (scans 48h and blocks MQTT). Set to `False` for production.
* **Logic:** It uses RegEx to find specific time markers (`6 h` or `16 h`) within the email body to determine the peak type.

## 🐚 3. Bash Bridge (`alerte_hq_mqtt.sh`)
The Python script calls this Bash script to interface with the MQTT broker on HA1.
* **Topic Structure:** `courriel/hydroquebec/{sensor}_filesize`.
* **Counter Logic:** Instead of a simple ON/OFF, it increments a value. This allows Home Assistant to trigger an automation every time a new "increment" is detected, even if the state was already "ON".
* **Reset Feature:** Running with the `reset` argument clears all sensors back to `0`.

## 🤖 4. MQTT Broker Integration (HA1)
The scripts target `127.0.0.1` (localhost) using the following credentials:
* **User:** `mosquito user`.
* **Port:** Standard MQTT Port (1883).
* **Retain Flag:** Enabled to ensure HA1 remembers the peak status after a reboot.

---
*Note: Ensure both scripts have execution permissions (`chmod +x`) on the HA1 filesystem.*
