# Third-party library imports
import pandas as pd
import os

# Project-specific imports
from src.data_loader import load_data
from src.matcher import match_with_feedback_loop
from src.feedback import generate_feedback
from src.evaluator import evaluate_schedule
from src.logger_config import logger

# File paths
STUDENTS_FILE = "data/students.csv"
TEACHERS_FILE = "data/teachers.csv"
OUTPUT_FILE = "output/schedule.csv"
FEEDBACK_FILE = "output/feedback.csv"


def main():
    try:
        # Load data
        students, teachers = load_data(STUDENTS_FILE, TEACHERS_FILE)
        logger.info(f"Loaded {len(students)} students and {len(teachers)} teachers.")

        # Generate (or reuse) feedback
        if os.path.exists(FEEDBACK_FILE):
            feedback_df = pd.read_csv(FEEDBACK_FILE)
        else:
            empty_schedule = pd.DataFrame(
                columns=["student_id", "teacher_id", "time_slot"]
            )
            feedback_df = generate_feedback(empty_schedule, feedback_file=FEEDBACK_FILE)

        # Run matching once with feedback loop
        schedule = match_with_feedback_loop(students, teachers, feedback_df)
        schedule_df = pd.DataFrame(schedule)
        logger.info(f"Matching completed. Total assignments: {len(schedule_df)}")

        # Save schedule
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        schedule_df.to_csv(OUTPUT_FILE, index=False)
        logger.info(f"Schedule saved to {OUTPUT_FILE}")

        # Generate new feedback for this run
        generate_feedback(schedule_df, feedback_file=FEEDBACK_FILE)
        logger.info("Feedback updated successfully.")

        # Evaluate schedule
        evaluate_schedule(schedule_df, students, teachers, feedback_file=FEEDBACK_FILE)
        logger.info("Schedule evaluation completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
