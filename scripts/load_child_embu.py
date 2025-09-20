#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# Child EMBU verilerini yükle ve incele
print("="*80)
print("ÇOCUK EMBU VERİLERİNİ YÜKLEME VE İNCELEME")
print("="*80)

# Excel dosyasını yükle
child_embu_file = 'data/raw/DM_Cocuk_EMBU.xlsx'
print(f"\nDosya: {child_embu_file}")

# Excel dosyasını oku
df_child_embu = pd.read_excel(child_embu_file)

print(f"\nVeri boyutu: {df_child_embu.shape}")
print(f"Satır sayısı: {len(df_child_embu)}")
print(f"Sütun sayısı: {df_child_embu.shape[1]}")

print("\nSütun isimleri:")
for i, col in enumerate(df_child_embu.columns, 1):
    print(f"  {i}. {col}")

print("\nİlk 5 satır:")
print(df_child_embu.head())

# EMBU sütunlarını bul
embu_cols = [col for col in df_child_embu.columns if 'EMBU' in str(col).upper()]
print(f"\nEMBU sütunları ({len(embu_cols)} adet):")
for col in embu_cols:
    print(f"  - {col}")

# Skala değerlerini kontrol et
if embu_cols:
    print("\nEMBU skorlarının değer aralıkları:")
    for col in embu_cols[:5]:  # İlk 5 EMBU sütunu
        if col in df_child_embu.columns:
            unique_vals = df_child_embu[col].dropna().unique()
            print(f"  {col}: {sorted(unique_vals)[:10]}")

# Katılımcı No sütununu kontrol et
id_columns = [col for col in df_child_embu.columns if 'Katılımcı' in str(col) or 'ID' in str(col).upper() or 'No' in str(col)]
print(f"\nKatılımcı ID sütunları:")
for col in id_columns:
    print(f"  - {col}")
    if col in df_child_embu.columns:
        sample_ids = df_child_embu[col].dropna().head(5).tolist()
        print(f"    Örnek değerler: {sample_ids}")

# Boş olmayan veri sayısını kontrol et
print("\nVeri doluluğu:")
non_empty_counts = df_child_embu.notna().sum()
for col in embu_cols[:5]:
    if col in df_child_embu.columns:
        count = non_empty_counts[col]
        percent = (count / len(df_child_embu)) * 100
        print(f"  {col}: {count}/{len(df_child_embu)} ({percent:.1f}%)")

# Özet istatistikler
if embu_cols:
    print("\nEMBU skorları özet istatistikleri:")
    print(df_child_embu[embu_cols].describe())

# Dosyayı CSV olarak kaydet (kolay işleme için)
output_file = 'data/raw/child_embu_data.csv'
df_child_embu.to_csv(output_file, index=False, encoding='utf-8')
print(f"\nVeri CSV olarak kaydedildi: {output_file}")