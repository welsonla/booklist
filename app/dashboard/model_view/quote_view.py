from flask_admin import expose
from flask_admin.form import SecureForm
from flask_admin.helpers import get_redirect_target
from flask_admin.model.template import EndpointLinkRowAction
from markupsafe import Markup

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
    column_list = ["id",  "chapter", 'page', "is_recommand", "updated_at"] #"cover_url",
    # column_searchable_list = ["name", "author"]
    column_default_sort = ("created_at", True)
    # column_filters = ["name"]

    column_searchable_list = ["content", "comment", "chapter"]
    form_excluded_columns = ['book','user']

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
        "content":"内容",
        "state":"状态",
        "is_recommand": "推荐状态",
        "created_at": "创建时间",
        "updated_at": "更新时间",
    }

    column_extra_row_actions = [
        EndpointLinkRowAction(
            'fa fa-heart glyphicon glyphicon-trash',
            'quote.activate_user_view',
        )
    ]

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
        """
            Activate user model view. Only GET method is allowed.
        """
        # return_url = get_redirect_target() or self.get_url('.index_view')
        #
        # id = request.args["id"]
        # model = self.get_one(id)
        #
        # if model is None:
        #     return redirect(return_url)
        #
        # if model.active:
        #     return redirect(return_url)
        #
        # model.active = True
        # model.save()
        #
        # return redirect(return_url)