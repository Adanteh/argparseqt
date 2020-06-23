import sys
import argparse
from .app import QtArgApp
from .gui import ArgDialog


class QtArgparsed:
    def __init__(self, appname: str, company: str = "", title: str = ""):
        """Decorator used to create a UI for the argumentparser

        Args:
            appname (str): Application name used for settings.
            company (str, optional): Name used for settings. Defaults to QtArgParsed.
            title (str, optional): Title shown in window titlebar. Defaults to `appname`.
        """
        self.appname = appname
        self.title = title if title != "" else appname
        self.company = company if company != "" else self.__class__.__name__

    def __call__(self, func: callable):
        """This actually decurates the function"""

        def wrapper(*args, **kwargs) -> ArgDialog:
            parser: argparse.ArgumentParser = func()

            app = QtArgApp(
                sys.argv, company=self.company, appname=self.appname
            )  # noqa: F841
            dialog = ArgDialog(parser)
            dialog.exec_()
            return dialog

        return wrapper
