# 36 cm interceptor

The cf2x drawn and flown at three times its size, for the Interceptor family. The family is
completed; the drone stays so its champion can still be re-run.

| File | What it is |
|---|---|
| `interceptor_drone.urdf` | the cf2x scaled by three: mass with the cube of the scale, inertia with its fifth power |
| `meshes/cf2.dae` | the cf2 mesh, drawn three times larger |
| `params.toml` | the scale and the controller gains sized for the larger body |

## Sources

- **Derived from cf2x**: the URDF's physics, scaled.
- **Tuned in simulation**: the DSL PID gains.
