# -*- coding: utf-8 -*-

import catia_app

FPATH = r'C:\Users\haole\Desktop\EPSRC case files\NACA_spline_test\NACA0012.CATPart'
PARAM_LIST = [
    'original', 'up1', 'up2', 'up3', 'up4', 'up5', 'up6', 'up7', 'up8', 'up9',
    'up10', 'dp1', 'dp2', 'dp3', 'dp4', 'dp5', 'dp6', 'dp7', 'dp8', 'dp9',
    'dp10'
]

NO_PARAM = len(PARAM_LIST)

for i in range(NO_PARAM):
    PARAMi = PARAM_LIST[i]
    EXPATH = r'C:\Users\haole\Desktop\EPSRC case files\NACA_spline_test\NACA0012_' + PARAMi + r'_x.igs'

    if PARAMi == 'original':
        PARAM_name = 'Part1\\PartBody\\' + PARAM_LIST[i + 6] + '\\X'
        fd_increment = '0.0001mm'
    else:
        PARAM_name = 'Part1\\PartBody\\' + PARAMi + '\\X'
        fd_increment = '0.1mm'

    NEW_PARAM = {PARAM_name: fd_increment}

    CATIA = catia_app.CatiaApp()
    CATIA.cadopen(FPATH)

    MFEATURE = catia_app.ManipulateFeature()
    MFEATURE.update_parameters(CATIA.prtobj, NEW_PARAM)

    CATIA.cadexport(EXPATH, 'igs')

    CATIA.cadclose()
