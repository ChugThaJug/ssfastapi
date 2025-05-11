from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubscriptionBase(BaseModel):
    plan: str

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    status: Optional[str] = None

class SubscriptionInDB(SubscriptionBase):
    id: int
    user_id: int
    paddle_subscription_id: str
    status: str
    current_period_start: datetime
    current_period_end: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Subscription(SubscriptionInDB):
    pass

class SubscriptionStatus(BaseModel):
    is_subscribed: bool
    plan: Optional[str] = None
    end_date: Optional[str] = None

class PaddleWebhookEvent(BaseModel):
    event_type: str
    occurred_at: str
    data: dict