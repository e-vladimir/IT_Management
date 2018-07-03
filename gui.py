from core_gui                 import *
from core_sqlite              import *

from gui_form_main            import FormMain
from gui_form_catalogs_fields import FormCatalogsFields


class AppManage(CApplication):
	sql_connection = None

	form_catalogs_fields = FormCatalogsFields
	form_main            = FormMain

	version = "180206/1321"

	def __init__(self):
		super(AppManage, self).__init__()

		self.init_sql()
		self.init_forms()

	def init_sql(self):
		self.sql_connection = TSQLiteConnection('{0}/{1}'.format(self.PATH_COMMON, "db.sqlite"))

	def init_forms(self):
		self.form_catalogs_fields = FormCatalogsFields(self)
		self.form_main            = FormMain(self)


app = AppManage()
app.form_main.showMaximized()
# app.form_catalogs_fields.load_and_show()
sys.exit(app.exec_())
