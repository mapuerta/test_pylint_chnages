#!/usr/bin/env python
# coding: utf-8

import csv
import click
import odoorpc
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)-5s - %(funcName)s - %(message)s')
_logging = logging.getLogger(__name__)
_logging.setLevel("DEBUG")

def string2float(string):
    string = string.strip()
    string = string.replace(',', '.')
    return float(string)

def normalice_create_record(data):
    res = {}
    for key, values in data.items():
        key = key.replace(',', '')
        res[key] = values
    return res

def data_csv(filename):
    result = []
    try:
        csvfile = open(filename, 'r', newline='')
        datas = list(csv.DictReader(csvfile))
        for data in datas:
            res = {}
            for key, vals in data.items():
                key = key.strip()
                res[key] = vals
            result.append(res)
    except IOError:
        result = [{}]
    return result

class RPCmethod(object):

    def __init__(self, url=None, port=8069, username=None, password=None,
                 dbname=False, company=False):
        self.url = url
        self.uid = 1
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = port
        self.conecction = None
        self.authenticate()
        self.company_id = self.set_company(company) 

    def authenticate(self):
        auth = odoorpc.ODOO(self.url, port=self.port)
        auth.login(self.dbname, self.username, self.password)
        self.uid = auth.env.user.id
        self.conecction = auth

    def set_company(self, company):
        companys = {
            'bpmedical': 'BP Medical S.A',
            'medimarket': 'Medimarket S.A'}
        company = companys.get(company)
        company_id = self.execute(
            ([('name', 'ilike', company)],),
            method='search', model='res.company')
        if isinstance(company_id, list):
            company_id = company_id[0]
        return company_id

    def update_stock(self, product_id, data):
        values = {
            'value': string2float(data['Costo']),
            'remaining_qty': int(data['Cantidad']),
            'remaining_value': string2float(data['Total']),
            'date': '2017-12-31'}
        stock_id = self.execute(
            ([('product_id', '=', product_id),
              ('company_id', '=', self.company_id)],),
            method='search', model='stock.move')
        if not stock_id:
            return
        stock = self.execute(
            (stock_id,), method='browse', model='stock.move')
        stock.write(values)
        inventory = stock.inventory_id
        if not inventory:
            return
        move_line = inventory.line_ids
        if move_line.product_qty != data['Cantidad']:
            move_line.product_qty = int(data['Cantidad'])

    @property
    def environment(self):
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
@click.option("--company", help="Nombre de la compania",
              default=False, required=True,
              type=click.Choice(['bpmedical', 'medimarket']))
def update_stock(username, password, port, host, dbname, company):
    rpc = RPCmethod(host, port, username, password, dbname, company)
    datas = data_csv(company+'_inventario.csv')
    stock_data = {}
    for data in datas:
        stock_data[data['Referencia']] = data
    domain = [
        ('default_code', 'in', list(stock_data.keys())),
        ('company_id', '=', rpc.company_id)]
    product_ids = rpc.execute(
        (domain,), method='search', model='product.product')
    products = rpc.execute(
        (product_ids,), method='browse', model='product.product')
    for product in products:
        _logging.debug("Update product %s", product.name)
        stock_value = stock_data[product.default_code]
        if not product.standard_price:
            product.standard_price = string2float(stock_value.get('Costo'))
        rpc.update_stock(product.id, stock_value)
if __name__ == '__main__':
    update_stock()

