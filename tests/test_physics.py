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

"""Every URDF loads in the engine the simulator flies, as the file describes it, and its inertias are physical."""

import math
import os
import sys
import tempfile
from collections.abc import Iterator
from xml.etree import ElementTree

import pybullet as p
import pytest

import swarm_description

FLYING = ("cf2x", "interceptor", "m4td", "tello", "swarm_drone")
PARTS = [(name, part) for name in swarm_description.drones() for part in swarm_description.get_params(name)["files"]]
GYM_JOINTS = {"prop0_joint", "prop1_joint", "prop2_joint", "prop3_joint", "center_of_mass_joint"}
POSER_JOINTS = {"gimbal_tilt"} | {f"rotor{i}_{kind}" for i in range(4) for kind in ("spin", "fold0", "fold1")}
WARNING_WORDS = ("warning", "fail", "error", "cannot", "unsupported")
INERTIA = ("ixx", "iyy", "izz", "ixy", "ixz", "iyz")
MOVING_MASS_CAP_KG = 0.001
MOVING_INERTIA_CAP = 1e-7


@pytest.fixture(scope="session")
def client() -> Iterator[int]:
    """One headless physics server for the whole session."""
    cid = p.connect(p.DIRECT)
    yield cid
    p.disconnect(cid)


def _root(name: str, part: str = "body") -> ElementTree.Element:
    """The parsed <robot> element of one URDF."""
    return ElementTree.parse(swarm_description.get_urdf(name, part)).getroot()


def _mass(link: ElementTree.Element) -> float:
    """A link's mass as written, zero when it has no inertial block."""
    mass = link.find("inertial/mass")
    return float(mass.get("value", "0")) if mass is not None else 0.0


def _inertia(link: ElementTree.Element) -> dict[str, float]:
    """A link's six inertia terms as written, zero when it has none."""
    tag = link.find("inertial/inertia")
    return {key: float(tag.get(key, "0")) if tag is not None else 0.0 for key in INERTIA}


def _load(cid: int, path: str) -> tuple[int, str]:
    """Load a URDF and return its body id with everything the engine printed while loading it."""
    sys.stdout.flush()
    saved = os.dup(1)
    with tempfile.TemporaryFile() as out:
        os.dup2(out.fileno(), 1)
        try:
            uid = p.loadURDF(path, flags=p.URDF_USE_INERTIA_FROM_FILE, physicsClientId=cid)
        finally:
            sys.stdout.flush()
            os.dup2(saved, 1)
            os.close(saved)
        out.seek(0)
        return uid, out.read().decode(errors="replace")


@pytest.mark.parametrize(("name", "part"), PARTS)
def test_every_urdf_loads_quietly_as_written(client: int, name: str, part: str) -> None:
    """The engine loads each URDF without a warning, with the masses and joints the file gives."""
    uid, printed = _load(client, swarm_description.get_urdf(name, part))
    assert uid >= 0
    noisy = [line for line in printed.splitlines() if any(word in line.lower() for word in WARNING_WORDS)]
    assert not noisy, f"{name} {part}: {noisy}"
    root = _root(name, part)
    links, joints = root.findall("link"), root.findall("joint")
    count = p.getNumJoints(uid, physicsClientId=client)
    assert count == len(joints)
    loaded = [p.getDynamicsInfo(uid, i, physicsClientId=client)[0] for i in range(-1, count)]
    assert loaded[0] == pytest.approx(_mass(links[0]))
    assert sum(loaded) == pytest.approx(sum(_mass(link) for link in links))


@pytest.mark.parametrize("name", FLYING)
def test_a_flying_body_has_the_gyms_fixed_joints(client: int, name: str) -> None:
    """Each drone body carries the four prop joints and the centre-of-mass joint the gym reads, all fixed."""
    uid, _ = _load(client, swarm_description.get_urdf(name))
    info = [p.getJointInfo(uid, j, physicsClientId=client) for j in range(p.getNumJoints(uid, physicsClientId=client))]
    assert {row[1].decode() for row in info} == GYM_JOINTS
    assert {row[2] for row in info} == {p.JOINT_FIXED}


def test_the_m4td_moving_parts_have_the_joints_the_poser_turns() -> None:
    """The gimbal tilts and each rotor spins and folds, about the joints the patrol poses before each picture."""
    joints = {joint.get("name"): joint.get("type") for joint in _root("m4td", "moving").findall("joint")}
    assert set(joints) == POSER_JOINTS
    assert {joints[name] for name in POSER_JOINTS} <= {"revolute", "continuous"}


@pytest.mark.parametrize("name", FLYING)
def test_a_drone_body_is_physical(name: str) -> None:
    """The main body has mass, a positive inertia diagonal that obeys the triangle inequality, and small cross terms."""
    base = _root(name).findall("link")[0]
    inertia = _inertia(base)
    ixx, iyy, izz = inertia["ixx"], inertia["iyy"], inertia["izz"]
    assert _mass(base) > 0.0 and min(ixx, iyy, izz) > 0.0
    assert ixx + iyy >= izz and ixx + izz >= iyy and iyy + izz >= ixx
    for cross, (a, b) in {"ixy": ("ixx", "iyy"), "ixz": ("ixx", "izz"), "iyz": ("iyy", "izz")}.items():
        assert abs(inertia[cross]) <= min(inertia[a], inertia[b])


@pytest.mark.parametrize("name", FLYING)
def test_the_helper_links_carry_nothing(name: str) -> None:
    """The prop and centre-of-mass links stay massless with zero inertia, as the gym's convention has them."""
    for link in _root(name).findall("link")[1:]:
        assert _mass(link) == 0.0
        assert set(_inertia(link).values()) == {0.0}


def test_the_m4td_moving_parts_stay_negligible() -> None:
    """Every link of the posed parts stays under a token mass and inertia, since nothing simulates them."""
    for link in _root("m4td", "moving").findall("link"):
        assert _mass(link) <= MOVING_MASS_CAP_KG
        assert max(abs(value) for value in _inertia(link).values()) <= MOVING_INERTIA_CAP


@pytest.mark.parametrize("name", FLYING)
def test_the_radius_of_gyration_matches_the_arm(name: str) -> None:
    """The yaw radius of gyration sits between a fifth and twice the arm length, so the inertia is on the right scale."""
    base = _root(name).findall("link")[0]
    gyration = math.sqrt(_inertia(base)["izz"] / _mass(base))
    arm = swarm_description.get_properties(name)["arm"]
    assert 0.2 * arm <= gyration <= 2.0 * arm
