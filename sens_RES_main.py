"""main script to control sensitivity manipulation workflow:
    cad (.igs) --> mesh (.vtk) --> vn (.vtu) --> sens_RES (.vtu)"""

from gmsh_scripts import naca_vn_msh
from pv_field_processing import naca_vn_field
from pv_field_processing import sens_RES_field_naca

cad_folder = r'/home/hao/ShapeOPT/TestDev2/Vn/Vn_cad'
mesh_folder = r'/home/hao/ShapeOPT/TestDev2/Vn/Vn_mesh'
vn_field_folder = r'/home/hao/ShapeOPT/TestDev2/Vn/Vn_field'

input_sens_file = r'/home/hao/ShapeOPT/TestDev2/CFD/surface_adjoint.vtk'
output_sens_file = r'/home/hao/ShapeOPT/TestDev2/Sens_RES_Results/sens_RES_field.vtu'

naca_vn_msh.generate_surface_meshes(cad_folder, mesh_folder)

naca_vn_field.generate_vn_fields(mesh_folder, vn_field_folder)

sens_RES_field_naca.generate_sens_RES_field(vn_field_folder, input_sens_file,
                                            output_sens_file)
