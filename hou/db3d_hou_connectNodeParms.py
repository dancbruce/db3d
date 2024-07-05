####Author: Dan C Bruce
####Email: dancbruce@gmail.com
####Date: 07/03/2023 
####Software: Houdini 19.0.622
####Version: 1.2
####Note: Connect multiple secondary node parameters to a single primary node.
####Update:  Added attribute type check for string attributes.

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import hou

class ConnectNodeParms(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setMinimumWidth(400)
        self.setWindowTitle('Connect Node Parameters')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.ui = ConnectNodeParms_UI()
        self.ui.setup_ui(self)
        
        self.ui.primary_button.pressed.connect(self.get_primary_node)
        self.ui.connect_button.pressed.connect(self.connect_nodes)

    def select_error(self):
        hou.ui.displayMessage('Select one node to be the primary node.')

    def get_primary_node(self):
        if len(hou.selectedNodes())!=1:
            self.select_error()
            return
        for node in hou.selectedNodes():
            self.ui.primary_button.setText(node.path())
 
    def connect_nodes(self):
        if self.ui.primary_button.text() == 'Select Primary Node':
            self.select_error()
            return
        
        primary_node = hou.node(self.ui.primary_button.text())
        primary_parms = primary_node.parms()          

        for node in hou.selectedNodes():
            if node != primary_node:            
                #Set path
                if self.ui.parm_path_toggle.isChecked():
                    path = primary_node.path()
                else:
                    path = node.relativePathTo(primary_node)
                #Set parm expressions
                for i in range(len(primary_parms)):
                    if primary_parms[i].parmTemplate().type().name() in ["Float","Int","Toggle"]:
                        node.parm(primary_parms[i].name()).setExpression('ch("'+path+'/'+primary_parms[i].name()+'")')
                    if primary_parms[i].parmTemplate().type().name() == "String":
                        node.parm(primary_parms[i].name()).setExpression('chs("'+path+'/'+primary_parms[i].name()+'")')

class ConnectNodeParms_UI():    
    def setup_ui(self, widget):

        self.primary_button = QtWidgets.QPushButton('Select Primary Node')
        self.parm_path_toggle = QtWidgets.QCheckBox('Absolute Path')
        self.connect_button = QtWidgets.QPushButton('Connect Secondary Nodes')

        #Main Layout
        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(self.primary_button,1,0)
        main_layout.addWidget(self.parm_path_toggle,2,0)
        main_layout.addWidget(self.connect_button,3,0)

        #Widget
        widget.setLayout(main_layout)

for window in QtGui.QGuiApplication.topLevelWindows():
    if window.objectName()== 'ConnectNodeParmsClassWindow':
        window.close()
    
ConnectNodeParms_dialog = ConnectNodeParms()
ConnectNodeParms_dialog.show()