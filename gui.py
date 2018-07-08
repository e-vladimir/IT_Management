from core_gui                      import *
from core_sqlite                   import *

from gui_form_main                 import FormMain
from gui_form_c_fields import FormCatalogFields


class AppManage(CApplication):
	sql_connection            = None

	form_main                 = FormMain
	form_equip_catalog_fields = FormCatalogFields

	version = "180206/1321"

	def __init__(self):
		super(AppManage, self).__init__()

		self.init_sql()
		self.init_forms()

	def init_sql(self):
		self.sql_connection = TSQLiteConnection('{0}/{1}'.format(self.PATH_COMMON, "db.sqlite"))

	def init_forms(self):
		self.form_main                 = FormMain(self)
		self.form_equip_catalog_fields = FormCatalogFields(self)


app = AppManage()
# app.form_main.showMaximized()
app.form_equip_catalog_fields.load_and_show()
sys.exit(app.exec_())
