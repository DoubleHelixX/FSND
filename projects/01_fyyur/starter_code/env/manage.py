#----------------------------------------------------------------------------#
# Migration Imports
#----------------------------------------------------------------------------#

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

#----------------------------------------------------------------------------#
# Manage Migration
#----------------------------------------------------------------------------#
def migration(app,db):
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)