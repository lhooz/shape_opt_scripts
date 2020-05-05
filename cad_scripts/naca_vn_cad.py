# -*- coding: utf-8 -*-

import catia_app

from win32com.client import Dispatch
FPATH = r'C:/Users/haole/Desktop/EPSRC case files/TestDev2/Vn/NACA0012.CATPart'
PARAM_LIST = [
    r'opt_U1', r'opt_U2', r'opt_U3', r'opt_U4', r'opt_U5', r'opt_L1',
    r'opt_L2', r'opt_L3', r'opt_L4', r'opt_L5'
]

for i in range(10):
    EXPATH = r'C:/Users/haole/Desktop/EPSRC case files/TestDev2/Vn/NACA0012_' + PARAM_LIST[
        i] + r'.igs'

    NEW_PARAM = {PARAM_LIST[i]: '10mm'}

    CATIA = catia_app.CatiaApp()
    CATIA.cadopen(FPATH)

    MFEATURE = catia_app.ManipulateFeature()
    MFEATURE.update_parameters(CATIA.prtobj, NEW_PARAM)

    CATIA.cadexport(EXPATH, 'igs')

    CATIA.cadclose()
