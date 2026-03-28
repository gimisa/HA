# ⚡ Hydro-Québec D-rate (HA automation)

This system provides automated energy management for the **Gimisa Ecosystem** during Hydro-Québec high-demand events. It focuses on reducing electrical load while maintaining household comfort through localized intelligence on **HA1**.

## 🏗️ System Logic & Workflow

The architecture follows a three-stage execution pattern to ensure the system is resilient and "security-first."

1. **Monitoring (Python Engine):**
   * The `check_hq.py` script identifies Hydro-Quebec peak periods emails
   * It determines as Hydro communication, it get specific peak type: Morning, Afternoon, or Dual-Peak.

2. **Communication (Bash Bridge):**
   * A Bash script (`check_hq.sh`) acts as the delivery layer.
   * **Email Alert:** Sends a direct notification to the administrator to confirm the peak status.
   * **MQTT Signal:** Publishes the state to the local broker on **HA1** with the **Retain** flag set to `true`.

3. **Execution (HA1 Automation):**
   * Home Assistant triggers a `choose` logic block immediately upon receiving the MQTT signal.
   * **Action:** On a centralised system, it power off the Main thermostat automatically at the proper time period. 
   * **Recovery:** Repower thermostat approprietly at end of period.

---
*Last Updated: March 2026*
