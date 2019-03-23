from datetime import date, datetime
from dateutil import relativedelta
import json
import time

import openerp
from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare, float_round
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement
import logging
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from openerp.osv import fields, osv, expression
from openerp.tools.float_utils import float_round as round


class sale_order(osv.osv):
    _inherit = "sale.order"

    _columns = {
        'order_close_reason': fields.char('Order Close Reason', required=True),
    }


class sale_order_close(osv.osv):
    _name = "sale.order.close"
    _description = "Sale Order close"

    _columns = {

        'order_close_reason': fields.char('Order Close Reason', required=True),
        'order_name': fields.char('Order Name'),
        'order_ref': fields.char('Order Ref.'),
    }

    def sale_order_close(self, cr, uid, ids, context=None):

        close_order_tbl_ids = ids

        ids = context['active_ids']
        order_close_reason = context['order_close_reason']
        so_obj = self.pool.get('sale.order')

        for so in so_obj.browse(cr, uid, ids, context=context):

            stock_picking_query = "SELECT id FROM stock_picking WHERE origin='{0}' and state!='done'".format(str(so.name))
            cr.execute(stock_picking_query)

            for sp_id in cr.fetchall():
                # unreserve
                self.pool.get('stock.picking').do_unreserve(cr, uid, int(sp_id[0]), context=context)

                # action cancel
                self.pool.get('stock.picking').action_cancel(cr, uid, int(sp_id[0]), context=context)

        # Action Done
        so_obj.action_done(cr, uid, ids, context=context)

        for so_id in ids:
            so_state_query = "UPDATE sale_order SET order_close_reason='{0}' WHERE id='{1}'".format(order_close_reason, so_id)

            cr.execute(so_state_query)
            cr.commit()

            for so in so_obj.browse(cr, uid, so_id, context=context):
                order_name = str(so.name)
                order_ref = str(so.client_order_ref)

                for co_id in close_order_tbl_ids:
                    so_state_query = "UPDATE sale_order_close SET order_name='{0}', order_ref='{1}' WHERE id='{2}'".format(
                        order_name, order_ref, co_id)

                    cr.execute(so_state_query)
                    cr.commit()

        return True
