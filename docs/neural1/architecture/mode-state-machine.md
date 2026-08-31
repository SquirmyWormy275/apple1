# Mode state machine

The virtual portal begins in `PORTAL`. `1`, `2`, and `3` enter `COMPUTER`,
`FIELD_LIBRARY`, and `NEURAL1`; `?` enters `ABOUT`; `0` returns to `PORTAL`.
The physical launch adapter is replaceable because CFFA1 boot/launch behavior
is unverified. `COMPUTER` causes no model call and owns no NEURAL1 state.

On future hardware, Reset bypasses this software state and returns to the
ordinary Monitor recovery environment. Animation is optional and skippable;
ordinary Monitor boot must never depend on it.
