# -*- coding: utf-8 -*-

import catia_app

FPATH = r'C:/Users/haole/Desktop/EPSRC case files/TestDev2/Vn/NACA0012.CATPart'
PARAM_LIST = [
    r'original', r'opt_U1_Y', r'opt_U2_Y', r'opt_U3_Y', r'opt_U4_Y',
    r'opt_U5_Y', r'opt_L1_Y', r'opt_L2_Y', r'opt_L3_Y', r'opt_L4_Y',
    r'opt_L5_Y', r'opt_LE_Y',
    r'opt_TE_Y'
]

NO_PARAM = len(PARAM_LIST)

for i in range(NO_PARAM):
    PARAMi = PARAM_LIST[i]
    EXPATH = r'C:/Users/haole/Desktop/EPSRC case files/TestDev2/Vn/NACA0012_' + PARAMi + r'.igs'

    if PARAMi == r'original':
        PARAM_name = PARAM_LIST[i + 1]
        fd_increment = r'0.0001mm'
    else:
        PARAM_name = PARAMi
        fd_increment = r'1mm'

    NEW_PARAM = {PARAM_name: fd_increment}

    CATIA = catia_app.CatiaApp()
    CATIA.cadopen(FPATH)

    MFEATURE = catia_app.ManipulateFeature()
    MFEATURE.update_parameters(CATIA.prtobj, NEW_PARAM)

    CATIA.cadexport(EXPATH, 'igs')

    CATIA.cadclose()
