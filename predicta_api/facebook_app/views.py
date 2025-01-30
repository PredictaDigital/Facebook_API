import requests
from django.http import JsonResponse
from django.views import View

class GetAdAccountUsers(View):

    def get_ad_account_users(self, ad_account_id, page_access_token):
        url = f'https://graph.facebook.com/v21.0/{ad_account_id}/users'
        params = {
            'access_token': page_access_token
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f"Error: {response.status_code}, {response.text}"}

    def get(self, request, *args, **kwargs):
        page_id = request.GET.get('page_id')
        page_access_token = request.GET.get('page_access_token')

        if not page_id or not page_access_token:
            return JsonResponse({'error': 'Missing page_id or page_access_token'}, status=400)

        # Step 1: Get the user's ad accounts
        ad_accounts_url = 'https://graph.facebook.com/v21.0/me/adaccounts'
        params = {
            'access_token': page_access_token
        }

        ad_accounts_response = requests.get(ad_accounts_url, params=params)
        if ad_accounts_response.status_code == 200:
            ad_accounts_data = ad_accounts_response.json()
            ad_accounts = ad_accounts_data.get('data', [])

            if not ad_accounts:
                return JsonResponse({'error': 'No ad accounts found for the user'}, status=404)

            # Step 2: Check if any ad account is linked to the page
            linked_ad_account = None
            for ad_account in ad_accounts:
                ad_account_id = ad_account.get('id')
                # Check if the ad account can manage the page
                page_permission_url = f'https://graph.facebook.com/v21.0/{ad_account_id}/adaccounts'
                page_permission_response = requests.get(page_permission_url, params=params)

                if page_permission_response.status_code == 200:
                    permissions_data = page_permission_response.json()
                    if 'data' in permissions_data:
                        for permission in permissions_data['data']:
                            if permission.get('page_id') == page_id:
                                linked_ad_account = ad_account
                                break

            if linked_ad_account:
                # Step 3: Fetch users for the linked ad account
                users = self.get_ad_account_users(linked_ad_account['id'], page_access_token)
                return JsonResponse({'linked_ad_account': linked_ad_account, 'users': users})

            return JsonResponse({'error': 'No ad account found that is linked to the page'}, status=404)

        return JsonResponse({'error': f"Error: {ad_accounts_response.status_code}, {ad_accounts_response.text}"}, status=ad_accounts_response.status_code)
