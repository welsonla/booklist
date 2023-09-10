from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request
from flask_login import login_manager
from datetime import date
from flask_admin.model import typefmt
from flask_babelex import get_locale

# 自定义日期格式化
def date_format(view, value):
    return value.strftime('%Y-%m-%d %H:%M:%S')

MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: date_format
})

class AdminView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS

    edit_template = 'admin/edit.html'
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'

    column_labels = {
        "created_at":"创建时间",
        "updated_at": "更新时间",
    }

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

