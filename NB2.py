# This file is used to automatically test python functions and code in students' work for NB2.

import numpy as np


## First check: ParticleClass
def check_brownian_particle_class(ParticleClass):
    p = ParticleClass(
        m=20.0,
        v=[0.0, 0.0],
        r=[1.0, -2.0],
        R=0.5,
        c="red"
    )

    assert p.m == 20.0
    np.testing.assert_allclose(p.v, [0.0, 0.0])
    np.testing.assert_allclose(p.r, [1.0, -2.0])
    assert p.R == 0.5
    assert p.c == "red"
    assert p.kin_energy == 0.0
    np.testing.assert_allclose(p.momentum, [0.0, 0.0])


## Second check: Collision detection
def check_brownian_collision_detection(collide_detection):
    class FakeParticle:
        def __init__(self, position, radius):
            self.r = np.array(position, dtype=float)
            self.R = radius

    test_cases = [
        ([0, 0], 1, [0, 0], 1, True),
        ([0, 0], 1, [1, 0], 1, True),
        ([0, 0], 1, [3, 0], 1, False),
        ([0, 0], 1, [2, 0], 1, False),
        ([0, 0], 2, [2, 0], 1, True),
        ([0, 0], 1, [1, 1], 1, True),
    ]

    for r1, R1, r2, R2, expected in test_cases:
        p1 = FakeParticle(r1, R1)
        p2 = FakeParticle(r2, R2)

        result = collide_detection(p1, p2)

        assert bool(result) == expected, (
            f"Collision detection failed for {r1}, {r2}: "
            f"expected {expected}, got {result}"
        )


## Third check: Elastic collision
def check_brownian_elastic_collision(particle_collision):
    class FakeParticle:
        def __init__(self, m, v, r):
            self.m = m
            self.v = np.array(v, dtype=float)
            self.r = np.array(r, dtype=float)

    p1 = FakeParticle(1.0, [1.0, 0.0], [-0.5, 0.0])
    p2 = FakeParticle(1.0, [-1.0, 0.0], [0.5, 0.0])

    momentum_before = p1.m * p1.v + p2.m * p2.v
    energy_before = (
        0.5 * p1.m * np.dot(p1.v, p1.v)
        + 0.5 * p2.m * np.dot(p2.v, p2.v)
    )

    particle_collision(p1, p2)

    momentum_after = p1.m * p1.v + p2.m * p2.v
    energy_after = (
        0.5 * p1.m * np.dot(p1.v, p1.v)
        + 0.5 * p2.m * np.dot(p2.v, p2.v)
    )

    np.testing.assert_allclose(momentum_after, momentum_before)
    np.testing.assert_allclose(energy_after, energy_before)
    np.testing.assert_allclose(p1.v, [-1.0, 0.0])
    np.testing.assert_allclose(p2.v, [1.0, 0.0])
