"""using gmsh generate surface mesh for vn calculation"""
import gmsh

PARAM_LIST = [
    r'opt_U1', r'opt_U2', r'opt_U3', r'opt_U4', r'opt_U5', r'opt_L1',
    r'opt_L2', r'opt_L3', r'opt_L4', r'opt_L5'
]

for i in range(10):

    gmsh.initialize()

    gmsh.open(r'/home/hao/ShapeOPT/TestDev2/Vn/NACA0012_' + PARAM_LIST[i] +
              r'.igs')

    # gmsh.model.addPhysicalGroup(2, [1], 1)
    # gmsh.model.setPhysicalName(2, 1, r'fluid')
    # gmsh.model.addPhysicalGroup(1, [1, 2], 1)
    # gmsh.model.setPhysicalName(1, 1, r'farfield')
    gmsh.model.addPhysicalGroup(1, [3, 4], 2)
    gmsh.model.setPhysicalName(1, 2, r'airfoil')

    gmsh.model.mesh.setTransfiniteCurve(1, 36)
    gmsh.model.mesh.setTransfiniteCurve(2, 36)
    gmsh.model.mesh.setTransfiniteCurve(3, 120, r'Bump', 0.05)
    gmsh.model.mesh.setTransfiniteCurve(4, 120, r'Bump', 0.05)

    gmsh.model.geo.synchronize()

    gmsh.model.mesh.generate(1)
    gmsh.model.mesh.generate(2)

    gmsh.write(r'/home/hao/ShapeOPT/TestDev2/Vn/NACA0012_' + PARAM_LIST[i] +
               r'.vtk')

    gmsh.finalize()
