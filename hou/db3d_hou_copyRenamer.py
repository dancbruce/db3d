####Author: Dan C Bruce
####Email: dancbruce@gmail.com
####Date: 04/25/2024
####Software: Houdini 19.0.622 Python 3
####Version: 1.0
####Note: Tool for copying and renaming selected nodes.
####Update: Initial release

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

import hou


class Copy_Renamer(QtWidgets.QWidget): 
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        self.setWindowTitle('Copy Renamer')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.ui = Check_OTL_Defaults_UI()
        self.ui.setup_ui(self)

        self.node_list = []

        #Connect UI
        self.ui.refresh_nodes_button.pressed.connect(self.update_refresh_node_select)
        self.ui.operation_combo.activated.connect(self.update_operation_select)

        self.ui.search_replace_count_spin.valueChanged.connect(self.op_search_replace_table)
        self.ui.search_edit.textEdited.connect(self.op_search_replace_table)
        self.ui.replace_edit.textEdited.connect(self.op_search_replace_table)

        self.ui.insert_overwrite_combo.activated.connect(self.op_insert_overwrite_table)
        self.ui.insert_overwrite_text_edit.textEdited.connect(self.op_insert_overwrite_table)
        self.ui.insert_overwrite_position_spin.valueChanged.connect(self.op_insert_overwrite_table)
        self.ui.insert_overwrite_position_combo.activated.connect(self.op_insert_overwrite_table)
        self.ui.insert_overwrite_spacing_toggle.stateChanged.connect(self.op_insert_overwrite_table)

        self.ui.numbering_enable_toggle.stateChanged.connect(self.op_numbering_table)
        self.ui.numbering_padding_spin.valueChanged.connect(self.op_numbering_table)
        self.ui.numbering_start_spin.valueChanged.connect(self.op_numbering_table)
        self.ui.numbering_insert_overwrite_combo.activated.connect(self.op_numbering_table)
        self.ui.numbering_position_spin.valueChanged.connect(self.op_numbering_table)
        self.ui.numbering_position_combo.activated.connect(self.op_numbering_table)
        self.ui.numbering_spacing_toggle.stateChanged.connect(self.op_numbering_table)

        self.ui.node_name_undo_button.pressed.connect(self.update_undo_node_list)
        self.ui.node_name_edit_button.pressed.connect(self.update_edit_node_list)

        self.ui.trim_number_toggle.stateChanged.connect(self.update_trim_toggle_select)

        self.ui.rename_button.pressed.connect(self.util_rename_nodes)

        self.update_refresh_node_select()

    #Update
    def update_ui(self):
        self.ui.search_edit.setText('')
        self.ui.replace_edit.setText('')
        self.ui.insert_overwrite_text_edit.setText('')
        self.ui.numbering_enable_toggle.setChecked(0)

    def update_refresh_node_list(self):
        self.node_list= []
        for node in hou.selectedNodes():
            if node.parent().path() == hou.selectedNodes()[0].parent().path():
                add_list = [node.name(),node.path(),node.parent().path()]
                self.node_list.append(add_list)
        self.node_list.sort()
            
    def update_refresh_node_name_table(self):
        for i in range(self.ui.node_name_table.rowCount()):
            self.ui.node_name_table.removeRow(0)

        for node in self.node_list:
            self.ui.node_name_table.insertRow(self.ui.node_name_table.rowCount())
            item = QtWidgets.QTableWidgetItem(node[-3])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.node_name_table.setItem(self.ui.node_name_table.rowCount()-1,0,item)
            self.ui.node_name_table.item(self.ui.node_name_table.rowCount()-1,0).setBackground(QtGui.QColor(100,100,100))

            name = self.util_trim_name_numbering(node[0])
            item = QtWidgets.QTableWidgetItem(name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.node_name_table.setItem(self.ui.node_name_table.rowCount()-1,1,item)
            self.ui.node_name_table.item(self.ui.node_name_table.rowCount()-1,1).setBackground(QtGui.QColor(100,100,100))

    def update_refresh_node_select(self):
        self.update_ui()
        self.update_refresh_node_list()
        self.update_refresh_node_name_table()

    def update_trim_toggle_select(self):
        self.update_refresh_node_name_table()

        index = self.ui.operation_combo.currentIndex()
        if index == 0:
            self.op_search_replace_table()
        if index == 1:
            self.op_insert_overwrite_table()
        if index == 2:
            self.op_numbering_table()

    def update_edit_node_list(self):
        count = len(self.node_list)
        for i in range(count):
            node = self.node_list[i]
            new_name = self.ui.node_name_table.item(i,1).text()
            node.insert(0,new_name)
            self.ui.node_name_table.item(i,1).setBackground(QtGui.QColor(100,100,100))
        self.ui.trim_number_toggle.setChecked(0)
        self.update_ui()

    def update_undo_node_list(self):
        count = len(self.node_list)
        for i in range(count):
            node = self.node_list[i]
            if len(node) > 3:
                item = QtWidgets.QTableWidgetItem(node[1])
                del node[0]
            node_name = self.util_trim_name_numbering(node[0])
            item = QtWidgets.QTableWidgetItem(node_name)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.node_name_table.setItem(i,1,item)
            self.ui.node_name_table.item(i,1).setBackground(QtGui.QColor(100,100,100))
        self.update_ui()
        
    def update_operation_select(self,index):
        self.ui.search_replace_widget.setVisible(0)
        self.ui.insert_overwrite_widget.setVisible(0)
        self.ui.numbering_widget.setVisible(0)

        if index == 0:
            self.ui.search_replace_widget.setVisible(1)
        if index == 1:
            self.ui.insert_overwrite_widget.setVisible(1)
        if index == 2:
            self.ui.numbering_widget.setVisible(1)
        self.update_ui()
        self.update_refresh_node_name_table()

    #Utilities
    def util_rename_nodes(self):
        self.update_edit_node_list()
        if self.ui.copy_toggle.isChecked():
            copy_list = []
            for node in self.node_list:
                node = hou.node(node[-2])
                copy_list.append(node)
            tuple(copy_list)
            copy_nodes = hou.copyNodesTo(copy_list,copy_list[0].parent())
            for i in range(len(self.node_list)):
                node_name = self.node_list[i][0]
                copy_nodes[i].setName(node_name,unique_name=True)
                copy_nodes[i].move((8,0))
            self.update_refresh_node_select()
        else:
            for node in self.node_list:
                node_path = hou.node(node[-2])
                node_name = node[0]
                node_path.setName(node_name,unique_name=True)
            self.update_refresh_node_select()

        for i in range(self.ui.node_name_table.rowCount()):
            self.ui.node_name_table.item(i,1).setBackground(QtGui.QColor(100,150,100))

    def util_trim_name_numbering(self,name):
        if self.ui.trim_number_toggle.isChecked():
            name = name.rstrip('0123456789_')
        return name

    def util_insert_text(self,i,name,text,position,ui_insert_overwrite,ui_position,ui_spacing):
        if ui_spacing:
            if position == 0 or position >= len(name):
                if ui_position:
                    if position >= len(name):
                        text += '_'
                    else:
                        text = '_'+text
                else:
                    if position >= len(name):
                        text = '_'+text
                    else:
                        text += '_'
            else:
                text = '_'+text+'_'
        if ui_insert_overwrite:
            if len(text) == len(name):
                name = ''
            else:
                name = list(name)
                if ui_position:
                    if position == 0 or position >= len(name)-1:
                        del name[(len(name)-len(text)):len(name)]
                    else:
                        del name[(len(name)-len(text)-position):(len(name)-position)]
                else:
                    if position >= len(name)-1:
                        del name[(len(name)-len(text)):len(name)]
                    else:
                        del name[position:(len(text)+position)]
                name = ''.join(name)
        if ui_position:                      
            if position == 0:
                name += text
            else:
                name = name[:(position*-1)]+text+name[(position*-1):]
        else:                        
            name = name[:position]+text+name[position:]
        item = QtWidgets.QTableWidgetItem(name)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.node_name_table.setItem(i,1,item)
        self.ui.node_name_table.item(i,1).setBackground(QtGui.QColor(150,100,100))

    #Operations
    def op_search_replace_table(self):
        search = self.ui.search_edit.text()
        replace = self.ui.replace_edit.text()
        if search == "":
            self.update_refresh_node_name_table() 
            return
        for i in range(len(self.node_list)):
            node = self.node_list[i]
            node_name = node[0]
            if self.ui.search_replace_count_spin.value() == 0:
                node_name_new = node_name.replace(search,replace)
            else:
                node_name_new = node_name.replace(search,replace,self.ui.search_replace_count_spin.value())
            if search in node[0]:
                if node_name != node_name_new:
                    node_name_new = self.util_trim_name_numbering(node_name_new)
                    item = QtWidgets.QTableWidgetItem(node_name_new)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.ui.node_name_table.setItem(i,1,item)
                    self.ui.node_name_table.item(i,1).setBackground(QtGui.QColor(150,100,100))            
            else:
                node_name = self.util_trim_name_numbering(node_name)
                item = QtWidgets.QTableWidgetItem(node_name)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.node_name_table.setItem(i,1,item)
                self.ui.node_name_table.item(i,1).setBackground(QtGui.QColor(100,100,100))

    def op_insert_overwrite_table(self):
        text = self.ui.insert_overwrite_text_edit.text()
        if text == "":
            self.update_refresh_node_name_table() 
            return
        position = self.ui.insert_overwrite_position_spin.value()
        ui_insert_overwrite = self.ui.insert_overwrite_combo.currentIndex()
        ui_position = self.ui.insert_overwrite_position_combo.currentIndex()
        ui_spacing = self.ui.insert_overwrite_spacing_toggle.isChecked()

        for i in range(len(self.node_list)):
            name = self.util_trim_name_numbering(self.node_list[i][0])
            self.util_insert_text(i,name,text,position,ui_insert_overwrite,ui_position,ui_spacing)

    def op_numbering_table(self):
        padding = self.ui.numbering_padding_spin.value()
        start = self.ui.numbering_start_spin.value()
        position = self.ui.numbering_position_spin.value()
        ui_insert_overwrite = self.ui.numbering_insert_overwrite_combo.currentIndex()
        ui_position = self.ui.numbering_position_combo.currentIndex()
        ui_spacing = self.ui.numbering_spacing_toggle.isChecked()

        if self.ui.numbering_enable_toggle.isChecked():
            for i in range(len(self.node_list)):
                name = self.util_trim_name_numbering(self.node_list[i][0])
                number = str(start+i).rjust(padding,str(0))
                self.util_insert_text(i,name,number,position,ui_insert_overwrite,ui_position,ui_spacing)
        else:
            self.update_refresh_node_name_table()             

class Check_OTL_Defaults_UI():
    def search_replace_ui(self):
        search_replace_count_label = QtWidgets.QLabel('Count: ')
        search_replace_count_label.setAlignment(QtCore.Qt.AlignRight)        
        self.search_replace_count_spin = QtWidgets.QSpinBox()

        search_replace_count_layout = QtWidgets.QHBoxLayout()
        search_replace_count_layout.addWidget(search_replace_count_label)
        search_replace_count_layout.addWidget(self.search_replace_count_spin)

        search_label = QtWidgets.QLabel('Search:   ')
        self.search_edit = QtWidgets.QLineEdit()

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)

        replace_label = QtWidgets.QLabel('Replace: ')
        self.replace_edit = QtWidgets.QLineEdit()
        
        replace_layout = QtWidgets.QHBoxLayout()
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_edit)

        search_replace_layout = QtWidgets.QVBoxLayout()
        search_replace_layout.addLayout(search_layout)
        search_replace_layout.addLayout(replace_layout)
        search_replace_layout.addLayout(search_replace_count_layout)

        self.search_replace_widget = QtWidgets.QWidget()
        self.search_replace_widget.setMinimumWidth(350)
        self.search_replace_widget.setLayout(search_replace_layout)

        return self.search_replace_widget

    def insert_overwrite_ui(self):
        self.insert_overwrite_combo = QtWidgets.QComboBox()
        self.insert_overwrite_combo.addItems(['Insert','Overwrite'])
        self.insert_overwrite_text_edit = QtWidgets.QLineEdit()

        insert_overwrite_text_layout = QtWidgets.QHBoxLayout()
        insert_overwrite_text_layout.addWidget(self.insert_overwrite_combo)
        insert_overwrite_text_layout.addWidget(self.insert_overwrite_text_edit)

        insert_overwrite_position_label = QtWidgets.QLabel('Position: ')
        insert_overwrite_position_label.setAlignment(QtCore.Qt.AlignRight)
        self.insert_overwrite_position_spin = QtWidgets.QSpinBox()
        self.insert_overwrite_position_combo = QtWidgets.QComboBox()
        self.insert_overwrite_position_combo.addItems(['Left','Right'])
        self.insert_overwrite_spacing_toggle = QtWidgets.QCheckBox('Spacing')

        insert_overwrite_position_layout = QtWidgets.QHBoxLayout()
        insert_overwrite_position_layout.addWidget(insert_overwrite_position_label)
        insert_overwrite_position_layout.addWidget(self.insert_overwrite_position_spin)
        insert_overwrite_position_layout.addWidget(self.insert_overwrite_position_combo)
        insert_overwrite_position_layout.addWidget(self.insert_overwrite_spacing_toggle)

        insert_overwrite_layout = QtWidgets.QVBoxLayout()
        insert_overwrite_layout.addLayout(insert_overwrite_text_layout)
        insert_overwrite_layout.addLayout(insert_overwrite_position_layout)

        self.insert_overwrite_widget = QtWidgets.QWidget()
        self.insert_overwrite_widget.setMinimumWidth(350)
        self.insert_overwrite_widget.setLayout(insert_overwrite_layout)

        return self.insert_overwrite_widget
    
    def numbering_ui(self):
        self.numbering_enable_toggle = QtWidgets.QCheckBox('Enable')

        self.numbering_insert_overwrite_combo = QtWidgets.QComboBox()
        self.numbering_insert_overwrite_combo.addItems(['Insert','Overwrite'])
        numbering_padding_label = QtWidgets.QLabel('Padding: ')
        numbering_padding_label.setAlignment(QtCore.Qt.AlignRight)
        self.numbering_padding_spin = QtWidgets.QSpinBox()
        self.numbering_padding_spin.setMinimum(1)
        self.numbering_padding_spin.setValue(2)
        numbering_start_label = QtWidgets.QLabel('Start With: ')
        numbering_start_label.setAlignment(QtCore.Qt.AlignRight)
        self.numbering_start_spin = QtWidgets.QSpinBox()
        self.numbering_start_spin.setRange(1,10000)

        numbering_text_layout = QtWidgets.QHBoxLayout()
        numbering_text_layout.addWidget(self.numbering_insert_overwrite_combo)
        numbering_text_layout.addWidget(numbering_padding_label)
        numbering_text_layout.addWidget(self.numbering_padding_spin)
        numbering_text_layout.addWidget(numbering_start_label)
        numbering_text_layout.addWidget(self.numbering_start_spin)

        numbering_position_label = QtWidgets.QLabel('Position: ')
        numbering_position_label.setAlignment(QtCore.Qt.AlignRight)
        self.numbering_position_spin = QtWidgets.QSpinBox()
        self.numbering_position_combo = QtWidgets.QComboBox()
        self.numbering_position_combo.addItems(['Left','Right'])
        self.numbering_spacing_toggle = QtWidgets.QCheckBox('Spacing')

        numbering_position_layout = QtWidgets.QHBoxLayout()
        numbering_position_layout.addWidget(numbering_position_label)
        numbering_position_layout.addWidget(self.numbering_position_spin)
        numbering_position_layout.addWidget(self.numbering_position_combo)
        numbering_position_layout.addWidget(self.numbering_spacing_toggle)

        numbering_layout = QtWidgets.QVBoxLayout()
        numbering_layout.addWidget(self.numbering_enable_toggle)
        numbering_layout.addLayout(numbering_text_layout)
        numbering_layout.addLayout(numbering_position_layout)

        self.numbering_widget = QtWidgets.QWidget()
        self.numbering_widget.setMinimumWidth(350)
        self.numbering_widget.setLayout(numbering_layout)
        
        return self.numbering_widget        

    def setup_ui(self, widget):
        #Refresh UI
        self.refresh_nodes_button = QtWidgets.QPushButton('Refresh Node Selection')
        self.refresh_nodes_button.setMinimumWidth(150)
        #Parameter Table
        self.node_name_table = QtWidgets.QTableWidget(0,2)
        self.node_name_table.setHorizontalHeaderLabels(['Node Name','New Node Name'])
        self.node_name_table.verticalHeader().setVisible(False)
        self.node_name_table.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.node_name_table.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)

        #Operation Selection
        self.operation_combo = QtWidgets.QComboBox()
        self.operation_combo.addItems(['Search & Replace','Insert/Overwrite','Numbering'])

        self.search_replace_ui()
        self.insert_overwrite_ui()
        self.numbering_ui()

        #Edit Undo Buttons
        self.node_name_undo_button = QtWidgets.QPushButton('Undo')
        self.node_name_edit_button = QtWidgets.QPushButton('Edit')
        edit_undo_layout = QtWidgets.QHBoxLayout()
        edit_undo_layout.addWidget(self.node_name_undo_button)
        edit_undo_layout.addWidget(self.node_name_edit_button)

        #Other Options
        self.trim_number_toggle = QtWidgets.QCheckBox('Trim Numbering')
        self.copy_toggle = QtWidgets.QCheckBox('Copy Nodes')
        other_options_layout = QtWidgets.QVBoxLayout()
        other_options_layout.addWidget(self.trim_number_toggle)
        other_options_layout.addWidget(self.copy_toggle)

        #Rename
        self.rename_button = QtWidgets.QPushButton('Rename Nodes')
        self.rename_button.setMinimumWidth(150)
        rename_layout = QtWidgets.QHBoxLayout()
        rename_layout.addWidget(self.rename_button)

        #Main Layout
        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(self.refresh_nodes_button,0,0)
        main_layout.addWidget(self.node_name_table,1,0,1,3)
        main_layout.addWidget(self.operation_combo,2,0)
        main_layout.addWidget(self.search_replace_widget,2,1)
        main_layout.addWidget(self.insert_overwrite_widget,2,1)
        self.insert_overwrite_widget.setVisible(0)
        main_layout.addWidget(self.numbering_widget,2,1)
        self.numbering_widget.setVisible(0)

        main_layout.addLayout(other_options_layout,2,2)
        main_layout.addLayout(edit_undo_layout,3,1)
        main_layout.addLayout(rename_layout,4,2)

        #Widget
        widget.setLayout(main_layout)

try:
    Check_OTL_Defaults_dialog.close()
    Check_OTL_Defaults_dialog.deleteLater()
except:
    pass

Check_OTL_Defaults_dialog = Copy_Renamer()
Check_OTL_Defaults_dialog.show()