# Standard library imports
from typing import Dict, List
from random import randint, choice
from collections import defaultdict

# Third-party library imports
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

# Project-specific imports
from .logger_config import logger
from .utils import subject_overlap, available_time_overlap


# Helper function
def assign_student_to_slot(
    student_id: int, teacher_id: int, slot: str, current_count: int
) -> Dict:
    """Create a schedule entry for a student-teacher assignment and log it."""
    lesson_type = "1:1" if current_count == 0 else "group"
    logger.info(
        f"Assigning Student {student_id} to Teacher {teacher_id} at {slot} ({lesson_type})"
    )
    return {
        "student_id": student_id,
        "teacher_id": teacher_id,
        "time_slot": slot,
        "lesson_type": lesson_type,
    }


def match_students_to_teachers(
    students: pd.DataFrame, teachers: pd.DataFrame
) -> List[Dict]:
    """Baseline matching based on subjects and time slots."""
    schedule = []

    required_student_cols = {"student_id", "subjects", "preferred_time_slots"}
    required_teacher_cols = {
        "teacher_id",
        "subjects",
        "available_time_slots",
        "max_students_per_slot",
    }

    if not required_student_cols.issubset(students.columns):
        missing = required_student_cols - set(students.columns)
        logger.error(f"Missing required student columns: {missing}")
        raise ValueError(f"Missing required student columns: {missing}")

    if not required_teacher_cols.issubset(teachers.columns):
        missing = required_teacher_cols - set(teachers.columns)
        logger.error(f"Missing required teacher columns: {missing}")
        raise ValueError(f"Missing required teacher columns: {missing}")

    logger.info(
        f"Starting student-teacher matching for {len(students)} students and {len(teachers)} teachers"
    )

    teacher_slots = {
        tid: {slot: 0 for slot in teacher["available_time_slots"]}
        for tid, teacher in teachers.set_index("teacher_id").iterrows()
    }

    for _, student in students.iterrows():
        matched = False
        for _, teacher in teachers.iterrows():
            if subject_overlap(student["subjects"], teacher["subjects"]):
                common_slots = available_time_overlap(
                    student["preferred_time_slots"], teacher["available_time_slots"]
                )
                for slot in common_slots:
                    if (
                        teacher_slots[teacher["teacher_id"]][slot]
                        < teacher["max_students_per_slot"]
                    ):
                        current_count = teacher_slots[teacher["teacher_id"]][slot]
                        schedule.append(
                            assign_student_to_slot(
                                student["student_id"],
                                teacher["teacher_id"],
                                slot,
                                current_count,
                            )
                        )
                        teacher_slots[teacher["teacher_id"]][slot] += 1
                        matched = True
                        break
            if matched:
                break
        if not matched:
            logger.warning(
                f"No available match found for Student {student['student_id']}"
            )

    logger.info(f"Completed matching. Total assignments: {len(schedule)}")
    return schedule


def train_teacher_recommender(schedule: pd.DataFrame, students: pd.DataFrame):
    """Train a Random Forest model to recommend teachers based on student subjects."""
    df = pd.merge(students, schedule[["student_id", "teacher_id"]], on="student_id")
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(df["subjects"])
    y = df["teacher_id"]
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    return clf, mlb


def match_with_feedback_loop(
    students: pd.DataFrame, teachers: pd.DataFrame, feedback_df: pd.DataFrame = None
) -> List[Dict]:
    """ML-guided matching with feedback loop."""
    final_schedule = []

    teacher_weights = defaultdict(lambda: 1.0)
    if feedback_df is not None and not feedback_df.empty:
        avg_ratings = feedback_df.groupby("teacher_id")["rating"].mean()
        for tid, rating in avg_ratings.items():
            teacher_weights[tid] = rating / 5.0

    teacher_slots = {
        tid: {slot: 0 for slot in teacher["available_time_slots"]}
        for tid, teacher in teachers.set_index("teacher_id").iterrows()
    }

    # Use baseline matching just for training
    initial_schedule = match_students_to_teachers(students, teachers)
    schedule_df = pd.DataFrame(initial_schedule)
    clf, mlb = train_teacher_recommender(schedule_df, students)

    for _, student in students.iterrows():
        candidate_teachers = teachers[
            teachers.apply(
                lambda t: subject_overlap(student["subjects"], t["subjects"]), axis=1
            )
        ].copy()  # FIX: avoid SettingWithCopyWarning

        candidate_teachers["weight"] = candidate_teachers["teacher_id"].map(
            teacher_weights
        )
        candidate_teachers = candidate_teachers.sort_values("weight", ascending=False)

        assigned = False
        for _, teacher in candidate_teachers.iterrows():
            common_slots = available_time_overlap(
                student["preferred_time_slots"], teacher["available_time_slots"]
            )
            for slot in common_slots:
                if (
                    teacher_slots[teacher["teacher_id"]][slot]
                    < teacher["max_students_per_slot"]
                ):
                    current_count = teacher_slots[teacher["teacher_id"]][slot]
                    final_schedule.append(
                        assign_student_to_slot(
                            student["student_id"],
                            teacher["teacher_id"],
                            slot,
                            current_count,
                        )
                    )
                    teacher_slots[teacher["teacher_id"]][slot] += 1
                    assigned = True
                    break
            if assigned:
                break

        if not assigned:
            predicted_teacher = clf.predict(mlb.transform([student["subjects"]]))[0]
            teacher_row = teachers[teachers["teacher_id"] == predicted_teacher].iloc[0]
            common_slots = available_time_overlap(
                student["preferred_time_slots"], teacher_row["available_time_slots"]
            )
            for slot in common_slots:
                if (
                    teacher_slots[predicted_teacher][slot]
                    < teacher_row["max_students_per_slot"]
                ):
                    current_count = teacher_slots[predicted_teacher][slot]
                    final_schedule.append(
                        assign_student_to_slot(
                            student["student_id"],
                            predicted_teacher,
                            slot,
                            current_count,
                        )
                    )
                    teacher_slots[predicted_teacher][slot] += 1
                    assigned = True
                    break

        if not assigned:
            logger.warning(
                f"No available match found for Student {student['student_id']}"
            )

    logger.info(
        f"Feedback loop matching completed. Total assignments: {len(final_schedule)}"
    )
    return final_schedule
