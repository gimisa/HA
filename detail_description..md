# 🏠 GiMiSa Home Ecosystem: Distributed Multi-Instance Architecture

**Advanced Home Automation Strategy** | *Architect: gimisa | *Established 2022*

---

## 🏗️ System Overview
My ecosystem is built on **Home Assistant**, prioritizing local privacy and high-availability control. It has evolved into a robust, multi-layer L3 network architecture across three distinct instances to provide total coverage for the property.

### 📊 Real-Time System Scale
| Metric | Count |
| :--- | :--- |
| **Total Devices** | 127 (Distributed HA1 + HA2) |
| **Total Automations** | 145 (Intelligence & Logic layers) |
| **Total Entities** | 1,360 (Sensors, Switches, & Data points) |

---

## 🚀 Future Roadmap: HA3 (Ollama Intelligence)
The next evolution is **HA3**, a dedicated instance for local Large Language Models (LLM).
* **Hardware:** Ubuntu 26.04 LTS on an 8-core AMD FX hardware profile.
* **Role:** Dedicated **Ollama** services for dynamic AI logic and complex voice/messaging automation.
* **Connectivity:** Integrated via **Remote Home Assistant** for seamless logic coordination.

---

## 📍 Instance HA1: The Central Brain
HA1 serves as the primary controller, MQTT broker, and automation engine.
* **Hardware:** Ubuntu 22.04.5 LTS / Ryzen 3 3200G / 21GB RAM.
* **Key Integrations:** * **Premium Appliances:** Miele (Washer/Dryer), Husqvarna (Automower), LG TV Notifications.
    * **Voice Architecture:** Alexa speakers utilized for house-wide and outdoor messaging.
* **Resilience:** Daily incremental backups using **Dirvish**.

## 📍 Instance HA2: Radio & Perimeter Bridge
HA2 acts as the physical interface for high-density radio protocols.
* **Role:** Handles **Zigbee Home Automation (ZHA)** and **rtl_433** sensors.
* **Zigbee Backbone:** **15+ specialized repeaters** create a dense mesh for 100% signal integrity across the entire property.
* **Communication:** Forwards data to HA1 via **Mosquitto MQTT** and **Remote Home Assistant**.

---

## 🛡️ Security & Remote Access
A zero-cloud-dependency security model ensures maximum privacy:
* **Custom Routing:** Secured via **Graped.ca** redirection for the `gimisa.ca` domain.
* **Encrypted Tunnel:** Mobile access is secured via a **WireGuard VPN** (wg0) hosted on HA1, utilizing NAT/MASQUERADE for secure LAN routing.
* **Network Strategy:** Multi-layered L3 setup with isolated segments for DMZ (Web), Private LAN (Home), and Guest Wi-Fi.

## ⚡ Flagship Project: Hydro-Québec (HQ) Energy Manager
* **Objective:** Automated response to Hydro-Québec peak demand (Hilo) emails alerts.
* **Action:** AI-assisted Python engine triggers "Economy Mode"—automatically shedding electrical loads to maximize savings.

---

## 🛡️ Operational Rigor (GiMiSa Protocol)
1. **Logic Before Code:** Every automation is planned in plain language before implementation.
2. **SSH Host Validation:** Mandatory check of the system prompt to prevent target host confusion.
3. **Visibility Axiom:** No changes are made without real-time log validation (tcpdump or HA Debugger).

---
*Architecture verified via HA.system.description.yaml. Powered by Gemini 3.0 & AI Studio 2.5 Pro.*
