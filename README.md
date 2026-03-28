# 🏠 Gimisa Home Automation Ecosystem

A robust, multi-node Home Assistant infrastructure designed for high availability, energy efficiency, and advanced network segmentation.

## 🏗️ System Architecture

The environment utilizes a primary/secondary node strategy to optimize logic processing and physical radio frequency coverage across the property.

* **HA1 (Cerebro):** Central logic engine and primary automation hub.
    * **OS:** Ubuntu 22.04.5 LTS (Ryzen 3 3200G).
    * **Version:** Home Assistant Core 2023.6.1 (venv).
    * **Inventory:** Managing **127 devices** and serving as the central MQTT Broker and ZHA Principal.

* **HA2 (Radio Bridge):** Distributed physical interface acting as a **Remote Home Assistant** node. 
    * **Purpose:** This node extends the system's range and device handling capability by offloading physical radio communication from the main brain.
    * **OS:** Ubuntu 24.04 LTS (Intel Core2 Duo).
    * **Version:** Home Assistant Core 2024.7.3.
    * **Inventory:** Managing **74 physical devices** via ZHA and 433MHz (rtl_433).

* **Networking:** A layered L3 architecture featuring a dedicated DMZ for web services and a private LAN for automation. Remote access is secured via a WireGuard VPN tunnel (Port 51820 UDP).

## 📡 Hardware & Device Inventory

The ecosystem is balanced across two nodes to ensure comprehensive radio coverage and high-availability logic processing throughout the property.

### **HA1 - Primary Node (Cerebro)**

Serving as the central intelligence of the home, **HA1** manages a robust inventory of **127 devices**. It operates on a Ryzen 3 3200G host running Ubuntu 22.04.5 LTS.

* **Coordination:** It acts as the primary ZHA coordinator using a Sonoff Zigbee 3.0 P-Series dongle.
* **Device Ecosystem:** This node handles a high density of SONOFF 01MINIZB switches for lighting and eWeLink sensors for security and environment (motion, leak, and door sensors).
* **Core Services:** HA1 hosts the central Mosquitto MQTT broker and manages critical Modbus RTU connections for real-time energy monitoring.

### **HA2 - Remote Node (Radio Bridge)**

Designed as a strategic range extender, **HA2** manages **74 devices** from an Intel Core2 Duo host running Ubuntu 24.04 LTS.

* **Range Extension:** By acting as a Remote Home Assistant node, it offloads physical device handling and provides a secondary Zigbee mesh via a Sonoff E-Series dongle.
* **Specialized Frequency:** This node is responsible for capturing 433MHz signals (via `rtl_433`), bringing in data from peripheral sensors that are physically distant from the main brain.

### **Custom ESPHome Engineering**

Beyond commercial hardware, I have engineered custom ESPHome solutions to monitor critical home infrastructure:

* **Water Treatment Monitoring (Salt Level)**
    * **Technology:** ESP8266/ESP32 + Ultrasonic Distance Sensor.
    * **Function:** Measures the gap in the brine tank to provide real-time salt levels.
    * **Automation:** Triggers automated "Low Salt" alerts via Telegram and Alexa to ensure continuous water softening.

* **Air Quality & Ventilation Control**
    * **Technology:** PM2.5 and CO2 sensing array.
    * **Function:** Monitors indoor air health and particulate concentration.
    * **Integration:** Tied directly to the central ventilation system to automatically increase air exchange when thresholds ( smoke) are exceeded. Also use in case of fire alarm with central  heating system shut down. 

## ⚡ Key Automations & Logic

* **Hydro-Québec Peak Management:** A custom Python/Bash hybrid system (`check_hq.py`) monitoring "Hi-lo" energy alerts. It automatically triggers heating load shedding for morning (06h), afternoon (16h), or dual-peak scenarios.

* **Radar:** Use in automation as presence detection in conjunction with esp32 indentity confirmation  security states and automation efficiency.

* **Self-Healing Sensors:** Home Assistant sensors use MQTT "Retain" flags to ensure the real state is restored immediately following a system restart.

## 🛡️ Resilience & Maintenance

* **Daily Backups:** Automated daily incremental backups managed via **Dirvish**.

* **Recovery Policy:** A strict "Restoration Priority" philosophy—restoring from a known stable backup is prioritized over deep debugging of corrupted configurations.

* **Standardized Nomenclature:** All entities follow a French descriptive naming convention (e.g., `switch.prise_lampe_gigi`).

---

*Maintained by Gimisa — 2026*
