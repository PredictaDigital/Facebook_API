from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .predicta_cust_model import PredictaCustomer

#get customer details using Azure ID
class CustomerData(APIView):
    def get(self, request, email):
        try:
            # Fetch customer by email
            customer = PredictaCustomer.objects.get(cnameid=email)
            data = {
                'id': customer.id,
                'fname': customer.fname,
                'lname': customer.lname,
                'email': customer.email,
                'phone': customer.phone,
                'cname': customer.cname,
                'password': customer.password,
                'plandet': customer.plandet,
                'costdet': customer.costdet,
                'validity': customer.validity,
                'address': customer.address,
                'country': customer.country,
                'state': customer.state,
                'plantype': customer.plantype,
                'users': customer.users,
                'city': customer.city,
                'zipCode': customer.zipCode,
                'cnameid': customer.cnameid,
                'logourl': customer.logourl,
                'themetype': customer.themetype,
                'custome_added': customer.custome_added,
                'auzureid': customer.auzureid,
            }
            return Response(data, status=status.HTTP_200_OK)
        except PredictaCustomer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
