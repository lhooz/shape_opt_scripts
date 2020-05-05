import numpy as np
import pvfielddata

inputfile = r'/home/hao/ShapeOPT/TestDev2/surface_adjoint.vtu'
outputfile = r'/home/hao/ShapeOPT/TestDev2/updated_field.vtu'

fielddata = pvfielddata.FieldDataProcessing(inputfile)

CellLength = fielddata.GetLength()

CellSens = fielddata.GetCellSensitivity()

CellPoints = fielddata.GetCellPoints()

CellCenterField = fielddata.GetCellCenters()

updatefield = pvfielddata.AppendFieldPolyData(inputfile)

CellPoints = np.array(CellPoints)

Npoints = len(CellPoints)
CellTangent = np.empty((Npoints, 3))

for i in range(Npoints):
    CellTangent[i - 1] = CellPoints[i] - CellPoints[i - 1]

Rot90 = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

CellNormal = np.empty((Npoints, 3))
for i in range(Npoints):
    CellNormali = np.dot(Rot90, CellTangent[i])
    CellNormal[i] = CellNormali / np.sqrt(np.dot(CellNormali, CellNormali))

# CellSens = np.array(CellSens)[:, np.newaxis]

# Normal = np.array(Normal)

# Sensfield = np.multiply(CellSens, Normal).tolist()
CellNormal = CellNormal.tolist()
updatefield.AppendVectorField(CellNormal, 'Normal')

updatefield.SavePolyDataField(outputfile)
