from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
class UserView(ModelView):
    form_base_class = SecureForm
    page_size = 20
    column_exclude_list = ['password_hash']