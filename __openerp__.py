{
    'name': 'Sale Order Close',
    'summary': """Close uncompleted Sale Order""",
    'description': """
Sale Order Close module will help to close sales orders which are not draft, not done or not cancelled. The user can close the order any time except these three types of sales orders.

Features:
    - Close sales order.
    - Reserved quantity of product will be released and stock into the inventory.
    - Stock picking line will be canceled
    """,
    'author': 'Shahjalal Hossain',
    'website': 'https://github.com/shahjalalh',
    'category': 'Sales',
    'version': '1.0.0',
    'depends': ['sale', 'account', 'stock', 'stock_account'],
    'data': [
            'security/sale_order_close_security.xml',
            'security/ir.model.access.csv',
            'wizard/order_close.xml',
            'sale_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
