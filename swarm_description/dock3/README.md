# DJI Dock 3

The station Swarm Sentinel's Matrice 4TD takes off from and lands in: a body with two lids that
swing open, and DJI's landing pad inside it.

| File | What it is |
|---|---|
| `dock3.urdf` | the body and its two lids on hinges fitted to DJI's closed and open sizes, a solid the aircraft can hit |
| `dock3_pad.urdf` | the landing pad, the only part where a landing counts |
| `meshes/` | the visual meshes of both bodies, from DJI's CAD |
| `params.toml` | closed and open sizes, the concrete base, the lids' travel time, the aircraft's resting height |

## Sources

- **DJI specifications and installation manual**: the closed and open sizes, the concrete base.
- **DJI CAD**: the meshes and the aircraft's resting height on the pad.
- **DJI's footage**: the time the lids take to move.

Both bodies load with a fixed base and no mass, so there is no `<properties>` tag. How the dock is
placed and when it opens stay in the Solar Patrol family.
