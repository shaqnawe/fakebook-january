from app import create_app, db
from app.blueprints.blog.models import Post
from app.blueprints.main.models import User

app = create_app()

@app.shell_context_processor
def application_context():
    return {
        'User': User,
        'db': db,
        'Post': Post
    }