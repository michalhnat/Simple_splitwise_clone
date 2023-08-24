from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import Group, Group_users, Expense, Debtors, Payback
from . import db
from .calculations import Total_balance
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        members = []
        members.append((request.form.get('member_name').split(', ')))
        description = request.form.get('group')#Gets the note from the HTML
        name = request.form.get('group_name')
        name_check = Group.query.filter_by(name=name).first()
        print(name_check)
        if len(name) < 1:
            flash('Name is too short!', category='error')
        elif not name_check:
            new_group = Group(name=name, data=description, creator_id=current_user.id)  #providing the schema for the note
            db.session.add(new_group)  # adding the note to the database
            db.session.flush()
            db.session.refresh(new_group)
            db.session.add(Group_users(group_id=new_group.id, name=current_user.first_name))
            for n in members[0]:
                db.session.add(Group_users(group_id=new_group.id, name=n))
            db.session.commit()
            flash('Group added!', category='success')
        else:
            flash('Group with that name already exists!', category='error')

    return render_template("home.html", user=current_user)

@views.route('/group-view-<current_id>', methods=['GET', 'POST'])
@login_required
def group_view(current_id):
    group = Group.query.filter_by(id=current_id).first()
    members = group.members

    group_balance = Total_balance(members, group).get_balance()



    if request.method == "POST":
        expense_name = request.form.get("expense_name")
        expense_amount = int(request.form.get("expense_amount"))
        expense_payer = request.form.get("expense_payer")
        for m in members:
            if m.name == (expense_payer.replace(" (You)", "")).strip():
                expense_payer_id = m.id
        expense_split_bool = request.form.get("expense_split_bool")
        new_expense = Expense(name=expense_name, amount=expense_amount, paid_by=expense_payer_id, group_id=group.id)
        db.session.add(new_expense)
        db.session.flush()
        db.session.refresh(new_expense)
        split_among = []
        if expense_split_bool == None:
            for member in members:
                if request.form.get(f"expense_split_among_{member.id}") != None:
                    split_among.append(member.id)
            if not split_among: flash("Noone was checked", category='error')
            for m_id in split_among:
                new_debtor = Debtors(debt_amount = (expense_amount/len(split_among)), group_user_id=m_id, expense_id=new_expense.id)
                db.session.add(new_debtor)
                db.session.commit()
        else:
            for m in members:
                new_debtor = Debtors(debt_amount = (expense_amount/len(members)), group_user_id=m.id, expense_id=new_expense.id)
                db.session.add(new_debtor)
                db.session.commit()
    if group.creator_id == current_user.id:
        group_balance = Total_balance(members, group).get_balance()
        debt_settlement = Total_balance(members, group).simplify_debts()

        return render_template('group.html', user=current_user, group=group, group_balance=group_balance, transactions=debt_settlement)
    else:
        flash('You dont have access to that page', category='error')
        return render_template("home.html", user=current_user)


@views.route('/delete-group', methods=['POST'])
def delete_group():
    group = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    #print(group)
    groupId = group['groupId']
    group = Group.query.get(groupId)
    #group_users = Group_users.query.get(groupId)
    #print(group_users)
    if group:
        if group.creator_id == current_user.id:
            #db.session.delete(group_users)
            db.session.delete(group)
            db.session.commit()

    return jsonify({})

@views.route('/delete-expense', methods=['POST'])
def delete_expense():
    expense = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    expenseId = expense['ExpenseId']
    expense = Expense.query.get(expenseId)
    #group_users = Group_users.query.get(groupId)
    #print(group_users)
    if expense:
        db.session.delete(expense)
        db.session.commit()

    return jsonify({})

@views.route('/delete-payback', methods=['POST'])
def delete_payback():
    payback = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    PaybackId = payback['PaybackId']
    payback = Payback.query.get(PaybackId)
    #group_users = Group_users.query.get(groupId)
    #print(group_users)
    if payback:
        db.session.delete(payback)
        db.session.commit()

    return jsonify({})

@views.route('/delete-user-debt', methods=['POST'])
def delete_user_debt():
    user_debt = json.loads(request.data) # this function expects a JSON from the INDEX.js file
    print(user_debt)
    payer_id= user_debt['MemberId']
    reciver_id = user_debt['Member_twoId']
    amount = user_debt['Amount']
    group_id = user_debt['GroupId']
    if user_debt:
        new_payback = Payback(payer=payer_id, reciver=reciver_id, amount=amount, group_id=group_id)
        db.session.add(new_payback)
        db.session.commit()


    #print(payer_id, reciver_id)
    #if expense:
    #    db.session.delete(expense)
    #    db.session.commit()

    return jsonify({})
