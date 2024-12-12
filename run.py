from app import create_app
from app.routes import register_routes
from flask_cors import CORS
from models.individual import Individual
from models.user import User
from flasgger import Swagger

app = create_app()
app.config['SWAGGER'] = { 'title': 'Swagger-UI', 'uiversion': 3 }
swagger_config = {
   'headers': [],
   'specs': [
      {
         'endpoint': 'apisec_1',
         'route': '/apispec_1.json',
         'rule_filter': lambda rule: True,
         'model_filter': lambda tag: True,
      }
   ],
   'static_url_path': '/flasgger_static',
   'swagger_ui': True,
}

Swagger(app, config=swagger_config, template_file="swagger_template.json")
CORS(app)

with app.app_context():
  from sql_alchemy import database
  database.create_all()

  if not User.query.first():
    individual = Individual('Admin', '000000000000', None)
    individual.save()

    new_user = User('admin@admin.com', 'admin', True, individual.id)

    database.session.add(new_user)
    database.session.commit()
    print("User 'Admin' created")

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
