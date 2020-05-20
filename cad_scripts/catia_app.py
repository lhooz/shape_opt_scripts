# -*- coding: utf-8 -*-

import os
import time
from win32com.client import Dispatch


class CatiaApp:
    """Opend catia COM object at specified path"""
    def __init__(self):
        self.catia = Dispatch('CATIA.Application')
        self.docs = self.catia.Documents
        try:
            self.prtobj = self.catia.ActiveDocument.Part
        except:
            print(
                r"No existing cad file open, use cadopen to launch cad file in specified path"
            )

    def cadopen(self, filepath):
        """Open catia file at file path"""
        cadfile = os.path.abspath(filepath)

        if not os.path.isfile(cadfile):
            raise FileNotFoundError(f'Could not find file {cadfile}.')

        self.docs.Open(cadfile)
        self.prtobj = self.catia.ActiveDocument.Part

    def cadexport(self, expath, cadformat):
        """export cad file at specified path"""
        outcadfile = os.path.abspath(expath)

        self.catia.ActiveDocument.ExportData(outcadfile, cadformat)

    def cadclose(self):
        self.catia.Quit()
        time.sleep(2)


class ManipulateFeature:
    """Manipulate cad features in opened cad part"""
    def __init__(self):
        self.non_updated_parameters = {}

    def update_parameters(self, prtobj, new_parameters):
        """update cad parameters using the data within the dictionary: new_parameters"""
        for k, value in new_parameters.items():
            try:
                pitem = prtobj.Parameters.Item(k)
                if not pitem.OptionalRelation is None:
                    pitem.OptionalRelation.Modify(value)
                else:
                    pitem.ValuateFromString(value)
            except:
                self.non_updated_parameters[k] = value

        prtobj.Update()

        updated_count = len(new_parameters) - len(self.non_updated_parameters)
        print(
            f'{updated_count} model parameters updated, parameters not updated:'
        )
        if len(self.non_updated_parameters) >= 1:
            for i, (k,
                    value) in enumerate(self.non_updated_parameters.items()):
                print('No.', i + 1, ' ', k, '=>', value)
        else:
            print('none')
