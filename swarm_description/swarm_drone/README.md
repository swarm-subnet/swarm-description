# Conveyor drone

The drones riding the warehouse conveyor belts. It is scenery: the warehouse loads it with a fixed
base and scales it up, so only its shape and look matter, to the pilots' cameras.

| File | What it is |
|---|---|
| `swarm_drone.urdf` | the cf2 body as a prop, with the mass and coefficients it was first written with |
| `meshes/cf2.dae` | the cf2 mesh from gym-pybullet-drones (MIT), the same file as `cf2x/meshes/cf2.dae` |
| `params.toml` | the URDF it loads; a prop has no other numbers |

## Sources

- **Upstream**: the mesh comes unchanged from
  [gym-pybullet-drones](https://github.com/utiasDSL/gym-pybullet-drones).

It keeps its own copy of `cf2.dae` because every folder is self-contained: the simulator stages
one folder at a time.
