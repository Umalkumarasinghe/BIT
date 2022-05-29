import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

from models.users import user_model_blueprint
from models.members import member_model_blueprint
from models.suppliers import supplier_model_blueprint
from models.production_teams import production_team_model_blueprint
from models.items import item_model_blueprint
from models.purchase_order import purchase_order_model_blueprint
from models.production import production_model_blueprint
from models.production_line import production_line_model_blueprint
from models.grn import grn_model_blueprint
from models.grn_line import grn_line_model_blueprint
from models.incomes_and_expenses import incomes_and_expenses_model_blueprint
from models.reordering import reordering_model_blueprint

manager.add_command('db', MigrateCommand)

# models
app.register_blueprint(user_model_blueprint)
app.register_blueprint(member_model_blueprint)
app.register_blueprint(supplier_model_blueprint)
app.register_blueprint(production_team_model_blueprint)
app.register_blueprint(item_model_blueprint)
app.register_blueprint(purchase_order_model_blueprint)
app.register_blueprint(production_line_model_blueprint)
app.register_blueprint(reordering_model_blueprint)
app.register_blueprint(grn_model_blueprint)
app.register_blueprint(production_model_blueprint)
app.register_blueprint(incomes_and_expenses_model_blueprint)

if __name__ == '__main__':
    manager.run()
