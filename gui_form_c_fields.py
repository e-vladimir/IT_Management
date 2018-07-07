from core_gui     import *
from core_objects import *


class FormCatalogFields(CForm):
	_fields = CCatalogFields
	_field  = CCatalogField

	def __init_objects__(self):
		self._object = CMetaObject(self.application.sql_connection)

	def __init_ui__(self):
		super(FormCatalogFields, self).__init_ui__()

		self.setWindowTitle("Каталог характеристик")
		self.setMinimumSize(480, 640)

	def __init_icons__(self):
		self.icon_small_insert = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_save   = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_small_close  = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

		self.icon_small_fields = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")

	def __init_actions__(self):
		self.action_save           = QAction(self.icon_small_save,   "Сохранить",               None)
		self.action_save_and_close = QAction(self.icon_small_save,   "Сохранить и закрыть",     None)
		self.action_close          = QAction(self.icon_small_close,  "Закрыть",                 None)

		self.action_add_group      = QAction(self.icon_small_insert, "Добавить группу",         None)
		self.action_delete_group   = QAction(self.icon_small_delete, "Удалить группу",          None)
		self.action_add_field      = QAction(self.icon_small_insert, "Добавить характеристику", None)
		self.action_delete_field   = QAction(self.icon_small_delete, "Удалить характеристику",  None)

		self.action_clear          = QAction(self.icon_small_delete, "Удалить все характеристики",      None)
		self.action_defaults       = QAction(self.icon_small_fields, "Стандартный набор характеристик", None)

	def __init_menu__(self):
		menu_main = QMenu("Действия")
		menu_main.addAction(self.action_save)
		menu_main.addAction(self.action_save_and_close)
		menu_main.addSeparator()
		menu_main.addAction(self.action_close)

		menu_fields = QMenu("Характеристики")
		menu_fields.addAction(self.action_add_group)
		menu_fields.addAction(self.action_delete_group)
		menu_fields.addSeparator()
		menu_fields.addAction(self.action_add_field)
		menu_fields.addAction(self.action_delete_field)

		menu_service = QMenu("Сервис")
		menu_service.addAction(self.action_clear)
		menu_service.addAction(self.action_defaults)

		self.menuBar().addMenu(menu_main)
		self.menuBar().addMenu(menu_fields)
		self.menuBar().addMenu(menu_service)