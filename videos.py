from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required
from flask_restful import Api, Resource, abort, reqparse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisissecret'

api = Api(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    
    
    def __init__(self, id, username):
        self.id = id
        self.username = username
        
class VideoModel(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    views = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    
    def __init__(self, video_id, title, views, rating):
        self.video_id = video_id
        self.title = title
        self.views = views
        self.rating = rating
        
    def toJson(self):
        return {'video_id': self.video_id,
                'title': self.title,
                'views': self.views,
                'rating': self.rating}
        
video_post_parser = reqparse.RequestParser()
video_post_parser.add_argument('title', type=str, required=True)
video_post_parser.add_argument('views', type=int)
video_post_parser.add_argument('rating', type=int)
        
@api.resource('/video/<int:id>')
class Video(Resource):
    def get(self, id):
        result = VideoModel.query.filter_by(video_id=id).first()
        if not result:
            abort(404, message='No video exists with that ID')
        return result.toJson(), 200
    
    def post(self, id):
        if VideoModel.query.filter_by(video_id=id).first():
            abort(409, message='Video already exists with that ID')
        
        args = video_post_parser.parse_args()
        video = VideoModel(video_id=id, title=str(args['title']), views=int(args['views']), rating=int(args['rating']))
        
        db.session.add(video)
        db.session.commit()
        
        return video.toJson(), 201
    
        

@app.route('/')
def index():
    return 'Home Page'

    

if __name__ == '__main__':
    app.run(debug=True)