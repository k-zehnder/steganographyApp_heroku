"""Application Entry Point"""
from app import create_app
from app.models import ImageFile, db

app = create_app()

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'ImageFile': ImageFile}

if __name__ == '__main__':
    app.run(debug=True)