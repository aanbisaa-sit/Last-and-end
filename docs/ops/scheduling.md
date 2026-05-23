# Scheduling

Scheduling should remain outside the core check logic. Cron, systemd timers, hosted runners, or a later internal loop can all call the same command-line entrypoint.
