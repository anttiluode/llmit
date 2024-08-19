from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///llmit.db'
db = SQLAlchemy(app)

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)

# Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

@app.route('/')
def index():
    with open('index.html', 'r') as file:
        return file.read()

@app.route('/get_posts', methods=['GET'])
def get_posts():
    group = request.args.get('group', 'frontpage')
    print(f"Fetching posts for group: {group}")
    
    if group == 'frontpage':
        posts = Post.query.order_by(Post.upvotes.desc()).limit(30).all()
    else:
        posts = Post.query.filter_by(group=group).order_by(Post.upvotes.desc()).limit(30).all()
    
    if posts:
        print(f"Found {len(posts)} posts for group {group}")
    else:
        print(f"No posts found for group {group}")

    return jsonify([{
        "id": post.id,
        "group": post.group,
        "title": post.title,
        "content": post.content,
        "upvotes": post.upvotes,
        "downvotes": post.downvotes
    } for post in posts])

@app.route('/get_comments', methods=['GET'])
def get_comments():
    post_id = request.args.get('post_id')
    print(f"Fetching comments for post_id: {post_id}")

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.upvotes.desc()).all()

    if comments:
        print(f"Found {len(comments)} comments for post_id {post_id}")
    else:
        print(f"No comments found for post_id {post_id}")

    return jsonify([{
        "id": comment.id,
        "content": comment.content,
        "upvotes": comment.upvotes,
        "downvotes": comment.downvotes
    } for comment in comments])

if __name__ == '__main__':
    app.run(debug=True)
