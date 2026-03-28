# ⚡ Hydro-Québec D-rate (HA automation)

This system provides automated energy management for the **Gimisa Ecosystem** during Hydro-Québec high-demand events. It focuses on reducing electrical load while maintaining household comfort through localized intelligence on **HA1**.

## 🏗️ System Architecture & Workflow

The architecture follows a three-stage execution pattern to ensure the system is resilient and "security-first."

1. **Monitoring (Python Engine):**
   * The `check_hq.py` script monitors your Yahoo inbox for official Hydro-Québec alert emails.
   * It analyzes the email body using RegEx to identify specific peak periods: Morning (**6h**) or Afternoon (**16h**).

2. **Communication (Bash Bridge):**
   * A Bash script (`alerte_hq_mqtt.sh`) acts as the delivery layer.
   * **Email Alert:** It confirms the peak status to the administrator via email.
   * **MQTT Signal:** It increments a specialized "filesize" sensor on the local **HA1** broker with the **Retain** flag set to `true` to ensure the state survives reboots.

3. **Execution (HA1 Automation):**
   * Home Assistant triggers a `choose` logic block immediately upon receiving the incremental MQTT signal.
   * **Action:** On this centralized system, it automatically powers off the main thermostat or reduces the setpoint at the exact start of the peak period.
   * **Recovery:** Restores power and original temperature setpoints appropriately once the peak period concludes.

---
*Last Updated: March 2026*
