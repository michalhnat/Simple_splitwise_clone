from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(100))
    amount = db.Column(db.Integer)
    paid_by = db.Column(db.Integer, db.ForeignKey('group_users.id'))
    debtors = db.relationship('Debtors', cascade="all, delete")
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

class Debtors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debt_amount = db.Column(db.Integer)
    group_user_id = db.Column(db.Integer, db.ForeignKey('group_users.id'))
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    expenses = db.relationship('Expense', cascade="all, delete")
    members = db.relationship('Group_users', cascade="all, delete")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Group_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    name = db.Column(db.String(100))
    expenses = db.relationship('Expense', cascade="all, delete")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    group_membership = db.relationship('Group_users')
    groups = db.relationship('Group')
    #debts = db.relationship('Debtors', cascade="all, delete")
    #{{ group.members[user[0]-1].name }}

'''
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    paid_by = db.Column(db.Integer, db.ForeignKey('group_users.id'))
    debtors = db.relationship('Debtors', cascade="all, delete")
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Debtors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debt_amount = db.Column(db.Integer)
    name = db.Column(db.String(100))
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.String(10000))
    expenses = db.relationship('Expense', cascade="all, delete")
    members = db.relationship('Group_users', cascade="all, delete")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Group_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    name = db.Column(db.String(100))
    expenses = db.relationship('Expense', cascade="all, delete")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    groups = db.relationship('Group')
    debts = db.relationship('Debtors', cascade="all, delete")

'''
