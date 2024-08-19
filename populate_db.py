import time
import random
from app import db, Post, Comment, client, app

# List of groups to populate, including the new 'AskLLMit'
groups = [
    'announcements', 'Art', 'AskLLMit', 'askscience', 'atheism', 'aww', 'blog',
    'books', 'creepy', 'dataisbeautiful', 'DIY', 'Documentaries', 'EarthPorn',
    'explainlikeimfive', 'food', 'funny', 'Futurology', 'gadgets', 'gaming',
    'GetMotivated', 'gifs', 'history', 'IAmA', 'InternetIsBeautiful', 'Jokes',
    'LifeProTips', 'listentothis', 'mildlyinteresting', 'movies', 'Music', 'news',
    'nosleep', 'nottheonion', 'OldSchoolCool', 'personalfinance', 'philosophy',
    'photoshopbattles', 'pics', 'science', 'Showerthoughts', 'space', 'sports',
    'television', 'tifu', 'todayilearned', 'TwoXChromosomes', 'UpliftingNews', 
    'videos', 'worldnews', 'WritingPrompts'
]

def generate_post_for_group(group_name):
    try:
        prompt = f"Generate a popular post for the {group_name} group."
        completion = client.chat.completions.create(
            model="model-identifier",  # Replace with your model identifier
            messages=[
                {"role": "system", "content": "You are generating posts for an online community."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        # Correctly accessing the content of the generated message
        post_content = completion.choices[0].message.content
        post_title = post_content.split('\n')[0]  # Simplified title extraction
        post_text = post_content

        # Creating the post
        post = Post(
            group=group_name,
            title=post_title,
            content=post_text,
            upvotes=random.randint(1, 1000),  # Simulating upvotes
            downvotes=random.randint(0, 500)   # Simulating downvotes
        )
        db.session.add(post)
        db.session.commit()

        print(f"Generated post for {group_name}: {post_title}")

        # Generating comments for the post
        for _ in range(random.randint(3, 15)):  # 3 to 15 comments per post
            generate_comment_for_post(post.id)

    except Exception as e:
        print(f"Error generating post for {group_name}: {e}")

def generate_comment_for_post(post_id):
    try:
        prompt = "Generate a comment for the post."
        completion = client.chat.completions.create(
            model="model-identifier",  # Replace with your model identifier
            messages=[
                {"role": "system", "content": "You are generating comments for an online community post."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        # Correctly accessing the content of the generated message
        comment_content = completion.choices[0].message.content

        # Creating the comment
        comment = Comment(
            post_id=post_id,
            content=comment_content,
            upvotes=random.randint(1, 100),  # Simulating upvotes
            downvotes=random.randint(0, 50)   # Simulating downvotes
        )
        db.session.add(comment)
        db.session.commit()

        print(f"Generated comment for post {post_id}")

    except Exception as e:
        print(f"Error generating comment: {e}")

if __name__ == "__main__":
    with app.app_context():
        for group in groups:
            generate_post_for_group(group)
            time.sleep(1)  # Add delay if needed to avoid overwhelming the server
