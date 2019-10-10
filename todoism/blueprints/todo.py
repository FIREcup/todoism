from flask import render_template, request, Blueprint, jsonify
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Item

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/app')
@login_required
def app():
    all_count = Item.query.with_parent(current_user).count()
    active_count = Item.query.with_parent(current_user).filter_by(done=False).count()
    completed_count = Item.query.with_parent(current_user).filter_by(done=True).count()
    return render_template('_app.html', items=current_user.items, all_count=all_count,
                           active_count=active_count, completed_count=completed_count)


@todo_bp.route('/items/new', methods=['POST'])
@login_required
def new_item():
    data = request.get_json()
    if data is None or data['body'].strip() == '':
        return jsonify(message='Invalid item body.'), 400
    item = Item(body=data['body'], author=current_user._get_current_object())
    db.session.add(item)
    db.session.commit()
    return jsonify(html=render_template('_item.html', item=item), message='+1')


@todo_bp.route('/item/clear', methods=['DELETE'])
@login_required
def clear_items():
    items = Item.query.with_parent(current_user).filter_by(done=True).all()
    for item in items:
        db.session.delete(item)
    db.session.commit()
    return jsonify(message='All clear')
