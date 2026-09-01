from .config import settings

def _stripe():
    if not settings.stripe_enabled or not settings.stripe_secret_key:
        raise RuntimeError('Stripe is disabled or not configured')
    import stripe
    stripe.api_key=settings.stripe_secret_key
    return stripe

def create_draft_invoice(customer_email:str, amount_usd:float, description:str, days_until_due:int=15, metadata:dict|None=None):
    stripe=_stripe()
    matches=stripe.Customer.search(query=f"email:'{customer_email}'",limit=1)
    customer=matches.data[0] if matches.data else stripe.Customer.create(email=customer_email,metadata=metadata or {})
    amount=int(round(float(amount_usd)*100))
    item=stripe.InvoiceItem.create(customer=customer.id,amount=amount,currency=settings.stripe_default_currency,description=description,metadata=metadata or {})
    invoice=stripe.Invoice.create(customer=customer.id,collection_method='send_invoice',days_until_due=max(1,int(days_until_due)),auto_advance=False,metadata=metadata or {})
    return {'customer_id':customer.id,'invoice_item_id':item.id,'invoice_id':invoice.id,'status':invoice.status,'hosted_invoice_url':getattr(invoice,'hosted_invoice_url',None)}

def verify_webhook(body:bytes, signature:str):
    stripe=_stripe()
    if not settings.stripe_webhook_secret: raise RuntimeError('STRIPE_WEBHOOK_SECRET missing')
    return stripe.Webhook.construct_event(body,signature,settings.stripe_webhook_secret)
