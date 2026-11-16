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

"""Every drone folder ships what it promises: its params, its URDFs, the meshes they draw with, and readable
properties. Standard library only, like the rest of these tests."""

import re
from pathlib import Path

import pytest

import swarm_description

DRONES = ("cf2x", "dock3", "interceptor", "m4td", "swarm_drone", "tello")
FLYING = ("cf2x", "interceptor", "m4td", "swarm_drone", "tello")
MESH = re.compile(r'filename="\./(meshes/[^"]+)"')


def test_the_package_lists_every_drone() -> None:
    """The loader finds exactly the drone folders the package ships."""
    assert swarm_description.drones() == list(DRONES)


@pytest.mark.parametrize("name", DRONES)
def test_each_drone_has_its_params_urdfs_and_readme(name: str) -> None:
    """Every drone has a README, a params file, and every URDF its params name."""
    folder = Path(swarm_description.drone_dir(name))
    assert (folder / "README.md").is_file()
    files = swarm_description.get_params(name)["files"]
    assert "body" in files
    for part in files:
        assert Path(swarm_description.get_urdf(name, part)).is_file()


@pytest.mark.parametrize("name", DRONES)
def test_every_mesh_a_urdf_draws_with_is_shipped(name: str) -> None:
    """Each ./meshes/ file a drone's URDFs reference exists in that drone's folder."""
    folder = Path(swarm_description.drone_dir(name))
    for part in swarm_description.get_params(name)["files"]:
        text = Path(swarm_description.get_urdf(name, part)).read_text(encoding="utf-8")
        for mesh in MESH.findall(text):
            assert (folder / mesh).is_file(), f"{name} {part} draws with missing {mesh}"


@pytest.mark.parametrize("name", FLYING)
def test_the_flying_body_carries_its_physics(name: str) -> None:
    """The flying body's URDF has the coefficients the simulator parses, all positive where they must be."""
    props = swarm_description.get_properties(name)
    for key in ("arm", "kf", "km", "thrust2weight", "prop_radius"):
        assert props[key] > 0.0


def test_urdf_names_are_unique_across_drones() -> None:
    """No two drones share a URDF file name, since the simulator stages and looks them up by name."""
    names = [file for name in DRONES for file in swarm_description.get_params(name)["files"].values()]
    assert len(names) == len(set(names))


def test_an_unknown_drone_or_part_is_refused_by_name() -> None:
    """Asking for a drone or URDF that does not exist raises KeyError naming what does."""
    with pytest.raises(KeyError, match="m4td"):
        swarm_description.get_params("phantom")
    with pytest.raises(KeyError, match="moving"):
        swarm_description.get_urdf("m4td", "landing_gear")


def test_a_urdf_without_properties_is_refused(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """A URDF with no <properties> tag raises KeyError instead of returning empty physics."""
    bare = tmp_path / "bare.urdf"
    bare.write_text('<robot name="bare"><link name="base"/></robot>', encoding="utf-8")
    monkeypatch.setattr(swarm_description, "get_urdf", lambda name, part="body": str(bare))
    with pytest.raises(KeyError, match="no <properties>"):
        swarm_description.get_properties("cf2x")


def test_params_come_back_as_a_fresh_copy() -> None:
    """Changing the params one caller got never changes what the next caller reads."""
    first = swarm_description.get_params("m4td")
    first["motors"]["max_rpm"] = 0.0
    assert swarm_description.get_params("m4td")["motors"]["max_rpm"] == 6300.0
