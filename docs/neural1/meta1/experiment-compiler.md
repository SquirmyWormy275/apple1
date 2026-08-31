# Experiment compiler

The compiler produces a stable experiment ID from a question plus factor,
levels, controls, metrics, seeds, analysis, and stopping rule. It rejects fewer
than two levels, empty metrics, or empty seeds. Compiled targets are virtual.
Natural language is only an input convenience; the resulting structured record
is what can be reviewed and executed.
