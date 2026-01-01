"""Business specification data models."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BusinessModel(str, Enum):
    """Supported business models."""
    SUBSCRIPTION = "subscription"
    ONE_TIME = "one_time"
    HYBRID = "hybrid"
    FREEMIUM = "freemium"


class ProductType(str, Enum):
    """Product types."""
    MICRO_SAAS = "micro_saas"
    TEMPLATES = "templates"
    COURSE = "course"
    COMMUNITY = "community"
    CONSULTING = "consulting"
    MARKETPLACE = "marketplace"


class Channel(str, Enum):
    """Marketing channels."""
    SEO = "seo"
    PAID_ADS = "paid_ads"
    COLD_OUTBOUND = "cold_outbound"
    PARTNERSHIPS = "partnerships"
    CONTENT = "content"
    SOCIAL = "social"


class BuildConstraints(BaseModel):
    """User constraints and inputs for business building."""
    skills: List[str] = Field(default_factory=list, description="Technical and non-technical skills")
    time_available_weekly: int = Field(default=10, description="Hours per week available")
    budget: int = Field(default=1000, description="Initial budget in USD")
    risk_tolerance: str = Field(default="medium", description="low, medium, high")
    preferred_model: BusinessModel = Field(default=BusinessModel.SUBSCRIPTION)
    topics: List[str] = Field(default_factory=list, description="Topics of interest/expertise")
    audience_access: dict = Field(default_factory=dict, description="Email list, social following, etc.")
    unfair_advantages: List[str] = Field(default_factory=list)
    ethical_boundaries: List[str] = Field(default_factory=list, description="Hard no's")
    target_income: int = Field(default=10000, description="Monthly target in USD")
    timeline_months: int = Field(default=6, description="Timeline to reach target")


class ICP(BaseModel):
    """Ideal Customer Profile."""
    title: str = Field(description="Who they are")
    pain_points: List[str] = Field(default_factory=list)
    goals: List[str] = Field(default_factory=list)
    budget_range: str = Field(description="e.g., $50-500/month")
    decision_criteria: List[str] = Field(default_factory=list)
    where_they_hang: List[str] = Field(default_factory=list, description="Communities, platforms")


class PricingTier(BaseModel):
    """Pricing tier definition."""
    name: str
    price_monthly: int
    price_annual: Optional[int] = None
    features: List[str] = Field(default_factory=list)
    target_customer: str
    limits: dict = Field(default_factory=dict)


class BusinessSpec(BaseModel):
    """Complete business specification."""
    id: str = Field(description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Core definition
    name: str = Field(description="Business name")
    tagline: str
    positioning: str = Field(description="One-sentence positioning wedge")
    
    # Market
    icp: ICP
    product_type: ProductType
    business_model: BusinessModel
    
    # Offer
    core_promise: str = Field(description="Measurable outcome + timeframe")
    unique_mechanism: str = Field(description="Why this works differently")
    pricing_tiers: List[PricingTier] = Field(default_factory=list)
    
    # Go-to-market
    primary_channel: Channel
    backup_channel: Channel
    
    # Operations
    fulfillment_strategy: str
    support_strategy: str
    automation_plan: dict = Field(default_factory=dict)
    
    # Metrics
    target_conversion_rate: float = Field(default=0.02)
    target_cac: int = Field(description="Customer acquisition cost")
    target_ltv: int = Field(description="Lifetime value")
    target_churn_monthly: float = Field(default=0.05)
    
    # Build plan
    mvp_scope: List[str] = Field(default_factory=list)
    v1_scope: List[str] = Field(default_factory=list)
    v2_scope: List[str] = Field(default_factory=list)
    
    # Constraints
    constraints: BuildConstraints
    
    # Risks
    risks: List[dict] = Field(default_factory=list)


class BusinessConcept(BaseModel):
    """A business concept proposal."""
    title: str
    description: str
    icp: str
    pain_solved: str
    measurable_outcome: str
    low_touch_rationale: str
    competitive_moat: str
    pricing_ladder: List[PricingTier]
    acquisition_channels: List[Channel]
    mvp_scope: str
    risks: List[str]
    score: Optional[float] = None
