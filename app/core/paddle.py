from paddle_billing_client.client import PaddleApiClient
from paddle_billing_client.models.customer import CustomerRequest
from paddle_billing_client.models.address import AddressRequest
from app.core.config import settings

paddle_client = PaddleApiClient(
    base_url="https://sandbox-api.paddle.com/",
    token=settings.PADDLE_API_TOKEN
)

def create_paddle_customer(user):
    customer_request = CustomerRequest(
        email=user.email,
        name=user.username
    )
    return paddle_client.create_customer(customer_request)

def create_paddle_address(user, address_data):
    address_request = AddressRequest(
        first_name=address_data.get('first_name'),
        last_name=address_data.get('last_name'),
        line1=address_data.get('line1'),
        city=address_data.get('city'),
        postal_code=address_data.get('postal_code'),
        country_code=address_data.get('country_code')
    )
    return paddle_client.create_address(user.paddle_customer_id, address_request)