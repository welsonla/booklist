from flask_admin.form import SecureForm
from app.dashboard.model_view.admin_view import AdminView
from wtforms.fields import SelectField
from flask import render_template, request,flash, redirect
from app.models.quote import Quote
from app.models.user import User
from app.models.favorite import Favorite
from app.extensions import db

class QuoteView(AdminView):
    form_base_class = SecureForm
    # 定义分页数量
    page_size = 10
    # 定义查询列表
    column_list = ["id",  "chapter", 'page', 'comment', "created_at", "updated_at"] #"cover_url",
    # column_searchable_list = ["name", "author"]
    column_default_sort = ("created_at", True)
    # column_filters = ["name"]

    # 自定义字段显示
    # form_overrides = dict(category=SelectField)
    # form_args = dict(
    #     category=dict(
    #         choices=[(0, '正常'), (1, '下架')]
    #     )
    # )

    column_widths = {
        "chapter":150,
        "page": 80,
        "comment": 200
    }

    column_labels = {
        "chapter":"章节",
        # "content": "摘抄",
        "page":"页码",
        "comment":"笔记",
        "state":"状态",
        "created_at": "创建时间",
        "updated_at": "更新时间",
    }

    def delete(self):
        params = request.form.to_dict()
        note_id = params.get("id")
        # 检查笔记是否存在
        quote = Quote.query.filter_by(id=note_id).first()
        if quote is not None:
            quote.state = 1
            db.session.commit()
            # 从用户收藏表查找用户的收藏记录
            favorites = Favorite.query.filter_by(type=2, item_id=quote.id).all()
            for item in favorites:
                item.state = 1
                db.session.delete(item)
            #保存变更状态
            db.session.commit()

            return redirect('/admin/notes')
        else:
            flash["message"] = "更新笔记状态失败"