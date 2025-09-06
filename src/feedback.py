# Standard library imports
import random
import os

# Third-party library imports
import pandas as pd

# Project-specific imports
from .logger_config import logger

FEEDBACK_FILE = "data/feedback.csv"

# Predefined realistic comments
COMMENTS_POOL = [
    "Excellent teaching!",
    "Very helpful.",
    "Clear explanations.",
    "Good effort.",
    "Average performance.",
    "Could improve pacing.",
    "Friendly and patient.",
    "Needs more examples.",
    "Highly recommended!",
    "Student understood concepts well.",
]


def generate_feedback(
    schedule_df: pd.DataFrame, feedback_file=FEEDBACK_FILE
) -> pd.DataFrame:
    """
    Simulates realistic feedback for each student-teacher assignment.
    - rating: integer 1-5
    - comments: realistic placeholder text
    """
    # Validate input
    required_columns = {"student_id", "teacher_id", "time_slot"}
    if not required_columns.issubset(schedule_df.columns):
        raise ValueError(f"schedule_df must contain columns: {required_columns}")

    feedback_list = []
    for _, row in schedule_df.iterrows():
        # Logic to simulate rating: higher if student has 1:1 match, otherwise slightly lower
        if "group" in row.get("match_type", ""):
            rating = random.randint(3, 5)
        else:
            rating = random.randint(4, 5)

        # Randomly pick a comment from the pool
        comment = random.choice(COMMENTS_POOL)

        feedback_list.append(
            {
                "student_id": row["student_id"],
                "teacher_id": row["teacher_id"],
                "time_slot": row["time_slot"],
                "rating": rating,
                "comments": comment,
            }
        )

    feedback_df = pd.DataFrame(feedback_list)

    # Ensure data directory exists
    os.makedirs(os.path.dirname(feedback_file), exist_ok=True)

    # Save feedback to CSV
    feedback_df.to_csv(feedback_file, index=False)
    logger.info(f"Feedback generated and saved to {feedback_file}")

    return feedback_df
