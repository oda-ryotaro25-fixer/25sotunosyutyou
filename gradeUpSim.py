import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
import seaborn as sns
import os

# 保存用ディレクトリの作成
save_dir = "career_simulation_graphs"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 日本語フォントの設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

# データの準備
# 上位予想（上位10%）
upper_years = [1, 2, 3, 4, 5, 7, 9, 11, 13, 16]
upper_salary = [340, 390, 430, 480, 520, 590, 700, 800, 900, 980]
upper_grade = ['B2', 'B1', 'P4', 'P3', 'P2', 'P1', 'M3', 'M2', 'M1', 'D3']
upper_retention = [100, 92, 85, 80, 75, 68, 60, 55, 50, 45]

# 標準予想（中央50%）
standard_years = [1, 2, 3, 4, 6, 8, 11, 14, 17]
standard_salary = [340, 340, 390, 430, 480, 520, 590, 700, 800]
standard_grade = ['B2', 'B2', 'B1', 'P4', 'P3', 'P2', 'P1', 'M3', 'M2']
standard_retention = [100, 95, 90, 85, 75, 65, 55, 45, 40]

# 下位予想（下位25%）
lower_years = [1, 3, 5, 7, 10, 13, 16]
lower_salary = [340, 340, 390, 430, 480, 520, 590]
lower_grade = ['B2', 'B2', 'B1', 'P4', 'P3', 'P2', 'P1']
lower_retention = [100, 90, 80, 70, 55, 45, 35]

# 1. 年収推移グラフ
plt.figure(figsize=(10, 8))
plt.plot(upper_years, upper_salary, 'o-', linewidth=2.5, markersize=8, 
         label='上位10%（ハイパフォーマー）', color='#FF6B6B')
plt.plot(standard_years, standard_salary, 's-', linewidth=2.5, markersize=8,
         label='標準50%（平均的成長）', color='#4ECDC4')
plt.plot(lower_years, lower_salary, '^-', linewidth=2.5, markersize=8,
         label='下位25%（緩やかな成長）', color='#95A5A6')

plt.xlabel('勤続年数', fontsize=12)
plt.ylabel('年収（万円）', fontsize=12)
plt.title('パフォーマンスグループ別年収推移', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(loc='upper left')
plt.xlim(0, 18)
plt.ylim(300, 1000)
plt.tight_layout()
plt.savefig(f'{save_dir}/01_salary_progression.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. 残存率グラフ
plt.figure(figsize=(10, 8))
plt.plot(upper_years, upper_retention, 'o-', linewidth=2.5, markersize=8,
         label='上位10%', color='#FF6B6B')
plt.plot(standard_years, standard_retention, 's-', linewidth=2.5, markersize=8,
         label='標準50%', color='#4ECDC4')
plt.plot(lower_years, lower_retention, '^-', linewidth=2.5, markersize=8,
         label='下位25%', color='#95A5A6')

plt.xlabel('勤続年数', fontsize=12)
plt.ylabel('残存率（%）', fontsize=12)
plt.title('パフォーマンスグループ別残存率', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right')
plt.xlim(0, 18)
plt.ylim(30, 105)
plt.tight_layout()
plt.savefig(f'{save_dir}/02_retention_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. グレード分布の積み上げ面グラフ
plt.figure(figsize=(12, 8))

# 各年次でのグレード別人数を推定（新卒54人ベース）
years = np.arange(1, 21)
grade_distribution = pd.DataFrame(index=years, columns=['B2', 'B1', 'P4', 'P3', 'P2', 'P1', 'M3', 'M2', 'M1', 'D3'])
grade_distribution = grade_distribution.fillna(0)

# 簡易的な分布モデル
for year in years:
    total = 54 * (0.95 ** (year-1))  # 離職率を考慮
    if year <= 2:
        grade_distribution.loc[year, 'B2'] = total * 0.7
        grade_distribution.loc[year, 'B1'] = total * 0.3
    elif year <= 4:
        grade_distribution.loc[year, 'B1'] = total * 0.3
        grade_distribution.loc[year, 'P4'] = total * 0.5
        grade_distribution.loc[year, 'P3'] = total * 0.2
    elif year <= 7:
        grade_distribution.loc[year, 'P4'] = total * 0.2
        grade_distribution.loc[year, 'P3'] = total * 0.4
        grade_distribution.loc[year, 'P2'] = total * 0.3
        grade_distribution.loc[year, 'P1'] = total * 0.1
    elif year <= 10:
        grade_distribution.loc[year, 'P3'] = total * 0.2
        grade_distribution.loc[year, 'P2'] = total * 0.4
        grade_distribution.loc[year, 'P1'] = total * 0.3
        grade_distribution.loc[year, 'M3'] = total * 0.1
    elif year <= 15:
        grade_distribution.loc[year, 'P2'] = total * 0.2
        grade_distribution.loc[year, 'P1'] = total * 0.4
        grade_distribution.loc[year, 'M3'] = total * 0.2
        grade_distribution.loc[year, 'M2'] = total * 0.15
        grade_distribution.loc[year, 'M1'] = total * 0.05
    else:
        grade_distribution.loc[year, 'P1'] = total * 0.3
        grade_distribution.loc[year, 'M3'] = total * 0.3
        grade_distribution.loc[year, 'M2'] = total * 0.2
        grade_distribution.loc[year, 'M1'] = total * 0.15
        grade_distribution.loc[year, 'D3'] = total * 0.05

# 積み上げ面グラフ
plt.stackplot(years, 
              grade_distribution['B2'], grade_distribution['B1'],
              grade_distribution['P4'], grade_distribution['P3'], 
              grade_distribution['P2'], grade_distribution['P1'],
              grade_distribution['M3'], grade_distribution['M2'], 
              grade_distribution['M1'], grade_distribution['D3'],
              labels=['B2', 'B1', 'P4', 'P3', 'P2', 'P1', 'M3', 'M2', 'M1', 'D3'],
              alpha=0.8)

plt.xlabel('勤続年数', fontsize=12)
plt.ylabel('社員数', fontsize=12)
plt.title('勤続年数別グレード分布（新卒54名/年）', fontsize=14, fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), ncol=1)
plt.grid(True, alpha=0.3)
plt.xlim(1, 20)
plt.tight_layout()
plt.savefig(f'{save_dir}/03_grade_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. 10年後の年収分布（ヒストグラム）
plt.figure(figsize=(10, 8))

# 10年後の年収分布をシミュレーション
np.random.seed(42)
n_employees = 54

# 各グループの人数
n_upper = int(n_employees * 0.1)
n_standard = int(n_employees * 0.65)
n_lower = n_employees - n_upper - n_standard

# 各グループの年収分布（正規分布でばらつきを追加）
upper_10y = np.random.normal(700, 50, n_upper)
standard_10y = np.random.normal(550, 40, n_standard)
lower_10y = np.random.normal(450, 30, n_lower)

all_salaries = np.concatenate([upper_10y, standard_10y, lower_10y])

plt.hist(all_salaries, bins=20, alpha=0.7, color='#3498DB', edgecolor='black')
plt.axvline(np.mean(all_salaries), color='red', linestyle='--', linewidth=2, 
            label=f'平均: {np.mean(all_salaries):.0f}万円')
plt.axvline(np.median(all_salaries), color='green', linestyle='--', linewidth=2,
            label=f'中央値: {np.median(all_salaries):.0f}万円')

plt.xlabel('入社10年後の年収（万円）', fontsize=12)
plt.ylabel('人数', fontsize=12)
plt.title('入社10年後の年収分布', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{save_dir}/04_salary_distribution_10years.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. 昇進タイミングの可視化
plt.figure(figsize=(12, 8))

# グレードを数値に変換
grade_to_num = {'B2': 1, 'B1': 2, 'P4': 3, 'P3': 4, 'P2': 5, 'P1': 6, 
                'M3': 7, 'M2': 8, 'M1': 9, 'D3': 10}

# 各グループのグレード推移をプロット
upper_grade_num = [grade_to_num[g] for g in upper_grade]
standard_grade_num = [grade_to_num[g] for g in standard_grade]
lower_grade_num = [grade_to_num[g] for g in lower_grade]

plt.plot(upper_years, upper_grade_num, 'o-', linewidth=3, markersize=10,
         label='上位10%', color='#FF6B6B')
plt.plot(standard_years, standard_grade_num, 's-', linewidth=3, markersize=10,
         label='標準50%', color='#4ECDC4')
plt.plot(lower_years, lower_grade_num, '^-', linewidth=3, markersize=10,
         label='下位25%', color='#95A5A6')

# グレード名をy軸に表示
plt.yticks(list(grade_to_num.values()), list(grade_to_num.keys()))

# 背景色でグレードレベルを表示
plt.axhspan(1, 2.5, alpha=0.2, color='lightcoral', label='ベーシックレベル')
plt.axhspan(2.5, 6.5, alpha=0.2, color='lightblue', label='プロフェッショナルレベル')
plt.axhspan(6.5, 9.5, alpha=0.2, color='lightgreen', label='マネージャーレベル')
plt.axhspan(9.5, 10.5, alpha=0.2, color='lightyellow', label='ディレクターレベル')

plt.xlabel('勤続年数', fontsize=14)
plt.ylabel('グレード', fontsize=14)
plt.title('パフォーマンスグループ別キャリア進行', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3, axis='x')
plt.legend(loc='upper left')
plt.xlim(0, 18)
plt.ylim(0.5, 10.5)
plt.tight_layout()
plt.savefig(f'{save_dir}/05_career_progression.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. 年収と昇進の相関を示す散布図
plt.figure(figsize=(10, 8))

# 全データを結合
all_years = upper_years + standard_years + lower_years
all_salaries_plot = upper_salary + standard_salary + lower_salary
all_grades = upper_grade + standard_grade + lower_grade
all_groups = ['上位10%']*len(upper_years) + ['標準50%']*len(standard_years) + ['下位25%']*len(lower_years)

# 散布図
colors = {'上位10%': '#FF6B6B', '標準50%': '#4ECDC4', '下位25%': '#95A5A6'}
for group in colors:
    mask = [g == group for g in all_groups]
    x = [y for y, m in zip(all_years, mask) if m]
    y = [s for s, m in zip(all_salaries_plot, mask) if m]
    plt.scatter(x, y, c=colors[group], label=group, s=100, alpha=0.7, edgecolors='black')

plt.xlabel('勤続年数', fontsize=14)
plt.ylabel('年収（万円）', fontsize=14)
plt.title('勤続年数と年収の相関', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{save_dir}/06_salary_correlation.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. キャリアパスの比較表
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('tight')
ax.axis('off')

# 比較表のデータ作成
comparison_data = []
max_years = 20

for year in range(1, max_years + 1):
    row = [f'{year}年目']
    
    # 上位10%
    if year in upper_years:
        idx = upper_years.index(year)
        row.append(f'{upper_grade[idx]} ({upper_salary[idx]}万円)')
    else:
        row.append('-')
    
    # 標準50%
    if year in standard_years:
        idx = standard_years.index(year)
        row.append(f'{standard_grade[idx]} ({standard_salary[idx]}万円)')
    else:
        row.append('-')
    
    # 下位25%
    if year in lower_years:
        idx = lower_years.index(year)
        row.append(f'{lower_grade[idx]} ({lower_salary[idx]}万円)')
    else:
        row.append('-')
    
    comparison_data.append(row)

# テーブル作成
table = ax.table(cellText=comparison_data,
                  colLabels=['勤続年数', '上位10%', '標準50%', '下位25%'],
                  cellLoc='center',
                  loc='center',
                  colWidths=[0.15, 0.28, 0.28, 0.28])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)

# ヘッダーの色設定
for i in range(4):
    table[(0, i)].set_facecolor('#4ECDC4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# 行の色を交互に設定
for i in range(1, len(comparison_data) + 1):
    if i % 2 == 0:
        for j in range(4):
            table[(i, j)].set_facecolor('#F0F0F0')

plt.title('キャリアパス比較表', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig(f'{save_dir}/07_career_comparison_table.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. 年収成長率の比較グラフ
plt.figure(figsize=(10, 8))

# 成長率の計算（初任給340万円を基準）
upper_growth = [s/340 * 100 for s in upper_salary]
standard_growth = [s/340 * 100 for s in standard_salary]
lower_growth = [s/340 * 100 for s in lower_salary]

plt.plot(upper_years, upper_growth, 'o-', linewidth=2.5, markersize=8,
         label='上位10%', color='#FF6B6B')
plt.plot(standard_years, standard_growth, 's-', linewidth=2.5, markersize=8,
         label='標準50%', color='#4ECDC4')
plt.plot(lower_years, lower_growth, '^-', linewidth=2.5, markersize=8,
         label='下位25%', color='#95A5A6')

plt.axhline(y=100, color='gray', linestyle='--', alpha=0.5, label='初任給基準')
plt.xlabel('勤続年数', fontsize=12)
plt.ylabel('年収成長率（%）', fontsize=12)
plt.title('初任給からの年収成長率', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(loc='upper left')
plt.xlim(0, 18)
plt.ylim(90, 300)
plt.tight_layout()
plt.savefig(f'{save_dir}/08_salary_growth_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. グレード到達確率のヒートマップ
plt.figure(figsize=(12, 8))

# データの準備
grades = ['B2', 'B1', 'P4', 'P3', 'P2', 'P1', 'M3', 'M2', 'M1', 'D3']
years_range = range(1, 21)

# 到達確率マトリックスの作成
probability_matrix = np.zeros((len(grades), len(years_range)))

# 各グループの到達確率を設定（簡易モデル）
for i, grade in enumerate(grades):
    for j, year in enumerate(years_range):
        # 基本的な到達確率の設定
        if grade == 'B2':
            probability_matrix[i, j] = 100 if year == 1 else 20 if year <= 3 else 5
        elif grade == 'B1':
            probability_matrix[i, j] = 0 if year == 1 else 80 if year == 2 else 60 if year <= 4 else 10
        elif grade == 'P4':
            probability_matrix[i, j] = 0 if year <= 2 else 70 if year == 3 else 80 if year == 4 else 40 if year <= 6 else 10
        elif grade == 'P3':
            probability_matrix[i, j] = 0 if year <= 3 else 50 if year == 4 else 70 if year <= 7 else 30 if year <= 10 else 10
        elif grade == 'P2':
            probability_matrix[i, j] = 0 if year <= 4 else 40 if year <= 8 else 60 if year <= 12 else 20
        elif grade == 'P1':
            probability_matrix[i, j] = 0 if year <= 5 else 20 if year <= 10 else 40 if year <= 15 else 30
        elif grade == 'M3':
            probability_matrix[i, j] = 0 if year <= 7 else 10 if year <= 12 else 20 if year <= 17 else 15
        elif grade == 'M2':
            probability_matrix[i, j] = 0 if year <= 9 else 5 if year <= 15 else 10
        elif grade == 'M1':
            probability_matrix[i, j] = 0 if year <= 11 else 3 if year <= 18 else 5
        elif grade == 'D3':
            probability_matrix[i, j] = 0 if year <= 14 else 1 if year <= 20 else 2

# ヒートマップの作成
sns.heatmap(probability_matrix, 
            xticklabels=years_range,
            yticklabels=grades,
            cmap='YlOrRd',
            annot=True,
            fmt='.0f',
            cbar_kws={'label': '到達確率 (%)'},
            vmin=0,
            vmax=100)

plt.xlabel('勤続年数', fontsize=12)
plt.ylabel('グレード', fontsize=12)
plt.title('グレード別到達確率ヒートマップ', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{save_dir}/09_grade_probability_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. 組織ピラミッド図
plt.figure(figsize=(10, 8))

# 現在の組織構成（推定）
org_data = {
    'Director (D1-D3)': 10,
    'Manager (M1-M3)': 42,
    'Professional (P1-P4)': 160,
    'Basic (B1-B2)': 166
}

levels = list(org_data.keys())
sizes = list(org_data.values())
colors = ['#FFD700', '#90EE90', '#87CEEB', '#FFB6C1']

# ピラミッドの作成
y_pos = np.arange(len(levels))
bars = plt.barh(y_pos, sizes, color=colors, edgecolor='black', linewidth=1.5)

# 各バーに人数と割合を表示
total = sum(sizes)
for i, (bar, size) in enumerate(zip(bars, sizes)):
    percentage = size / total * 100
    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, 
             f'{size}名 ({percentage:.1f}%)', 
             va='center', fontsize=11, fontweight='bold')

plt.yticks(y_pos, levels)
plt.xlabel('人数', fontsize=12)
plt.title('推定組織構成ピラミッド（全378名）', fontsize=14, fontweight='bold')
plt.xlim(0, max(sizes) * 1.3)
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig(f'{save_dir}/10_organization_pyramid.png', dpi=300, bbox_inches='tight')
plt.close()

# 保存完了メッセージ
print("=" * 60)
print("すべてのグラフが保存されました")
print("=" * 60)
print(f"保存先ディレクトリ: {save_dir}/")
print("\n保存されたファイル:")
print("1. 01_salary_progression.png - パフォーマンスグループ別年収推移")
print("2. 02_retention_rate.png - パフォーマンスグループ別残存率")
print("3. 03_grade_distribution.png - 勤続年数別グレード分布")
print("4. 04_salary_distribution_10years.png - 入社10年後の年収分布")
print("5. 05_career_progression.png - キャリア進行グラフ")
print("6. 06_salary_correlation.png - 勤続年数と年収の相関")
print("7. 07_career_comparison_table.png - キャリアパス比較表")
print("8. 08_salary_growth_rate.png - 年収成長率の比較")
print("9. 09_grade_probability_heatmap.png - グレード到達確率ヒートマップ")
print("10. 10_organization_pyramid.png - 組織構成ピラミッド")
print("=" * 60)

# サマリーレポートをテキストファイルとして保存
with open(f'{save_dir}/career_simulation_summary.txt', 'w', encoding='utf-8') as f:
    f.write("新卒社員キャリアシミュレーション統計サマリー\n")
    f.write("=" * 60 + "\n\n")
    f.write("【企業情報】\n")
    f.write("・業種：IT系上場企業（上場3年目）\n")
    f.write("・従業員数：378名\n")
    f.write("・平均年齢：27.8歳\n")
    f.write("・新卒採用：54名/年（大卒50%、高専卒50%）\n\n")
    
    f.write("【入社10年後の到達グレードと年収】\n")
    f.write("・上位10% : M3グレード (700万円) - 残存率: 60%\n")
    f.write("・標準50% : P1グレード (590万円) - 残存率: 55%\n")
    f.write("・下位25% : P3グレード (480万円) - 残存率: 55%\n\n")
    
    f.write("【キャリアの重要な節目】\n")
    f.write("・3-5年目  : プロフェッショナル層への昇進で初めて差がつく\n")
    f.write("・8-10年目 : マネージャー層への昇進が大きな分岐点\n")
    f.write("・15年目以降: ディレクター層は極めて限定的（全体の2-3%）\n\n")
    
    f.write("【年収成長率（入社時比）】\n")
    f.write(f"・上位10% : 10年で{700/340:.1f}倍、15年で{900/340:.1f}倍\n")
    f.write(f"・標準50% : 10年で{590/340:.1f}倍、15年で{700/340:.1f}倍\n")
    f.write(f"・下位25% : 10年で{480/340:.1f}倍、15年で{520/340:.1f}倍\n\n")
    
    f.write("【推定される組織構成】\n")
    f.write("・Director層 (D1-D3): 8-12名 (3%)\n")
    f.write("・Manager層 (M1-M3): 38-45名 (11%)\n")
    f.write("・Professional層 (P1-P4): 150-170名 (43%)\n")
    f.write("・Basic層 (B1-B2): 150-170名 (43%)\n")

print("\nサマリーレポートも保存されました: career_simulation_summary.txt")