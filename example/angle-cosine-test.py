import hoomd,hoomd.md
import math
pi=math.pi
hoomd.context.initialize("--mode=gpu")
NP=100
snapshot=hoomd.data.make_snapshot(N=NP,
                                  box=hoomd.data.boxdim(Lx=NP,Ly=NP,Lz=NP),
                                  particle_types=['A'],
                                  bond_types=['B'],
                                  angle_types=['C'])

for i in range(NP):
    snapshot.particles.typeid[i]=0;
    snapshot.particles.position[i,0]=i-NP/2+0.5;
    snapshot.particles.position[i,1]=0.0;
    snapshot.particles.position[i,2]=0.0;

snapshot.bonds.resize(NP-1);
for i in range(NP-1):
    snapshot.bonds.group[i,0]=i;
    snapshot.bonds.group[i,1]=i+1;

snapshot.angles.resize(NP-2);
for i in range(NP-2):
    snapshot.angles.group[i,0]=i;
    snapshot.angles.group[i,1]=i+1;
    snapshot.angles.group[i,2]=i+2;

hoomd.init.read_snapshot(snapshot);

nl=hoomd.md.nlist.cell();

lj=hoomd.md.pair.lj(r_cut=2.0**(1.0/6.0), nlist=nl);
lj.pair_coeff.set('A', 'A', epsilon=1.0, sigma=1.0, r_cut=2.0**(1.0/6.0));
nl.reset_exclusions(exclusions = []);

fene = hoomd.md.bond.fene()
fene.bond_coeff.set('B', k=30.0, r0=1.5, sigma=1.0, epsilon=1.0)

angle = hoomd.md.angle.cosine()
angle.angle_coeff.set('C', k=1.0, t0=0.0)

hoomd.md.integrate.mode_standard(dt=0.005);
all = hoomd.group.all();

integrator=hoomd.md.integrate.langevin(group=all, kT=1.0, seed=5, dscale=0.5);

log=hoomd.analyze.log(filename="log-output.log",
                      quantities=['time', 'potential_energy', 'temperature'],
                      period=2e3,
                      overwrite=True);
dump=hoomd.dump.gsd("trajectory.gsd", period=2e3, group=all, overwrite=True);

hoomd.run(2e5,profile=True);
