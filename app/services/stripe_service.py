import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout_session(report_id, success_url, cancel_url):
    """
    Creates a Stripe Checkout Session for a one-time payment of $19.
    """
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Financial Health Report #{report_id}',
                            'description': 'One-time payment for full financial analysis and PDF download.',
                        },
                        'unit_amount': 1900, # $19.00
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={'report_id': report_id}
        )
        return checkout_session
    except Exception as e:
        # Logistic logging for debugging in test mode
        print(f"Stripe Session Error: {e}")
        return None

def verify_payment_session(session_id):
    """
    Directly retrieves a session to verify payment status (Fallback for polling).
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status == 'paid'
    except Exception as e:
        print(f"Stripe Retrieval Error: {e}")
        return False

def construct_event(payload, sig_header):
    """
    Securely constructs a Stripe webhook event.
    """
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    return stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
