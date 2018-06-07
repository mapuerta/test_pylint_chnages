#!/usr/bin/env python
# coding: utf-8

import click
import odoorpc
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)-5s - %(funcName)s - %(message)s')
_logging = logging.getLogger(__name__)
_logging.setLevel("DEBUG")


class RPCmethod(object):

    def __init__(self, url=None, port=8069, username=None, password=None,
                 dbname=False):
        self.url = url
        self.uid = 1
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = port
        self.conecction = None
        self.authenticate()

    def authenticate(self):
        auth = odoorpc.ODOO(self.url, port=self.port)
        auth.login(self.dbname, self.username, self.password)
        self.uid = auth.env.user.id
        self.conecction = auth

    @property
    def env(self):
        return self.conecction.env

    def execute(self, params, method="create", model=False):
        env = self.conecction.env[model]
        if method == "create":
            params = normalice_create_record(*params)
            params = (params, )
        result = getattr(env, method)(*params)
        _logging.debug('Running {0} record in {1} parameters {2}'.format(
            method, model, params))
        return result

    def update_modules(self, module):
        domain = [('name', '=', module)]
        if module == 'all':
            domain = [('state', '=', 'installed')]
        module_obj = self.env['ir.module.module']
        module_id = module_obj.search(domain)
        module = module_obj.browse(module_id)
        module.write({'state': 'to update'})
        module.button_upgrade()


@click.group()
def cli():
    pass

@cli.command()
@click.option("-u", "--username", help="Usuario de la instancia odoo",
              default=False, required=True)
@click.option("-w", "--password", help="Password de la instancia odoo",
              default=False, required=True)
@click.option("-p", "--port", help="Puerto de la instancia odoo",
              default=False, required=True)
@click.option("-h", "--host", help="URL de la instancia odoo",
              default='localhost', required=True)
@click.option("-d", "--dbname", help="Nombre de la base de datos en la instancia",
              default=False, required=True)
@click.option("-m", "--module", help="Nombre del modulo",
              default=False, required=True)
def update_modules(username, password, port, host, dbname, module):
    rpc = RPCmethod(host, port, username, password, dbname)
    rpc.update_modules(module)

if __name__ == '__main__':
    update_modules()
