from flask_admin.form import SecureForm
from markupsafe import Markup

from app.dashboard.model_view.admin_view import AdminView
from wtforms.fields import SelectField
from flask import render_template, request,flash, redirect
from app.models.book import Book
from app.extensions import db
class BookView(AdminView):
    def _cover_image(self, context, model, name):
        return Markup('<img src="%s" style="width:100px;height:150px;"'%(model.image_url))

    form_base_class = SecureForm
    # 定义分页数量
    page_size = 15
    # 定义查询列表
    column_list = ["id","image_url", "name",  "author", 'category', "created_at", "updated_at"] #"cover_url",
    column_searchable_list = ["name", "author"]
    column_default_sort = ("created_at", True)
    column_filters = ["name"]

    # 自定义字段显示
    form_overrides = dict(category=SelectField)
    form_args = dict(
        category=dict(
            choices=[(0, '正常'), (1, '下架')]
        )
    )

    column_formatters = {
        'image_url': _cover_image
    }

    # 自定义列显示
    column_labels = {
        "name":"书名",
        "author": "作者",
        "category":"类目",
        "created_at": "创建时间",
        "updated_at": "更新时间",
    }

    def add(self,view):
        # 从请求中获取表单信息
        params = request.form.to_dict()
        book_name = params["name"]
        isbn = params["isbn"]
        # 检查书籍信息是否重复
        exists_book = Book.query.filter_by(book_name=book_name,isbn=isbn).first()
        if exists_book is None:
            book = Book(**params)
            db.session.add(book)
            db.session.commit()
            return redirect('/admin/book')
        else:
            flash["message"] = "书籍信息重复"



