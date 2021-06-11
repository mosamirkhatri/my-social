from flask import Flask, request
import os
from app.routes.auth import auth
from app.routes.post import post
from app.routes.like import like
from app.utils.decorators.login_required import login_required

app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(post, url_prefix='/api/post')
app.register_blueprint(like, url_prefix='/api/like')


@app.route('/')
def health():
    print("ENV", os.environ.get('SECRET_KEY'))
    return "Working"


@app.route("/protected", methods=['POST', 'GET'])
@login_required
def protected(current_user):
    request_data = request.get_json()
    return {"data": current_user}
