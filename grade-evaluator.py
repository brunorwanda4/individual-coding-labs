import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    if not data:
        print("FAILED: The CSV contains no assignment records.")
        return

    invalid_scores = []
    invalid_rows = []
    for record in data:
        score = record["score"]
        weight = record["weight"]
        if score < 0 or score > 100:
            invalid_scores.append(record["assignment"])
        if weight < 0:
            invalid_rows.append(record["assignment"])

    if invalid_scores:
        print("FAILED: Scores must be between 0 and 100:")
        for name in invalid_scores:
            print(f"  - {name}")
        return
    if invalid_rows:
        print("FAILED: Assignment weights cannot be negative:")
        for name in invalid_rows:
            print(f"  - {name}")
        return

    total_weight = sum(record["weight"] for record in data)
    summative_weight = sum(record["weight"] for record in data if record["group"].lower() == "summative")
    formative_weight = sum(record["weight"] for record in data if record["group"].lower() == "formative")

    print(f"Total weight: {total_weight:g}")
    print(f"Summative weight: {summative_weight:g}")
    print(f"Formative weight: {formative_weight:g}")

    if abs(total_weight - 100) > 0.0001:
        print("FAILED: Total assignment weight must equal 100.")
        return
    if abs(summative_weight - 40) > 0.0001:
        print("FAILED: Summative weight must equal 40.")
        return
    if abs(formative_weight - 60) > 0.0001:
        print("FAILED: Formative weight must equal 60.")
        return

    final_grade = sum(record["score"] * record["weight"] for record in data) / 100
    gpa = (final_grade / 100) * 5

    summative_records = [record for record in data if record["group"].lower() == "summative"]
    formative_records = [record for record in data if record["group"].lower() == "formative"]

    summative_score = sum(record["score"] * record["weight"] for record in summative_records) / summative_weight
    formative_score = sum(record["score"] * record["weight"] for record in formative_records) / formative_weight

    print(f"\nFinal Grade: {final_grade:.2f}%")
    print(f"GPA: {gpa:.2f}")
    print(f"Summative Average: {summative_score:.2f}%")
    print(f"Formative Average: {formative_score:.2f}%")

    passed = summative_score >= 50 and formative_score >= 50
    print("\nFinal Decision: " + ("PASSED" if passed else "FAILED"))

    failed_formative = [
        record for record in formative_records
        if record["score"] < 50
    ]
    if failed_formative:
        highest_weight = max(record["weight"] for record in failed_formative)
        eligible = [
            record["assignment"] for record in failed_formative
            if record["weight"] == highest_weight
        ]
        print("Resubmission eligible:")
        for name in eligible:
            print(f"  - {name}")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)