# Standard library imports
from typing import List

# Project-specific imports
from .logger_config import logger


# Check if a student and teacher share at least one subject
def subject_overlap(student_subjects: List[str], teacher_subjects: List[str]) -> bool:
    """
    Returns True if there is at least one common subject between student and teacher.
    Logs the result.

    Args:
        student_subjects (List[str]): Subjects the student wants to learn
        teacher_subjects (List[str]): Subjects the teacher can teach

    Returns:
        bool: True if there is at least one overlapping subject, False otherwise
    """
    # Input validation
    if not isinstance(student_subjects, list) or not isinstance(teacher_subjects, list):
        raise TypeError("Both student_subjects and teacher_subjects must be lists")

    if not all(isinstance(s, str) for s in student_subjects + teacher_subjects):
        raise TypeError("All elements in subjects lists must be strings")

    overlap = bool(set(student_subjects) & set(teacher_subjects))

    # Logging
    logger.info(
        f"Checked subject overlap: {student_subjects} & {teacher_subjects} => {overlap}"
    )

    return overlap


# Get overlapping available time slots between student and teacher
def available_time_overlap(
    student_times: List[str], teacher_times: List[str]
) -> List[str]:
    """
    Returns a sorted list of overlapping time slots where both student and teacher are available.
    Logs the overlap.

    Args:
        student_times (List[str]): Time slots student prefers
        teacher_times (List[str]): Time slots teacher is available

    Returns:
        List[str]: Sorted list of common available time slots (empty if none)
    """
    # Input validation
    if not isinstance(student_times, list) or not isinstance(teacher_times, list):
        raise TypeError("Both student_times and teacher_times must be lists")

    if not all(isinstance(t, str) for t in student_times + teacher_times):
        raise TypeError("All elements in time lists must be strings")

    overlap = sorted(set(student_times) & set(teacher_times))

    # Logging
    logger.info(f"Checked time overlap: {student_times} & {teacher_times} => {overlap}")

    return overlap
