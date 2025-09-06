# Third-party library imports
import pandas as pd
import os

# Project-specific imports
from .logger_config import logger

FEEDBACK_FILE = "data/feedback.csv"


def evaluate_schedule(
    schedule: pd.DataFrame,
    students: pd.DataFrame,
    teachers: pd.DataFrame,
    feedback_file: str = FEEDBACK_FILE,
):
    """
    Evaluates the student-teacher schedule and logs a summary.

    Args:
        schedule (pd.DataFrame): Schedule with student-teacher assignments
        students (pd.DataFrame): Original student dataset
        teachers (pd.DataFrame): Original teacher dataset
        feedback_file (str): Path to the feedback CSV containing ratings

    Logs:
        - Total number of students
        - Number of students matched
        - Teacher time slot utilization
        - Overall average satisfaction score
        - Average satisfaction per teacher
    """

    # Input validation
    required_schedule_cols = {"student_id", "teacher_id", "time_slot"}
    if not required_schedule_cols.issubset(schedule.columns):
        missing = required_schedule_cols - set(schedule.columns)
        logger.error(f"Schedule missing required columns: {missing}")
        raise ValueError(f"Schedule missing required columns: {missing}")

    # Remove placeholder rows (students/teachers with no valid slot)
    clean_schedule = schedule[schedule["time_slot"] != "N/A"].copy()

    # Count unique students that were successfully matched
    num_students_matched = clean_schedule["student_id"].nunique()

    # Calculate teacher time slot utilization
    teacher_usage = (
        clean_schedule.groupby(["teacher_id", "time_slot"])
        .size()
        .reset_index(name="students_assigned")
    )

    # Log the basic evaluation summary
    logger.info(f"Total students: {len(students)}")
    logger.info(f"Students matched (valid slots only): {num_students_matched}")
    logger.info("Teacher time slot utilization:\n%s", teacher_usage)

    # Include Average Satisfaction Score
    if os.path.exists(feedback_file):
        try:
            feedback_df = pd.read_csv(feedback_file)

            # Exclude feedback with placeholder slots
            feedback_df = feedback_df[feedback_df["time_slot"] != "N/A"]

            # Merge schedule with feedback
            merged_df = clean_schedule.merge(
                feedback_df[["student_id", "teacher_id", "time_slot", "rating"]],
                on=["student_id", "teacher_id", "time_slot"],
                how="left",
            )

            # Calculate overall average satisfaction
            if not merged_df["rating"].dropna().empty:
                avg_satisfaction = merged_df["rating"].mean()
                logger.info(
                    f"Overall average satisfaction score: {avg_satisfaction:.2f}"
                )

                # Calculate average satisfaction per teacher
                teacher_satisfaction = (
                    merged_df.groupby("teacher_id")["rating"].mean().reset_index()
                )
                teacher_satisfaction.rename(
                    columns={"rating": "avg_satisfaction"}, inplace=True
                )
                logger.info(
                    "Average satisfaction per teacher:\n%s", teacher_satisfaction
                )
            else:
                logger.warning("No valid ratings found in feedback for evaluation.")

        except Exception as e:
            logger.error(f"Error calculating satisfaction scores: {e}")
    else:
        logger.warning(
            f"Feedback file not found at {feedback_file}. Skipping satisfaction score calculation."
        )
