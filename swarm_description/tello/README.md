# Ryze Tello

The 87 g indoor drone of the Office Interceptor family, flown through the body-frame stick commands
of the Tello SDK. The family is completed; the drone stays so its champions can still be re-run.

| File | What it is |
|---|---|
| `tello.urdf` | the flying body, with its physics coefficients in the `<properties>` tag |
| `meshes/` | the body, guards and lens meshes |
| `params.toml` | stick-full speeds, motor lag, ground effect, body drag and size, camera position, the telemetry link |

## Sources

- **Tello SDK documentation**: stick-full speed and yaw rate, the state packet rate and its units.
- **The SecureLink Tello dataset**: the telemetry noise figures, calibrated against it (the swarm
  repository's `docs/families/securelink_calibration_summary.json`).
- **Measured on the real Tello**: the camera position, ToF and barometer noise.
- **Tuned in simulation**: motor lag, link delay.

The controller is the gym's stock DSL PID, tuned for the same weight class.

The office family adds its own body drag and ground-effect model on top of the gym's, so
`params.toml` carries `drag_coef` and `ground_effect_coef` beside the URDF's rotor-drag and
ground-effect coefficients: two models, no value repeated.
