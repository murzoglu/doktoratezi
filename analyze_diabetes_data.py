#!/usr/bin/env python3
"""
Comprehensive analysis of diabetes patient data to find missing patients.
"""

import pandas as pd
import os
import glob

def analyze_main_dataset():
    """Analyze the main dataset for diabetes patients and potential misclassifications."""

    # Read the main dataset with groups
    df_path = "/d/GitHub Repos/doktoratezi/data/raw/main_dataset_with_groups.csv"

    try:
        df = pd.read_csv(df_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(df_path, encoding='latin-1')

    print("=== MAIN DATASET ANALYSIS ===")
    print(f"Total records: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    # Check group distribution
    if 'Grup' in df.columns:
        group_counts = df['Grup'].value_counts()
        print("\nGroup distribution:")
        for group, count in group_counts.items():
            print(f"  {group}: {count}")

    # Check diabetes diagnosis dates
    dm_date_col = 'DM Tanı Tarihi'
    if dm_date_col in df.columns:
        # Find records with diabetes diagnosis dates
        has_dm_date = df[dm_date_col].notna() & (df[dm_date_col] != '')
        print(f"\nRecords with diabetes diagnosis date: {has_dm_date.sum()}")

        # Check if any control patients have diabetes diagnosis dates
        if 'Grup' in df.columns:
            control_with_dm = df[(df['Grup'] == 'Kontrol') & has_dm_date]
            print(f"Control patients with DM diagnosis date: {len(control_with_dm)}")

            if len(control_with_dm) > 0:
                print("\nControl patients with diabetes diagnosis dates:")
                print(control_with_dm[['Katılımcı No', dm_date_col, 'Grup']].head(10))

            diabetes_with_dm = df[(df['Grup'] == 'Diyabet') & has_dm_date]
            print(f"Diabetes patients with DM diagnosis date: {len(diabetes_with_dm)}")

    # Check participant ID patterns
    print("\nParticipant ID patterns:")
    if 'Katılımcı No' in df.columns:
        participant_ids = df['Katılımcı No'].dropna()

        # Diabetes group IDs
        if 'Grup' in df.columns:
            diabetes_ids = df[df['Grup'] == 'Diyabet']['Katılımcı No'].dropna()
            control_ids = df[df['Grup'] == 'Kontrol']['Katılımcı No'].dropna()

            print(f"Diabetes patient ID examples: {diabetes_ids.head(5).tolist()}")
            print(f"Control patient ID examples: {control_ids.head(5).tolist()}")

            # Check for ID patterns
            diabetes_id_prefixes = [str(id_).split('-')[0] for id_ in diabetes_ids if '-' in str(id_)]
            control_id_prefixes = [str(id_).split('-')[0] for id_ in control_ids if '-' in str(id_)]

            print(f"Diabetes ID prefixes: {set(diabetes_id_prefixes)}")
            print(f"Control ID prefixes: {set(control_id_prefixes)}")

    return df

def check_other_data_files():
    """Check for other data files in the project."""

    print("\n=== OTHER DATA FILES ANALYSIS ===")

    # Check all CSV and Excel files
    data_dir = "/d/GitHub Repos/doktoratezi"
    file_patterns = ['**/*.csv', '**/*.xlsx', '**/*.xls']

    all_files = []
    for pattern in file_patterns:
        files = glob.glob(os.path.join(data_dir, pattern), recursive=True)
        all_files.extend(files)

    # Filter out Orange3 test files and focus on project data
    project_files = [f for f in all_files if 'orange3' not in f.lower() and 'test' not in f.lower()]

    print(f"Found {len(project_files)} data files:")
    for file in sorted(project_files):
        file_size = os.path.getsize(file) if os.path.exists(file) else 0
        print(f"  {file} ({file_size} bytes)")

        # Try to read each file and check for diabetes-related data
        if file_size > 0:
            try:
                if file.endswith('.csv'):
                    temp_df = pd.read_csv(file, nrows=5)
                elif file.endswith(('.xlsx', '.xls')):
                    temp_df = pd.read_excel(file, nrows=5)

                print(f"    Columns: {len(temp_df.columns)}, Rows: {len(temp_df)}")

                # Check for diabetes-related keywords in columns
                diabetes_keywords = ['diyabet', 'diabetes', 'dm', 'tanı', 'grup']
                relevant_cols = [col for col in temp_df.columns if any(keyword in str(col).lower() for keyword in diabetes_keywords)]
                if relevant_cols:
                    print(f"    Potential diabetes columns: {relevant_cols}")

            except Exception as e:
                print(f"    Error reading file: {e}")

def analyze_cleaned_data():
    """Analyze the cleaned datasets."""

    print("\n=== CLEANED DATA ANALYSIS ===")

    cleaned_files = [
        "/d/GitHub Repos/doktoratezi/data/cleaned/cleaned_dataset.csv",
        "/d/GitHub Repos/doktoratezi/data/cleaned/cleaned_dataset_no_duplicates.csv"
    ]

    for file_path in cleaned_files:
        if os.path.exists(file_path):
            print(f"\nAnalyzing: {os.path.basename(file_path)}")
            try:
                df = pd.read_csv(file_path)
                print(f"  Total records: {len(df)}")
                print(f"  Columns: {len(df.columns)}")

                if 'group' in df.columns:
                    group_counts = df['group'].value_counts()
                    print("  Group distribution:")
                    for group, count in group_counts.items():
                        print(f"    {group}: {count}")

            except Exception as e:
                print(f"  Error reading file: {e}")

def main():
    """Main analysis function."""

    print("COMPREHENSIVE DIABETES PATIENT DATA ANALYSIS")
    print("=" * 50)

    # Analyze main dataset
    main_df = analyze_main_dataset()

    # Check other data files
    check_other_data_files()

    # Analyze cleaned data
    analyze_cleaned_data()

    print("\n" + "=" * 50)
    print("SUMMARY AND RECOMMENDATIONS")
    print("=" * 50)

    print("""
Based on the analysis:
1. The main dataset shows only 38 diabetes patients vs expected ~100
2. Need to check Google Drive for additional data files
3. Verify if there are separate data collection batches
4. Check for patients with diabetes diagnosis dates in control group
5. Look for additional Excel files or database exports
    """)

if __name__ == "__main__":
    main()