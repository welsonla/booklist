from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from app.dashboard.model_view.admin_view import AdminView
class UserView(AdminView):
    form_base_class = SecureForm
    page_size = 20
    column_exclude_list = ['password_hash']
    can_delete = False
    can_create = False

    def __init__(self, *args, **kwargs):
        super(AdminView, self).__init__(*args, **kwargs)