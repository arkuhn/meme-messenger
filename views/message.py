import os

from sqlalchemy import null
from sqlalchemy import or_

from models.message import Message
from models.conversation import Conversation, get_conversation, get_conversations
from models.friendship import get_friends_db
from models.user import get_username_from_id, get_id_from_username
from flask import Blueprint, render_template, request, app, url_for
from werkzeug.utils import secure_filename, redirect
from views.auth import is_logged_in, get_email, get_username, login

message = Blueprint('message', __name__, url_prefix='/message')

ALLOWED_EXTENSIONS = set('.jpg')

@message.route('/conversation')
def converse(messaging_user=""):
    # Implement socket functionality

    # check log in and grab user name
    if is_logged_in():

        #check log in and grab user name
        main_user = get_username()
        main_user_id = get_id_from_username(main_user)

        #Grab friends
        friends = get_friends_db(main_user_id)

        #Grab every conversation
        all_conversations = get_conversations(main_user_id)

        #map friends to conversations and messages
        conversations = {}
        for friend in friends:
            friend_id= get_id_from_username(friend)
            for conversation in all_conversations:
                if conversation.first_user_id == friend_id or conversation.second_user_id == friend_id:
                    conversations[friend] = conversation.messages
            
    else:
        #send to home screen if not logged in user
        return redirect('/auth/login')

    return render_template('conversation.html', username=main_user, friends=friends, conversations=conversations)

def allowed_type(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@message.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_type(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_MEME'], filename))
            return redirect(url_for('conversation'))