{
    'name': 'Utech Templates',
    'version': '1.0',
    'category': 'Customer Relationship Management',
    'sequence': 5,
    'description': """

Invoice and quotation templates.
=================================
This application Inherits the openerp existing openerp templates and adds Utech templates to the System.
     """,
    'author': 'Endosoft OpenERP Team',
    'website': 'http://www.endosoft.com',
    'depends': ['sale','account','stock'],
    'data': [
        'account_report.xml',
        'company_view.xml'
            ],
    'test': [],
    'installable': True,
    'auto_install': False,
 #   'images': ['images/claim_categories.jpeg','images/claim_stages.jpeg','images/claims.jpeg'],
}
