# This file is used to automatically test python functions and code in students' work for NB2.

import numpy as np


## First check: Particle class
def check_brownian_particle_class(ParticleClass):

    particle = ParticleClass(
        m=20.0,
        v=[0.0, 0.0],
        r=[1.0, -2.0],
        R=0.5,
        c="red"
    )

    assert particle.m == 20.0, "Incorrect particle mass"
    np.testing.assert_allclose(particle.v, [0.0, 0.0])
    np.testing.assert_allclose(particle.r, [1.0, -2.0])
    assert particle.R == 0.5, "Incorrect particle radius"
    assert particle.c == "red", "Incorrect particle color"

    assert particle.kin_energy == 0.0, "Incorrect kinetic energy"
    np.testing.assert_allclose(particle.momentum, [0.0, 0.0])


## Second check: Collision detection
def check_brownian_collision_detection(ParticleClass):

    test_cases = [
        ([0, 0], 1, [0, 0], 1, True),
        ([0, 0], 1, [1, 0], 1, True),
        ([0, 0], 1, [3, 0], 1, False),
        ([0, 0], 1, [2, 0], 1, False),
        ([0, 0], 2, [2, 0], 1, True),
        ([0, 0], 1, [1, 1], 1, True),
    ]

    for r1, R1, r2, R2, expected in test_cases:

        particle1 = ParticleClass(m=1, v=[0, 0], r=r1, R=R1)
        particle2 = ParticleClass(m=1, v=[0, 0], r=r2, R=R2)

        result = particle1.collide_detection(particle2)

        assert bool(result) == expected, (
            f"Incorrect collision detection for "
            f"r1={r1}, R1={R1}, r2={r2}, R2={R2}. "
            f"Expected {expected}, got {result}."
        )


## Third check: Elastic collisions
def check_brownian_elastic_collision(ParticleClass):

    particle1 = ParticleClass(
        m=1.0, v=[1.0, 0.0], r=[-0.5, 0.0], R=0.5
    )
    particle2 = ParticleClass(
        m=1.0, v=[-1.0, 0.0], r=[0.5, 0.0], R=0.5
    )

    momentum_before = particle1.momentum + particle2.momentum
    energy_before = particle1.kin_energy + particle2.kin_energy

    particle1.particle_collision(particle2)

    momentum_after = particle1.momentum + particle2.momentum
    energy_after = particle1.kin_energy + particle2.kin_energy

    np.testing.assert_allclose(
        momentum_after, momentum_before,
        err_msg="Momentum is not conserved"
    )

    np.testing.assert_allclose(
        energy_after, energy_before,
        err_msg="Kinetic energy is not conserved"
    )

    np.testing.assert_allclose(particle1.v, [-1.0, 0.0])
    np.testing.assert_allclose(particle2.v, [1.0, 0.0])
