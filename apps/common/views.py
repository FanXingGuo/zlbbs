from flask import Blueprint,request,make_response
from .forms import SMSCaptchaForm
from utils import restful
from utils import zlcache
from utils.captcha import Captcha
from io import BytesIO
bp=Blueprint("common",__name__,url_prefix="/c")

@bp.route("/")
def index():
    return "common index"

@bp.route("/sms_captcha/",methods=['POST'])
def sms_captcha():
    form=SMSCaptchaForm(request.form)
    if form.validate():
        telephone=form.telephone.data
        capt=Captcha.gene_text(number=4)
        # 发送验证码
        zlcache.set(telephone,capt)
        print("向手机{}发送验证码:{}".format(telephone,capt))
        return restful.success()
    else:
        return restful.params_error("手机号码格式有误")

@bp.route("/captcha/")
def graph_captcha():
    text,image=Captcha.gene_graph_captcha()
    zlcache.set(text.lower(),text.lower())
    out=BytesIO()
    image.save(out,"png")
    out.seek(0)
    resp=make_response(out.read())
    resp.content_type="image/png"
    return resp



