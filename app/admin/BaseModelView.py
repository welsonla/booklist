from flask_admin.contrib.sqla import ModelView
import flask_login as login
from flask import redirect, request, url_for
from flask_admin.form import SecureForm
class BaseModelView(ModelView):

    can_delete = True
    page_size = 20
    can_view_details = True
    can_edit = True
    can_create = True
    form_base_class = SecureForm

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'), next=request.url)