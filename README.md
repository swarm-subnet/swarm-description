<a id="readme-top"></a>

<p align="center">
  <img src="https://raw.githubusercontent.com/swarm-subnet/swarm/main/swarm/assets/Swarm_2.png" alt="Swarm" width="62%" />
</p>

<h1 align="center">Swarm Description</h1>

<p align="center">
  <b>Every drone a Swarm pilot flies, one folder each.</b><br/>
  <i>The URDFs, the meshes and the parameters the simulator loads, released by tag.</i>
</p>

<p align="center">
  <a href="https://discord.gg/8dPqPDw7GC"><img alt="Discord" src="https://img.shields.io/badge/Discord-Join-5865F2?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://x.com/SwarmSubnet"><img alt="X" src="https://img.shields.io/badge/X-Follow-111111?style=flat-square&logo=x&logoColor=white" /></a>
  <a href="https://swarm124.com"><img alt="Website" src="https://img.shields.io/badge/swarm124.com-visit-F5D400?style=flat-square&labelColor=111111" /></a>
</p>

---

<!-- ABOUT -->
## What Is This Repository

[Swarm](https://swarm124.com) is Bittensor subnet 124: an open arena where anyone can train a drone
pilot and prove it against the world. This repository is the single place that says what each of
those drones is: its shape, its physics, its motors, its controller and its sensors.

The simulator in the [swarm](https://github.com/swarm-subnet/swarm) repository installs this one as
a Python package, pinned to a release tag. The worlds the drones fly through live in
[swarm-worlds](https://github.com/swarm-subnet/swarm-worlds).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- DRONES -->
## The Drones

| Drone | Folder | Flown in |
|---|---|---|
| **DJI Matrice 4TD** | `m4td/` | Swarm Sentinel (Solar Patrol) |
| **Bitcraze Crazyflie 2.x** | `cf2x/` | Search and Rescue, Swarm Search and Rescue |
| **Ryze Tello** | `tello/` | Office Interceptor (completed, kept for re-runs) |
| **36 cm interceptor** | `interceptor/` | Interceptor (completed, kept for re-runs) |

Each folder's README says where its numbers come from.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- LAYOUT -->
## Layout

```
swarm_description/
  <drone>/
    README.md        where the drone's specs come from
    <drone>.urdf     the flying body: shape, mass, inertia and the coefficients in its <properties> tag
    meshes/          the files the URDFs draw with, referenced as ./meshes/<file>
    params.toml      every number the URDF cannot hold, each with its source
tests/               checks that every drone ships its params, URDFs, meshes and physics
```

**Each value is written once.** Everything the gym parses (mass, inertia, arm length, prop radius,
thrust, torque, rotor drag, ground effect and downwash coefficients) lives in the URDF, because that
is where the simulator reads it. `params.toml` holds the rest: motor limits, controller gains,
camera and sensor specs, link timings, and the coefficients of any force model a family adds on
top of the gym's. A value carries its source beside it: the maker's spec, CAD, a measurement, or
tuned in simulation.

Only the aircraft lives here. How a family uses it (mission rules, scoring, what a pilot observes)
stays in the family's code.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- USING -->
## Using It

```python
import swarm_description

swarm_description.drones()                    # ['cf2x', 'interceptor', 'm4td', 'tello']
swarm_description.get_urdf("m4td")            # .../m4td/m4td.urdf, the flying body
swarm_description.get_urdf("m4td", "moving")  # .../m4td/m4td_moving.urdf, any URDF named in [files]
swarm_description.get_params("m4td")          # params.toml as nested dicts, a fresh copy each call
swarm_description.get_properties("tello")     # the URDF's <properties> numbers: kf, km, prop_radius...
```

The swarm repository pins a tagged release in its `requirements.txt`:

```
swarm-description @ git+https://github.com/swarm-subnet/swarm-description.git@v1.0.0
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- ADDING -->
## Adding a Drone

1. Make `swarm_description/<drone>/` with the flying body as a URDF. Its `<properties>` tag carries
   the physics coefficients the gym parses; its meshes go in `meshes/`, referenced as
   `./meshes/<file>`.
2. Write `params.toml`. A `[files]` table names every URDF, `body` first; the other tables hold the
   numbers the URDF cannot, each with its source in a comment.
3. Write the folder's `README.md`: what the drone is and where its specs come from.
4. Add the name to `DRONES` in `tests/test_drones.py`, then run the checks below.

A drone added here flies nowhere yet. A family picks its drone in the swarm repository by name:
it stages it with `gym_assets.stage_drone("<drone>")` and reads its numbers with
`swarm_description.get_params("<drone>")`. A drone that flies with the stock DSL PID controller needs
nothing more; one that needs its own controller adds that controller to the family.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- CHANGING -->
## Changing a Drone

1. Open a pull request here. CI installs the built wheel and checks every drone folder.
2. Bump `__version__` in `swarm_description/__init__.py`, add the release to `CHANGELOG.md`, and tag
   the merge commit with the same number (`v1.1.0`).
3. Bump the tag in the swarm repository's `requirements.txt`, refresh its `pixi.lock`, and bump the
   swarm version. A drone change changes flight results, so it follows the same release rules as a
   scoring change.

```bash
uv sync --group dev
uv run pytest
uv run pre-commit run --all-files
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- LICENSE -->
## License

The package is distributed under the MIT License, see [LICENSE](LICENSE). `cf2x/cf2x.urdf` and the
`cf2.dae` mesh come from [gym-pybullet-drones](https://github.com/utiasDSL/gym-pybullet-drones),
also MIT licensed.
