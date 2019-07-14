"Telegarm file"
import io
import flask
from flask import send_file
from .ext import bot as bot_ext

bp = flask.Blueprint('file', __name__)


@bp.route('/file/<file_id>')
def file(file_id):
    bot = bot_ext.bot
    file_ = bot.get_file(file_id)
    buf = io.BytesIO()
    file_.download(out=buf)
    buf.seek(0)
    return send_file(buf, mimetype="image/webp")
