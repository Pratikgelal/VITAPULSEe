"""app/models/workout.py — Workout logs | Feature: Workout Plan Generator"""
from app.models.base_model import BaseModel


class WorkoutModel(BaseModel):
    TABLE = 'workouts'

    @classmethod
    def log(cls, uid, wtype, duration, burned, notes, date):
        # Updated columns to match schema: activity_type and duration_minutes
        return cls.execute(
            'INSERT INTO workouts(user_id, activity_type, duration_minutes, calories_burned, notes, log_date, created_at) VALUES(%s, %s, %s, %s, %s, %s, NOW())',
            (uid, wtype, duration, burned, notes, date)
        )

    @classmethod
    def recent(cls, uid, limit=7):
        return cls.fetch_all('SELECT * FROM workouts WHERE user_id=%s ORDER BY log_date DESC LIMIT %s', (uid, limit))

    @classmethod
    def week_total(cls, uid, start, end):
        # Updated SUM target to duration_minutes to match schema
        row = cls.fetch_one(
            'SELECT COUNT(*) AS sessions, COALESCE(SUM(duration_minutes), 0) AS mins, COALESCE(SUM(calories_burned), 0) AS burned FROM workouts WHERE user_id=%s AND log_date BETWEEN %s AND %s',
            (uid, start, end)
        )
        return row or {'sessions': 0, 'mins': 0, 'burned': 0}

    @classmethod
    def delete(cls, wid, uid):
        return cls.execute('DELETE FROM workouts WHERE id=%s AND user_id=%s', (wid, uid))
