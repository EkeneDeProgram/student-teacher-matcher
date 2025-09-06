# Student-Teacher Matching Automation

## Overview
**Goal:** Build a system that can match students with teachers for 1:1 and group lessons, taking into account subjects, availability, and preferences.  


## Installation

### Clone the Repository
```bash
git clone https://github.com/EkeneDeProgram/student-teacher-matcher.git
cd student-teacher-matcher
```

### Create and Activate Virtual Environment
```bash
# Create a virtual environment named 'env'
python -m venv env

# Activate the virtual environment
# On Windows
env\Scripts\activate

# On macOS/Linux
source env/bin/activate
```

### Install Dependencies

Install all required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
## Usage

1. Prepare your dataset (Students.csv and Teachers.csv) in the data/ folder.

2. Run the main script to generate the matching schedule:

```bash
python main.py
```

3. Check for (schedule.csv and feedback.csv) in the output/ folder

## Project Structure

```bash
student-teacher-matcher/
│
├─ data/ # CSV files for students and teachers
├─ env/ # Virtual environment folder
├─ logs/ # Log files for program execution
├─ output/ # Generated schedules and feedback (CSVs)
├─ src/ # core logic and utilities
├─ main.py # Main script to run the matcher
├─ requirements.txt # Python dependencies
├─ README.md # Project documentation
├─ .gitignore # Git ignore file
```

## Approach & Assumptions

### Approach
The **Student-Teacher Matching Automation** project is designed to efficiently assign students to teachers for 1:1 or group lessons, taking into account subjects, availability, and preferences. The system follows a structured approach:

1. **Data Loading and Preprocessing**
   - Student and teacher data are read from CSV files.
   - List-based fields such as `subjects` and `time slots` are parsed and standardized.
   - Invalid or missing data is handled with safe defaults and logged for transparency.

2. **Matching Algorithm**
   - Students are matched with teachers based on overlapping subjects.
   - Matching respects both student preferred time slots and teacher availability.
   - Teachers have a maximum number of students per slot, ensuring group sessions are appropriately sized.
   - A baseline schedule is generated with either 1:1 or group lessons.

3. **Optional Feedback Loop**
   - Simulated feedback can be incorporated to adjust teacher assignments for improved satisfaction.
   - A machine learning model (Random Forest) is optionally trained to recommend teachers based on prior assignments and student subjects.

4. **Evaluation**
   - The schedule is evaluated with metrics such as:
     - Total number of students matched.
     - Teacher time slot utilization.
     - Average satisfaction score per teacher (from feedback if available).
   - Logging ensures transparency of each step and allows tracking potential issues.

### Assumptions
- All students and teachers have at least one subject and one available time slot.
- Missing or invalid data is minimal and handled using default values.
- Each teacher has a maximum number of students per time slot to prevent overcrowding.
- Feedback ratings are simulated realistically for evaluation purposes.
- The system prioritizes subject overlap first, then availability, and optionally uses historical feedback for further optimization.

This design ensures a balance between **practical scheduling constraints** and **student-teacher preference alignment**, while maintaining flexibility for enhancements such as machine learning-based recommendations.



