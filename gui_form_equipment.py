from core_gui     import *
from core_objects import *


class NoneModelItem(QStandartItemWithID):
	def __init__(self):
		super(NoneModelItem, self).__init__("", None)


class FormEquipment(CForm):
	_groups      = CCatalogFieldGroups
	_group       = CCatalogFieldGroup

	_equipments  = CEquipments
	_equipment   = CEquipment

	model_fields = QStandardItemModel
	tree_fields  = QTreeView

	current_group = None
	current_field = None

	def __init_actions__(self):
		self.action_save         = QAction(self.icon_small_save,   "Сохранить",           None)
		self.action_save_as_copy = QAction(self.icon_small_save,   "Сохранить как копию", None)
		self.action_delete       = QAction(self.icon_small_delete, "Удалить",             None)
		self.action_open         = QAction(self.icon_small_open,   "Загрузить",           None)
		self.action_close        = QAction(self.icon_small_close,  "Закрыть",             None)

	def __init_events__(self):
		self.tree_fields.expanded.connect(self._gui_resize_fields)
		self.tree_fields.collapsed.connect(self._gui_resize_fields)

		self.action_save.triggered.connect(self.save)

	def __init_icons__(self):
		self.icon_small_insert = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_open   = QIcon(self.application.PATH_ICONS_SMALL + "table_open.png")
		self.icon_small_save   = QIcon(self.application.PATH_ICONS_SMALL + "table_save.png")
		self.icon_small_close  = QIcon(self.application.PATH_ICONS_SMALL + "table_close.png")

		self.icon_small_fields = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")

		self.icon_small_up     = QIcon(self.application.PATH_ICONS_SMALL + "arrow_up.png")
		self.icon_small_down   = QIcon(self.application.PATH_ICONS_SMALL + "arrow_down.png")

	def __init_objects__(self):
		self._groups      = CCatalogFieldGroups(self.application.sql_connection)
		self._group       = CCatalogFieldGroup(self.application.sql_connection)
		self._equipments  = CEquipments(self.application.sql_connection)
		self._equipment   = CEquipment(self.application.sql_connection)

		self.model_fields = QStandardItemModel()

	def __init_menu__(self):
		menu_actions = QMenu("Действия")
		menu_actions.addAction(self.action_save)
		menu_actions.addAction(self.action_save_as_copy)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_open)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_delete)
		menu_actions.addSeparator()
		menu_actions.addAction(self.action_close)

		self.menuBar().addMenu(menu_actions)

	def __init_ui__(self):
		super(FormEquipment, self).__init_ui__()
		
		self.setWindowTitle("ОС и ТМЦ")
		self.setMinimumSize(460, 640)

		self._init_tabs_()

	def _init_tabs_(self):
		self.tabs = QTabWidget()
		self.field_note = QLineEdit()
		self.field_note.setPlaceholderText("Примечание")

		central_layout = QVBoxLayout()
		central_layout.setContentsMargins(3, 3, 3, 3)
		central_layout.setSpacing(3)
		central_layout.addWidget(self.tabs)
		central_layout.addWidget(self.field_note)

		central_widget = QWidget()
		central_widget.setLayout(central_layout)

		self.setCentralWidget(central_widget)

		self._init_tab_main_()

	def _init_tab_main_(self):
		self.tree_fields = QTreeView()
		self.tree_fields.setMinimumWidth(300)
		self.tree_fields.setModel(self.model_fields)
		self.tree_fields.header().hide()
		self.tree_fields.setAlternatingRowColors(True)

		self.field_values = QListWidget()

		splitter_main = QSplitter()
		splitter_main.setContentsMargins(3, 3, 3, 3)
		splitter_main.addWidget(self.tree_fields)
		splitter_main.addWidget(self.field_values)

		self.tabs.addTab(splitter_main, "Характеристики")

	def _set_field(self, in_field="", in_value=""):
		_group = extract_field_group(in_field)
		_field = extract_field_name(in_field)

		_item_group = None
		_item_field = None
		_item_value = QStandartItemWithID(in_value)

		for _index_row in range(self.model_fields.rowCount()):
			_item_group = self.model_fields.item(_index_row)

			if _item_group.text() == _group:
				for _index_row in range(_group.childCount()):
					# TODO
					pass

				break

	def load_fields(self):
		self.model_fields.clear()

		list_groups = self._groups.get_list()

		for group in list_groups:
			self._group.load(group)

			item_group = QStandartItemWithID(self._group.name, None)
			item_group.setCheckable(True)

			list_fields = self._group.get_fields()
			for field in list_fields:
				item_group.appendRow([QStandartItemWithID(field, None), NoneModelItem()])

			self.model_fields.appendRow([item_group, NoneModelItem()])

	def load(self, in_id=None):
		self.load_fields()

		if in_id is not None:
			self._equipment.load(in_id)

			self.setWindowTitle("{} - {} {}".format(self._equipment.base.subcategory, self._equipment.base.brand, self._equipment.base.model))

			_list_fields = self._equipment.fields.get_list()

			for _field in _list_fields:
				_value = self._equipment.fields.get_field(_field)

				self._set_field(_field, _value)

		self._gui_resize_fields()

		self.showCentered()

	def _gui_resize_fields(self):
		self.tree_fields.resizeColumnToContents(0)

	def save(self):
		self._equipment.clear()

		for index_group in range(self.model_fields.rowCount()):
			item_group = self.model_fields.item(index_group)
			group      = item_group.text()

			if item_group.checkState() == Qt.Checked:
				for index_field in range(item_group.rowCount()):
					item_field = item_group.child(index_field, 0)
					item_value = item_group.child(index_field, 1)

					field      = item_field.text()
					value      = item_value.text()

					self._equipment.set(group, field, value)

		self._equipment.note = self.field_note.text()

		self._equipment.save()
