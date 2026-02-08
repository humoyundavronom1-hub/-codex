from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    email: str
    password: str

class GroupRuleUpdate(BaseModel):
    invite_required: int = Field(ge=1, le=50)
    reset_on_leave: bool
    ignore_bots: bool
    admins_bypass: bool
    auto_kick_timeout: int = Field(ge=60, le=86400)
    risk_threshold: float = Field(ge=0.0, le=1.0)
    is_enabled: bool

class ManualUnlockRequest(BaseModel):
    group_id: int
    user_id: int

class ResetProgressRequest(BaseModel):
    group_id: int
    user_id: int
