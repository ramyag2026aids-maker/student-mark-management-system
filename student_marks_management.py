import sys
from typing import Dict, List, Any, Optional

# Core Configuration Constants
SUBJECTS: List[str] = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Computer Science",
    "English"
]

MAX_MARK: float = 100.0
MIN_MARK: float = 0.0
PASSING_MARK: float = 40.0


def print_header(title: str, width: int = 70) -> None:
    """Prints a styled decorative header."""
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def get_valid_roll_no(existing_roll_nos: List[str]) -> str:
    """
    Prompts user for a roll number, ensuring it is non-empty and unique.
    
    Args:
        existing_roll_nos: List of roll numbers currently in the system.
        
    Returns:
        A unique, valid roll number string.
    """
    while True:
        roll_no = input("Enter Roll Number / Student ID: ").strip()
        if not roll_no:
            print("  [Error] Roll number cannot be empty. Please enter a valid ID.")
            continue
        if roll_no in existing_roll_nos:
            print(f"  [Error] Roll number '{roll_no}' already exists! Each student must have a unique ID.")
            continue
        return roll_no


def get_valid_name() -> str:
    """
    Prompts user for a student name, ensuring it is non-empty and contains valid characters.
    
    Returns:
        A formatted (Title Cased) student name.
    """
    while True:
        name = input("Enter Student Full Name: ").strip()
        if not name:
            print("  [Error] Student name cannot be blank. Please try again.")
            continue
        # Check if name contains at least one alphabetic character
        if not any(char.isalpha() for char in name):
            print("  [Error] Name must contain alphabetic characters. Please try again.")
            continue
        # Ensure only allowed characters: letters, spaces, hyphens, dots
        if not all(char.isalpha() or char.isspace() or char in ".-'" for char in name):
            print("  [Error] Name contains invalid characters. Use letters, spaces, or hyphens.")
            continue
        return name.title()


def get_valid_mark(subject: str) -> float:
    """
    Prompts user for marks in a given subject, with validation for type and range.
    
    Args:
        subject: Name of the subject.
        
    Returns:
        Validated mark as a float between MIN_MARK and MAX_MARK.
    """
    while True:
        raw_input = input(f"  Enter marks for {subject} ({int(MIN_MARK)}-{int(MAX_MARK)}): ").strip()
        try:
            mark = float(raw_input)
            if mark < MIN_MARK or mark > MAX_MARK:
                print(f"    [Error] Marks must be between {MIN_MARK} and {MAX_MARK}. You entered '{raw_input}'.")
                continue
            return round(mark, 2)
        except ValueError:
            print(f"    [Error] Invalid input '{raw_input}'! Please enter a valid numeric value.")


def calculate_total(marks: Dict[str, float]) -> float:
    """
    Calculates the sum of marks obtained across all subjects.
    
    Args:
        marks: Dictionary mapping subject name to marks obtained.
        
    Returns:
        Total marks as a float.
    """
    return round(sum(marks.values()), 2)


def calculate_percentage(total: float, num_subjects: int) -> float:
    """
    Calculates the aggregate percentage.
    
    Args:
        total: Total marks obtained.
        num_subjects: Total number of subjects.
        
    Returns:
        Percentage as a float rounded to 2 decimal places.
    """
    if num_subjects == 0:
        return 0.0
    max_total = num_subjects * MAX_MARK
    return round((total / max_total) * 100.0, 2)


def check_pass_fail(marks: Dict[str, float], passing_threshold: float = PASSING_MARK) -> tuple:
    """
    Evaluates whether the student has passed or failed.
    A student passes only if marks in EVERY subject >= passing_threshold.
    
    Args:
        marks: Dictionary of subject marks.
        passing_threshold: Minimum mark required to pass a subject.
        
    Returns:
        Tuple of (status: str, failed_subjects: List[str])
    """
    failed_subjects = [sub for sub, mark in marks.items() if mark < passing_threshold]
    status = "Pass" if len(failed_subjects) == 0 else "Fail"
    return status, failed_subjects


def calculate_grade(percentage: float, status: str) -> str:
    """
    Determines the letter grade according to academic percentage standards.
    If the student failed in any subject, grade is strictly 'F'.
    
    Grading Scale:
        >= 90%      : A+ (Outstanding)
        80% - 89.9% : A  (Excellent)
        70% - 79.9% : B  (Very Good)
        60% - 69.9% : C  (Good)
        50% - 59.9% : D  (Average)
        40% - 49.9% : E  (Pass)
        < 40%       : F  (Fail)
    """
    if status == "Fail":
        return "F"
    if percentage >= 90.0:
        return "A+"
    elif percentage >= 80.0:
        return "A"
    elif percentage >= 70.0:
        return "B"
    elif percentage >= 60.0:
        return "C"
    elif percentage >= 50.0:
        return "D"
    elif percentage >= 40.0:
        return "E"
    else:
        return "F"


def create_student_record(roll_no: str, name: str, marks: Dict[str, float]) -> Dict[str, Any]:
    """
    Packages student data and computed metrics into a structured dictionary.
    """
    total = calculate_total(marks)
    percentage = calculate_percentage(total, len(marks))
    status, failed_subs = check_pass_fail(marks, PASSING_MARK)
    grade = calculate_grade(percentage, status)

    return {
        "roll_no": roll_no,
        "name": name,
        "marks": marks,
        "total": total,
        "percentage": percentage,
        "status": status,
        "failed_subjects": failed_subs,
        "grade": grade
    }


def add_student_flow(students: List[Dict[str, Any]]) -> None:
    """Handles user interaction to collect and store a new student record."""
    print_header("ADD NEW STUDENT RECORD")
    existing_rolls = [s["roll_no"] for s in students]
    
    roll_no = get_valid_roll_no(existing_rolls)
    name = get_valid_name()
    
    print("\nEnter Marks for each subject (out of 100):")
    marks: Dict[str, float] = {}
    for sub in SUBJECTS:
        marks[sub] = get_valid_mark(sub)
        
    student = create_student_record(roll_no, name, marks)
    students.append(student)
    
    print(f"\n[Success] Record for '{name}' (Roll No: {roll_no}) added successfully!")
    print(f"Total: {student['total']}/{len(SUBJECTS)*100} | Percentage: {student['percentage']}% | Grade: {student['grade']} | Status: {student['status']}")


def display_student_card(student: Dict[str, Any]) -> None:
    """Prints a single student's complete marks report card."""
    print("\n" + "┌" + "─" * 58 + "┐")
    print(f"│ {'STUDENT MARKS REPORT CARD'.center(56)} │")
    print("├" + "─" * 58 + "┤")
    print(f"│ Roll Number : {student['roll_no']:<42} │")
    print(f"│ Name        : {student['name']:<42} │")
    print("├" + "─" * 58 + "┤")
    print(f"│ {'SUBJECT':<30} {'MARKS (100)':<12} {'RESULT':<10} │")
    print("├" + "─" * 58 + "┤")
    for sub, mk in student["marks"].items():
        res = "PASS" if mk >= PASSING_MARK else "FAIL"
        print(f"│ {sub:<30} {mk:<12.2f} {res:<10} │")
    print("├" + "─" * 58 + "┤")
    max_total = len(student["marks"]) * 100
    print(f"│ Total Marks : {student['total']:.2f} / {max_total:<28} │")
    print(f"│ Percentage  : {student['percentage']:.2f}%{'':<33} │")
    print(f"│ Grade       : {student['grade']:<42} │")
    status_str = f"{student['status']} ({', '.join(student['failed_subjects'])})" if student['failed_subjects'] else student['status']
    print(f"│ Final Status: {status_str:<42} │")
    print("└" + "─" * 58 + "┘")


def display_all_students(students: List[Dict[str, Any]]) -> None:
    """Displays all student records in a formatted tabular layout."""
    if not students:
        print("\n[Notice] No student records available in the database.")
        return

    print_header("ALL STUDENT RECORDS")
    
    # Header format
    hdr = f"{'Roll No':<10} | {'Student Name':<20} | {'Total':<8} | {'%':<7} | {'Grade':<6} | {'Status':<6}"
    sep = "-" * len(hdr)
    print(sep)
    print(hdr)
    print(sep)
    
    for s in students:
        print(f"{s['roll_no']:<10} | {s['name']:<20} | {s['total']:<8.2f} | {s['percentage']:<6.2f}% | {s['grade']:<6} | {s['status']:<6}")
    print(sep)
    print(f"Total Students Displayed: {len(students)}")


def search_student(students: List[Dict[str, Any]]) -> None:
    """Searches for a student by roll number or name."""
    if not students:
        print("\n[Notice] Database is empty. Add students before searching.")
        return

    print_header("SEARCH STUDENT RECORD")
    query = input("Enter Roll Number or Name to search: ").strip()
    if not query:
        print("  [Error] Search query cannot be blank.")
        return

    found = []
    for s in students:
        if s["roll_no"].lower() == query.lower() or query.lower() in s["name"].lower():
            found.append(s)

    if found:
        print(f"\n[Found] {len(found)} matching record(s):")
        for s in found:
            display_student_card(s)
    else:
        print(f"\n[Not Found] No student matching '{query}' was found.")


def display_class_statistics(students: List[Dict[str, Any]]) -> None:
    """Calculates and displays comprehensive class performance analytics."""
    if not students:
        print("\n[Notice] No student records available to calculate statistics.")
        return

    print_header("CLASS PERFORMANCE & STATISTICAL SUMMARY")
    total_students = len(students)
    passed_students = [s for s in students if s["status"] == "Pass"]
    failed_students = [s for s in students if s["status"] == "Fail"]
    
    all_percentages = [s["percentage"] for s in students]
    class_average = round(sum(all_percentages) / total_students, 2)
    
    topper = max(students, key=lambda s: s["total"])
    lowest = min(students, key=lambda s: s["total"])
    pass_pct = round((len(passed_students) / total_students) * 100.0, 2)

    print(f"Total Enrolled Students : {total_students}")
    print(f"Students Passed         : {len(passed_students)} ({pass_pct}%)")
    print(f"Students Failed         : {len(failed_students)} ({round(100.0 - pass_pct, 2)}%)")
    print(f"Class Average Score     : {class_average}%")
    print("-" * 50)
    print(f"Class Topper            : {topper['name']} (Roll No: {topper['roll_no']})")
    print(f"  -> Total: {topper['total']} | Percentage: {topper['percentage']}% | Grade: {topper['grade']}")
    print(f"Lowest Scorer           : {lowest['name']} (Roll No: {lowest['roll_no']})")
    print(f"  -> Total: {lowest['total']} | Percentage: {lowest['percentage']}% | Grade: {lowest['grade']}")
    print("-" * 50)

    # Subject-wise statistics
    print("SUBJECT-WISE ANALYSIS:")
    print(f"{'Subject':<22} | {'Highest':<8} | {'Lowest':<8} | {'Average':<8}")
    print("-" * 52)
    for sub in SUBJECTS:
        sub_marks = [s["marks"][sub] for s in students]
        sub_max = max(sub_marks)
        sub_min = min(sub_marks)
        sub_avg = round(sum(sub_marks) / total_students, 2)
        print(f"{sub:<22} | {sub_max:<8.2f} | {sub_min:<8.2f} | {sub_avg:<8.2f}")
    print("-" * 52)


def delete_student(students: List[Dict[str, Any]]) -> None:
    """Deletes a student record by roll number."""
    if not students:
        print("\n[Notice] No student records available to delete.")
        return

    print_header("DELETE STUDENT RECORD")
    roll = input("Enter Roll Number to delete: ").strip()
    for i, s in enumerate(students):
        if s["roll_no"].lower() == roll.lower():
            confirm = input(f"Are you sure you want to delete record of '{s['name']}' ({s['roll_no']})? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                deleted = students.pop(i)
                print(f"[Success] Record for '{deleted['name']}' deleted.")
            else:
                print("[Cancelled] Deletion cancelled.")
            return
    print(f"[Not Found] Student with Roll Number '{roll}' not found.")


def print_menu() -> None:
    """Displays the main operation menu."""
    print("\n" + "=" * 45)
    print("   STUDENT MARKS MANAGEMENT SYSTEM")
    print("=" * 45)
    print(" [1] Add New Student Record")
    print(" [2] View All Student Records (Table)")
    print(" [3] Search Student (By Roll No / Name)")
    print(" [4] View Class Analytics & Summary")
    print(" [5] Delete Student Record")
    print(" [6] Exit System")
    print("=" * 45)


def main() -> None:
    """Main application loop."""
    students: List[Dict[str, Any]] = []

    print_header("WELCOME TO STUDENT MARKS MANAGEMENT SYSTEM")
    print("Academic Grading and Student Performance Tracker\n")

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student_flow(students)
        elif choice == "2":
            display_all_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            display_class_statistics(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            print("\nThank you for using Student Marks Management System. Goodbye!\n")
            break
        else:
            print("  [Error] Invalid choice! Please select an option between 1 and 6.")


if __name__ == "__main__":
    main()
