import nfem
import numpy as np


model = nfem.Model()

model.add_node('A', x=0, y=0, z=0, support='xyz')
model.add_node('B', x=1, y=1, z=0, support='z', fy=-1)
model.add_node('C', x=2, y=0, z=0, support='xyz')

model.add_truss('1', node_a='A', node_b='B', youngs_modulus=1, area=1)
model.add_truss('2', node_a='B', node_b='C', youngs_modulus=1, area=1)

for t in np.linspace(0, 1, 10):
    model.load_factor = t
    model.perform_load_control_step()

model.show()
