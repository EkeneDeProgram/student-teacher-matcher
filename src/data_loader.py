# Standard library imports
from typing import Tuple

# Third-party library imports
import pandas as pd

# Project-specific imports
from .logger_config import logger


# Function to preprocess list fields safely
def safe_split(value, field_name: str, default: str) -> list:
    """
    Safely split comma-separated strings into a list.
    Handles missing or invalid values by logging and returning a default.
    """
    if pd.isna(value) or str(value).strip() == "":
        logger.warning(f"Missing value for '{field_name}', using default '{default}'")
        return [default]
    return [item.strip() for item in str(value).split(",") if item.strip()]


# Function to load and preprocess student data
def load_students(file_path: str) -> pd.DataFrame:
    """
    Reads the Students CSV file and preprocesses the data.
    - Drops invalid rows (missing student_id).
    - Converts 'subjects' and 'preferred_time_slots' into lists.
    - Fills defaults for missing values.
    """
    try:
        students = pd.read_csv(file_path)
        initial_count = len(students)

        # Drop rows with missing student_id
        students = students.dropna(subset=["student_id"])
        dropped = initial_count - len(students)
        if dropped > 0:
            logger.warning(
                f"Dropped {dropped} invalid student rows (missing student_id)"
            )

        # Preprocess list fields with safe defaults
        students["subjects"] = students["subjects"].apply(
            lambda x: safe_split(x, "subjects", "Unknown")
        )
        students["preferred_time_slots"] = students["preferred_time_slots"].apply(
            lambda x: safe_split(x, "preferred_time_slots", "N/A")
        )

        logger.info(f"Loaded {len(students)} students from {file_path}")
        logger.info("Preprocessed student subjects and time slots")
        return students

    except Exception as e:
        logger.error(f"Error loading students from {file_path}: {e}")
        raise


# Function to load and preprocess teacher data
def load_teachers(file_path: str) -> pd.DataFrame:
    """
    Reads the Teachers CSV file and preprocesses the data.
    - Drops invalid rows (missing teacher_id).
    - Converts 'subjects' and 'available_time_slots' into lists.
    - Fills defaults for missing values.
    """
    try:
        teachers = pd.read_csv(file_path)
        initial_count = len(teachers)

        # Drop rows with missing teacher_id
        teachers = teachers.dropna(subset=["teacher_id"])
        dropped = initial_count - len(teachers)
        if dropped > 0:
            logger.warning(
                f"Dropped {dropped} invalid teacher rows (missing teacher_id)"
            )

        # Preprocess list fields with safe defaults
        teachers["subjects"] = teachers["subjects"].apply(
            lambda x: safe_split(x, "subjects", "Unknown")
        )
        teachers["available_time_slots"] = teachers["available_time_slots"].apply(
            lambda x: safe_split(x, "available_time_slots", "N/A")
        )

        logger.info(f"Loaded {len(teachers)} teachers from {file_path}")
        logger.info("Preprocessed teacher subjects and available time slots")
        return teachers

    except Exception as e:
        logger.error(f"Error loading teachers from {file_path}: {e}")
        raise


# Function to load both students and teachers together
def load_data(
    students_file: str, teachers_file: str
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Loads and preprocesses both students and teachers CSV files.
    - Cleans missing data.
    - Logs progress and warnings.
    """
    logger.info("Starting to load student and teacher data")
    students = load_students(students_file)
    teachers = load_teachers(teachers_file)
    logger.info("Successfully loaded and preprocessed both students and teachers")
    return students, teachers
