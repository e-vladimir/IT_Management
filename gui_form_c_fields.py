from core_gui     import *
from core_objects import *


class FormCatalogFields(CForm):
	_groups      = CCatalogFieldGroups
	_group       = CCatalogFieldGroup

	model_fields = QStandardItemModel
	tree_fields  = QTreeView

	current_group = None
	current_field = None

	def __init_objects__(self):
		self._groups      = CCatalogFieldGroups(self.application.sql_connection)
		self._group       = CCatalogFieldGroup(self.application.sql_connection)

		self.model_fields = QStandardItemModel()

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

	def __init_events__(self):
		self.action_save.triggered.connect(self.save)
		self.action_defaults.triggered.connect(self._service_defaults)

		self.action_add_field.triggered.connect(self._add_field)
		self.action_add_group.triggered.connect(self._add_group)

		self.action_delete_field.triggered.connect(self._delete_field)
		self.action_delete_group.triggered.connect(self._delete_group)

		self.tree_fields.clicked.connect(self._get_current)

	def __init_icons__(self):
		self.icon_small_insert = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_save   = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_small_close  = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

		self.icon_small_fields = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")

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

	def __init_ui__(self):
		super(FormCatalogFields, self).__init_ui__()

		self.setWindowTitle("Каталог характеристик")
		self.setMinimumSize(480, 640)

		self.tree_fields = QTreeView()
		self.tree_fields.setModel(self.model_fields)
		self.tree_fields.header().hide()

		self.setCentralWidget(self.tree_fields)

	def _get_current(self):
		current_index = self.tree_fields.currentIndex()
		current_item  = self.model_fields.itemFromIndex(current_index)

		if current_item is None:
			self.current_field = None
			self.current_group = None
		else:
			current_parent = current_item.parent()

			if current_parent is None:
				self.current_group = current_item
				self.current_field = None
			else:
				self.current_group = current_parent
				self.current_field = current_item

		self._gui_enable_disable()

	def _add_field(self):
		field_name = "Характеристика"
		field_name, result = QInputDialog.getText(self, "Добавление характеристики", "Укажите характеристику", text=field_name)

		if result:
			list_fields = []

			for index_field in range(self.current_group.rowCount()):
				item_field = self.current_group.child(index_field)
				list_fields.append(item_field.text())

			if field_name not in list_fields:
				self.current_group.appendRow(QStandartItemWithID(field_name, None))

				self.tree_fields.sortByColumn(0, Qt.AscendingOrder)

	def _add_group(self):
		group_name = "Название раздела"
		group_name, result = QInputDialog.getText(self, "Добавление раздела", "Укажите название раздела", text=group_name)

		if result:
			list_groups = self._groups.get_list()

			if group_name not in list_groups:
				item_group = QStandartItemWithID(group_name, None)

				self.model_fields.appendRow(item_group)

				self.tree_fields.sortByColumn(0, Qt.AscendingOrder)

	def _delete_field(self):
		self.current_group.removeChild(self.current_field.row())

	def _delete_group(self):
		self.model_fields.removeRow(self.current_group.row())

	def _gui_enable_disable(self):
		self.action_add_field.setEnabled(self.current_group is not None)
		self.action_delete_field.setEnabled(self.current_field is not None)
		self.action_delete_group.setEnabled(self.current_group is not None)

	def _service_defaults(self):
		self.model_fields.clear()

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

		item_group = QStandartItemWithID("Бухгалтерия", None)
		item_group.appendRow(QStandartItemWithID("Инвентарный номер",    None))
		item_group.appendRow(QStandartItemWithID("Числится",             None))
		item_group.appendRow(QStandartItemWithID("Сотрудник",            None))
		item_group.appendRow(QStandartItemWithID("Дата поступления",     None))
		self.model_fields.appendRow(item_group)

		self.tree_fields.sortByColumn(0, Qt.AscendingOrder)

	def load(self):
		self.model_fields.clear()

		list_groups_id = self._groups.get_list_id()

		for group_id in list_groups_id:
			self._group.load(int(group_id))

			item_group = QStandartItemWithID(self._group.name, self._group.id)

			for field in self._group.get_fields():
				item_group.appendRow(QStandartItemWithID(field, None))

			self.model_fields.appendRow(item_group)

		self.tree_fields.sortByColumn(0, Qt.AscendingOrder)

		self.current_field = None
		self.current_group = None
		self._gui_enable_disable()

	def load_and_show(self):
		self.load()
		self.showCentered()

	def save(self):
		list_id = self._groups.get_list_id()
		for group_id in list_id:
			self._group.id = group_id
			self._group.delete()

		for index_row in range(self.model_fields.rowCount()):
			item_group = self.model_fields.item(index_row)
			group = item_group.text()

			self._group.clear(True)
			self._group.name = group
			self._group.id   = item_group.id

			for index_fields in range(item_group.rowCount()):
				item_field = item_group.child(index_fields)
				field = item_field.text()

				self._group.fields.set_field("Характеристика/{0}".format(index_fields), field)

			if item_group.rowCount() > 0:
				self._group.save()
