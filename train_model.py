import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

def classify_performance(score):
    if score >= 75:
        return 'Good'
    elif score >= 50:
        return 'Average'
    else:
        return 'Needs Improvement'

def prepare_data(df):
    # Create a performance label for each subject
    subjects = ['Math', 'Science', 'English', 'History', 'Geography']
    for subject in subjects:
        df[subject + '_perf'] = df[subject].apply(classify_performance)

    # For simplicity, create a target label: if any subject is 'Needs Improvement', label as 1 else 0
    df['Needs_Improvement'] = df[[sub + '_perf' for sub in subjects]].apply(lambda x: 1 if 'Needs Improvement' in x.values else 0, axis=1)

    # Encode categorical variables
    le_gender = LabelEncoder()
    le_class = LabelEncoder()
    df['Gender_enc'] = le_gender.fit_transform(df['Gender'])
    df['Class_enc'] = le_class.fit_transform(df['Class'])

    # Features: Age, Gender_enc, Class_enc, Attendance, subject scores
    feature_cols = ['Age', 'Gender_enc', 'Class_enc', 'Attendance'] + subjects
    X = df[feature_cols]
    y = df['Needs_Improvement']

    return X, y, le_gender, le_class

def train_and_save_model():
    df = pd.read_csv('data/student_data.csv')
    X, y, le_gender, le_class = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Save model and encoders
    joblib.dump(clf, 'models/student_performance_model.joblib')
    joblib.dump(le_gender, 'models/le_gender.joblib')
    joblib.dump(le_class, 'models/le_class.joblib')
    print("Model and encoders saved to models/ directory")

if __name__ == "__main__":
    train_and_save_model()
