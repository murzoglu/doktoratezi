#!/usr/bin/env python3
"""
Beck Score Inconsistency Correction Script
==========================================

This script identifies and corrects inconsistencies between Beck Depression Inventory
total scores and the sum of individual Beck items using statistical imputation methods.

Author: Data Analysis Script
Date: 2025-09-20
"""

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class BeckScoreCorrector:
    """Class to handle Beck score inconsistencies and imputation."""

    def __init__(self, data_path):
        """Initialize with dataset path."""
        self.data_path = data_path
        self.df = None
        self.beck_items = [f'Beck {i}' for i in range(1, 22)]
        self.correction_log = []

    def load_data(self):
        """Load the dataset."""
        print("Loading dataset...")
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset loaded: {self.df.shape[0]} records, {self.df.shape[1]} columns")

    def identify_inconsistencies(self):
        """Identify records with Beck score inconsistencies."""
        print("\n" + "="*60)
        print("IDENTIFYING BECK SCORE INCONSISTENCIES")
        print("="*60)

        # Calculate current sum from available items
        self.df['current_calculated_sum'] = self.df[self.beck_items].sum(axis=1, skipna=True)
        self.df['missing_beck_count'] = self.df[self.beck_items].isna().sum(axis=1)
        self.df['has_inconsistency'] = (
            (self.df['Beck Toplam'].notna()) &
            (self.df['Beck Toplam'] != self.df['current_calculated_sum'])
        )

        inconsistent_count = self.df['has_inconsistency'].sum()
        total_count = len(self.df)

        print(f"Total records: {total_count}")
        print(f"Records with inconsistencies: {inconsistent_count}")
        print(f"Percentage of inconsistent records: {(inconsistent_count/total_count)*100:.2f}%")

        # Analyze patterns in inconsistencies
        print("\nInconsistency patterns:")
        inconsistent_records = self.df[self.df['has_inconsistency']]

        print(f"Records with Beck total but missing all items: {(inconsistent_records['missing_beck_count'] == 21).sum()}")
        print(f"Records with partial missing items: {(inconsistent_records['missing_beck_count'] < 21).sum()}")

        # Show missing value pattern
        print("\nMissing values per Beck item:")
        for item in self.beck_items:
            missing_count = self.df[item].isna().sum()
            print(f"{item}: {missing_count} ({(missing_count/total_count)*100:.1f}%)")

        return inconsistent_records

    def mean_imputation_by_available_items(self, record_idx):
        """Impute missing Beck items using mean of available items for the same record."""
        record = self.df.loc[record_idx]
        available_items = []

        for item in self.beck_items:
            if pd.notna(record[item]):
                available_items.append(record[item])

        if available_items:
            mean_value = np.mean(available_items)
            # Round to nearest valid Beck score (0, 1, 2, 3)
            imputed_value = max(0, min(3, round(mean_value)))
            return imputed_value
        else:
            return None

    def regression_based_imputation(self, target_item):
        """Use regression to predict missing Beck items based on other variables."""
        # Prepare features for regression
        feature_cols = []

        # Add available Beck items as features
        for item in self.beck_items:
            if item != target_item:
                feature_cols.append(item)

        # Add demographic variables that might be predictive
        demographic_cols = ['Anne Doğum Tarihi', 'Çocuk Sayısı', 'Eğitim Durumu',
                           'Çalışma Durumu', 'Medeni Durum']

        for col in demographic_cols:
            if col in self.df.columns:
                # Convert to numeric if possible
                try:
                    self.df[f'{col}_numeric'] = pd.to_numeric(self.df[col], errors='coerce')
                    feature_cols.append(f'{col}_numeric')
                except:
                    pass

        # Create training data (records with target item available)
        train_mask = self.df[target_item].notna()

        if train_mask.sum() < 10:  # Need minimum samples for regression
            return None

        X_train = self.df.loc[train_mask, feature_cols].fillna(0)
        y_train = self.df.loc[train_mask, target_item]

        # Use Random Forest for better handling of missing values and non-linear relationships
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Predict missing values
        predict_mask = self.df[target_item].isna()
        if predict_mask.sum() > 0:
            X_predict = self.df.loc[predict_mask, feature_cols].fillna(0)
            predictions = model.predict(X_predict)

            # Clip to valid range and round
            predictions = np.clip(np.round(predictions), 0, 3)
            return predict_mask, predictions

        return None, None

    def distribute_total_score(self, record_idx):
        """Distribute total Beck score across missing items proportionally."""
        record = self.df.loc[record_idx]
        total_score = record['Beck Toplam']

        if pd.isna(total_score):
            return None

        # Count missing items
        missing_items = []
        available_sum = 0

        for item in self.beck_items:
            if pd.isna(record[item]):
                missing_items.append(item)
            else:
                available_sum += record[item]

        if not missing_items:
            return None

        # Calculate remaining score to distribute
        remaining_score = max(0, total_score - available_sum)

        # Distribute proportionally
        items_count = len(missing_items)
        if items_count > 0:
            base_score = remaining_score / items_count

            # Create distribution (some randomness to avoid all items having same score)
            np.random.seed(42 + record_idx)  # Reproducible randomness
            weights = np.random.dirichlet(np.ones(items_count))

            imputed_values = {}
            for i, item in enumerate(missing_items):
                value = base_score * weights[i] * items_count
                value = max(0, min(3, round(value)))  # Ensure valid range
                imputed_values[item] = value

            return imputed_values

        return None

    def apply_corrections(self):
        """Apply various correction methods to inconsistent records."""
        print("\n" + "="*60)
        print("APPLYING BECK SCORE CORRECTIONS")
        print("="*60)

        inconsistent_records = self.df[self.df['has_inconsistency']]
        corrections_made = 0

        for idx in inconsistent_records.index:
            record = self.df.loc[idx]
            participant_id = record['Katılımcı No']
            total_score = record['Beck Toplam']
            missing_count = record['missing_beck_count']

            print(f"\nProcessing participant {participant_id} (missing {missing_count} items, total score: {total_score})")

            # Strategy 1: If all items are missing but total score exists, distribute the score
            if missing_count == 21 and pd.notna(total_score):
                print("  Applying total score distribution method...")

                # Distribute total score across all items
                base_value = total_score / 21

                # Use beta distribution to create realistic variation
                np.random.seed(42 + idx)
                if total_score > 0:
                    # Create values that sum to total_score
                    weights = np.random.dirichlet(np.ones(21))
                    values = weights * total_score
                    # Round and adjust to ensure sum equals total
                    values = np.round(values).astype(int)
                    values = np.clip(values, 0, 3)

                    # Adjust to match total score exactly
                    current_sum = values.sum()
                    diff = int(total_score - current_sum)

                    # Distribute the difference
                    if diff != 0:
                        indices = np.random.choice(21, abs(diff), replace=True)
                        for i in indices:
                            if diff > 0 and values[i] < 3:
                                values[i] += 1
                            elif diff < 0 and values[i] > 0:
                                values[i] -= 1
                else:
                    values = np.zeros(21)

                # Apply the values
                for i, item in enumerate(self.beck_items):
                    self.df.loc[idx, item] = values[i]

                corrections_made += 1
                self.correction_log.append({
                    'participant_id': participant_id,
                    'method': 'total_score_distribution',
                    'original_total': total_score,
                    'missing_items': missing_count,
                    'imputed_values': dict(zip(self.beck_items, values))
                })

            # Strategy 2: If some items are available, use regression imputation
            elif missing_count < 21 and missing_count > 0:
                print("  Applying regression-based imputation...")

                # Use KNN imputation for Beck items
                beck_data = self.df[self.beck_items].copy()
                imputer = KNNImputer(n_neighbors=5)

                # Fit on all data and transform just this record
                beck_imputed = imputer.fit_transform(beck_data)

                # Update missing values for this record
                original_values = {}
                for i, item in enumerate(self.beck_items):
                    if pd.isna(self.df.loc[idx, item]):
                        original_values[item] = self.df.loc[idx, item]
                        imputed_val = max(0, min(3, round(beck_imputed[idx, i])))
                        self.df.loc[idx, item] = imputed_val

                corrections_made += 1
                self.correction_log.append({
                    'participant_id': participant_id,
                    'method': 'knn_imputation',
                    'original_total': total_score,
                    'missing_items': missing_count,
                    'imputed_items': list(original_values.keys())
                })

        print(f"\nTotal corrections applied: {corrections_made}")
        return corrections_made

    def validate_corrections(self):
        """Validate that corrections are within reasonable bounds."""
        print("\n" + "="*60)
        print("VALIDATING CORRECTIONS")
        print("="*60)

        # Check value ranges
        validation_errors = 0

        for item in self.beck_items:
            item_values = self.df[item].dropna()
            if len(item_values) > 0:
                min_val = item_values.min()
                max_val = item_values.max()

                if min_val < 0 or max_val > 3:
                    print(f"ERROR: {item} has values outside valid range (0-3): min={min_val}, max={max_val}")
                    validation_errors += 1
                else:
                    print(f"OK {item}: valid range (min={min_val}, max={max_val})")

        # Recalculate totals and check consistency
        self.df['corrected_calculated_sum'] = self.df[self.beck_items].sum(axis=1, skipna=True)

        # For validation, only check records that should have been corrected
        # (i.e., records where we have both Beck Toplam and corrected individual items)
        has_total = self.df['Beck Toplam'].notna()
        has_items = self.df[self.beck_items].notna().any(axis=1)

        self.df['final_inconsistency'] = (
            has_total & has_items &
            (self.df['Beck Toplam'] != self.df['corrected_calculated_sum'])
        )

        remaining_inconsistencies = self.df['final_inconsistency'].sum()
        print(f"\nRemaining inconsistencies after correction: {remaining_inconsistencies}")

        if validation_errors == 0:
            print("OK All Beck item values are within valid range (0-3)")
        else:
            print(f"ERROR {validation_errors} validation errors found")

        return validation_errors == 0 and remaining_inconsistencies == 0

    def update_total_scores(self):
        """Recalculate Beck total scores based on corrected items."""
        print("\n" + "="*60)
        print("UPDATING TOTAL SCORES")
        print("="*60)

        # Update Beck Toplam with corrected calculated sums
        original_totals = self.df['Beck Toplam'].copy()
        self.df['Beck Toplam'] = self.df[self.beck_items].sum(axis=1, skipna=True)

        # Track changes
        changes_made = (original_totals != self.df['Beck Toplam']).sum()
        print(f"Total scores updated for {changes_made} records")

        # Update the Beck_Calculated_New column as well
        if 'Beck_Calculated_New' in self.df.columns:
            self.df['Beck_Calculated_New'] = self.df['Beck Toplam']
            print("OK Beck_Calculated_New column updated")

        return changes_made

    def generate_report(self):
        """Generate a detailed report of all corrections made."""
        print("\n" + "="*60)
        print("GENERATING CORRECTION REPORT")
        print("="*60)

        report = {
            'summary': {
                'total_records': len(self.df),
                'records_corrected': len(self.correction_log),
                'correction_methods_used': list(set([log['method'] for log in self.correction_log])),
                'total_missing_items_imputed': sum([log.get('missing_items', 0) for log in self.correction_log])
            },
            'corrections_by_method': {},
            'detailed_corrections': self.correction_log
        }

        # Group by method
        for log in self.correction_log:
            method = log['method']
            if method not in report['corrections_by_method']:
                report['corrections_by_method'][method] = 0
            report['corrections_by_method'][method] += 1

        # Print summary
        print(f"Total records processed: {report['summary']['total_records']}")
        print(f"Records corrected: {report['summary']['records_corrected']}")
        print(f"Total missing items imputed: {report['summary']['total_missing_items_imputed']}")

        print("\nCorrections by method:")
        for method, count in report['corrections_by_method'].items():
            print(f"  {method}: {count} records")

        # Statistical summary
        print("\nStatistical summary of corrected Beck scores:")
        beck_totals = self.df['Beck Toplam'].dropna()
        print(f"  Mean: {beck_totals.mean():.2f}")
        print(f"  Median: {beck_totals.median():.2f}")
        print(f"  Std Dev: {beck_totals.std():.2f}")
        print(f"  Range: {beck_totals.min():.0f} - {beck_totals.max():.0f}")

        return report

    def save_corrected_data(self, output_path):
        """Save the corrected dataset."""
        print("\n" + "="*60)
        print("SAVING CORRECTED DATASET")
        print("="*60)

        # Add metadata columns
        corrected_indices = []
        for log in self.correction_log:
            # Find indices that match the participant ID
            participant_id = log.get('participant_id')
            if participant_id:
                matching_indices = self.df[self.df['Katılımcı No'] == participant_id].index
                corrected_indices.extend(matching_indices)

        self.df['beck_correction_applied'] = self.df.index.isin(corrected_indices)
        self.df['beck_correction_date'] = pd.Timestamp.now().strftime('%Y-%m-%d')

        # Save corrected dataset
        self.df.to_csv(output_path, index=False)
        print(f"OK Corrected dataset saved to: {output_path}")

        # Save correction log
        log_path = output_path.replace('.csv', '_correction_log.json')
        import json
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.correction_log, f, indent=2, ensure_ascii=False)
        print(f"OK Correction log saved to: {log_path}")

        return output_path


def main():
    """Main execution function."""
    print("BECK SCORE INCONSISTENCY CORRECTION TOOL")
    print("=" * 50)

    # Define paths
    input_path = "D:/GitHub Repos/doktoratezi/data/cleaned/dataset_with_merged_beck.csv"
    output_path = "D:/GitHub Repos/doktoratezi/data/cleaned/dataset_beck_corrected.csv"

    # Initialize corrector
    corrector = BeckScoreCorrector(input_path)

    try:
        # Execute correction pipeline
        corrector.load_data()
        inconsistent_records = corrector.identify_inconsistencies()

        if len(inconsistent_records) > 0:
            corrections_made = corrector.apply_corrections()
            validation_success = corrector.validate_corrections()

            if validation_success:
                changes_made = corrector.update_total_scores()
                report = corrector.generate_report()
                output_file = corrector.save_corrected_data(output_path)

                print("\n" + "="*60)
                print("CORRECTION COMPLETED SUCCESSFULLY")
                print("="*60)
                print(f"OK Input file: {input_path}")
                print(f"OK Output file: {output_file}")
                print(f"OK Records corrected: {corrections_made}")
                print(f"OK Total scores updated: {changes_made}")
                print("OK All validation checks passed")

            else:
                print("\n" + "="*60)
                print("VALIDATION FAILED")
                print("="*60)
                print("ERROR Some corrections failed validation. Please review the data manually.")

        else:
            print("\n" + "="*60)
            print("NO CORRECTIONS NEEDED")
            print("="*60)
            print("OK No Beck score inconsistencies found in the dataset")

    except Exception as e:
        print(f"\nERROR during correction process: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()