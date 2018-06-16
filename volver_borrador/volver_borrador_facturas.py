# -*- coding: utf-8 -*-
"""
Script para pasar facturas abiertas a borrador
"""
import xmlrpc.client
import csv

PARAMETERS_CONECTION = 'parameters_conection.csv'
CTAS_CHANGE = 'lista_invoice.csv'


def conectar_db():
    """
    Metodo para conectarse con parametros provenientes
    de un archivo
    """
    param_conection = csv.DictReader(
        open(PARAMETERS_CONECTION), delimiter='|')
    for row_con in param_conection:
        host = row_con['host']
        port = row_con['port']
        pdata_b = row_con['db']
        user = row_con['user']
        ppassword = row_con['password']
        break

    sock_common = xmlrpc.client.ServerProxy(
        '{0}:{1}/xmlrpc/common'.format(host, port))
    puid = sock_common.login(pdata_b, user, ppassword)
    psock = xmlrpc.client.ServerProxy(
        '{0}:{1}/xmlrpc/object'.format(host, port))

    return pdata_b, puid, ppassword, psock


def main():
    """
    Metodo que realiza los cambios a las facturas
    """
    data_b, uid, password, sock = conectar_db()

    if not uid:
        print("No se pudo realizar la conexion.")
        exit()

    # Se asume:
    # * Que son para la misma compañia:
    # verificar diario y cuenta
    # * Que estan abiertas sin conciliaciones
    journal_id = 15
    account_id = 9
    val_update_journal = {
        'update_posted': True
    }
    result_journal = sock.execute_kw(
        data_b, uid, password, 'account.journal', 'write', [
            [journal_id], val_update_journal])
    print("Permitir cancelar asiento ID: %s Resultado: %s" % (
        journal_id, result_journal))

    ctas_change_invoice = csv.DictReader(open(CTAS_CHANGE), delimiter=',')

    print("""Iniciando Proceso
        (Cambio de facturas a borrador)...""")
    try:
        for row in ctas_change_invoice:
            # Por cada factura
            # invoce.action_invoice_cancel() y action_invoice_draft()
            invoice_id = int(row['invoice_id'])
            result_invoice_cancel = sock.execute_kw(
                data_b, uid, password,
                'account.invoice', 'action_invoice_cancel',
                [invoice_id])
            print("Cancelar Factura ID: %s Resultado: %s" % (
                invoice_id, result_invoice_cancel))

            result_invoice_draft = sock.execute_kw(
                data_b, uid, password,
                'account.invoice', 'action_invoice_draft',
                [invoice_id])
            print("Borrador Factura ID: %s Resultado: %s" % (
                invoice_id, result_invoice_draft))

            # cambiar la cuenta
            val_update_invoice = {
                'account_id': account_id,
            }
            result_invoice_id = sock.execute_kw(
                data_b, uid, password, 'account.invoice', 'write',
                [
                    [invoice_id], val_update_invoice
                ])
            print("Cambiar cuenta Factura ID: %s Resultado: %s" % (
                invoice_id, result_invoice_id))

        print('Hecho')

    finally:
        val_update_journal = {
            'update_posted': False
        }
        result_journal = sock.execute_kw(
            data_b, uid, password, 'account.journal', 'write',
            [
                [journal_id], val_update_journal
            ])
        print("No permitir cancelar asiento ID: %s Resultado: %s" % (
            journal_id, result_journal))
        print('Chau, mundo!')

main()
