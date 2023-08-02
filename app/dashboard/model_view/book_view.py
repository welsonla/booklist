from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from datetime import datetime
from flask_admin.model import typefmt
from app.dashboard.model_view.admin_view import AdminView
from wtforms.fields import SelectField

class BookView(AdminView):
    form_base_class = SecureForm
    page_size = 20

    column_list = ["name",  "author", 'category', "desc", "created_at", "updated_at"] #"cover_url",
    column_searchable_list = ["name", "author"]
    column_default_sort = ("created_at", True)
    column_filters = ["name"]

    # 自定义字段显示
    form_overrides = dict(category=SelectField)
    form_args = dict(
        category=dict(
            choices=[(0, 'waiting'), (1, 'in_progress'), (2, 'finished')]
        )
    )

    def __init__(self, *args, **kwargs):
        super(AdminView, self).__init__(*args, **kwargs)
        # super(AdminView, self).__init__(*args, **kwargs)

        self.static_folder = 'static'
        self.column_formatters = dict(typefmt.BASE_FORMATTERS)
        # self.column_formatters.update({
        #     type(None): typefmt.null_formatter,
        #     datetime: self.date_format
        # })

        self.column_type_formatters = self.column_formatters



    def date_format(self, view, value):
        return value.strftime('%B-%m-%Y %I:%M:%p')