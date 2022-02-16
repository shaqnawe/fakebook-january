from app import create_app, db, cli
from app.blueprints.blog.models import Post
from app.blueprints.authentication.models import User

app = create_app()
cli.register(app)

@app.shell_context_processor
def application_context():
    return {
        'User': User,
        'db': db,
        'Post': Post
    }