from app import db


class Group(db.Model):

    __routename__ = "group"
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # 组名
    parent_id = db.Column(db.Integer, nullable=True)  # 父级ID
    permissions = db.relation(
        "Permission", secondary="group_permission_relation")


class Permission(db.Model):

    __routename__ = "permission"
    __tablename__ = "permission"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # 权限名称
    groups = db.relation("Group", secondary="group_permission_relation")


class Group_Permission_Relation(db.Model):

    __routename__ = "group_permission_relation"
    __tablename__ = "group_permission_relation"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'))
