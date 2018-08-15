from core_gui import *
from shutil   import copyfile
from datetime import datetime
from core_sqlite import TSQLiteConnection
from dict import *
import os


class FormBackups(CForm):
	path_backups = ""

	def __init_objects__(self):
		self.path_backups = self.application.PATH_COMMON + "backups/"

	def __init_icons__(self):
		self.icon_small_backups       = QIcon(self.application.PATH_ICONS_SMALL + "database_cleanup.png")
		self.icon_small_backup_save   = QIcon(self.application.PATH_ICONS_SMALL + "database_save.png")
		self.icon_small_backup_delete = QIcon(self.application.PATH_ICONS_SMALL + "database_delete.png")

		self.icon_small_close         = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

	def __init_actions__(self):
		self.action_backup_save    = QAction(self.icon_small_backup_save,   "Сделать резервную копию", None)
		self.action_backup_delete  = QAction(self.icon_small_backup_delete, "Удалить резервную копию", None)
		self.action_backup_restore = QAction(self.icon_small_backups,       "Восстановить из резервной копии", None)

		self.action_close          = QAction(self.icon_small_close,         "Закрыть",                 None)

	def __init_menu__(self):
		menu_actions = QMenu("Действия")
		menu_actions.addAction(self.action_backup_save)
		menu_actions.addAction(self.action_backup_restore)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_backup_delete)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_close)

		self.menuBar().addMenu(menu_actions)

	def __init_events__(self):
		self.action_close.triggered.connect(self.close)
		self.action_backup_save.triggered.connect(self.backup_save)
		self.action_backup_restore.triggered.connect(self.backup_restore)
		self.action_backup_delete.triggered.connect(self.backup_delete)

	def __ui__(self):
		self.__init_dirs()

		self.table_backups = QTableWidget()
		self.table_backups.setEditTriggers(QTableWidget.NoEditTriggers)
		self.table_backups.setSelectionBehavior(QTableWidget.SelectRows)

		self.setMinimumSize(640, 480)
		self.setWindowTitle("Управление резервными копиями")
		self.setContentsMargins(3, 3, 3, 3)
		self.setCentralWidget(self.table_backups)

	def __init_dirs(self):
		if not os.path.exists(self.path_backups):
			os.mkdir(self.path_backups)

	def backup_exec(self):
		_dialog = QMessageBox()
		_dialog.setWindowTitle("Резервное копирование")

		try:
			_date = datetime.now()
			_from = self.application.PATH_COMMON + "db.sqlite"
			_to   = self.path_backups + _date.strftime("%Y-%m-%d %H-%M") + ".sqlite"

			copyfile(_from, _to)

			_dialog.information(self, "Резервное копирование", "База скопирована в \n{}".format(_to))
		except Exception as error:
			_dialog.setText("Ошибка при выполнении копирования")
			_dialog.setIcon(QMessageBox.Critical)
			_dialog.setDetailedText(str(error))

			_dialog.exec_()

	def backup_save(self):
		self.backup_exec()
		self.backups_load()

	def backups_load(self):
		self.table_backups.setRowCount(0)
		self.table_backups.setColumnCount(3)

		_files = os.listdir(self.path_backups)
		_files.sort()

		for _file in _files:
			if _file.endswith('.sqlite'):
				_connect = TSQLiteConnection("{}{}".format(self.path_backups, _file), _file)

				_sql = "SELECT COUNT(ID) FROM {}".format(TABLE_META)
				_obj_counts = _connect.get_single(_sql)

				_item_date  = QTableWidgetItem()
				_item_date.setText(_file[0:10])
				_item_date.setTextAlignment(Qt.AlignCenter)

				_item_time  = QTableWidgetItem()
				_item_time.setText(_file[11:16])
				_item_time.setTextAlignment(Qt.AlignCenter)

				_item_count = QTableWidgetItem()
				_item_count.setText(_obj_counts)
				_item_count.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

				self.table_backups.setRowCount(self.table_backups.rowCount() + 1)

				_row = self.table_backups.rowCount() - 1

				self.table_backups.setItem(_row, 0, _item_date)
				self.table_backups.setItem(_row, 1, _item_time)
				self.table_backups.setItem(_row, 2, _item_count)

				_connect.close()

			self.table_backups.setHorizontalHeaderLabels(["Дата копии", "Время копии", "Количество объектов"])
			self.table_backups.resizeRowsToContents()
			self.table_backups.resizeColumnsToContents()

	def load_and_show(self):
		self.backups_load()
		self.showCentered()

	def backup_restore(self):
		_row = self.table_backups.currentRow()

		if _row >= 0:
			_item_date = self.table_backups.item(_row, 0)
			_item_time = self.table_backups.item(_row, 1)

			_date = _item_date.text()
			_time = _item_time.text()

			_from = self.path_backups + "{} {}.sqlite".format(_date, _time)
			_to   = self.application.PATH_COMMON + "db.sqlite"

			_dialog = QMessageBox()
			_result = _dialog.question(self,
			                           "Восстановление",
			                           "Восстановить базу на {} {}? \n Перед восстановление будет сделана резервная копия.".format(_date, _time),
			                           QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes

			if _result:
				self.backup_exec()

				_dialog = QMessageBox()
				_dialog.setWindowTitle("Резервное копирование")

				try:
					copyfile(_from, _to)

					_dialog.information(self, "Резервное копирование", "База восстановлена на {} {}".format(_date, _time))
				except Exception as error:
					_dialog.setText("Ошибка при выполнении восстановления")
					_dialog.setIcon(QMessageBox.Critical)
					_dialog.setDetailedText(str(error))

					_dialog.exec_()

	def backup_delete(self):
		_row     = self.table_backups.currentRow()
		_date    = self.table_backups.item(_row, 0).text()
		_time    = self.table_backups.item(_row, 1).text()
		_objects = self.table_backups.item(_row, 2).text()

		_dialog  = QMessageBox()
		_result  = _dialog.question(self,
		                            "Удаление копии",
		                            "Подтвердите удаление резервной копии\nДата\время: {} {}. Объектов: {}".format(_date, _time, _objects),
		                            QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes

		if _result:
			os.remove("{}{} {}.sqlite".format(self.path_backups,
			                                  _date,
			                                  _time))
			self.backups_load()
