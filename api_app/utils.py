import stripe
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_customer(email):
    try:
        customer = stripe.Customer.create(email=email)
        return customer
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error occurred while creating customer: {e.user_message}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred while creating customer: {e}")
        return None

def create_subscription(customer_id, price_id):
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
        )
        logger.info(f"Subscription created: {subscription}")
        return subscription
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error occurred while creating subscription: {e.user_message}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred while creating subscription: {e}")
        return None