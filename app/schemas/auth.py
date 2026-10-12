from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User, UserPreference, UserProfile

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def get_settings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    prefs = {row.key: row.value for row in db.query(UserPreference).filter(UserPreference.user_id == current_user.id).all()}
    return {
        "theme": profile.theme if profile else "dark",
        "accent": profile.accent if profile else "purple",
        "autoplay": profile.autoplay if profile else True,
        "default_landing_page": profile.default_landing_page if profile else "discover",
        "layout_density": profile.layout_density if profile else "comfortable",
        "reduced_motion": profile.reduced_motion if profile else False,
        "preferences": prefs,
    }


@router.put("")
def save_settings(payload: dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict[str, Any]:
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
    for key in ["theme", "accent", "autoplay", "default_landing_page", "layout_density", "reduced_motion"]:
        if key in payload:
            setattr(profile, key, payload[key])
    for key, value in payload.get("preferences", {}).items():
        existing = db.query(UserPreference).filter(UserPreference.user_id == current_user.id, UserPreference.key == key).first()
        if existing:
            existing.value = str(value)
        else:
            db.add(UserPreference(user_id=current_user.id, key=key, value=str(value)))
    db.commit()
    return get_settings(db=db, current_user=current_user)
