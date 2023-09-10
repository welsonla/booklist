from flask_admin.form import SecureForm
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
    column_list = ["id",  "name", 'like_count', "created_at", "updated_at"] #"cover_url",
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

    # column_widths = {
    #     "chapter":150,
    #     "page": 80,
    #     "comment": 200
    # }
    #
    column_labels = {
        "name":"书单名称",
        # "content": "摘抄",
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