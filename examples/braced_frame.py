import nfem

import numpy as np

from compas_cem.diagrams import TopologyDiagram

from compas_cem.elements import Node
from compas_cem.elements import TrailEdge
from compas_cem.elements import DeviationEdge

from compas_cem.loads import NodeLoad
from compas_cem.supports import NodeSupport

from compas_cem.equilibrium import static_equilibrium

from compas_cem.plotters import TopologyPlotter
from compas_cem.plotters import FormPlotter


# ------------------------------------------------------------------------------
# Data
#-------------------------------------------------------------------------------

nodes = [(0, [0.0, 0.0, 0.0]),
         (1, [0.0, 1.0, 0.0]),
         (2, [1.0, 0.0, 0.0]),
         (3, [1.0, 1.0, 0.0])]

trail_edges = [(0, 1),
               (2, 3)]

deviation_edges = [(1, 3),
                   (0, 3),
                   (2, 1)
                   ]

nodes_support = [0, 2]
nodes_load = [1, 3]

load = [0.0, -1.0, 0.0]

area = 1.0
youngs_modulus = 1.0

non_linear_analysis = True

# ------------------------------------------------------------------------------
# Topology Diagram
# ------------------------------------------------------------------------------

topology = TopologyDiagram()

# ------------------------------------------------------------------------------
# Add Nodes
# ------------------------------------------------------------------------------

for key, point in nodes:
    topology.add_node(Node(key, point))

# ------------------------------------------------------------------------------
# Add Trail Edges
# ------------------------------------------------------------------------------

for u, v in trail_edges:
    topology.add_edge(TrailEdge(u, v, length=-1.0, plane=[[0.0, 0.0, 0.0], [0.0, 1.0, 0.0]]))

# ------------------------------------------------------------------------------
# Add Deviation Edges
# ------------------------------------------------------------------------------

for u, v in deviation_edges:
    topology.add_edge(DeviationEdge(u, v, force=2.5))

# ------------------------------------------------------------------------------
# Set Supports Nodes
# ------------------------------------------------------------------------------

for key in nodes_support:
    topology.add_support(NodeSupport(key))

# ------------------------------------------------------------------------------
# Add Loads
# ------------------------------------------------------------------------------

for key in nodes_load:
    topology.add_load(NodeLoad(key, load))

# ------------------------------------------------------------------------------
# Collect Trails and Edge lines
# ------------------------------------------------------------------------------

edge_lines = [topology.edge_coordinates(*edge) for edge in topology.edges()]

# ------------------------------------------------------------------------------
# Equilibrium of forces
# ------------------------------------------------------------------------------

topology.build_trails()
form = static_equilibrium(topology, eta=1e-6, tmax=100, verbose=True)

for node in form.support_nodes():
    print(node, form.reaction_force(node))

# ------------------------------------------------------------------------------
# Instantiate FEM model
# ------------------------------------------------------------------------------

model = nfem.Model()

# ------------------------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------------------------

for key in form.nodes():

    support = "z"
    if form.node_attribute(key, "type") == "support":
        support = "xyz"

    node_kwargs = {"id": str(key),
                   "x": form.node_attribute(key, "x"),
                   "y": form.node_attribute(key, "y"),
                   "z": form.node_attribute(key, "z"),
                   "fx": form.node_attribute(key, "qx"),
                   "fy": form.node_attribute(key, "qy"),
                   "fz": form.node_attribute(key, "qz"),
                   "support": support
                   }

    model.add_node(**node_kwargs)

# ------------------------------------------------------------------------------
# Add trusses
# ------------------------------------------------------------------------------

for u, v in form.edges():

    truss_kwargs = {"id": f"{u}-{v}",
                    "node_a": str(u),
                    "node_b": str(v),
                    "youngs_modulus": youngs_modulus,
                    "area": area,
                    "prestress": form.edge_force((u, v))
                    }

    model.add_truss(**truss_kwargs)

# ------------------------------------------------------------------------------
# Solve FEA model
# ------------------------------------------------------------------------------

for t in np.linspace(0, 1, 20):
    model.load_factor = t
    if non_linear_analysis:
        model.perform_load_control_step(info=False)
    else:
        model.perform_linear_solution_step()

# ------------------------------------------------------------------------------
# Show FEA model
# ------------------------------------------------------------------------------

model.show()

# ------------------------------------------------------------------------------
# Plot load displacement curves
# ------------------------------------------------------------------------------

plot = nfem.Plot2D()
plot.add_load_displacement_curve(model, dof=('1', 'u'))
plot.add_load_displacement_curve(model, dof=('1', 'v'))
plot.show()
# ------------------------------------------------------------------------------
# Instantiate FEM model
# ------------------------------------------------------------------------------

model = nfem.Model()

# ------------------------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------------------------

for key in form.nodes():

    support = "z"
    if form.node_attribute(key, "type") == "support":
        support = "xyz"

    node_kwargs = {"id": str(key),
                   "x": form.node_attribute(key, "x"),
                   "y": form.node_attribute(key, "y"),
                   "z": form.node_attribute(key, "z"),
                   "fx": form.node_attribute(key, "qx"),
                   "fy": form.node_attribute(key, "qy"),
                   "fz": form.node_attribute(key, "qz"),
                   "support": support
                   }

    model.add_node(**node_kwargs)

# ------------------------------------------------------------------------------
# Add trusses
# ------------------------------------------------------------------------------

for u, v in form.edges():

    truss_kwargs = {"id": f"{u}-{v}",
                    "node_a": str(u),
                    "node_b": str(v),
                    "youngs_modulus": youngs_modulus,
                    "area": area,
                    "prestress": form.edge_force((u, v))
                    }

    model.add_truss(**truss_kwargs)

# ------------------------------------------------------------------------------
# Solve FEA model
# ------------------------------------------------------------------------------

for t in np.linspace(0, 1, 20):
    model.load_factor = t
    model.perform_load_control_step(info=True)

# ------------------------------------------------------------------------------
# Show FEA model
# ------------------------------------------------------------------------------

plot = nfem.Plot2D()
plot.add_load_displacement_curve(model, dof=('1', 'u'))
plot.add_load_displacement_curve(model, dof=('1', 'v'))

plot.show()

model.show()

