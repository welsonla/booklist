from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

class DashboardView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')