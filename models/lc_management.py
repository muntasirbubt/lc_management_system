from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LCRequest(models.Model):
    _name = 'lc.management'
    _description = 'Letter of Credit Request'
    _order = 'id desc'
    _rec_name = 'name'

    name = fields.Char(string="LC Number", default=lambda self: self.env['ir.sequence'].next_by_code('lc.management'), readonly=True, copy=False)
    request_date = fields.Date(string="Request Date", default=fields.Date.context_today)
    # partner_id = fields.Many2one('res.partner', string="Vendor", required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('closed', 'Closed')
    ], default='draft', string="Status")

    purchase_order_ids = fields.Many2many('purchase.order', string="Purchase Orders", domain=[('state', '!=', 'cancel')])
    document_ids = fields.Many2many('ir.attachment', string="Documents")
    total_amount = fields.Monetary(string="Amount", required=True, compute='_compute_total_po')

    bank_name = fields.Many2one('res.bank', string="Bank", required=True)
    lc_no = fields.Char(string="LC Number")
    date = fields.Date(string="Date", default=fields.Date.context_today)


    beneficiary_name = fields.Many2one('res.partner',string="Beneficiary Name")
    beneficiary_country = fields.Char(string="Address Country",related='beneficiary_name.country_id.name')
    beneficiary_state = fields.Char(string="Address State", related='beneficiary_name.street')

    openers_name = fields.Many2one('res.partner',string="Opener Name")
    openers_country = fields.Char(string="Address Country",related='openers_name.country_id.name')
    openers_state = fields.Char(string="Address State", related='openers_name.street')


    bd_bank_registration_no = fields.Char(string="Bangladesh Bank Registration Number")
    hs_code = fields.Char(string="HS Code")
    import_licence_no = fields.Char(string="Import Licence No")
    irc_no = fields.Char(string="IRC Licence No")

    terms_and_conditions = fields.Text(string="Terms and Conditions")


    @api.depends('purchase_order_ids')
    def _compute_total_po(self):
        for rec in self:
            if rec.purchase_order_ids:
                rec.total_amount = sum(rec.purchase_order_ids.mapped('amount_total'))
            else:
                rec.total_amount = 0

    def action_approve(self):
        for record in self:
            if record.status != 'draft':
                raise ValidationError("Only draft requests can be approved.")
            record.status = 'approved'

    def action_close(self):
        for record in self:
            if record.status != 'approved':
                raise ValidationError("Only approved LCs can be closed.")
            record.status = 'closed'
