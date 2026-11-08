# Bitcraze Crazyflie 2.x

The default drone: a 27 g quadcopter in X configuration. Both search-and-rescue families fly it, as
did the completed Autopilot families.

| File | What it is |
|---|---|
| `cf2x.urdf` | the flying body, with its physics coefficients in the `<properties>` tag |
| `meshes/cf2.dae` | the body mesh |
| `params.toml` | the hull radius and camera position the simulation uses |

## Sources

- **Upstream**: `cf2x.urdf` and `cf2.dae` come unchanged from
  [gym-pybullet-drones](https://github.com/utiasDSL/gym-pybullet-drones) (MIT), except for the
  mesh path. Its coefficients come from the papers that URDF cites.
- **Set in simulation**: the hull radius and camera position.

The controller is the gym's stock DSL PID, with upstream's gains for this drone.
