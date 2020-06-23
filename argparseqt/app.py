from qtpy.QtCore import QSettings
from qtpy.QtWidgets import QApplication

from . import FOLDER


class QtArgApp(QApplication):
    def __init__(self, argv: list, company: str, appname: str, Liststr=None):
        """
        Creates instance of QApplication for our application, will autoinit settings

        Args:
            argv (List): [description]
            Liststr ([type], optional): [description]. Defaults to None.
            company (str, optional): Company name for settings saving. Defaults to "QtArgApp".
            appname (str, optional): App name for settings saving. Defaults to "DefaultApp".
        """
        if company is None:
            company = self.__class__.__name__
        QSettings.setPath(QSettings.IniFormat, QSettings.UserScope, str(FOLDER.parent / "settings"))
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, company, appname)
        super().__init__(argv)

    @staticmethod
    def instance(*args, **kwargs) -> "QtArgApp":
        return QApplication.instance()


def get_app():
    return QtArgApp.instance()
