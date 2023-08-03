from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request
from flask_login import login_manager

class AdminView(ModelView):

    edit_template = 'admin/edit.html'
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    # FIXME: 添加用户登录判断
    # def is_accessible(self):
    #     # return session.get('user') == 'welsonla'
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     if not self.is_accessible():
    #         return redirect(url_for('main.login', next=request.url))