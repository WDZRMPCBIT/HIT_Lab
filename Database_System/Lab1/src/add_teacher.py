# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/add_teacher.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddTeacherWidget(object):
    def setupUi(self, AddTeacherWidget):
        AddTeacherWidget.setObjectName("AddTeacherWidget")
        AddTeacherWidget.resize(800, 480)
        self.teacher_name_label = QtWidgets.QLabel(AddTeacherWidget)
        self.teacher_name_label.setGeometry(QtCore.QRect(160, 110, 240, 40))
        self.teacher_name_label.setObjectName("teacher_name_label")
        self.teacher_id_label = QtWidgets.QLabel(AddTeacherWidget)
        self.teacher_id_label.setGeometry(QtCore.QRect(160, 190, 240, 40))
        self.teacher_id_label.setObjectName("teacher_id_label")
        self.teacher_name_edit = QtWidgets.QLineEdit(AddTeacherWidget)
        self.teacher_name_edit.setGeometry(QtCore.QRect(400, 110, 240, 40))
        self.teacher_name_edit.setObjectName("teacher_name_edit")
        self.teacher_id_edit = QtWidgets.QLineEdit(AddTeacherWidget)
        self.teacher_id_edit.setGeometry(QtCore.QRect(400, 190, 240, 40))
        self.teacher_id_edit.setObjectName("teacher_id_edit")

        self.accept_button = QtWidgets.QPushButton(AddTeacherWidget)
        self.accept_button.setGeometry(QtCore.QRect(280, 320, 240, 40))
        self.accept_button.setObjectName("accept_button")
        self.accept_button.clicked.connect(self._add_teacher)

        self.retranslateUi(AddTeacherWidget)
        QtCore.QMetaObject.connectSlotsByName(AddTeacherWidget)
        self.widget = AddTeacherWidget

    def retranslateUi(self, AddTeacherWidget):
        _translate = QtCore.QCoreApplication.translate
        AddTeacherWidget.setWindowTitle(_translate("AddTeacherWidget", "添加教师"))
        self.teacher_name_label.setText(_translate("AddTeacherWidget", "教师姓名"))
        self.teacher_id_label.setText(_translate("AddTeacherWidget", "教工号"))
        self.accept_button.setText(_translate("AddTeacherWidget", "添加"))

    def _add_teacher(self):
        database = sqlite3.connect('Database_System/Lab1/data/data.db')

        teacher_name = self.teacher_name_edit.text()
        teacher_id = self.teacher_id_edit.text()
        if teacher_id.isnumeric() == False:
            QtWidgets.QMessageBox.warning(self.widget, '警告', '教工号必须为纯数字')
            return
        teacher_id = int(teacher_id)

        exist_id = database.execute('SELECT id FROM TEACHER')
        for row in exist_id:
            if row[0] == teacher_id:
                QtWidgets.QMessageBox.warning(self.widget, '警告', '该教工号已存在')
                return

        command = 'INSERT INTO TEACHER VALUES (%d, \'%s\')' % (teacher_id,
                                                               teacher_name)
        database.execute(command)

        QtWidgets.QMessageBox.information(self.widget, '提示', '添加成功')
        database.execute('COMMIT;')
        database.close()
