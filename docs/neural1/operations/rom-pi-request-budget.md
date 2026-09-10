# Exact 256-byte Pi request budget

Native Pi 5 acceptance exposed transport failures before the model returned a complete response. These are software qualification failures, not negative scientific results; no response or accepted command was fabricated.

- Run `N1-P-8467772B2C791133`: two-thread requests ended at the former 180-second timeout after approximately 637 and 688 generated tokens. Provider logs recorded cancellation and released inference slots. The subsequent repeated attempt was cancelled through the application.
- Run `N1-P-D5063F9E83B146C9` at revision `df8359d`: one-thread request hit its 420-second timeout with zero completed provider responses and zero accepted commands. Provider logs reached approximately 805 generated tokens; cold loading and prompt evaluation took approximately 100 seconds. Observed generation declined from roughly 3.1 to 1.95 tokens/second; Pi temperatures were approximately 63–67°C, with no throttling flags.

The default is now one generation, one logical participant, one Ollama CPU thread, a 570-second transport bound, and at most 1024 output tokens. The 600-second campaign deadline and independent 75°C resource guard remain enforced. The larger timeout allows for measured cold-start overhead; this adjustment still needs a complete native provider response and strict evaluator qualification. It does not establish that every model output will fit the token or time budget.

Every candidate must still explicitly deposit exactly 256 bytes in the permitted range and pass the existing parser and executable checks. Historical timeout records remain intact. The effective per-run registry records these resource settings without changing the historical source registry.
