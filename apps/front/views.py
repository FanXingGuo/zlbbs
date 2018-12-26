from flask import Blueprint,views,render_template,request,url_for,session
from .forms import SignupForm,SigninForm
from utils import restful
from .models import FrontUser
from exts import db
from utils import safeutils
import config
bp=Blueprint("front",__name__,url_prefix="")



@bp.route("/")
def index():
    return render_template("front/front_index.html")
@bp.route("/test/")
def test():
    return render_template("front/test.html")


class SignupView(views.MethodView):
    def get(self):
        return_to=request.referrer
        if return_to and return_to!=request.url and safeutils.is_safe_url(return_to):
            return render_template("front/front_signup.html",return_to=return_to)
        else:
            return render_template("front/front_signup.html")
    def post(self):
        form=SignupForm(request.form)
        if form.validate():
            #需要验证手机号码唯一
            telephone=form.telephone.data
            username=form.username.data
            password=form.password.data
            user=FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            message=form.get_error()
            return restful.params_error(message=message)
class SigninView(views.MethodView):
    def get(self):
        return_to=request.referrer
        if return_to and return_to !=request.url and return_to!=url_for("front.signin") and safeutils.is_safe_url(return_to):
            return render_template("front/front_signin.html",return_to=return_to)
        else:
            return render_template("front/front_signin.html")
    def post(self):
        form=SigninForm(request.form)

        if form.validate():
            telephone=form.telephone.data
            password=form.password.data
            remember=form.remember.data
            user=FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent=True
                return restful.success()
            else:
                return restful.params_error(message="用户名或密码错误")
        else:
            return restful.params_error(message=form.get_error())





bp.add_url_rule("/signin/",view_func=SigninView.as_view("signin"))
bp.add_url_rule("/signup/",view_func=SignupView.as_view("signup"))


