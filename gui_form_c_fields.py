from core_gui     import *
from core_objects import *


class FormCatalogFields(CForm):
	_groups      = CCatalogFieldGroups
	_group       = CCatalogFieldGroup

	model_fields = QStandardItemModel
	tree_fields  = QTreeView

	def __init_objects__(self):
		self._groups      = CCatalogFieldGroups(self.application.sql_connection)
		self._group       = CCatalogFieldGroup(self.application.sql_connection)

		self.model_fields = QStandardItemModel()

	def __init_ui__(self):
		super(FormCatalogFields, self).__init_ui__()

		self.setWindowTitle("Каталог характеристик")
		self.setMinimumSize(480, 640)

		self.tree_fields = QTreeView()
		self.tree_fields.setModel(self.model_fields)
		self.tree_fields.header().hide()

		self.setCentralWidget(self.tree_fields)

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

	def __init_events__(self):
		self.action_save.triggered.connect(self.save)
		self.action_defaults.triggered.connect(self.service_defaults)

	def service_defaults(self):
		item_group = QStandartItemWithID("Общее описание", None)
		item_group.appendRow(QStandartItemWithID("Производитель",        None))
		item_group.appendRow(QStandartItemWithID("Модель",               None))
		item_group.appendRow(QStandartItemWithID("Серийный номер",       None))
		item_group.appendRow(QStandartItemWithID("Техническое описание", None))
		item_group.appendRow(QStandartItemWithID("Состояние",            None))
		self.model_fields.appendRow(item_group)

		item_group = QStandartItemWithID("Местоположение", None)
		item_group.appendRow(QStandartItemWithID("Подразделение",        None))
		item_group.appendRow(QStandartItemWithID("Местоположение",       None))
		item_group.appendRow(QStandartItemWithID("Сотрудник",            None))
		self.model_fields.appendRow(item_group)

	def save(self):
		for index_row in range(self.model_fields.rowCount()):
			item_group = self.model_fields.item(index_row)
			group = item_group.text()

			self._group.clear(True)
			self._group.name = group

			for index_fields in range(item_group.rowCount()):
				item_field = item_group.child(index_fields)
				field = item_field.text()

				self._group.fields.set_field("Характеристика/{0}".format(index_fields), field)

			if item_group.rowCount() > 0:
				self._group.save()

	def load(self):
		self.model_fields.clear()

		list_groups_id = self._groups.get_groups_id()

		for group_id in list_groups_id:
			self._group.load(int(group_id))

			item_group = QStandartItemWithID(self._group.name, self._group.id)

			for field_name in self._group.fields.get_list():
				field_value = self._group.fields.get_field(field_name)
				item_group.appendRow(QStandartItemWithID(field_value, None))

			self.model_fields.appendRow(item_group)

	def load_and_show(self):
		self.load()
		self.showCentered()