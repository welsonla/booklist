from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from app.dashboard.model_view.admin_view import AdminView
from wtforms.fields import SelectField, DateField
from flask_babel import lazy_gettext
from app.models.user import User
from flask import render_template, request

class UserView(AdminView):
    form_base_class = SecureForm
    page_size = 20
    column_list = ["id", "name", "nickname", 'email', 'role', "created_at", "updated_at"]
    column_exclude_list = ['password_hash']
    can_delete = False
    can_create = False
    form_excluded_columns = ['password_hash', 'reviews', 'collects']

    column_searchable_list = ["name", "nickname", "email"]
    column_default_sort = ("created_at", True)
    column_filters = ["name"]

    # 自定义样式
    form_overrides = dict(state=SelectField,role=SelectField)
    form_args = dict(
        state=dict(
            choices=[(0, '正常'), (1, '冻结')]
        ),
        role=dict(
            choices=[(0,'管理员'),(1,'普通用户')]
        )
    )

    column_labels = {
        "name":"用户名",
        "nickname": "昵称",
        "bio":"个人简介",
        "email":"邮箱",
        "role":"角色",
        "state":"状态",
        "created_at": "创建时间",
        "updated_at": "更新时间",
    }

    column_formatters = {
        'role': lambda v, c, m, p: '管理员' if m.role == 0 else '用户'

        # 'is_recommand': lambda v, c, m, p: '未推荐' if m.is_recommand == 0 else '推荐'
    }

    def __init__(self, *args, **kwargs):
        super(AdminView, self).__init__(*args, **kwargs)

    def list(self):
        # 配置显示列
        page_size = 20
        column_list = ["id", "name", "nickname", 'email', "created_at", "updated_at"]
        # 隐藏用户密码展示
        column_exclude_list = ['password_hash']
        # 配置可搜索字段
        column_searchable_list = ["name", "nickname", "email"]
        # 设置过滤字段
        column_filters = ["name"]
        # 加载用户数据
        offset = min(0, request.get_data('offset'))
        users = User.query.order_by(User.id.desc()).limit(page_size).offset(offset).all()
        return render_template('user/index', users)

