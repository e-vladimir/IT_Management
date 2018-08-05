from core_gui     import *
from core_objects import *


class FormMain(CForm):
	model_equipments = QStandardItemModel

	_equipments = CEquipments
	_equipment  = CEquipment

	_current_equipment_item = None

	def __init_actions__(self):
		self.action_select_equipment       = QAction(self.icon_small_equipment, "Учёт ОС и ТМЦ",        None)
		self.action_catalogs_fields        = QAction(self.icon_small_equipment, "Характеристики",       None)

		self.action_equipment_add          = QAction(self.icon_small_add,       "Добавить ОС или ТМЦ",  None)
		self.action_equipment_delete       = QAction(self.icon_small_delete,    "Удалить <ОС или ТМЦ>", None)

		self.action_equipment_refresh      = QAction(self.icon_small_refresh,   "Обновить список",      None)

		self.action_service_replace_fields = QAction(self.icon_small_fields,    "Замена названия",      None)
		self.action_service_set_value      = QAction(self.icon_small_search,    "Запись значения",      None)

	def __init_events__(self):
		self.action_select_equipment.triggered.connect(self._select_equipments)

		self.action_equipment_add.triggered.connect(self.equipment_add)
		self.action_equipment_delete.triggered.connect(self.equipment_delete)
		self.action_equipment_refresh.triggered.connect(self.equipments_load)

		self.action_catalogs_fields.triggered.connect(self.open_catalog_fields)

		self.action_service_replace_fields.triggered.connect(self.open_service_replace_fields)
		self.action_service_set_value.triggered.connect(self.open_service_set_value)

		self.panel_equipment.clicked.connect(self._equipments_get_current)
		self.panel_equipment.doubleClicked.connect(self.equipment_load)
		self.panel_equipment.expanded.connect(self.equipments_resize)
		self.panel_equipment.collapsed.connect(self.equipments_resize)

	def __init_icons__(self):
		self.icon_small_equipment = QIcon(self.application.PATH_ICONS_SMALL + "equipments.png")
		self.icon_small_catalog   = QIcon(self.application.PATH_ICONS_SMALL + "catalog.png")
		self.icon_small_fields    = QIcon(self.application.PATH_ICONS_SMALL + "fields.png")
		self.icon_small_search    = QIcon(self.application.PATH_ICONS_SMALL + "search_field.png")

		self.icon_small_add       = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete    = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

		self.icon_small_refresh   = QIcon(self.application.PATH_ICONS_SMALL + "arrow_refresh_small.png")

	def __init_menu__(self):
		self.menu_sections  = QMenu("Раздел")
		self.menu_sections.addAction(self.action_select_equipment)

		self.menu_catalogs  = QMenu("Каталоги")
		self.menu_catalogs.addAction(self.action_catalogs_fields)

		self.menu_equipment = QMenu("Действия")
		self.menu_equipment.setVisible(False)
		self.menu_equipment.addAction(self.action_equipment_add)
		self.menu_equipment.addSeparator()
		self.menu_equipment.addAction(self.action_equipment_delete)
		self.menu_equipment.addSeparator()
		self.menu_equipment.addAction(self.action_equipment_refresh)

		self.menu_service   = QMenu("Сервис")
		self.menu_service.addAction(self.action_service_replace_fields)
		self.menu_service.addAction(self.action_service_set_value)

		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_catalogs)
		self.menuBar().addMenu(self.menu_service)

	def __init_objects__(self):
		self.model_equipments = QStandardItemModel()

		self._equipment  = CEquipment(self.application.sql_connection)
		self._equipments = CEquipments(self.application.sql_connection)

	def __ui__(self):
		self.setMinimumSize(800, 640)
		self.setWindowTitle("IT-management")

		self._init_panel_equipment_()

	def _init_panel_equipment_(self):
		self.panel_equipment = QTreeView()
		self.panel_equipment.setModel(self.model_equipments)
		self.panel_equipment.setEditTriggers(QTreeView.NoEditTriggers)
		self.panel_equipment.header().hide()

	def _equipment_append_to_table(self, in_id=None):
		_color_group    = QColor.fromRgb(230, 230, 230)
		_color_subgroup = QColor.fromRgb(240, 240, 240)

		self._equipment.load(in_id)

		item_brand           = QStandartItemWithID(self._equipment.base.brand,          in_id)
		item_model           = QStandartItemWithID(self._equipment.base.model,          in_id)
		item_state           = QStandartItemWithID(self._equipment.base.state,          in_id)
		item_place_struct    = QStandartItemWithID(self._equipment.placement.struct,    in_id)
		item_place_placement = QStandartItemWithID(self._equipment.placement.placement, in_id)
		item_place_people    = QStandartItemWithID(self._equipment.placement.people,    in_id)
		item_note            = QStandartItemWithID(self._equipment.note,                in_id)

		item_acc_number      = QStandartItemWithID(self._equipment.accounting.number,   in_id)
		item_acc_people      = QStandartItemWithID(self._equipment.accounting.people,   in_id)

		item_brand.setFont(FONT_BOLD)
		item_model.setFont(FONT_BOLD)

		item_note.setFont(FONT_ITALIC)

		item_acc_number.setForeground(Qt.darkBlue)
		item_acc_people.setForeground(Qt.darkBlue)

		list_items           = [item_state,
		                        item_brand,
		                        item_model,
		                        item_place_struct,
		                        item_place_placement,
		                        item_place_people,
		                        item_note,
		                        item_acc_number,
		                        item_acc_people]

		item_category        = None
		item_subcategory     = None

		for _row in range(self.model_equipments.rowCount()):
			_item = self.model_equipments.item(_row)

			if _item.text() == self._equipment.base.category:
				item_category = _item

				break

		if item_category is None:
			item_category = QStandartItemWithID(self._equipment.base.category)
			item_category.setBackground(_color_group)
			self.model_equipments.appendRow([item_category] + [QNoneModelItem(_color_group) for index in range(len(list_items) - 1)])

		for _row in range(item_category.rowCount()):
			_item = item_category.child(_row)

			if _item.text() == self._equipment.base.subcategory:
				item_subcategory = _item

				break

		if item_subcategory is None:
			item_subcategory = QStandartItemWithID(self._equipment.base.subcategory)
			item_subcategory.setBackground(_color_subgroup)
			item_category.appendRow([item_subcategory]  + [QNoneModelItem(_color_subgroup) for index in range(len(list_items) - 1)])

		if (item_category is not None) and (item_subcategory is not None):
			item_subcategory.appendRow(list_items)

	def _equipments_get_current(self):
		if self._equipment_get_level() == 2:
			_current_index = self.panel_equipment.currentIndex()
			_current_item  = self.model_equipments.itemFromIndex(_current_index)

			if _current_item is not None:
				_current_row    = _current_item.row()
				_current_parent = _current_item.parent()

				if _current_parent is not None:
					_current_item = _current_parent.child(_current_row)
				else:
					_current_item = None

				self._current_equipment_item = _current_item
			else:
				self._current_equipment_item = None
		else:
			self._current_equipment_item = None

		self.equipments_enable_disable()
		self._equipments_expand()

	def _equipments_expand(self):
		_index = self.panel_equipment.currentIndex()

		if _index is not None:
			self.panel_equipment.setExpanded(_index, True)

	def _equipment_get_level(self):
		_index = self.panel_equipment.currentIndex()
		_item  = self.model_equipments.itemFromIndex(_index)
		_level = 0

		if _item is not None:
			_parent = _item.parent()

			while _parent is not None:
				_item   = _parent
				_parent = _item.parent()

				_level += 1

		return _level

	def _select_equipments(self):
		self.equipments_load()

		self.menu_sections.setTitle(self.action_select_equipment.text())

		self.setCentralWidget(self.panel_equipment)

		self.menuBar().clear()
		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_equipment)
		self.menuBar().addMenu(self.menu_catalogs)
		self.menuBar().addMenu(self.menu_service)

	def equipment_add(self):
		self.application.form_equipment.new_and_show()

	def equipment_delete(self):
		_dialog = QMessageBox()

		self._equipment.load(self._current_equipment_item.id)

		_result = _dialog.question(self,
		                           "Удаление ОС и ТМЦ",
		                           "Подтвердите удаление: {} {}".format(self._equipment.base.brand,
		                                                                self._equipment.base.model),
		                           QMessageBox.Yes | QMessageBox.No)

		if _result == QMessageBox.Yes:
			self._equipment.delete()

			self.equipments_load()

	def equipment_load(self):
		if self._current_equipment_item is not None:
			self.application.form_equipment.load(self._current_equipment_item.id)

	def equipments_enable_disable(self):
		self.action_equipment_delete.setEnabled(self._current_equipment_item is not None)

		if self._current_equipment_item is None:
			self.action_equipment_delete.setText("Удалить ОС и ТМЦ")
		else:
			_parent     = self._current_equipment_item.parent()
			_row        = self._current_equipment_item.row()
			_item_brand = _parent.child(_row, 1)
			_item_model = _parent.child(_row, 2)
			_brand      = _item_brand.text()
			_model      = _item_model.text()

			self.action_equipment_delete.setText("Удалить {} {}".format(_brand, _model))

	def equipments_load(self):
		self._equipments_get_current()

		if self._current_equipment_item is not None:
			_current_item_id = self._current_equipment_item.id
		else:
			_current_item_id = None

		self.model_equipments.clear()

		_list_id = self._equipments.get_list_id()

		for _id in _list_id:
			self._equipment_append_to_table(_id)

		self.panel_equipment.sortByColumn(0, Qt.AscendingOrder)

		for _row in range(self.model_equipments.rowCount()):
			_item  = self.model_equipments.item(_row)
			_index = self.model_equipments.indexFromItem(_item)

			self.panel_equipment.setExpanded(_index, True)

		self.equipments_jump_to_id(_current_item_id)

		self.equipments_resize()
		self._equipments_get_current()

	def equipments_jump_to_id(self, in_id=None):
		pass

	def equipments_resize(self):
		self.panel_equipment.hide()

		for index_col in range(self.model_equipments.columnCount()):
			self.panel_equipment.resizeColumnToContents(index_col)

		self.panel_equipment.show()

	def open_catalog_fields(self):
		self.application.form_catalog_fields.load_and_show()

	def open_service_replace_fields(self):
		self.application.form_service_fields.open_replace_field()

	def open_service_set_value(self):
		self.application.form_service_fields.open_set_value()

