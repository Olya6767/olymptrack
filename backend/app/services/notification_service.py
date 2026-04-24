from datetime import date, timedelta
from ..models.olympiad import Olympiad
from ..models.mood import MoodEntry


def get_morning_summary(user_id: int) -> str:
    today = date.today()
    upcoming = Olympiad.query.filter(
        Olympiad.user_id == user_id,
        Olympiad.deadline >= today,
        Olympiad.deadline <= today + timedelta(days=7),
    ).all()

    lines = [f"Доброе утро! Сегодня {today.strftime('%d.%m.%Y')}"]
    if upcoming:
        lines.append("Ближайшие дедлайны:")
        for o in upcoming:
            days_left = (o.deadline - today).days
            lines.append(f"  - {o.name}: через {days_left} дн.")
    else:
        lines.append("Ближайших дедлайнов нет.")
    return "\n".join(lines)


def get_evening_prompt() -> str:
    return "Как прошёл день? Оцени настроение от 1 до 5."
