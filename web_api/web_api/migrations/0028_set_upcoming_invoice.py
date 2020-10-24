# Generated by Django 3.0.3 on 2020-10-24 23:21
from typing import Any

import stripe
from django.db import migrations

from web_api import billing
from web_api.models import Account, StripeCustomerInformation


def forward(apps: Any, schema_editor: Any) -> None:
    db_alias = schema_editor.connection.alias
    for stripe_info in StripeCustomerInformation.objects.using(db_alias).all():
        account = Account.objects.get(stripe_customer_id=stripe_info.customer_id)
        stripe_customer = stripe.Customer.retrieve(stripe_info.customer_id)
        billing.update_subscription(
            account=account, customer=stripe_customer, stripe_customer_info=stripe_info
        )


class Migration(migrations.Migration):

    dependencies = [
        ("web_api", "0027_auto_20201024_2320"),
    ]

    operations = [migrations.RunPython(forward, migrations.RunPython.noop)]