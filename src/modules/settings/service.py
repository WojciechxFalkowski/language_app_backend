from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from ..sql_app.database import get_db
from ..user.service import get_current_user
from ..user.models import User

from . import schemas, models

set_up_settings = [
    {
        "label": "levels",
        "options": [
            {
                "label": "prawda / fałsz",
                "is_selected": 1,
            },
            {
                "label": "A / B / C / D",
                "is_selected": 1,
            },
            {
                "label": "wpisz tekst",
                "is_selected": 1,
            }
        ]
    }
]

def create_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        for setting in set_up_settings:
            setting_levels = db.query(models.Setting).filter(models.Setting.user_id==current_user.id).all()
            if setting_levels:
                return setting_levels
            else:
                db_setting = models.Setting(label=setting['label'], user_id=current_user.id)
                db.add(db_setting)
                db.commit()
                for option in setting['options']:
                    db_option = models.Level(label=option['label'], is_selected=option['is_selected'], setting_id=db_setting.id)
                    db.add(db_option)
                    db.commit()
                    db.refresh(db_option)
                db.refresh(db_setting)
        return db.query(models.Setting).filter(models.Setting.user_id==current_user.id).join(models.Level, models.Setting.options).order_by(models.Level.id).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return db.query(models.Setting).filter(models.Setting.user_id == current_user.id).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def change_level(level_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        level: models.Level = db.query(models.Level).filter(models.Level.id == level_id).first()
        print('current_user.id')
        print(current_user.id)
        setting = db.query(models.Setting).filter(models.Setting.user_id==current_user.id).filter(models.Setting.id == level.setting_id).first()
        if setting:
            level.is_selected = not level.is_selected
            db.commit()
        else:
            raise Exception("Wrong level id")
        return db.query(models.Setting).filter(models.Setting.user_id == current_user.id).join(models.Level, models.Setting.options).order_by(models.Level.id).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))