from flask import Blueprint,views,render_template,request,url_for,session,redirect,g,jsonify
from .forms import loginForm,ResetpwdForm,ResetEmailForm
from .models import CMSUser
from .decorators import login_required
import config
from exts import db,mail
from flask_mail import Message
from utils import restful
import string
import random
from utils import zlcache

bp=Blueprint("cms",__name__,url_prefix="/cms")
# from .hooks import before_request

@bp.route("/")
@login_required
def index():
    return render_template("cms/cms_index.html")

@bp.route("/email/")
def send_email():
    message=Message("测试",["office2012.rain@gmail.com"],"hello world !")
    mail.send(message)
    return "success"

@bp.route("/email_captcha/")
def email_captcha():
    email=request.args.get("email")
    if not email:
        return restful.params_error("请输入邮箱")
    source=list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha="".join(random.sample(source,6))
    zlcache.set(email,captcha)
    message=Message("验证码",[email],"您的验证码是:%s"%captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    return restful.success()

@bp.route("/logout/")
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for("cms.login"))
@bp.route("/profile/")
def profile():
    return render_template("cms/cms_profile.html")

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
            message=form.get_error()
            return self.get(message=message)
class ResetPwdView(views.MethodView):
    def get(self):
        return render_template("cms/cms_resetpwd.html")
    def post(self):
        form=ResetpwdForm(request.form)
        if form.validate():
            newpwd=form.newpwd.data
            oldpwd=form.oldpwd.data
            user=g.cms_user
            if user.check_password(oldpwd):
                user.password=newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.get_error())
class ResetEmailView(views.MethodView):
    def get(self):
        return render_template("cms/cms_resetemail.html")
    def post(self):
        form=ResetEmailForm(request.form)
        if form.validate():
            g.cms_user.email=form.email.data
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())
bp.add_url_rule("/resetemail/",view_func=ResetEmailView.as_view("resetemail"))
bp.add_url_rule("/resetpwd/",view_func=ResetPwdView.as_view("resetpwd"))
bp.add_url_rule("/login/",view_func=loginView.as_view("login"))




