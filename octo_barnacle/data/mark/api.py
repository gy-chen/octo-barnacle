import flask
from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
from .ext import model as model_ext
from .model import Mark, ResourceNotAcquiredError

bp = flask.Blueprint('mark', __name__)


class _MarkForm(FlaskForm):
    resource = StringField('resource', validators=[DataRequired()])
    mark = StringField('mark', validators=[DataRequired()])

    def validate_mark(form, field):
        try:
            Mark(field.data)
        except ValueError:
            raise ValidationError('Invalid mark')


@bp.route('/stickerset/mark/next_batch', methods=['POST'])
def next_batch():
    model = model_ext.model
    batch = model.next_batch()
    return jsonify({"batch": batch})


@bp.route('/stickerset/<stickerset_name>/mark', methods=['POST'])
def mark(stickerset_name):
    form = _MarkForm()
    model = model_ext.model
    if form.validate_on_submit():
        try:
            model.mark(
                stickerset_name, form.mark.data, form.resource.data)
        except ResourceNotAcquiredError:
            return ('', 401)
        return ('', 200)
    return ('', 400)
