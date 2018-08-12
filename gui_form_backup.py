from core_gui import *
from shutil   import copyfile
from datetime import datetime


class FormBackups(CForm):
	path_backups = ""

	def __init_objects__(self):
		self.path_backups = self.application.PATH_COMMON + "backups/"

	def __ui__(self):
		self.__init_dirs()

		self.table_backups = QTableWidget()

		self.setMinimumSize(640, 480)
		self.setWindowTitle("Управление резервными копиями")
		self.setContentsMargins(3, 3, 3, 3)
		self.setCentralWidget(self.table_backups)

	def __init_dirs(self):
		if not os.path.exists(self.path_backups):
			os.mkdir(self.path_backups)

	def exec_backup(self):
		_dialog = QMessageBox()
		_dialog.setWindowTitle("Резеврное копирование")

		try:
			_date = datetime.now()
			_from = self.application.PATH_COMMON + "db.sqlite"
			_to   = self.path_backups + _date.strftime("%Y-%m-%d %H-%M") + ".sqlite"

			self.application.sql_connection.close()

			copyfile(_from, _to)

			self.application.sql_connection.open()

			_dialog.information(self, "Резервное копирование", "База скопирована в \n{}".format(_to))
		except Exception as error:
			_dialog.setText("Ошибка при выполнении копирования")
			_dialog.setIcon(QMessageBox.Critical)
			_dialog.setDetailedText(error)

			_dialog.exec_()
