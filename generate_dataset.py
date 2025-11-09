import pandas as pd
import numpy as np
import random

def generate_sample_data(num_records=200):
    np.random.seed(42)
    random.seed(42)

    names = [f"Student_{i}" for i in range(1, num_records + 1)]
    ages = np.random.randint(12, 18, size=num_records)
    genders = np.random.choice(['Male', 'Female'], size=num_records)
    classes = np.random.choice(['7th', '8th', '9th', '10th', '11th', '12th'], size=num_records)

    subjects = ['Math', 'Science', 'English', 'History', 'Geography']
    data = {
        'Name': names,
        'Age': ages,
        'Gender': genders,
        'Class': classes,
        'Attendance': np.random.uniform(60, 100, size=num_records).round(2)
    }

    # Generate scores for each subject between 0 and 100
    for subject in subjects:
        data[subject] = np.random.randint(40, 101, size=num_records)

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv('data/student_data.csv', index=False)
    print(f"Generated dataset with {num_records} records and saved to data/student_data.csv")

if __name__ == "__main__":
    generate_sample_data()
