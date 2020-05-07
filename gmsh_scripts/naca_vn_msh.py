"""using gmsh generate surface mesh for vn calculation"""
import os
import shutil
from gmsh_scripts import gmsh


# cad_folder = r'/home/hao/ShapeOPT/TestDev2/Vn'
# mesh_folder = r'/home/hao/ShapeOPT/TestDev2/Vn'
def generate_surface_meshes(cad_folder, mesh_folder):
    """function to generate_surface_meshes for all cad files"""
    if os.path.exists(mesh_folder):
        shutil.rmtree(mesh_folder)
    os.mkdir(mesh_folder)
    input_files = []
    output_files = []
    for file in os.listdir(cad_folder):
        if file.endswith(r'.igs'):
            input_files.append(os.path.join(cad_folder, file))
            output_files.append(
                os.path.join(mesh_folder,
                             file.split(r'.')[0] + r'.vtk'))
    NO_PARAM = len(input_files)
    for i in range(NO_PARAM):

        gmsh.initialize()

        gmsh.open(input_files[i])

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

        gmsh.write(output_files[i])

        gmsh.finalize()
