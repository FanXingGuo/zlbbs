from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,Length,InputRequired

class loginForm(Form):
    email=StringField(validators=[Email(message="请输入争取到邮箱格式"),InputRequired(message="请输入邮箱")])
    password=StringField(validators=[Length(min=3,max=20,message="请输入正确格式的密码")])
    remember=IntegerField()
