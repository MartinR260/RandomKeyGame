from flask import Flask, render_template, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)


class Leaderboard(Resource):
    def get(self):
        sorted_scores = Score.query.order_by(Score.score.desc()).limit(10).all()
        return [{'username': score.username, 'score': score.score} for score in sorted_scores]

class SubmitScore(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        score = data.get('score')

        new_score = Score(username=username, score=score)
        db.session.add(new_score)
        db.session.commit()

        return {'message': 'Score submitted successfully'}

api.add_resource(Leaderboard, '/leaderboard')
api.add_resource(SubmitScore, '/submit_score')

@app.route('/')
def home():
    return render_template('website.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
