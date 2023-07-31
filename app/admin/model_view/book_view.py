from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
class BookView(ModelView):
    form_base_class = SecureForm
    page_size = 20