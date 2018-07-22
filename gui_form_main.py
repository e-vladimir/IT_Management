from core_gui     import *
from core_objects import *


class FormMain(CForm):
	model_equipment = QStandardItemModel

	_equipments = CEquipments
	_equipment  = CEquipment

	_current_equipment_item = None

	def __init_actions__(self):
		self.action_select_equipment = QAction(self.icon_small_equipment, "Учёт ОС и ТМЦ",        None)
		self.action_catalogs_fields  = QAction(self.icon_small_equipment, "Характеристики",       None)

		self.action_equipment_add    = QAction(self.icon_small_add,       "Добавить ОС или ТМЦ",  None)
		self.action_equipment_delete = QAction(self.icon_small_delete,    "Удалить <ОС или ТМЦ>", None)

	def __init_events__(self):
		self.action_select_equipment.triggered.connect(self._select_equipments)

		self.action_equipment_add.triggered.connect(self.equipment_add)
		self.action_equipment_delete.triggered.connect(self.equipment_delete)

		self.action_catalogs_fields.triggered.connect(self.open_catalog_fields)

		self.panel_equipment.clicked.connect(self._equipment_get_current)
		self.panel_equipment.doubleClicked.connect(self.equipment_load)

	def __init_icons__(self):
		self.icon_small_equipment = QIcon(self.application.PATH_ICONS_SMALL + "equipments.png")
		self.icon_small_catalog   = QIcon(self.application.PATH_ICONS_SMALL + "catalog.png")

		self.icon_small_add       = QIcon(self.application.PATH_ICONS_SMALL + "table_row_insert.png")
		self.icon_small_delete    = QIcon(self.application.PATH_ICONS_SMALL + "table_row_delete.png")

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

		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_catalogs)

	def __init_objects__(self):
		self.model_equipment = QStandardItemModel()

		self._equipment  = CEquipment(self.application.sql_connection)
		self._equipments = CEquipments(self.application.sql_connection)

	def __init_ui__(self):
		super(FormMain, self).__init_ui__()

		self.setMinimumSize(800, 640)
		self.setWindowTitle("IT-management")

		self._init_panel_equipment_()

	def _init_panel_equipment_(self):
		self.panel_equipment = QTreeView()
		self.panel_equipment.setModel(self.model_equipment)
		self.panel_equipment.header().hide()
		self.panel_equipment.setEditTriggers(QTreeView.NoEditTriggers)

	def _select_equipments(self):
		self.equipments_load()

		self.menu_sections.setTitle(self.action_select_equipment.text())

		self.setCentralWidget(self.panel_equipment)

		self.menuBar().clear()
		self.menuBar().addMenu(self.menu_sections)
		self.menuBar().addMenu(self.menu_equipment)
		self.menuBar().addMenu(self.menu_catalogs)

	def _equipment_append_to_table(self, in_id=None):
		self._equipment.load(in_id)

		item_category        = QStandartItemWithID(self._equipment.base.category,       in_id)
		item_subcategory     = QStandartItemWithID(self._equipment.base.subcategory,    in_id)
		item_brand           = QStandartItemWithID(self._equipment.base.brand,          in_id)
		item_model           = QStandartItemWithID(self._equipment.base.model,          in_id)
		item_state           = QStandartItemWithID(self._equipment.base.state,          in_id)
		item_place_struct    = QStandartItemWithID(self._equipment.placement.struct,    in_id)
		item_place_placement = QStandartItemWithID(self._equipment.placement.placement, in_id)
		item_place_people    = QStandartItemWithID(self._equipment.placement.people,    in_id)
		item_note            = QStandartItemWithID(self._equipment.note,                in_id)

		item_brand.setFont(FONT_BOLD)
		item_model.setFont(FONT_BOLD)

		item_state.setFont(FONT_ITALIC)

		self.model_equipment.appendRow([item_category, item_subcategory, item_brand, item_model, item_state, item_place_struct, item_place_placement, item_place_people, item_note])

	def _equipment_get_current(self):
		_current_index = self.panel_equipment.currentIndex()
		_current_item  = self.model_equipment.itemFromIndex(_current_index)

		if _current_item is not None:
			_current_row   = _current_item.row()
			_current_item  = self.model_equipment.item(_current_row)

			self._current_equipment_item = _current_item
		else:
			self._current_equipment_item = None

		self.equipment_enable_disable()

	def equipment_add(self):
		self.application.form_equipment.new_and_show()

	def equipment_load(self):
		if self._current_equipment_item is not None:
			self.application.form_equipment.load(self._current_equipment_item.id)

	def equipments_load(self):
		self.model_equipment.clear()

		_list_id = self._equipments.get_list_id()

		for _id in _list_id:
			self._equipment_append_to_table(_id)

		self.equipments_resize()
		self._equipment_get_current()

	def equipments_resize(self):
		self.panel_equipment.hide()

		for index_col in range(self.model_equipment.columnCount()):
			self.panel_equipment.resizeColumnToContents(index_col)

		self.panel_equipment.show()

	def open_catalog_fields(self):
		self.application.form_catalog_fields.load_and_show()

	def equipment_enable_disable(self):
		self.action_equipment_delete.setEnabled(self._current_equipment_item is not None)

		if self._current_equipment_item is None:
			self.action_equipment_delete.setText("Удалить ОС и ТМЦ")
		else:
			_current_row = self._current_equipment_item.row()
			_item_brand = self.model_equipment.item(_current_row, 2)
			_item_model = self.model_equipment.item(_current_row, 3)
			_brand = _item_brand.text()
			_model = _item_model.text()

			self.action_equipment_delete.setText("Удалить {} {}".format(_brand, _model))

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
