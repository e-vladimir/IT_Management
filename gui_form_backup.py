from core_gui import *


class FormBackups(CForm):
	def __init_ui__(self):
		self.__init_dirs__()

		self.table_backups = QTableWidget()

		self.setMinimumSize(640, 480)
		self.setWindowTitle("Управление резервными копиями")
		self.setContentsMargins(3, 3, 3, 3)
		self.setCentralWidget(self.table_backups)

	def __init_dirs__(self):
		pass
