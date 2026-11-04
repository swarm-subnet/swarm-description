# The MIT License (MIT)
# Copyright © 2026 Swarm

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Every drone the Swarm simulator flies, one folder each.

A folder holds the drone's URDFs, the meshes they draw with, and a params.toml with
the numbers the URDF cannot carry: motor limits, controller gains, sensor specs.
Everything the gym parses (mass, inertia, thrust, rotor drag, ground effect) stays
in the URDF, where the simulator reads it, so no value is written twice.
"""

import tomllib
from importlib.resources import files
from typing import Any
from xml.etree import ElementTree

__version__ = "1.0.0"

_ROOT = files(__name__)
PARAMS_FILE = "params.toml"


def drones() -> list[str]:
    """Names of every drone in the package, sorted."""
    return sorted(entry.name for entry in _ROOT.iterdir() if entry.is_dir() and (entry / PARAMS_FILE).is_file())


def drone_dir(name: str) -> str:
    """Absolute path of one drone's folder; raises KeyError for a drone the package does not have."""
    folder = _ROOT / name
    if not (folder / PARAMS_FILE).is_file():
        raise KeyError(f"no drone named {name!r}; the package has {', '.join(drones())}")
    return str(folder)


def get_params(name: str) -> dict[str, Any]:
    """A fresh copy of one drone's params.toml as nested dicts, in file order."""
    drone_dir(name)
    with (_ROOT / name / PARAMS_FILE).open("rb") as handle:
        return tomllib.load(handle)


def get_urdf(name: str, part: str = "body") -> str:
    """Absolute path of one of a drone's URDFs, named by its [files] entry: the flying body unless told otherwise."""
    entries = get_params(name)["files"]
    if part not in entries:
        raise KeyError(f"{name} has no {part!r} URDF; it has {', '.join(entries)}")
    return str(_ROOT / name / entries[part])


def get_properties(name: str, part: str = "body") -> dict[str, float]:
    """The <properties> numbers of a drone's URDF (arm, kf, km, prop_radius, drag...), as the simulator parses them."""
    tag = ElementTree.parse(get_urdf(name, part)).getroot().find("properties")
    if tag is None:
        raise KeyError(f"{name}'s {part} URDF has no <properties> tag")
    return {key: float(value) for key, value in tag.attrib.items()}
