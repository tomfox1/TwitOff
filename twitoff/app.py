"""Main application and routing logic for Twitoff."""
from decouple import config 
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_user

def create_app():
    """Create and configure an instance of the flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route('/') 
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/update')
    def update(): 
        if config('ENV') == 'production':
            CACHE.flushall()
            CACHED_COMPARISONS.clear()
        update_all_users()
        return render_template('base.html', users=User.query.all(),
                                title='Cache cleared and all Tweets updated!')   

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message= ''
        name = name or request.values['user_name']
        try: 
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} succesfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message) 

    @app.route('/compare', methods=['POST'])
    def compare():
        user1, user2 = request.values['user1'], request.values['user2']
        if user1 == user2:
            return 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            return user1 if prediction else user2
   
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset', users=[]) 
        
    return app 