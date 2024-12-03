from app import create_app
from app.routes import register_routes

app = create_app()

with app.app_context():
    from sql_alchemy import database
    database.create_all()

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
