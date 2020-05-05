# -*- coding: utf-8 -*-

import catia_app

from win32com.client import Dispatch
FPATH = r'C:/Users/haole/Desktop/EPSRC case files/TestDev2/Vn/NACA0012.CATPart'

EXPATH = r'C:/Users/haole/Desktop/EPSRC case files/TestDev2/Vn/NACA0012.igs'

NEW_PARAM = {r'opt_U1': r'0mm'}

CATIA = catia_app.CatiaApp()
CATIA.cadopen(FPATH)

MFEATURE = catia_app.ManipulateFeature()
MFEATURE.update_parameters(CATIA.prtobj, NEW_PARAM)

CATIA.cadexport(EXPATH, 'igs')

CATIA.cadclose()
