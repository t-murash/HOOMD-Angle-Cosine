import hoomd,hoomd.md
import math
import gsd.hoomd
import numpy
import datetime

pi=math.pi
NP=100
snapshot=gsd.hoomd.Snapshot()
snapshot.particles.N=NP
pos=[]
for i in range(NP):
    pos.append([i-NP/2+0.5,0.0,0.0])
snapshot.particles.position=pos
snapshot.particles.types=['A']
snapshot.particles.typeid=[0]*NP
snapshot.configuration.box=[NP,NP,NP,0,0,0]

snapshot.bonds.N=NP-1
snapshot.bonds.types=['A-A']
snapshot.bonds.typeid=[0]*(NP-1)
bonds=[]
for i in range(NP-1):
    bonds.append([i,i+1])
snapshot.bonds.group=bonds

snapshot.angles.N=NP-2
snapshot.angles.types=['A-A-A']
snapshot.angles.typeid=[0]*(NP-2)
angles=[]
for i in range(NP-2):
    angles.append([i,i+1,i+2])
snapshot.angles.group=angles

with gsd.hoomd.open(name='init.gsd',mode='wb') as f:
    f.append(snapshot)

gpu=hoomd.device.GPU()

sim=hoomd.Simulation(device=gpu,seed=1)
sim.create_state_from_gsd(filename='init.gsd')

integrator=hoomd.md.Integrator(dt=0.005)
cell=hoomd.md.nlist.Cell(buffer=0.4)
###
lj=hoomd.md.pair.LJ(nlist=cell);
lj.params[('A','A')]=dict(epsilon=1.0,sigma=1.0)
lj.r_cut[('A','A')]=2.0**(1./6.)
integrator.forces.append(lj)
###
fenewca = hoomd.md.bond.FENEWCA()
fenewca.params['A-A']=dict(k=30.0,r0=1.5,epsilon=1.0,sigma=1.0,delta=0.0)
integrator.forces.append(fenewca)
###
anglecosine = hoomd.md.angle.Cosine()
anglecosine.params['A-A-A']=dict(k=10.0,t0=0.0)
integrator.forces.append(anglecosine)
langevin=hoomd.md.methods.Langevin(filter=hoomd.filter.All(),kT=1.0,default_gamma=0.5)
integrator.methods.append(langevin)
###
sim.operations.integrator=integrator
sim.state.thermalize_particle_momenta(filter=hoomd.filter.All(),kT=1.0)
###
thermodynamic_properties=hoomd.md.compute.ThermodynamicQuantities(filter=hoomd.filter.All())
sim.operations.computes.append(thermodynamic_properties)

class Status():
    def __init__(self,sim):
        self.sim=sim

    @property
    def kinetic_temperature(self):
        try:
            return(thermodynamic_properties.kinetic_temperature)
        except:
            return 0
        
    @property
    def kinetic_energy(self):
        try:
            return(thermodynamic_properties.kinetic_energy)
        except:
            return 0
    
    @property
    def potential_energy(self):
        try:
            return(thermodynamic_properties.potential_energy)
        except:
            return 0

logger=hoomd.logging.Logger(categories=['scalar','string'])
logger.add(sim,quantities=['timestep','tps'])
status=Status(sim)
logger[('Status','kinetic_temperature')]=(status,'kinetic_temperature','scalar')
logger[('Status','kinetic_energy')]=(status,'kinetic_energy','scalar')
logger[('Status','potential_energy')]=(status,'potential_energy','scalar')

table=hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=2000),logger=logger)
sim.operations.writers.append(table)

file=open('log.txt',mode='w',newline='\n')
table_file=hoomd.write.Table(output=file,trigger=hoomd.trigger.Periodic(period=2000),logger=logger)
sim.operations.writers.append(table_file)

gsd_writer=hoomd.write.GSD(filename='test_trajectory.gsd',trigger=hoomd.trigger.Periodic(2000),mode='wb')
sim.operations.writers.append(gsd_writer)

sim.run(2.0e+5);
