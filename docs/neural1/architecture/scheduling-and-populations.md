# Scheduling and populations

The deterministic scheduler orders logical agent IDs, derives per-turn seeds
from run seed and round, and routes each turn through its selected provider and
the shared WozMon world. Each agent owns a separate context list even when all
share one model backend. Provider rotation changes only an explicit key.

Migration copies a named address range and records both colonies and the exact
payload hash. Archaeology records byte-identification and structural inference
scores. Newcomer records separate turns-to-protocol, message, routine use, and
compatible contribution plus failures. Summary statistics retain count, mean,
standard deviation, range, and empty-data state.
