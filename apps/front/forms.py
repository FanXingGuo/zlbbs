from ..forms import BaseFrom
from wtforms import StringField
from wtforms.validators import regexp,EqualTo,ValidationError
from utils import zlcache

class SignupForm(BaseFrom):
    telephone=StringField(validators=[regexp(r'1[3578]\d{9}',message="请输入正确格式手机号码")])
    sms_captcha=StringField(validators=[regexp(r"\w{4}",message="请输入正确格式验证码")])
    username=StringField(validators=[regexp(r'.{2,20}',message="请输入正确格式用户名")])
    password=StringField(validators=[regexp(r'[0-9a-zA-Z_\.]{6,20}',message="请输入正确格式密码")])
    password2=StringField(validators=[EqualTo("password",message="两次输入密码不一致")])
    graph_captcha=StringField(validators=[regexp(r"\w{4}",message="请输入正确格式的图片验证码")])

    def validate_sms_captcha(self,field):
        if field.data!="1111":
            sms_captcha=field.data
            telephone=self.telephone.data
            sms_captcha_mem=zlcache.get(telephone)
            if not sms_captcha_mem or sms_captcha.lower()!= sms_captcha_mem.lower() :
                raise ValidationError(message="短信验证码错误")
    def validate_graph_captcha(self,field):
        if field.data != "1111":
            graph_captcha=field.data
            graph_captcha_mem=zlcache.get(graph_captcha.lower())
            if not graph_captcha_mem:
                raise ValidationError("图形验证码错误")

class SigninForm(BaseFrom):
    telephone = StringField(validators=[regexp(r'1[3578]\d{9}', message="请输入正确格式手机号码")])
    password = StringField(validators=[regexp(r'[0-9a-zA-Z_\.]{6,20}', message="请输入正确格式密码")])
    remember = StringField()


