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
from models.production_order import production_order_model_blueprint
from models.grn import grn_model_blueprint
from models.gin import gin_model_blueprint
from models.grn_line import grn_line_model_blueprint
from models.gin_line import gin_line_model_blueprint

manager.add_command('db', MigrateCommand)

# models
app.register_blueprint(user_model_blueprint)
app.register_blueprint(member_model_blueprint)
app.register_blueprint(supplier_model_blueprint)
app.register_blueprint(production_team_model_blueprint)
app.register_blueprint(item_model_blueprint)
app.register_blueprint(purchase_order_model_blueprint)
app.register_blueprint(production_order_model_blueprint)
app.register_blueprint(grn_model_blueprint)
app.register_blueprint(gin_model_blueprint)
app.register_blueprint(grn_line_model_blueprint)
app.register_blueprint(gin_line_model_blueprint)

if __name__ == '__main__':
    manager.run()
