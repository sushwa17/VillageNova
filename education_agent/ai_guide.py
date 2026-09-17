"""School and AI innovation updates for the education agent."""

from __future__ import annotations


def get_ai_update(school_name: str, learner_type: str, ai_topic: str) -> str:
    """Return a practical daily AI and school innovation update."""
    school = (school_name or "School").strip() or "School"
    learner = (learner_type or "student").strip().lower()
    topic = (ai_topic or "basics").strip().lower()

    lines = [
        f"AI update for {school}: today’s learning idea is to explore {topic} in a simple, practical way.",
        "Students can compare how AI helps with writing, image ideas, and basic research while keeping teacher guidance in the loop.",
        "Teachers can use AI tools to prepare quiz questions, explain concepts, and support project-based learning without replacing classroom teaching.",
    ]

    if learner in {"student", "child", "school"}:
        lines.append("Students should use AI as a helper for learning, not as a shortcut for copying assignments or answers.")
    else:
        lines.append("Adult learners can use AI for digital literacy, skill practice, and understanding everyday technology in a safe way.")

    lines.append("School innovation reminder: keep a human check on all AI-generated work, verify facts, and focus on creativity, problem-solving, and responsible use.")
    return " ".join(lines)
