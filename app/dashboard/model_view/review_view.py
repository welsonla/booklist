from flask_admin import expose
from flask_admin.form import SecureForm
from flask_admin.model.template import EndpointLinkRowAction
from markupsafe import Markup

from app.dashboard.model_view.admin_view import AdminView
from wtforms.fields import SelectField
from flask import render_template, request,flash, redirect
from app.models.review import Review
from app.extensions import db

class ReviewView(AdminView):
    form_base_class = SecureForm
    # 定义分页数量
    page_size = 10
    # 定义查询列表
    # column_list = ["id", "title", 'is_recommand'],
    column_list = ["id", "title", 'is_recommand', "like_count", "updated_at"]  # "cover_url",
    column_default_sort = ("created_at", True)

    # 自定义字段显示
    # form_args = dict(
    #     is_recommand=dict(
    #         choices=[(0, '正常'), (1, '下架')]
    #     )
    # )

    form_overrides = dict(is_recommand=SelectField)
    form_args = dict(
        is_recommand=dict(
            choices=[(0, '未推荐'), (1, '推荐')]
        )
    )

    column_formatters = {
        'is_recommand': lambda v, c, m, p: Markup(
            "<span class='fa fa-heart glyphicon glyphicon-trash'></span>") if m.is_recommand == 0 else Markup(
            "<span class='fa fa-heart glyphicon glyphicon-trash' style='color:red;'></span>")

        # 'is_recommand': lambda v, c, m, p: '未推荐' if m.is_recommand == 0 else '推荐'
    }

    # column_choices = {
    #     'is_recommand': [
    #         (0, '未推荐'),
    #         (1,'推荐')
    #     ]
    # }

    column_searchable_list = ["title", "content"]

    column_extra_row_actions = [
        EndpointLinkRowAction(
            'fa fa-heart glyphicon glyphicon-trash',
            'quote.activate_user_view',
        )
    ]

    column_widths = {
        "chapter":150,
        "page": 80,
        "comment": 200
    }

    column_labels = {
        "title":"标题",
        "like_count": "收藏次数",
        "content":"内容",
        "is_recommand":"推荐状态",
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

    @expose('/activate/', methods=('GET',))
    def activate_user_view(self):
        print(f"Hello")