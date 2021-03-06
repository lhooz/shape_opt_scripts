"""
module for processing sensivity data field
using paraview vtk field data manipulator
"""

import csv
import numpy as np
from paraview.simple import XMLUnstructuredGridReader, XMLPolyDataReader, LegacyVTKReader, SaveData, servermanager
from paraview.simple import ExtractSurface, CellSize, CellCenters, GenerateSurfaceNormals, PointDatatoCellData, CellDatatoPointData, ProgrammableFilter


class FieldDataProcessing:
    """geometric processing for input field data: obtaining cell areas and unit normal field"""
    def __init__(self, inputfile):
        """open input field data"""
        importsuccess = True

        if inputfile.endswith(r'.vtp'):
            FDATA = XMLPolyDataReader(FileName=[inputfile])
        elif inputfile.endswith(r'.vtu'):
            FDATA = XMLUnstructuredGridReader(FileName=[inputfile])
        elif inputfile.endswith(r'vtk'):
            temp_F = LegacyVTKReader(FileNames=[inputfile])
            SaveData(r'/home/hao/.PVFieldData/input_vtk_to_vtu.vtu',
                     proxy=temp_F)
            FDATA = XMLUnstructuredGridReader(
                FileName=[r'/home/hao/.PVFieldData/input_vtk_to_vtu.vtu'])
        else:
            print(r'Err: file cannot be opened:  ' + inputfile)
            importsuccess = False

        if importsuccess is True:
            self.f_data_in = ExtractSurface(Input=FDATA)

    def GetLength(self):
        """get cell length field for 2d meshes"""
        CELLSIZE = CellSize(Input=self.f_data_in)

        CELLDATA = servermanager.Fetch(CELLSIZE)
        NOFCELLS = CELLDATA.GetNumberOfCells()
        CDATA = CELLDATA.GetCellData()

        LENGTH = []
        for i in range(NOFCELLS):
            LENGTH.append(CDATA.GetArray('Length').GetValue(i))
        return LENGTH

    def GetArea(self):
        """get cell area field"""
        CELLSIZE = CellSize(Input=self.f_data_in)

        CELLDATA = servermanager.Fetch(CELLSIZE)
        NOFCELLS = CELLDATA.GetNumberOfCells()
        CDATA = CELLDATA.GetCellData()

        AREA = []
        for i in range(NOFCELLS):
            AREA.append(CDATA.GetArray('Area').GetValue(i))
        return AREA

    def GetCellScalarField(self, scalar_field_name):
        """get scalar field for cells"""
        PTOCELL = PointDatatoCellData(Input=self.f_data_in)

        CELLDATA = servermanager.Fetch(PTOCELL)
        NOFCELLS = CELLDATA.GetNumberOfCells()
        CDATA = CELLDATA.GetCellData()

        Sfield = []
        for i in range(NOFCELLS):
            Sfield.append(CDATA.GetArray(scalar_field_name).GetValue(i))
        return Sfield

    def GetCellVectorField(self, vector_field_name):
        """get vector field for cells"""
        PTOCELL = PointDatatoCellData(Input=self.f_data_in)

        CELLDATA = servermanager.Fetch(PTOCELL)
        NOFCELLS = CELLDATA.GetNumberOfCells()
        CDATA = CELLDATA.GetCellData()

        Vfieldi = []
        Vfield = []
        for i in range(NOFCELLS):
            Vfieldi = [
                CDATA.GetArray(vector_field_name).GetTuple(i)[0],
                CDATA.GetArray(vector_field_name).GetTuple(i)[1],
                CDATA.GetArray(vector_field_name).GetTuple(i)[2]
            ]
            Vfield.append(Vfieldi)
        return Vfield

    def GetCellPoints(self):
        """get point coordinates in cell vortices order"""
        POINTDATA = servermanager.Fetch(self.f_data_in)
        NOFPOINTS = POINTDATA.GetNumberOfPoints()

        Pointi = []
        Points = []
        for i in range(NOFPOINTS):
            Pointi = [
                POINTDATA.GetPoint(i)[0],
                POINTDATA.GetPoint(i)[1],
                POINTDATA.GetPoint(i)[2]
            ]
            Points.append(Pointi)
        return Points

    def GetCellCenters(self):
        """get cell center coordinates"""
        CELLCENTER = CellCenters(Input=self.f_data_in)

        POINTDATA = servermanager.Fetch(CELLCENTER)
        NOFPOINTS = POINTDATA.GetNumberOfPoints()

        CellCenteri = []
        CellCenter = []
        for i in range(NOFPOINTS):
            CellCenteri = [
                POINTDATA.GetPoint(i)[0],
                POINTDATA.GetPoint(i)[1],
                POINTDATA.GetPoint(i)[2]
            ]
            CellCenter.append(CellCenteri)
        return CellCenter

    def Get2dNormal(self):
        """get unit normal field for 2d surfaces"""
        FACENORMALFIELD = GenerateSurfaceNormals(Input=self.f_data_in)
        FACENORMALFIELD.ComputeCellNormals = 1

        CELLDATA = servermanager.Fetch(FACENORMALFIELD)
        NOFCELLS = CELLDATA.GetNumberOfCells()
        CDATA = CELLDATA.GetCellData()

        Normali = []
        Normal = []
        for i in range(NOFCELLS):
            Normali = [
                CDATA.GetArray('Normals').GetTuple(i)[0],
                CDATA.GetArray('Normals').GetTuple(i)[1],
                CDATA.GetArray('Normals').GetTuple(i)[2]
            ]
            Normal.append(Normali)
        return Normal

    def Get1dNormal(self):
        """get unit normal field for 1d curves"""
        CellPoints = self.GetCellPoints()
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

        CellNormal = CellNormal.tolist()
        return CellNormal


class AppendFieldPolyData:
    """append new field data to a given data field"""
    def __init__(self, inputfile):
        """open input field data"""
        self.inputfile = inputfile
        importsuccess = True

        if self.inputfile.endswith('.vtp'):
            FDATA = XMLPolyDataReader(FileName=[inputfile])
        elif self.inputfile.endswith('.vtu'):
            FDATA = XMLUnstructuredGridReader(FileName=[inputfile])
        elif inputfile.endswith(r'vtk'):
            temp_F = LegacyVTKReader(FileNames=[inputfile])
            SaveData(r'/home/hao/.PVFieldData/input_vtk_to_vtu.vtu',
                     proxy=temp_F)
            FDATA = XMLUnstructuredGridReader(
                FileName=[r'/home/hao/.PVFieldData/input_vtk_to_vtu.vtu'])
        else:
            print(r'Err: file cannot be opened:  ' + inputfile)
            importsuccess = False

        if importsuccess is True:
            self.f_data_in = FDATA

    def AppendScalarField(self, field_data, field_name):
        """append scalar field to file"""
        NAMETOTXT = open(r'/home/hao/.PVFieldData/field_name.txt', 'w')
        DATATOCSV = open(r'/home/hao/.PVFieldData/field_data.csv', 'w')

        with NAMETOTXT:
            NAMETOTXT.write(field_name)

        with DATATOCSV:
            writer = csv.writer(DATATOCSV)
            writer.writerows(map(lambda x: [x], field_data))

        INSERTDATA = ProgrammableFilter(Input=self.f_data_in)

        INSERTDATA.Script = """import csv
fname = open(\'/home/hao/.PVFieldData/field_name.txt\', \'r\')
with fname:
    field_name = fname.readline()
 
fdata = open(\'/home/hao/.PVFieldData/field_data.csv\', \'r\')
int_field=[]
with fdata:
     reader = csv.reader(fdata)
     for row in reader:
         for e in row:
             int_field.append(float(e))
  
polydata = output
array = vtk.vtkDoubleArray()
array.SetNumberOfComponents(1)
array.SetName(field_name)
for i in range(polydata .GetNumberOfCells()):
    array.InsertNextValue(int_field[i])
polydata.GetCellData().AddArray(array)"""

        INSERTDATA.RequestInformationScript = ''
        INSERTDATA.RequestUpdateExtentScript = ''
        INSERTDATA.CopyArrays = 1
        INSERTDATA.PythonPath = ''

        if self.inputfile.endswith(r'.vtp'):
            SaveData(r'/home/hao/.PVFieldData/temp_field_data.vtp',
                     proxy=INSERTDATA)
            self.f_data_in = AppendFieldPolyData(
                r'/home/hao/.PVFieldData/temp_field_data.vtp').f_data_in
        elif self.inputfile.endswith(r'.vtu') or self.inputfile.endswith(r'.vtk'):
            SaveData(r'/home/hao/.PVFieldData/temp_field_data.vtu',
                     proxy=INSERTDATA)
            self.f_data_in = AppendFieldPolyData(
                r'/home/hao/.PVFieldData/temp_field_data.vtu').f_data_in

    def AppendVectorField(self, field_data, field_name):
        """append scalar field to file"""
        NAMETOTXT = open(r'/home/hao/.PVFieldData/field_name.txt', 'w')
        DATATOCSV = open(r'/home/hao/.PVFieldData/field_data.csv', 'w')

        with NAMETOTXT:
            NAMETOTXT.write(field_name)

        with DATATOCSV:
            writer = csv.writer(DATATOCSV)
            writer.writerows(field_data)

        INSERTDATA = ProgrammableFilter(Input=self.f_data_in)

        INSERTDATA.Script = """import csv
fname = open(\'/home/hao/.PVFieldData/field_name.txt\', \'r\')
with fname:
    field_name = fname.readline()
 
fdata = open(\'/home/hao/.PVFieldData/field_data.csv\', \'r\')
int_field=[]
with fdata:
     reader = csv.reader(fdata)
     for row in reader:
         int_field.append([float(row[0]),float(row[1]),float(row[2])])
  
polydata = output
array = vtk.vtkDoubleArray()
array.SetNumberOfComponents(3)
array.SetName(field_name)
for i in range(polydata .GetNumberOfCells()):
    array.InsertNextTuple(int_field[i])
polydata.GetCellData().AddArray(array)"""

        INSERTDATA.RequestInformationScript = ''
        INSERTDATA.RequestUpdateExtentScript = ''
        INSERTDATA.CopyArrays = 1
        INSERTDATA.PythonPath = ''

        if self.inputfile.endswith(r'.vtp'):
            SaveData(r'/home/hao/.PVFieldData/temp_field_data.vtp',
                     proxy=INSERTDATA)
            self.f_data_in = AppendFieldPolyData(
                r'/home/hao/.PVFieldData/temp_field_data.vtp').f_data_in
        elif self.inputfile.endswith(r'.vtu') or self.inputfile.endswith(r'.vtk'):
            SaveData(r'/home/hao/.PVFieldData/temp_field_data.vtu',
                     proxy=INSERTDATA)
            self.f_data_in = AppendFieldPolyData(
                r'/home/hao/.PVFieldData/temp_field_data.vtu').f_data_in

    def SavePolyDataField(self, outputfile):
        """save appended poly data field"""
        CELLTOP = CellDatatoPointData(Input=self.f_data_in)
        CELLTOP.PassCellData = 1

        if self.inputfile.endswith(r'.vtp'):
            SaveData(outputfile.split(r'.')[0] + r'.vtp', proxy=CELLTOP)
        elif self.inputfile.endswith(r'.vtu') or self.inputfile.endswith(r'.vtk'):
            SaveData(outputfile.split(r'.')[0] + r'.vtu', proxy=CELLTOP)
