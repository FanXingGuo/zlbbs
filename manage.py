from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from zlbbs import create_app
from exts import db

from apps.cms import models as cms_models
from apps.front import models as front_models
CMSUser=cms_models.CMSUser
CMSRole=cms_models.CMSRole
CMSPermission=cms_models.CMSPermission
FrontUser=front_models.FrontUser

app=create_app()
manager=Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)

#添加管理用户
@manager.option("-u","--username",dest="username")
@manager.option("-p","--password",dest="password")
@manager.option("-e","--email",dest="email")
def create_user(username,password,email):
    user=CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户添加成功")

#添加后台测试用户
@manager.command
def create_role():
    # 访问者
    visitor=CMSRole(name="访问者",desc="只能查看后台,不能作出修改")
    visitor.permissions=CMSPermission.VISITOR
    #运营人员
    operator=CMSRole(name="运营者",desc="管理帖子,管理评论,管理前台用户")
    operator.permissions=CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER
    #管理员
    admin=CMSRole(name="管理员",desc="拥有本系统所有权限")
    admin.permissions=CMSPermission.FRONTUSER|CMSPermission.VISITOR|CMSPermission.COMMENTER|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.BOARDER
    #开发者
    developer=CMSRole(name="开发者",desc="开发者人员专用角色")
    developer.permissions=CMSPermission.ALL_PERMISSION
    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()
    print("创建成功")

#测试后台用户权限
@manager.command
def test_permission():
    user=CMSUser.query.filter_by(username="visitor").first()
    if user.is_developer:
        print("这个用户有开发者权限")
    else:
        print("这个用户无开发者权限")

#给后台用户添加角色
@manager.option("-e","--email",dest="email")
@manager.option("-n","--name",dest="name")
def add_user_to_role(email,name):
    user=CMSUser.query.filter_by(email=email).first()
    role=CMSRole.query.filter_by(name=name).first()
    if user:
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户%s %s角色 添加成功!"%(email,name))
        else:
            print("%s角色不存在"%name)
    else:
        print("邮箱:%s,无这个用户"%email)

#添加前台用户
@manager.option("-t","--telephone",dest="telephone")
@manager.option("-u","--username",dest="username")
@manager.option("-p","--password",dest="password")
def create_front_user(telephone,username,password):
    user=FrontUser(telephone=telephone,password=password,username=username)
    db.session.add(user)
    db.session.commit()
    print("添加%s成功"%username)



if __name__ == '__main__':
    manager.run()