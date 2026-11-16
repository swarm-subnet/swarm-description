# DJI Matrice 4TD

The aircraft of Swarm Sentinel (Solar Patrol): a 1,850 g enterprise quadcopter with a wide, two zoom
and a thermal camera on a 3-axis gimbal, a laser rangefinder, and a dock it takes off from and lands in.

| File | What it is |
|---|---|
| `m4td.urdf` | the flying body: the real outline as its collision shape (dome, fuselage, feet, gull-wing arms, motor pods), thrust at the CAD motor positions |
| `m4td_moving.urdf` | the parts that move on the real aircraft but not in its physics: four rotors with folding blades and the gimbal head, with no collision |
| `meshes/` | the visual meshes of both bodies, from DJI's CAD |
| `params.toml` | motors, tilt limit, controller gains, gimbal and sensor positions, cameras, laser, downward sensor, RTK accuracy, link delays, surface heat |

## Sources

- **DJI specifications and manual**: rotor speed, tilt limit in Normal mode, hover time, camera fields
  of view, lenses and ISO, laser range and accuracy, downward vision range, RTK hovering accuracy,
  link delays, blade folding in the dock.
- **DJI CAD**: motor positions, gimbal pivot, camera glass and laser window positions, the outline.
- **Tuned in simulation**: idle rotor speed and the controller gains, on the patrol's physics.
- **Estimates**: surface temperatures (motor rise measured in flight, arXiv 1906.04152), camera read
  noise and the stream's noise reduction.

Each value in `params.toml` carries its own source beside it.
