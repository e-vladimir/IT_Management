# GUI-обёртка для нужных объектов
# V1-2018-07-30

from   PySide.QtCore import *
from   PySide.QtGui  import *
import sys
import os


FONT_BOLD = QFont()
FONT_BOLD.setBold(True)

FONT_ITALIC = QFont()
FONT_ITALIC.setItalic(True)


class CApplication(QApplication):
	def __init__(self):
		super(CApplication, self).__init__(sys.argv)

		self.__init_paths__()

	def __init_paths__(self):
		self.PATH_COMMON        = "{0}".format(os.path.dirname(__file__))
		self.PATH_ICONS         = "{0}/icons/".format(self.PATH_COMMON)
		self.PATH_ICONS_SMALL   = "{0}/small/".format(self.PATH_ICONS)
		self.PATH_ICONS_TOOLBAR = "{0}/toolbar/".format(self.PATH_ICONS)


class CForm(QMainWindow):
	def __init__(self, in_application=None):
		super(CForm, self).__init__()

		self.application = in_application

		self.__init_ui__()
		self.__init_events__()

	def __init_ui__(self):
		self.__init_objects__()

		self.__init_icons__()

		self.__init_actions__()

		self.__init_menu__()
		self.__init_toolbar__()

	def __init_objects__(self):
		pass

	def __init_icons__(self):
		pass

	def __init_actions__(self):
		pass

	def __init_events__(self):
		pass

	def __init_menu__(self):
		pass

	def __init_toolbar__(self):
		pass

	def showCentered(self):
		screen = self.application.desktop().screenGeometry()
		scr_width = screen.width()
		scr_height = screen.height()

		self.move((scr_width - self.width()) / 2, (scr_height - self.height()) / 2)

		self.show()

	def show_message(self, in_message="", in_timeout=1000):
		self.statusBar().showMessage(in_message, in_timeout)


class QStandartItemWithID(QStandardItem):
	id = ""

	def __init__(self, in_caption, in_id="", in_editable=True):
		super(QStandartItemWithID, self).__init__(in_caption)

		self.id = in_id
		self.setEditable(in_editable)


class QLabelR(QLabel):
	def __init__(self, in_caption):
		super(QLabelR, self).__init__(in_caption)

		self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


class QLabelC(QLabel):
	def __init__(self, in_caption):
		super(QLabelC, self).__init__(in_caption)

		self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
