from wtforms import StringField,IntegerField
from wtforms.validators import Email,Length,InputRequired,EqualTo,ValidationError
from ..forms import BaseFrom
from utils import zlcache
from flask import g

class loginForm(BaseFrom):
    email=StringField(validators=[Email(message="请输入争取到邮箱格式"),InputRequired(message="请输入邮箱")])
    password=StringField(validators=[Length(min=3,max=20,message="请输入正确格式的密码")])
    remember=IntegerField()
class ResetpwdForm(BaseFrom):
    oldpwd=StringField(validators=[Length(min=3,max=20,message="请输入正确格式旧密码")])
    newpwd=StringField(validators=[Length(min=3,max=20,message="请输入正确格式新密码")])
    newpwd2=StringField(validators=[EqualTo("newpwd")])

class ResetEmailForm(BaseFrom):
    email=StringField(validators=[Email("请输入正确格式的邮箱")])
    captcha=StringField(validators=[Length(min=6,max=6,message="请输入正确长度的验证码!")])

    def validate_captcha(self,field):
        captcha=field.data
        email=self.email.data
        captcha_cache=zlcache.get(email)
        if not captcha_cache or captcha_cache.lower()!=captcha.lower():
            raise ValidationError("邮箱验证码错误")
    def validate_email(self,field):
        email=field.data
        if g.cms_user.email==email:
            raise ValidationError("不能修改为相同的邮箱")