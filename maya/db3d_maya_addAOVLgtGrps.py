####Author: Dan Bruce
####Email: dancbruce@gmail.com
####Date: 05/30/2024
####Software: Maya 2022.4
####Script: maya_addAOVLightGrps
####Version: 1.0
####Note:Adds and removes direct and indirect light group AOVs.

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds
import mtoa.aovs as aovs

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(main_window_ptr, QtWidgets.QWidget)    

class AddLgtGrps(QtWidgets.QDialog):    
    def __init__(self, parent=maya_main_window()):
        super(AddLgtGrps, self).__init__(parent)
        
        self.setWindowTitle("Add AOV Light Groups")
        self.setMinimumWidth(100)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
    def create_widgets(self):
        ##AOVs
        self.lblAov = QtWidgets.QLabel('AOVs:', self)
        self.checkCoatDir = QtWidgets.QCheckBox('coat_direct', self)
        self.checkCoatDir.toggle()
        self.checkCoatInDir = QtWidgets.QCheckBox('coat_indirect', self)
        self.checkCoatInDir.toggle()
        self.checkDifDir = QtWidgets.QCheckBox('diffuse_direct', self)
        self.checkDifDir.toggle()
        self.checkDifInDir = QtWidgets.QCheckBox('diffuse_indirect', self)
        self.checkDifInDir.toggle()
        self.checkSpecDir = QtWidgets.QCheckBox('specular_direct', self)
        self.checkSpecDir.toggle()
        self.checkSpecInDir = QtWidgets.QCheckBox('specular_indirect', self)
        self.checkSpecInDir.toggle()
        self.checkTranDir = QtWidgets.QCheckBox('transmission_direct', self)
        self.checkTranDir.toggle()
        self.checkTranInDir = QtWidgets.QCheckBox('transmission_indirect', self)
        self.checkTranInDir.toggle()

        #Light Groups
        self.lblLgtGrp = QtWidgets.QLabel('Light Groups:', self)
        self.checkA = QtWidgets.QCheckBox('A')
        self.checkA.toggle()
        self.checkB = QtWidgets.QCheckBox('B', self)
        self.checkC = QtWidgets.QCheckBox('C', self)
        self.checkD = QtWidgets.QCheckBox('D', self)
        self.checkE = QtWidgets.QCheckBox('E', self)
        self.checkF = QtWidgets.QCheckBox('F', self)
        self.checkG = QtWidgets.QCheckBox('G', self)
        self.checkH = QtWidgets.QCheckBox('H', self)
        self.checkI = QtWidgets.QCheckBox('I', self)
        self.checkJ = QtWidgets.QCheckBox('J', self)

        self.prefixLbl = QtWidgets.QLabel('Prefix:', self)
        self.prefixEdit = QtWidgets.QLineEdit('Lgt')

        #Run Button
        self.run_btn = QtWidgets.QPushButton("Add AOVs")
        self.checkRemove = QtWidgets.QCheckBox('Remove Unchecked', self)
        self.checkRemove.toggle()
         
    def create_layouts(self):
        form_layout = QtWidgets.QFormLayout()
        #AOVs
        form_layout.addRow(self.lblAov)
        form_layout.addRow(self.checkCoatDir)
        form_layout.addRow(self.checkCoatInDir)
        form_layout.addRow(self.checkDifDir)
        form_layout.addRow(self.checkDifInDir)
        form_layout.addRow(self.checkSpecDir)
        form_layout.addRow(self.checkSpecInDir)
        form_layout.addRow(self.checkTranDir)
        form_layout.addRow(self.checkTranInDir)
        #Light Groups
        form_layout.addRow(self.lblLgtGrp)

        check_col1_layout = QtWidgets.QVBoxLayout()
        check_col1_layout.addWidget(self.checkA)
        check_col1_layout.addWidget(self.checkB)
        check_col1_layout.addWidget(self.checkC)
        check_col1_layout.addWidget(self.checkD)
        check_col1_layout.addWidget(self.checkE)        

        check_col2_layout = QtWidgets.QVBoxLayout()
        check_col2_layout.addWidget(self.checkF)
        check_col2_layout.addWidget(self.checkG)
        check_col2_layout.addWidget(self.checkH)
        check_col2_layout.addWidget(self.checkI)
        check_col2_layout.addWidget(self.checkJ)          

        check_layout = QtWidgets.QHBoxLayout()
        check_layout.addLayout(check_col1_layout)
        check_layout.addLayout(check_col2_layout)

        form_layout.addRow(check_layout)

        prefix_layout = QtWidgets.QHBoxLayout()
        prefix_layout.addWidget(self.prefixLbl)
        prefix_layout.addWidget(self.prefixEdit)

        form_layout.addRow(prefix_layout)

        #Run Button
        form_layout.addRow(self.run_btn)
        form_layout.addRow(self.checkRemove)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)

    def create_connections(self):
        self.run_btn.clicked.connect(self.run)

    def run(self):
        grpList = [self.checkA, self.checkB, self.checkC, self.checkD, self.checkE, self.checkF, self.checkG, self.checkH, self.checkI, self.checkJ]
        aovList = [self.checkCoatDir, self.checkCoatInDir, self.checkDifDir, self.checkDifInDir, self.checkSpecDir, self.checkSpecInDir, self.checkTranDir, self.checkTranInDir]
        for grp in grpList:
            name = self.prefixEdit.text()+grp.text()
            for aov in aovList:
                if grp.isChecked() and aov.isChecked():
                    if cmds.objExists('aiAOV_'+aov.text()+'_'+name)==False:
                        aovs.AOVInterface().addAOV(aov.text()+'_'+name, aovType='rgb') 
                else:
                    if self.checkRemove.isChecked():
                        if cmds.objExists('aiAOV_'+aov.text()+'_'+name)==True:
                            aovs.AOVInterface().removeAOV(aov.text()+'_'+name)
##Launch UI
if __name__ =="__main__":
    try:
        addLgtGrps_dialog.close() # pylint: disable=E0601
        addLgtGrps_dialog.deleteLater()
    except:
        pass
    addLgtGrps_dialog = AddLgtGrps()
    addLgtGrps_dialog.show()