from core_gui     import *
from core_objects import *


class FormServiceFields(CForm):
	_groups     = CCatalogFieldGroups
	_equipments = CEquipments
	_group      = CCatalogFieldGroup

	tabs        = QTabWidget

	def __init_actions__(self):
		self.action_exec = QAction(self.icon_small_gears, "Выполнить", None)

	def __init_events__(self):
		self.tree_r_field_to.clicked.connect(self.select_replace_field_field)
		self.tree_r_value_from.clicked.connect(self.select_set_value_field)
		self.action_exec.triggered.connect(self.exec)
		self.tabs.currentChanged.connect(self.select_tab)

	def __init_icons__(self):
		self.icon_small_fields    = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")
		self.icon_small_gears     = QIcon(self.application.PATH_ICONS_SMALL + "gears.png")
		self.icon_small_search    = QIcon(self.application.PATH_ICONS_SMALL + "search_field.png")

	def __init_objects__(self):
		self._groups     = CCatalogFieldGroups(self.application.sql_connection)
		self._equipments = CEquipments(self.application.sql_connection)
		self._group      = CCatalogFieldGroup(self.application.sql_connection)

	def __init_menu__(self):
		self.menu_actions = QMenu("Действия")

		self.menu_actions.addAction(self.action_exec)

		self.menuBar().addMenu(self.menu_actions)

	def __ui__(self):
		self.setMinimumSize(640, 480)
		self.setWindowTitle("Обработка характеристик")

		self.tabs = QTabWidget()

		self.setCentralWidget(self.tabs)
		self.setContentsMargins(3, 3, 3, 3)

		self._init_tab_replace_field_()
		self._init_tab_set_value_()

	def _exec_replace_field(self):
		_from_group = ""
		_from_field = ""
		_to_group   = self.le_r_field_to_group.text()
		_to_field   = self.le_r_field_to_field.text()

		_item  = self.tree_r_field_from.currentItem()

		if _item is not None:
			_parent = _item.parent()

			if _parent is None:
				_from_group = _item.text(0)
			else:
				_from_group = _parent.text(0)
				_from_field = _item.text(0)

		_from = _from_group
		if not _from_field == "":
			_from += "/"
			_from += _from_field

		_to   = _to_group
		if not _to_field == "":
			_to += "/"
			_to += _to_field

		_dialog     = QMessageBox()
		_result     = _dialog.question(self,
		                               "Замена характеристик",
		                               "Подтвердите замену \n {} на \n {}".format(_from,
		                                                                          _to),
		                               QMessageBox.Yes | QMessageBox.No)

		if _result:
			_result = self._equipments.replace_field(_from, _to)

			if _result:
				self.show_message("Выполнено: {} -> {}".format(_from, _to))
			else:
				self.show_message("SQL Ошибка: {} -> {}".format(_from, _to), 10000)

	def _exec_set_value(self):
		_from_group = ""
		_from_field = ""

		_item  = self.tree_r_value_from.currentItem()

		if _item is not None:
			_parent = _item.parent()

			if _parent is None:
				_from_group = _item.text(0)
			else:
				_from_group = _parent.text(0)
				_from_field = _item.text(0)

		_field = _from_group
		if not _from_field == "":
			_field += "/"
			_field += _from_field

		_value   = self.le_r_value_to_value.text()

		_dialog     = QMessageBox()
		_result     = _dialog.question(self,
		                               "Запись значения",
		                               "Подтвердите запись  \n{} в \n{}".format(_value,
		                                                                          _field),
		                               QMessageBox.Yes | QMessageBox.No)

		if _result:
			_result = self._equipments.set_value(_field, _value)

			if _result:
				self.show_message("Выполнено: {} -> {}".format(_value, _field))
			else:
				self.show_message("SQL Ошибка: {} -> {}".format(_value, _field), 10000)

	def _init_tab_replace_field_(self):
		self.tree_r_field_from = QTreeWidget()
		self.tree_r_field_from.clear()

		self.tree_r_field_to   = QTreeWidget()
		self.tree_r_field_to.clear()

		self.le_r_field_to_group = QLineEdit()
		self.le_r_field_to_group.setPlaceholderText("Группа")

		self.le_r_field_to_field = QLineEdit()
		self.le_r_field_to_field.setPlaceholderText("Характеристика")

		layout_r_field = QGridLayout()
		layout_r_field.setSpacing(3)
		layout_r_field.setContentsMargins(3, 3, 3, 3)
		layout_r_field.addWidget(self.tree_r_field_from, 0, 0, 3, 1)
		layout_r_field.addWidget(self.tree_r_field_to, 0, 1)
		layout_r_field.addWidget(self.le_r_field_to_group, 1, 1)
		layout_r_field.addWidget(self.le_r_field_to_field, 2, 1)

		panel_r_field = QWidget()
		panel_r_field.setLayout(layout_r_field)

		self.tabs.addTab(panel_r_field, self.icon_small_fields, "Замена названия")

	def _init_tab_set_value_(self):
		self.tree_r_value_from  = QTreeWidget()
		self.tree_r_value_from.clear()

		self.list_r_value_values = QListWidget()
		self.list_r_value_values.clear()

		self.le_r_value_to_value = QLineEdit()
		self.le_r_value_to_value.setPlaceholderText("Значение")

		layout_r_value = QGridLayout()
		layout_r_value.setSpacing(3)
		layout_r_value.setContentsMargins(3, 3, 3, 3)
		layout_r_value.addWidget(self.tree_r_value_from, 0, 0, 2, 1)
		layout_r_value.addWidget(self.list_r_value_values, 0, 1)
		layout_r_value.addWidget(self.le_r_value_to_value, 1, 1)

		panel_r_value = QWidget()
		panel_r_value.setLayout(layout_r_value)

		self.tabs.addTab(panel_r_value, self.icon_small_search, "Запись значения")

	def exec(self):
		_tab_index = self.tabs.currentIndex()

		if   _tab_index == 0:
			self._exec_replace_field()
		elif _tab_index == 1:
			self._exec_set_value()

	def load_replace_field(self):
		_list_groups = self._equipments.get_list_groups()

		_list_groups = list(set(_list_groups))
		_list_groups.sort()

		self.tree_r_field_from.clear()
		self.tree_r_field_from.header().hide()

		for _group in _list_groups:
			list_fields = self._equipments.get_list_fields(_group)

			item_group = QTreeWidgetItem()
			item_group.setText(0, _group)

			for _field in list_fields:
				item_field = QTreeWidgetItem()
				item_field.setText(0, _field)

				item_group.addChild(item_field)

			self.tree_r_field_from.addTopLevelItem(item_group)

		_list_groups += self._groups.get_list()
		_list_groups  = list(set(_list_groups))
		_list_groups.sort()

		self.tree_r_field_to.clear()
		self.tree_r_field_to.header().hide()

		for _group in _list_groups:
			item_group = QTreeWidgetItem()
			item_group.setText(0, _group)

			self._group.load(_group)
			list_fields  = self._equipments.get_list_fields(_group)
			list_fields += self._group.get_fields()
			list_fields  = list(set(list_fields))
			list_fields.sort()

			for _field in list_fields:
				item_field = QTreeWidgetItem()
				item_field.setText(0, _field)

				item_group.addChild(item_field)

			self.tree_r_field_to.addTopLevelItem(item_group)

		self.tree_r_field_from.sortByColumn(0, Qt.AscendingOrder)
		self.tree_r_field_to.sortByColumn(0, Qt.AscendingOrder)

	def load_set_value(self):
		_list_groups = self._equipments.get_list_groups()

		_list_groups = list(set(_list_groups))
		_list_groups.sort()

		self.tree_r_value_from.clear()
		self.tree_r_value_from.header().hide()

		for _group in _list_groups:
			list_fields = self._equipments.get_list_fields(_group)

			item_group = QTreeWidgetItem()
			item_group.setText(0, _group)

			for _field in list_fields:
				item_field = QTreeWidgetItem()
				item_field.setText(0, _field)

				item_group.addChild(item_field)

			self.tree_r_value_from.addTopLevelItem(item_group)

		self.tree_r_value_from.sortByColumn(0, Qt.AscendingOrder)

	def select_replace_field_field(self):
		_current_item   = self.tree_r_field_to.currentItem()
		_current_parent = None

		if _current_item is not None:
			_current_parent = _current_item.parent()

		if _current_parent is not None:
			self.le_r_field_to_group.setText(_current_parent.text(0))
			self.le_r_field_to_field.setText(_current_item.text(0))
		else:
			if _current_item is not None:
				self.le_r_field_to_group.setText(_current_item.text(0))

	def select_set_value_field(self):
		_current_item   = self.tree_r_value_from.currentItem()
		_current_parent = None

		if _current_item is not None:
			_current_parent = _current_item.parent()

		if _current_parent is not None:
			_field = "{}/{}".format(_current_parent.text(0),
			                        _current_item.text(0))
			self.list_r_value_values.clear()
			self.list_r_value_values.addItems(self._equipments.get_list_values(_field))
		else:
			self.list_r_value_values.clear()

	def select_tab(self):
		_tab_index = self.tabs.currentIndex()

		if   _tab_index == 0:
			self.load_replace_field()
		elif _tab_index == 1:
			self.load_set_value()

	def open_replace_field(self):
		self.load_replace_field()
		self.showCentered()
		self.tabs.setCurrentIndex(0)

	def open_set_value(self):
		self.load_set_value()
		self.showCentered()
		self.tabs.setCurrentIndex(1)

