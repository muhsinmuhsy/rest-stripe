from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from .models import Customer, Subscription
from .utils import create_customer, create_subscription

import stripe

from django.conf import settings
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

class IndexView(APIView):
    def get(self, request, format=None):
        response_data = {
            "index": "helloworld"
        }        
        return Response(response_data)
    
class CreateCustomerView(APIView):
    def get(self, request, format=None):
        user = request.user
        response_data = {
            "user": str(user.username)
        }        
        return Response(response_data)
    
    def post(self, request):
        user = request.user
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        stripe_customer = create_customer(email)
        customer = Customer.objects.create(user=user, stripe_customer_id=stripe_customer['id'])

        return Response({"message": "Customer created successfully"}, status=status.HTTP_201_CREATED)

{
  "email": "customer@example.com"
}



# class CreateSubscriptionView(APIView):
#     def post(self, request):
#         customer_id = request.data.get('customer_id')
#         price_id = request.data.get('price_id')
        
#         print(price_id, customer_id)

#         if not customer_id:
#             return Response({"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         if not price_id:
#             return Response({"error": "Price ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         stripe_subscription = stripe.Subscription.create(
#             customer=customer_id,
#             items=[{"price": price_id}],
#         )
        
#         # stripe_subscription = create_subscription(customer_id, price_id)

#         subscription = Subscription.objects.create(
#             stripe_subscription_id=stripe_subscription['id'],
#             active=True
#         )
        
        

#         return Response({"message": "Subscription created successfully"}, status=status.HTTP_201_CREATED)





class CreateSubscriptionView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        price_id = request.data.get('price_id')
        payment_method_id = request.data.get('payment_method_id')

        print(price_id, customer_id, payment_method_id)

        if not customer_id:
            return Response({"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not price_id:
            return Response({"error": "Price ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not payment_method_id:
            return Response({"error": "Payment Method ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the subscription
            stripe_subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                default_payment_method=payment_method_id,
            )
            
            subscription = Subscription.objects.create(
                stripe_subscription_id=stripe_subscription['id'],
                active=True
            )
            
            return Response({"message": "Subscription created successfully"}, status=status.HTTP_201_CREATED)
        
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error occurred while creating subscription: {e.user_message}")
            return Response({"error": e.user_message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred while creating subscription: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)