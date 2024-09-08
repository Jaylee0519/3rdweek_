from datetime import datetime

from flask import Blueprint, render_template, request, url_for, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Question
from ..forms import QuestionForm

bp = Blueprint('question', __name__, url_prefix='/question')

# @bp.route('/list/')
# def _list():
#     page = request.args.get('page', type=int, default=1)
#     question_list = Question.query.order_by(Question.create_date.desc())
#     question_list = question_list.paginate(page=page, per_page=10)
#     return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question) 

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)  


@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        question_list = question_list.filter(Question.subject.ilike(search) | Question.content.ilike(search)).distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)