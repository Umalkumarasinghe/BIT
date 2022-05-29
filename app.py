from flask import Flask, Blueprint, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

SECRET_KEY = 'you will never find'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://odoo:admin@localhost:5432/grn'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'umalonline7@gmail.com'
app.config['MAIL_PASSWORD'] = '*******'
mail = Mail(app)
db = SQLAlchemy(app)

from models.users import user_model_blueprint, User
from models.members import member_model_blueprint
from models.suppliers import supplier_model_blueprint
from models.items import item_model_blueprint
from models.production_teams import production_team_model_blueprint
from models.purchase_order import purchase_order_model_blueprint
from models.production import production_model_blueprint
from models.production_line import production_line_model_blueprint
from models.grn import grn_model_blueprint
from models.grn_line import grn_line_model_blueprint
from models.incomes_and_expenses import incomes_and_expenses_model_blueprint
from models.reordering import reordering_model_blueprint


from controllers.user_actions_controllers import user_actions_controller
from controllers.member_actions_controllers import member_actions_controller
from controllers.supplier_actions_controllers import supplier_actions_controller
from controllers.production_team_actions_controllers import production_team_actions_controller
from controllers.item_actions_controllers import item_actions_controller
from controllers.purchase_order_actions_controllers import purchase_order_actions_controllers
from controllers.grn_actions_controllers import grn_actions_controllers
from controllers.production_actions_controllers import production_actions_controllers
from controllers.incomes_and_expenses_actions_controllers import incomes_and_expenses_actions_controller

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "user_actions_controller.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


# models
app.register_blueprint(user_model_blueprint)
app.register_blueprint(member_model_blueprint)
app.register_blueprint(supplier_model_blueprint)
app.register_blueprint(production_team_model_blueprint)
app.register_blueprint(item_model_blueprint)
app.register_blueprint(production_model_blueprint)
app.register_blueprint(purchase_order_model_blueprint)
app.register_blueprint(production_team_model_blueprint)
app.register_blueprint(grn_model_blueprint)
app.register_blueprint(grn_line_model_blueprint)
app.register_blueprint(incomes_and_expenses_model_blueprint)
app.register_blueprint(reordering_model_blueprint)
app.secret_key = SECRET_KEY

# controllers
app.register_blueprint(user_actions_controller)
app.register_blueprint(member_actions_controller)
app.register_blueprint(supplier_actions_controller)
app.register_blueprint(production_team_actions_controller)
app.register_blueprint(item_actions_controller)
app.register_blueprint(purchase_order_actions_controllers)
app.register_blueprint(production_actions_controllers)
app.register_blueprint(grn_actions_controllers)
app.register_blueprint(incomes_and_expenses_actions_controller)

if __name__ == '__main__':
    app.run(debug=True)
