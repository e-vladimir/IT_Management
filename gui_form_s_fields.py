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
		self.replace_tree_to.doubleClicked.connect(self.select_replace_to)
		self.action_exec.triggered.connect(self.exec)

	def __init_icons__(self):
		self.icon_small_fields    = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")
		self.icon_small_gears     = QIcon(self.application.PATH_ICONS_SMALL + "gears.png")

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

		self._init_tab_replace_()

	def _init_tab_replace_(self):
		self.replace_tree_from = QTreeWidget()
		self.replace_tree_from.clear()

		self.replace_tree_to   = QTreeWidget()
		self.replace_tree_to.clear()

		self.replace_le_to_group = QLineEdit()
		self.replace_le_to_group.setPlaceholderText("Группа")

		self.replace_le_to_field = QLineEdit()
		self.replace_le_to_field.setPlaceholderText("Характеристика")

		layout_replace = QGridLayout()
		layout_replace.setSpacing(3)
		layout_replace.setContentsMargins(3, 3, 3, 3)
		layout_replace.addWidget(self.replace_tree_from,   0, 0, 3, 1)
		layout_replace.addWidget(self.replace_tree_to,     0, 1)
		layout_replace.addWidget(self.replace_le_to_group, 1, 1)
		layout_replace.addWidget(self.replace_le_to_field, 2, 1)

		panel_replace = QWidget()
		panel_replace.setLayout(layout_replace)

		self.tabs.addTab(panel_replace, self.icon_small_fields, "Замена характеристик")

		self.replace_load()

	def replace_load(self):
		_list_groups = self._equipments.get_list_groups()

		_list_groups = list(set(_list_groups))
		_list_groups.sort()

		self.replace_tree_from.clear()
		self.replace_tree_from.header().hide()

		for _group in _list_groups:
			list_fields = self._equipments.get_list_fields(_group)

			item_group = QTreeWidgetItem()
			item_group.setText(0, _group)

			for _field in list_fields:
				item_field = QTreeWidgetItem()
				item_field.setText(0, _field)

				item_group.addChild(item_field)

			self.replace_tree_from.addTopLevelItem(item_group)

		_list_groups += self._groups.get_list()
		_list_groups  = list(set(_list_groups))
		_list_groups.sort()

		self.replace_tree_to.clear()
		self.replace_tree_to.header().hide()

		for _group in _list_groups:
			list_fields = self._equipments.get_list_fields(_group)

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

			self.replace_tree_to.addTopLevelItem(item_group)

		self.replace_tree_from.sortByColumn(0, Qt.AscendingOrder)
		self.replace_tree_to.sortByColumn(0, Qt.AscendingOrder)

	def select_replace_to(self):
		_current_item = self.replace_tree_to.currentItem()

		if _current_item is not None:
			_current_parent = _current_item.parent()

		if _current_parent is not None:
			self.replace_le_to_group.setText(_current_parent.text(0))
			self.replace_le_to_field.setText(_current_item.text(0))
		else:
			if _current_item is not None:
				self.replace_le_to_group.setText(_current_item.text(0))

	def _exec_replace(self):
		_from_group = ""
		_from_field = ""
		_to_group   = self.replace_le_to_group.text()
		_to_field   = self.replace_le_to_field.text()

		_item  = self.replace_tree_from.currentItem()

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

	def exec(self):
		_tab_index = self.tabs.currentIndex()

		if _tab_index == 0:
			self._exec_replace()
