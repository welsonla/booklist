from flask_admin import expose
from flask_admin.form import SecureForm
from flask_admin.model.template import EndpointLinkRowAction
from markupsafe import Markup

from app.dashboard.model_view.admin_view import AdminView
from wtforms.fields import SelectField
from flask import render_template, request,flash, redirect
from app.models.collect import Collect
from app.extensions import db

class CollectView(AdminView):
    form_base_class = SecureForm
    # 定义分页数量
    page_size = 10
    # 定义查询列表
    column_list = ["id",  "name", 'like_count', "is_recommand", "updated_at"] #"cover_url",
    # column_searchable_list = ["name", "author"]
    column_default_sort = ("created_at", True)

    column_extra_row_actions = [
        EndpointLinkRowAction(
            'fa fa-heart glyphicon glyphicon-trash',
            'quote.activate_user_view',
        )
    ]

    # form_excluded_columns = ['password_hash', 'reviews', 'collects']

    form_overrides = dict(is_recommand=SelectField)
    form_args = dict(
        is_recommand=dict(
            choices=[(0, '未推荐'), (1, '推荐')]
        )
    )

    column_searchable_list = ["name"]
    column_formatters = {
        'is_recommand': lambda v, c, m, p: Markup(
            "<span class='fa fa-heart glyphicon glyphicon-trash'></span>") if m.is_recommand == 0 else Markup(
            "<span class='fa fa-heart glyphicon glyphicon-trash' style='color:red;'></span>")

        # 'is_recommand': lambda v, c, m, p: '未推荐' if m.is_recommand == 0 else '推荐'
    }

    column_labels = {
        "name":"书单名称",
        "is_recommand": "推荐状态",
        "like_count":"收藏次数",
        "state":"状态",
        "created_at": "创建时间",
        "updated_at": "更新时间",
    }

    def recommend(self):
        # 从请求中获取书单信息
        params = request.form.to_dict()
        collect_id = params.get("id")
        # 检查当前书单是否存在
        collect = Collect.query.filter_by(id=collect_id).first()
        if collect is not None:
            collect.recomment = 1
            db.session.commit()
            return redirect('/admin/collect')
        else:
            flash["message"] = "书单信息不正确"



    expose('/activate/', methods=('GET',))
    def activate_user_view(self):
        print(f"Hello")