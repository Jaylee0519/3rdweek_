from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


#@bp.route('/')
#def index():
    #question_list=Question.query.order_by(Question.create_date.desc())
    #return render_template('question/question_list.html', question_list=question_list)

@bp.route('/')
def index():
    return redirect(url_for('question._list'))



