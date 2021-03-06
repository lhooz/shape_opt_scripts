"""obtaining sensitivity residual field for current cad parameters"""
import os
import numpy as np
from pv_field_processing import pvfielddata

# vn_field_folder = r'/home/hao/ShapeOPT/TestDev2/Vn/Vn_field'
# input_sens_file = r'/home/hao/ShapeOPT/TestDev2/surface_adjoint.vtk'
# output_sens_file = r'/home/hao/ShapeOPT/TestDev2/Sens_RES_Results/sens_RES_field.vtu'


def generate_sens_RES_field(vn_field_folder, input_sens_file,
                            output_sens_file):
    """generate_sens_RES_field for current cad parameters"""
    input_field_data = pvfielddata.FieldDataProcessing(input_sens_file)

    CellSize = input_field_data.GetLength()
    CellSens = input_field_data.GetCellScalarField(r'Surface_Sensitivity')
    CellSens = np.array(CellSens)

    CellNormal = input_field_data.Get1dNormal()
    CellNormal = np.array(CellNormal)

    # CellCenter = input_field_data.GetCellCenters()

    input_vn_files = []
    for file in os.listdir(vn_field_folder):
        if file.endswith(r'.vtu'):
            input_vn_files.append(os.path.join(vn_field_folder, file))

    NO_PARAM = len(input_vn_files)

    # test_weights = [1, -1, 0]

    current_moving_direction = np.zeros(len(CellSens))
    for i in range(NO_PARAM):
        vn_field_datai = pvfielddata.FieldDataProcessing(input_vn_files[i])
        vn_fieldi = vn_field_datai.GetCellScalarField(r'Vn_Scalar')
        vn_fieldi = np.array(vn_fieldi)

        weighti = np.dot(np.multiply(CellSens, np.array(CellSize)), vn_fieldi)
        # weighti = test_weights[i]
        # print(input_vn_files[i])
        print(input_vn_files[i].split(r'/')[-1].split('.')[0] + r'_weight =',
              weighti)
        current_moving_direction += weighti * vn_fieldi

    current_moving_direction = current_moving_direction / np.sqrt(
        np.dot(current_moving_direction,
               np.multiply(current_moving_direction, np.array(CellSize))))
    current_moving_direction = np.dot(
        CellSens, np.multiply(current_moving_direction,
                              np.array(CellSize))) * current_moving_direction

    sens_residual_field = CellSens - current_moving_direction

# transforming resulting fields: sens, current_md, sens_res into vector fields
    sens_vector_field = np.multiply(CellSens[:, np.newaxis],
                                    CellNormal).tolist()

    current_moving_direction_vector_field = np.multiply(
        current_moving_direction[:, np.newaxis], CellNormal).tolist()
    current_moving_direction = current_moving_direction.tolist()

    sens_residual_vector_field = np.multiply(
        sens_residual_field[:, np.newaxis], CellNormal).tolist()
    sens_residual_field = sens_residual_field.tolist()

    CellSens = CellSens.tolist()

# appending resulting fields to outputfile
    input_file_to_append = pvfielddata.AppendFieldPolyData(input_sens_file)

    input_file_to_append.AppendScalarField(current_moving_direction,
                                           r'Current_MD')
    input_file_to_append.AppendVectorField(
        current_moving_direction_vector_field, r'Current_MD_Vector')
    input_file_to_append.AppendScalarField(sens_residual_field,
                                           r'Sensitivity_RES')
    input_file_to_append.AppendVectorField(sens_residual_vector_field,
                                           r'Sensitivity_RES_Vector')

    input_file_to_append.AppendScalarField(CellSens,
                                           r'Surface_Sensitivity_Cell')
    input_file_to_append.AppendVectorField(sens_vector_field,
                                           r'Sensitivity_Vector')

    input_file_to_append.SavePolyDataField(output_sens_file)
