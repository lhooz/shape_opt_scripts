import numpy as np
import pvfielddata

inputfile = r'/home/hao/gdrive/EPSRC case files/Onera M6/surface_adjoint.vtu'
outputfile = r'/home/hao/gdrive/EPSRC case files/Onera M6/sens_vec_field.vtp'

fielddata = pvfielddata.FieldDataProcessing(inputfile)

Area = fielddata.GetArea()

CellSens = fielddata.GetCellSensitivity()

CellPoints = fielddata.GetCellPoints()

CellCenterField = fielddata.GetCellCenters()

Normal = fielddata.GetNormal()

# print(Normal)

updatefield = pvfielddata.AppendFieldPolyData(inputfile)

# upfatefield.AppendScalarField(Area, 'area')

# upfatefield.AppendScalarField(CellSens, 'cell_sens_field')

# upfatefield.AppendVectorField(CellCenterField, 'cell_center_field')

# upfatefield.AppendVectorField(Normal, 'unit_normal_field')

CellSens = np.array(CellSens)[:, np.newaxis]

Normal = np.array(Normal)

Sensfield = np.multiply(CellSens, Normal).tolist()

updatefield.AppendVectorField(Sensfield, 'sens_vec_field')

updatefield.SavePolyDataField(outputfile)
