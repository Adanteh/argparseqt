# -*- coding: utf-8 -*-
""" Widgets for displaying argparse arguments in a GUI """

import argparse
from typing import Dict, Any
from qtpy import QtCore, QtWidgets

from . import wrappedWidgets
from ..parser import groupingTools


class ArgDialog(QtWidgets.QDialog):
    """ A simple settings dialog containing a single ArgparseWidget and stardard ok/cancel dialog buttons """

    valueAdjusted = QtCore.Signal()

    def __init__(self, argParser: argparse.ArgumentParser, orphanGroupName="Main", parent=None, title="Settings"):
        super().__init__(parent)

        self.argParser = argParser
        self.argparseWidget = ArgparseListWidget(self.argParser, orphanGroupName)
        self.argparseWidget.valueAdjusted.connect(self.valueAdjusted.emit)

        self.setWindowTitle(title)

        self.buttons = QtWidgets.QDialogButtonBox(self)
        self.buttons.addButton(QtWidgets.QDialogButtonBox.Ok)
        self.buttons.addButton(QtWidgets.QDialogButtonBox.Cancel)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.argparseWidget)
        self.layout().addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.resize(800, 400)

    def setValues(self, values: Dict[str, Any]):
        return self.argparseWidget.setValues(values)

    def getValues(self) -> Dict[str, Any]:
        return self.argparseWidget.getValues()


class ArgparseListWidget(QtWidgets.QWidget):
    """ A widget with a list of argparse groups in a listbox on the left, and stacked ArgGroupWidgets on the right.
        This widget can be embedded into dialogs, windows, and other widgets

        Clicking a group in the list on the left will display the settings for that group on the right
    """

    valueAdjusted = QtCore.Signal()

    def __init__(self, argParser, orphanGroupName, parent=None):
        super().__init__(parent)

        self.argParser = argParser
        self.groupedParser = groupingTools.organizeIntoGroups(self.argParser)
        self.setLayout(QtWidgets.QHBoxLayout())

        self.groupList = QtWidgets.QListWidget(self)
        self.widgetStack = QtWidgets.QStackedWidget(self)

        self.groupList.setMaximumWidth(100)
        self.layout().addWidget(self.groupList)
        self.layout().addWidget(self.widgetStack, stretch=1)

        self.orphanGroupname = orphanGroupName
        self.createStackWidgets(self.groupedParser)

    def createStackWidgets(self, groups: dict):
        """Create stack widget for each one of the category settings"""
        for group, arguments in self.groupedParser.items():
            if group.title in ["positional arguments", "optional arguments"]:
                groupName = self.orphanGroupname
                if self.widgetStack.count() > 0:
                    groupWidget = self.widgetStack.widget(0)
                else:
                    groupWidget = self._addGroup(groupName, self.argParser.description)
            else:
                groupName = group.title
                groupWidget = self._addGroup(groupName, group.description)

            groupWidget.addArguments(arguments.values())

        self.groupList.setCurrentRow(0)
        self.groupList.currentRowChanged.connect(self.widgetStack.setCurrentIndex)
        if self.groupList.count() == 1:
            self.groupList.hide()

    def _addGroup(self, name, description):
        """Adds the widget that will contain all parameters for our parser group"""
        self.groupList.addItem(name)
        groupWidget = ArgGroupWidget(name, description=description)
        groupWidget.valueAdjusted.connect(self.valueAdjusted.emit)
        self.widgetStack.addWidget(groupWidget)

        return groupWidget

    def setValues(self, values: Dict[str, Any]):
        for i in range(self.widgetStack.count()):
            groupName = self.groupList.item(i).text()
            if groupName in values:
                self.widgetStack.widget(i).setValues(values[groupName])
            else:
                self.widgetStack.widget(i).setValues(values)

    def getValues(self) -> Dict[str, Any]:
        settings = {}
        for i in range(self.widgetStack.count()):
            groupName = self.groupList.item(i).text()
            if groupName == self.orphanGroupname:
                settings = {**settings, **self.widgetStack.widget(i).getValues()}
            else:
                settings[groupName] = self.widgetStack.widget(i).getValues()

        return settings


class ArgGroupWidget(QtWidgets.QWidget):
    """ Container for a group of argument widgets

        This widget can be embedded into other containers if you wanted, say, a tabbed-based view
    """

    valueAdjusted = QtCore.Signal()

    def __init__(self, name, arguments=[], description=None, parent=None):
        super().__init__(parent)
        self.name = name

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        self.form = QtWidgets.QWidget()
        self.form.setLayout(QtWidgets.QFormLayout())
        self.form.layout().setHorizontalSpacing(32)

        if description is None:
            text = QtWidgets.QLabel(f"<h1>{name}</h1>")
        else:
            text = QtWidgets.QLabel(f"<h1>{name}</h1><h2>{description}</h2>")

        text.setWordWrap(True)
        self.layout().addWidget(text)
        self.layout().addWidget(self.form)

        self.addArguments(arguments)

    def onValueChanged(self, _):
        self.valueAdjusted.emit()

    def addArguments(self, arguments):
        """Adds an argparser argument to a group and creates a widget for it"""
        for argument in arguments:
            widget = wrappedWidgets.makeWidget(argument, self)
            widget.valueChanged.connect(self.onValueChanged)

            helpText = argument.help
            widget.setToolTip(helpText)
            widget.setWhatsThis(helpText)

            self.form.layout().addRow(argument.dest, widget)

    def setValues(self, values: Dict[str, Any]):
        """Gets values for the argument group"""
        for row in range(self.form.layout().rowCount()):
            itemName = self.form.layout().itemAt(row, QtWidgets.QFormLayout.LabelRole).widget().text()
            if itemName in values:
                widget = self.form.layout().itemAt(row, QtWidgets.QFormLayout.FieldRole).widget()
                widget.setValue(values[itemName])

    def getValues(self) -> Dict[str, Any]:
        """Get values for this argument group"""
        values = {}
        for row in range(self.form.layout().rowCount()):
            itemName = self.form.layout().itemAt(row, QtWidgets.QFormLayout.LabelRole).widget().text()
            itemValue = self.form.layout().itemAt(row, QtWidgets.QFormLayout.FieldRole).widget().value()

            values[itemName] = itemValue

        return values
