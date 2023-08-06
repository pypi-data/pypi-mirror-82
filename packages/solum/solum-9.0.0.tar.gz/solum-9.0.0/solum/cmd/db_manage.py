#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Starter script for solum-db-manage."""

import os

from oslo_config import cfg
from oslo_db import options
from oslo_db.sqlalchemy.migration_cli import manager

CONF = cfg.CONF


def do_version(mgr):
    print('Current DB revision is %s' % mgr.version())


def do_upgrade(mgr):
    mgr.upgrade(CONF.command.revision)


def do_downgrade(mgr):
    mgr.downgrade(CONF.command.revision)


def do_stamp(mgr):
    mgr.stamp(CONF.command.revision)


def do_revision(mgr):
    mgr.revision(message=CONF.command.message,
                 autogenerate=CONF.command.autogenerate)


def add_command_parsers(subparsers):
    parser = subparsers.add_parser('version')
    parser.set_defaults(func=do_version)

    parser = subparsers.add_parser('upgrade')
    parser.add_argument('revision', nargs='?')
    parser.set_defaults(func=do_upgrade)

    parser = subparsers.add_parser('downgrade')
    parser.add_argument('revision', nargs='?')
    parser.set_defaults(func=do_downgrade)

    parser = subparsers.add_parser('stamp')
    parser.add_argument('revision', nargs='?')
    parser.set_defaults(func=do_stamp)

    parser = subparsers.add_parser('revision')
    parser.add_argument('-m', '--message')
    parser.add_argument('--autogenerate', action='store_true')
    parser.set_defaults(func=do_revision)


def get_manager():
    if cfg.CONF.database.connection is None:
        raise ValueError(
            'Database connection not set in /etc/solum/solum.conf')

    alembic_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '..', 'objects', 'sqlalchemy',
                     'migration', 'alembic.ini'))
    migrate_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '..', 'objects', 'sqlalchemy',
                     'migration', 'alembic_migrations'))
    migration_config = {'alembic_ini_path': alembic_path,
                        'alembic_repo_path': migrate_path,
                        'db_url': CONF.database.connection}
    return manager.MigrationManager(migration_config)


def main():
    command_opt = cfg.SubCommandOpt('command',
                                    title='Command',
                                    help='Available commands',
                                    handler=add_command_parsers)
    CONF.register_cli_opt(command_opt)

    # set_defaults() is called to register the db options.
    options.set_defaults(CONF)

    CONF(project='solum')
    CONF.command.func(get_manager())
