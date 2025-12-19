#!/usr/bin/env python3
"""
HOOMD-blue v6 test script for Cosine angle force
Simplified version without GSD dependency
"""
import hoomd
import hoomd.md
import numpy as np

# Simulation parameters
NP = 100
timesteps = 10000  # Reduced from 200000 for quick test

# Create CPU device (can be changed to GPU if available)
device = hoomd.device.CPU()

# Create simulation
sim = hoomd.Simulation(device=device, seed=1)

# Create initial configuration - linear chain of particles
spacing = 1.0
snapshot = hoomd.Snapshot(device.communicator)

if device.communicator.rank == 0:
    snapshot.configuration.box = [NP, NP, NP, 0, 0, 0]
    snapshot.particles.N = NP
    snapshot.particles.types = ['A']

    # Position particles in a line
    positions = []
    for i in range(NP):
        positions.append([i - NP/2 + 0.5, 0.0, 0.0])
    snapshot.particles.position[:] = positions
    snapshot.particles.typeid[:] = [0] * NP

    # Create bonds
    snapshot.bonds.N = NP - 1
    snapshot.bonds.types = ['A-A']
    bonds = []
    for i in range(NP - 1):
        bonds.append([i, i + 1])
    snapshot.bonds.group[:] = bonds
    snapshot.bonds.typeid[:] = [0] * (NP - 1)

    # Create angles
    snapshot.angles.N = NP - 2
    snapshot.angles.types = ['A-A-A']
    angles = []
    for i in range(NP - 2):
        angles.append([i, i + 1, i + 2])
    snapshot.angles.group[:] = angles
    snapshot.angles.typeid[:] = [0] * (NP - 2)

sim.create_state_from_snapshot(snapshot)

# Set up integrator
integrator = hoomd.md.Integrator(dt=0.005)

# Neighbor list
cell = hoomd.md.nlist.Cell(buffer=0.4)

# LJ pair potential
lj = hoomd.md.pair.LJ(nlist=cell)
lj.params[('A', 'A')] = dict(epsilon=1.0, sigma=1.0)
lj.r_cut[('A', 'A')] = 2.0**(1.0/6.0)
integrator.forces.append(lj)

# FENEWCA bond potential
fenewca = hoomd.md.bond.FENEWCA()
fenewca.params['A-A'] = dict(k=30.0, r0=1.5, epsilon=1.0, sigma=1.0, delta=0.0)
integrator.forces.append(fenewca)

# Cosine angle potential - THIS IS THE NEW FEATURE
anglecosine = hoomd.md.angle.Cosine()
anglecosine.params['A-A-A'] = dict(k=10.0, t0=0.0)
integrator.forces.append(anglecosine)

# Langevin thermostat
langevin = hoomd.md.methods.Langevin(filter=hoomd.filter.All(), kT=1.0)
langevin.gamma.default = 0.5
integrator.methods.append(langevin)

# Add integrator to simulation
sim.operations.integrator = integrator

# Thermalize initial velocities
sim.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=1.0)

# Set up thermodynamic properties logger
thermodynamic_properties = hoomd.md.compute.ThermodynamicQuantities(
    filter=hoomd.filter.All()
)
sim.operations.computes.append(thermodynamic_properties)

# Custom status logger
class Status:
    def __init__(self, sim):
        self.sim = sim

    @property
    def kinetic_temperature(self):
        try:
            return thermodynamic_properties.kinetic_temperature
        except:
            return 0

    @property
    def kinetic_energy(self):
        try:
            return thermodynamic_properties.kinetic_energy
        except:
            return 0

    @property
    def potential_energy(self):
        try:
            return thermodynamic_properties.potential_energy
        except:
            return 0

# Set up logging
logger = hoomd.logging.Logger(categories=['scalar', 'string'])
logger.add(sim, quantities=['timestep', 'tps'])
status = Status(sim)
logger[('Status', 'kinetic_temperature')] = (status, 'kinetic_temperature', 'scalar')
logger[('Status', 'kinetic_energy')] = (status, 'kinetic_energy', 'scalar')
logger[('Status', 'potential_energy')] = (status, 'potential_energy', 'scalar')

# Console output
table = hoomd.write.Table(
    trigger=hoomd.trigger.Periodic(period=1000),
    logger=logger
)
sim.operations.writers.append(table)

# GSD write
gsd_writer = hoomd.write.GSD(
    trigger=hoomd.trigger.Periodic(1000), # every 1000 steps
    filename="trajectory.gsd",
    mode='ab' # append mode
)
sim.operations.writers.append(gsd_writer)


# File output
with open('status.txt', mode='w', newline='\n') as file:
    table_file = hoomd.write.Table(
        output=file,
        trigger=hoomd.trigger.Periodic(period=1000),
        logger=logger
    )
    sim.operations.writers.append(table_file)

    print(f"\n{'='*60}")
    print("HOOMD-blue v6 - Cosine Angle Force Test")
    print(f"{'='*60}")
    print(f"Number of particles: {NP}")
    print(f"Number of bonds: {NP-1}")
    print(f"Number of angles: {NP-2}")
    print(f"Timesteps: {timesteps}")
    print(f"Device: {device.__class__.__name__}")
    print(f"{'='*60}\n")

    # Run simulation
    sim.run(timesteps)

    print(f"\n{'='*60}")
    print("Simulation completed successfully!")
    print(f"{'='*60}")
    print(f"Final temperature: {thermodynamic_properties.kinetic_temperature:.3f}")
    print(f"Final potential energy: {thermodynamic_properties.potential_energy:.3f}")
    print(f"Final kinetic energy: {thermodynamic_properties.kinetic_energy:.3f}")
    print(f"{'='*60}\n")
