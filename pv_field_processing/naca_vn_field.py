"""obtaining design velocity field using mesh files"""
import os
import shutil
import numpy as np

from pv_field_processing import pvfielddata

# mesh_folder = r'/home/hao/ShapeOPT/TestDev2/Vn'
# vn_field_folder = r'/home/hao/ShapeOPT/TestDev2/Vn/Vn_field'

def generate_vn_fields(mesh_folder, vn_field_folder):
    """generate_vn_fields for all mesh files"""
    if os.path.exists(vn_field_folder):
        shutil.rmtree(vn_field_folder)
    os.mkdir(vn_field_folder)
    # found_original_mesh_file = False
    input_files = []
    output_files = []
    for file in os.listdir(mesh_folder):
        if file.endswith(r'original.vtk'):
            mesh_file_original = os.path.join(mesh_folder, file)
            # found_original_mesh_file = True
        elif file.endswith(r'.vtk'):
            input_files.append(os.path.join(mesh_folder, file))
            output_files.append(
                os.path.join(vn_field_folder,
                             file.split(r'.')[0] + r'.vtu'))

    fielddata_original = pvfielddata.FieldDataProcessing(mesh_file_original)
    cell_center_array_original = fielddata_original.GetCellCenters()
    cell_center_array_original = np.array(cell_center_array_original)

    cell_normal_field = fielddata_original.Get1dNormal()
    cell_normal_field = np.array(cell_normal_field)

    NO_PARAM = len(input_files)
    for i in range(NO_PARAM):
        fielddata = pvfielddata.FieldDataProcessing(input_files[i])
        cell_center_array = fielddata.GetCellCenters()
        cell_center_array = np.array(cell_center_array)

        disp_fieldi = cell_center_array - cell_center_array_original

        vn_scalari = []
        vn_vectori = []
        for dispj, normalj in zip(disp_fieldi, cell_normal_field):
            vn_scalarij = np.dot(dispj, normalj)
            vn_vectorij = vn_scalarij * normalj
            vn_scalari.append(vn_scalarij)
            vn_vectori.append(vn_vectorij.tolist())

        updatefield = pvfielddata.AppendFieldPolyData(input_files[i])

        updatefield.AppendScalarField(vn_scalari, 'Vn_Scalar')

        updatefield.AppendVectorField(vn_vectori, 'Vn_Vector')

        updatefield.SavePolyDataField(output_files[i])
