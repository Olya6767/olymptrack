import anthropic
from flask import current_app
from ..models.olympiad import Olympiad
from ..models.mood import MoodEntry
from ..models.time_tracker import TimeEntry


def get_user_context(user_id: int) -> str:
    olympiads = Olympiad.query.filter_by(user_id=user_id).all()
    moods = MoodEntry.query.filter_by(user_id=user_id).order_by(MoodEntry.date.desc()).limit(7).all()
    time_entries = TimeEntry.query.filter_by(user_id=user_id).order_by(TimeEntry.date.desc()).limit(14).all()

    lines = ["Данные пользователя:"]
    if olympiads:
        lines.append("Олимпиады: " + ", ".join(f"{o.name} ({o.status})" for o in olympiads))
    if moods:
        avg = sum(m.score for m in moods) / len(moods)
        lines.append(f"Настроение за 7 дней (среднее): {avg:.1f}/5")
    if time_entries:
        total_actual = sum(e.actual_minutes for e in time_entries)
        lines.append(f"Учёт времени за 2 недели: {total_actual} мин факт")
    return "\n".join(lines)


def get_ai_response(user_id: int, message: str) -> str:
    client = anthropic.Anthropic(api_key=current_app.config["ANTHROPIC_API_KEY"])
    context = get_user_context(user_id)
    system_prompt = (
        "Ты помощник для школьника, участвующего в олимпиадах. "
        "Ты знаешь данные пользователя и помогаешь с планированием, мотивацией и вопросами.\n\n"
        + context
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": message}],
    )
    return response.content[0].text
