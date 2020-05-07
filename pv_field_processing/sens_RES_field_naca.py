"""obtaining sensitivity residual field for current cad parameters"""
import os
import numpy as np
import pvfielddata

input_vn_folder = r'/home/hao/ShapeOPT/TestDev2/Vn/Vn_field'
input_sens_file = r'/home/hao/ShapeOPT/TestDev2/surface_adjoint.vtk'
output_sens_file = r'/home/hao/ShapeOPT/TestDev2/Sens_RES_Results/sens_RES_field.vtu'

input_field_data = pvfielddata.FieldDataProcessing(input_sens_file)

CellSize = input_field_data.GetLength()
CellSens = input_field_data.GetCellScalarField(r'Surface_Sensitivity')
CellSens = np.array(CellSens)

CellSens_Size = np.multiply(CellSens, np.array(CellSize))

CellNormal = input_field_data.Get1dNormal()
CellNormal = np.array(CellNormal)

input_vn_files = []
for file in os.listdir(input_vn_folder):
    if file.endswith(r'.vtu'):
        input_vn_files.append(os.path.join(input_vn_folder, file))

NO_PARAM = len(input_vn_files)

current_moving_direction = np.zeros(len(CellSens_Size))
for i in range(NO_PARAM):
    vn_field_datai = pvfielddata.FieldDataProcessing(input_vn_files[i])
    vn_fieldi = vn_field_datai.GetCellScalarField(r'Vn_Scalar')
    vn_fieldi = np.array(vn_fieldi)

    weighti = np.dot(CellSens_Size, vn_fieldi)
    # print(input_vn_files[i])
    # print(weighti)
    current_moving_direction += weighti * vn_fieldi

current_moving_direction = current_moving_direction / np.sqrt(
    np.dot(current_moving_direction, current_moving_direction))

sens_residual_field = CellSens - np.dot(
    CellSens, current_moving_direction) * current_moving_direction

"""transforming resulting fields: sens, current_md, sens_res into vector fields"""
sens_vector_field = np.multiply(CellSens[:, np.newaxis], CellNormal).tolist()

current_moving_direction_vector_field = np.multiply(
    current_moving_direction[:, np.newaxis], CellNormal).tolist()
current_moving_direction = current_moving_direction.tolist()

sens_residual_vector_field = np.multiply(sens_residual_field[:, np.newaxis],
                                         CellNormal).tolist()
sens_residual_field = sens_residual_field.tolist()

"""appending resulting fields to outputfile"""
input_file_to_append = pvfielddata.AppendFieldPolyData(input_sens_file)

input_file_to_append.AppendScalarField(current_moving_direction, r'Current_MD')
input_file_to_append.AppendVectorField(current_moving_direction_vector_field,
                                       r'Current_MD_Vector')
input_file_to_append.AppendScalarField(sens_residual_field, r'Sensitivity_RES')
input_file_to_append.AppendVectorField(sens_residual_vector_field,
                                       r'Sensitivity_RES_Vector')

input_file_to_append.AppendVectorField(sens_vector_field,
                                       r'Sensitivity_Vector')

input_file_to_append.SavePolyDataField(output_sens_file)
