from flask import Blueprint,views,render_template,request,url_for,session,redirect
from .forms import loginForm
from .models import CMSUser
from .decorators import login_required
import config

bp=Blueprint("cms",__name__,url_prefix="/cms")

@bp.route("/")
@login_required
def index():
    return "cms index"

class loginView(views.MethodView):
    def get(self,message=None):
        return render_template("cms/login.html",message=message)
    def post(self):
        form=loginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            remember=form.remember.data
            user=CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID]=user.id
                if remember:
                    session.permanent=True
                return redirect(url_for("cms.index"))
            else:
                return self.get(message="用户名或密码错误")
        else:
            # print(form.errors)
            message=form.errors.popitem()[1][0]
            return self.get(message=message)

bp.add_url_rule("/login/",view_func=loginView.as_view("login"))
