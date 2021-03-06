from exts import db
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class GenderEnum(enum.Enum):
    MALE=1
    FEMALE=2
    SECRET=3
    UNKNOW=4

class FrontUser(db.Model):
    __tablename__="front_user"
    id=db.Column(db.String(30),primary_key=True,default=shortuuid.uuid)
    telephone=db.Column(db.String(11),nullable=False,unique=True)
    username=db.Column(db.String(50),nullable=False)
    _password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(50),unique=True)
    realname=db.Column(db.String(50))
    avatar=db.Column(db.String(100))
    signature=db.Column(db.String(100))
    gender=db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time=db.Column(db.DateTime,default=datetime.now)


    @property
    def password(self):
        return self._password
    @password.setter
    def password(self,raw_password):
        self._password=generate_password_hash(raw_password)
    def check_password(self,raw_password):
        return check_password_hash(self.password,raw_password)
