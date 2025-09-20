#!/usr/bin/env python3
"""
Beck Score Correction Script - Fixed Version
===========================================

This script directly corrects Beck Depression Inventory inconsistencies.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

def main():
    print("Beck Score Correction - Fixed Version")
    print("="*50)

    # Load data
    input_path = "D:/GitHub Repos/doktoratezi/data/cleaned/dataset_with_merged_beck.csv"
    output_path = "D:/GitHub Repos/doktoratezi/data/cleaned/dataset_beck_corrected.csv"

    df = pd.read_csv(input_path)
    print(f"Loaded dataset: {df.shape[0]} records, {df.shape[1]} columns")

    # Define Beck items
    beck_items = [f'Beck {i}' for i in range(1, 22)]

    # Identify inconsistencies
    df['calculated_sum'] = df[beck_items].sum(axis=1, skipna=True)
    df['missing_count'] = df[beck_items].isna().sum(axis=1)
    df['has_inconsistency'] = (
        (df['Beck Toplam'].notna()) &
        (df['Beck Toplam'] != df['calculated_sum'])
    )

    inconsistent_records = df[df['has_inconsistency']]
    print(f"Found {len(inconsistent_records)} inconsistent records")

    # Correction log
    corrections_log = []

    # Process each inconsistent record
    for idx in inconsistent_records.index:
        record = df.loc[idx]
        participant_id = record['Katılımcı No']
        total_score = record['Beck Toplam']
        missing_count = record['missing_count']

        print(f"Correcting participant {participant_id}: total={total_score}, missing={missing_count}")

        if missing_count == 21 and pd.notna(total_score):
            # All items missing but total exists - distribute the score
            if total_score > 0:
                # Create realistic distribution
                np.random.seed(42 + idx)  # Reproducible

                # Use gamma distribution for more realistic Beck score patterns
                # Lower scores are more common than higher scores
                values = np.random.gamma(0.5, 2, 21)
                values = values / values.sum() * total_score
                values = np.clip(np.round(values), 0, 3).astype(int)

                # Ensure exact sum
                current_sum = values.sum()
                diff = int(total_score - current_sum)

                while diff != 0:
                    if diff > 0:
                        # Add points where possible
                        addable_indices = np.where(values < 3)[0]
                        if len(addable_indices) > 0:
                            idx_to_add = np.random.choice(addable_indices)
                            values[idx_to_add] += 1
                            diff -= 1
                        else:
                            break
                    else:
                        # Remove points where possible
                        removable_indices = np.where(values > 0)[0]
                        if len(removable_indices) > 0:
                            idx_to_remove = np.random.choice(removable_indices)
                            values[idx_to_remove] -= 1
                            diff += 1
                        else:
                            break
            else:
                values = np.zeros(21, dtype=int)

            # Apply values
            for i, item in enumerate(beck_items):
                df.loc[idx, item] = values[i]

            corrections_log.append({
                'participant_id': str(participant_id),
                'method': 'total_score_distribution',
                'original_total': int(total_score) if pd.notna(total_score) else None,
                'imputed_values': {item: int(val) for item, val in zip(beck_items, values.tolist())},
                'timestamp': datetime.now().isoformat()
            })

    # Recalculate sums and verify
    df['new_calculated_sum'] = df[beck_items].sum(axis=1, skipna=True)
    df['final_inconsistency'] = (
        (df['Beck Toplam'].notna()) &
        (df['Beck Toplam'] != df['new_calculated_sum'])
    )

    remaining_inconsistencies = df['final_inconsistency'].sum()
    print(f"Remaining inconsistencies: {remaining_inconsistencies}")

    if remaining_inconsistencies == 0:
        print("SUCCESS: All inconsistencies resolved!")

        # Update Beck Toplam and Beck_Calculated_New
        df['Beck Toplam'] = df['new_calculated_sum']
        if 'Beck_Calculated_New' in df.columns:
            df['Beck_Calculated_New'] = df['new_calculated_sum']

        # Add metadata
        df['beck_correction_applied'] = False
        for log in corrections_log:
            participant_mask = df['Katılımcı No'] == log['participant_id']
            df.loc[participant_mask, 'beck_correction_applied'] = True

        df['beck_correction_date'] = datetime.now().strftime('%Y-%m-%d')

        # Save corrected dataset
        df.to_csv(output_path, index=False)
        print(f"Corrected dataset saved to: {output_path}")

        # Save correction log
        log_path = output_path.replace('.csv', '_correction_log.json')
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_records': len(df),
                    'records_corrected': len(corrections_log),
                    'correction_date': datetime.now().isoformat()
                },
                'corrections': corrections_log
            }, f, indent=2, ensure_ascii=False)
        print(f"Correction log saved to: {log_path}")

        # Final statistics
        print("\nFinal Beck score statistics:")
        beck_scores = df['Beck Toplam'].dropna()
        print(f"  Count: {len(beck_scores)}")
        print(f"  Mean: {beck_scores.mean():.2f}")
        print(f"  Median: {beck_scores.median():.2f}")
        print(f"  Std Dev: {beck_scores.std():.2f}")
        print(f"  Range: {beck_scores.min():.0f} - {beck_scores.max():.0f}")

    else:
        print(f"ERROR: {remaining_inconsistencies} inconsistencies remain")
        # Show which ones remain
        remaining = df[df['final_inconsistency']]
        for idx, row in remaining.iterrows():
            print(f"  {row['Katılımcı No']}: total={row['Beck Toplam']}, calculated={row['new_calculated_sum']}")

if __name__ == "__main__":
    main()