# ⚡ Hydro-Québec Peak Management (Hivelo)

This system provides automated energy management for the **Gimisa Ecosystem** during Hydro-Québec high-demand events. It focuses on reducing electrical load while maintaining household comfort through localized intelligence on **HA1**.

## 🏗️ System Logic & Workflow

The architecture follows a three-stage execution pattern to ensure the system is resilient and "security-first."

1. **Monitoring (Python Engine):**
   * The `check_hq.py` script identifies peak periods: Morning (**06:00–09:00**) and Afternoon (**16:00–20:00**).
   * It determines the specific peak type: Morning, Afternoon, or Dual-Peak.

2. **Communication (Bash Bridge):**
   * A Bash script (`check_hq.sh`) acts as the delivery layer.
   * **Email Alert:** Sends a direct notification to the administrator to confirm the peak status.
   * **MQTT Signal:** Publishes the state to the local broker on **HA1** with the **Retain** flag set to `true`.

3. **Execution (HA1 Automation):**
   * Home Assistant triggers a `choose` logic block immediately upon receiving the MQTT signal.
   * **Action:** Automatically adjusts all thermostats to a lower setpoint (e.g., 17°C or 18°C) and disables high-draw appliances like water heaters.
   * **Recovery:** Restores all comfort settings (e.g., 21°C) once the peak event concludes.

---
*Last Updated: March 2026*
