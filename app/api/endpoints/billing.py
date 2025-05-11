# app/api/endpoints/billing.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.config import settings
from app.api import deps
from app.models.user import User
from app.schemas.billing import SubscriptionCreate, SubscriptionStatus
from paddle_billing_client.client import PaddleApiClient
from paddle_billing_client.models.subscription import SubscriptionRequest
from paddle_billing_client.helpers import validate_webhook_signature
from apiclient import HeaderAuthentication
from datetime import datetime
import logging

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

paddle_client = PaddleApiClient(
    base_url="https://sandbox-api.paddle.com/",
    authentication_method=HeaderAuthentication(token=settings.PADDLE_API_TOKEN)
)

@router.post("/create_subscription")
async def create_subscription(
    subscription: SubscriptionCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    if not current_user.paddle_customer_id or not current_user.paddle_address_id:
        raise HTTPException(status_code=400, detail="User is not set up for billing")
    
    try:
        price_id = settings.PRO_PRICE_ID if subscription.plan == "pro" else settings.BASIC_PRICE_ID
        subscription_request = SubscriptionRequest(
            customer_id=current_user.paddle_customer_id,
            address_id=current_user.paddle_address_id,
            currency_code='USD',
            items=[{"price_id": price_id, "quantity": 1}],
            custom_data={'user_id': current_user.id}
        )
        subscription = paddle_client.create_subscription(subscription_request)
        return {"checkout_url": subscription.checkout.url}
    except Exception as e:
        logger.error(f"Failed to create subscription: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to create subscription: {str(e)}")

@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(deps.get_db)):
    try:
        signature = request.headers.get('Paddle-Signature')
        data = await request.json()
        body = await request.body()

        if not validate_webhook_signature(signature, body, settings.PADDLE_WEBHOOK_SECRET):
            raise HTTPException(status_code=400, detail="Invalid signature")

        event_type = data.get('event_type')
        if event_type == 'subscription.created':
            await handle_subscription_created(data, db)
        elif event_type == 'subscription.updated':
            await handle_subscription_updated(data, db)
        elif event_type == 'subscription.canceled':
            await handle_subscription_canceled(data, db)
        else:
            logger.warning(f"Unhandled webhook event type: {event_type}")

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def handle_subscription_created(data: dict, db: Session):
    try:
        subscription = data['subscription']
        user = db.query(User).filter(User.paddle_customer_id == subscription['customer_id']).first()
        if user:
            user.paddle_subscription_id = subscription['id']
            user.is_subscribed = True
            user.subscription_plan = subscription['items'][0]['price']['product_name'].lower()
            user.subscription_end_date = datetime.fromisoformat(subscription['current_billing_period']['ends_at'])
            db.commit()
            logger.info(f"Subscription created for user {user.id}")
        else:
            logger.warning(f"User not found for customer_id: {subscription['customer_id']}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error handling subscription created: {str(e)}")

async def handle_subscription_updated(data: dict, db: Session):
    try:
        subscription = data['subscription']
        user = db.query(User).filter(User.paddle_customer_id == subscription['customer_id']).first()
        if user:
            user.is_subscribed = subscription['status'] == 'active'
            user.subscription_plan = subscription['items'][0]['price']['product_name'].lower()
            user.subscription_end_date = datetime.fromisoformat(subscription['current_billing_period']['ends_at'])
            db.commit()
            logger.info(f"Subscription updated for user {user.id}")
        else:
            logger.warning(f"User not found for customer_id: {subscription['customer_id']}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error handling subscription updated: {str(e)}")

async def handle_subscription_canceled(data: dict, db: Session):
    try:
        subscription = data['subscription']
        user = db.query(User).filter(User.paddle_customer_id == subscription['customer_id']).first()
        if user:
            user.is_subscribed = False
            user.subscription_plan = 'free'
            user.subscription_end_date = None
            db.commit()
            logger.info(f"Subscription canceled for user {user.id}")
        else:
            logger.warning(f"User not found for customer_id: {subscription['customer_id']}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error handling subscription canceled: {str(e)}")

@router.get("/subscription_status")
async def subscription_status(current_user: User = Depends(deps.get_current_user)):
    try:
        return SubscriptionStatus(
            is_subscribed=current_user.is_subscribed,
            plan=current_user.subscription_plan,
            end_date=current_user.subscription_end_date
        )
    except Exception as e:
        logger.error(f"Error fetching subscription status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching subscription status: {str(e)}")