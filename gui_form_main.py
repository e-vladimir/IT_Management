from core_gui     import *
from core_objects import *
# import functools


class FormMain(CForm):
	def __init_ui__(self):
		super(FormMain, self).__init_ui__()

		self.application.init_sql()

		self.setMinimumSize(640, 480)
		self.setWindowTitle("IT-management - {0}".format(self.application.version))
