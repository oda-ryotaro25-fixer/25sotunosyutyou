import matplotlib.pyplot as plt
import numpy as np

# 日本語フォントの設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# グレードと想定年収
grades = ['B2', 'B1', 'P4', 'P3', 'P2', 'P1', 'M3', 'M2', 'M1', 'D3', 'D2', 'D1']
salaries = [340, 390, 430, 480, 520, 590, 700, 800, 900, 980, 1100, 1300]

# 年齢とグレードのマッピング（11年目でD2想定）
def get_grade_and_salary(years_of_service):
    if years_of_service <= 1:
        return 'B2', 340
    elif years_of_service <= 2:
        return 'B1', 390
    elif years_of_service <= 3:
        return 'P4', 430
    elif years_of_service <= 4:
        return 'P3', 480
    elif years_of_service <= 5:
        return 'P2', 520
    elif years_of_service <= 6:
        return 'P1', 590
    elif years_of_service <= 7:
        return 'M3', 700
    elif years_of_service <= 8:
        return 'M2', 800
    elif years_of_service <= 9:
        return 'M1', 900
    elif years_of_service <= 10:
        return 'D3', 980
    elif years_of_service <= 15:
        return 'D2', 1100
    else:
        return 'D1', 1300

# シミュレーション設定
start_age = 22
retirement_age = 60
years = np.arange(0, retirement_age - start_age + 1)
ages = start_age + years

# 年収の推移
annual_salaries = []
grade_history = []
for year in years:
    grade, salary = get_grade_and_salary(year + 1)
    annual_salaries.append(salary)
    grade_history.append(grade)

annual_salaries = np.array(annual_salaries)

# 3つのケースでシミュレーション
# ケース1: 貯金のみ（年収の20%）
savings_rate_1 = 0.20
# ケース2: 控えめな投資（年収の20%を投資、年利4%）
savings_rate_2 = 0.20
investment_return_2 = 0.04
# ケース3: 積極的な投資（年収の25%を投資、年利6%）
savings_rate_3 = 0.25
investment_return_3 = 0.06

# 資産計算
assets_case1 = np.zeros_like(years, dtype=float)
assets_case2 = np.zeros_like(years, dtype=float)
assets_case3 = np.zeros_like(years, dtype=float)
cumulative_saved = np.zeros_like(years, dtype=float)

for i in range(len(years)):
    annual_savings_1 = annual_salaries[i] * savings_rate_1
    annual_savings_2 = annual_salaries[i] * savings_rate_2
    annual_savings_3 = annual_salaries[i] * savings_rate_3
    
    if i == 0:
        assets_case1[i] = annual_savings_1
        assets_case2[i] = annual_savings_2
        assets_case3[i] = annual_savings_3
        cumulative_saved[i] = annual_savings_1
    else:
        # ケース1: 貯金のみ
        assets_case1[i] = assets_case1[i-1] * 1.00001 + annual_savings_1
        
        # ケース2: 控えめな投資
        assets_case2[i] = assets_case2[i-1] * (1 + investment_return_2) + annual_savings_2
        
        # ケース3: 積極的な投資
        assets_case3[i] = assets_case3[i-1] * (1 + investment_return_3) + annual_savings_3
        
        # 累積貯蓄額（ケース1の元本）
        cumulative_saved[i] = cumulative_saved[i-1] + annual_savings_1

# メイングラフ
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# 左上：年収推移とグレード
ax1.fill_between(ages, 0, annual_salaries, alpha=0.3, color='green')
ax1.plot(ages, annual_salaries, 'g-', linewidth=3)

# グレード変更点にマーカー
prev_grade = None
for i, (age, grade, salary) in enumerate(zip(ages, grade_history, annual_salaries)):
    if grade != prev_grade:
        ax1.plot(age, salary, 'go', markersize=8)
        ax1.text(age, salary + 30, grade, ha='center', va='bottom', fontsize=9, fontweight='bold')
        prev_grade = grade

ax1.set_xlabel('年齢', fontsize=12)
ax1.set_ylabel('年収（万円）', fontsize=12)
ax1.set_title('年収推移とグレード', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(22, 60)

# 右上：3つのケースの資産推移
ax2.plot(ages, assets_case1, 'b-', linewidth=3, label='貯金のみ（年収の20%）')
ax2.plot(ages, assets_case2, 'orange', linewidth=3, label='控えめ投資（20%、年利4%）')
ax2.plot(ages, assets_case3, 'r-', linewidth=3, label='積極投資（25%、年利6%）')
ax2.fill_between(ages, 0, assets_case1, alpha=0.2, color='blue')
ax2.fill_between(ages, 0, assets_case3, alpha=0.2, color='red')

# 重要なポイントに注釈
for check_age in [30, 40, 50, 60]:
    idx = np.where(ages == check_age)[0][0]
    if check_age == 60:
        ax2.text(check_age + 0.5, assets_case1[idx], f'{assets_case1[idx]:.0f}万円', 
                ha='left', va='center', fontsize=10, color='blue')
        ax2.text(check_age + 0.5, assets_case2[idx], f'{assets_case2[idx]:.0f}万円', 
                ha='left', va='center', fontsize=10, color='orange')
        ax2.text(check_age + 0.5, assets_case3[idx], f'{assets_case3[idx]:.0f}万円', 
                ha='left', va='center', fontsize=10, color='red')

ax2.set_xlabel('年齢', fontsize=12)
ax2.set_ylabel('総資産（万円）', fontsize=12)
ax2.set_title('投資戦略別の資産推移', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(22, 62)

# 左下：資産の差額
gap_2vs1 = assets_case2 - assets_case1
gap_3vs1 = assets_case3 - assets_case1

ax3.bar(ages[::3] - 0.4, gap_2vs1[::3], width=0.8, color='orange', alpha=0.7, label='控えめ投資の効果')
ax3.bar(ages[::3] + 0.4, gap_3vs1[::3], width=0.8, color='red', alpha=0.7, label='積極投資の効果')

ax3.set_xlabel('年齢', fontsize=12)
ax3.set_ylabel('貯金のみとの差額（万円）', fontsize=12)
ax3.set_title('投資による資産増加効果', fontsize=14, fontweight='bold')
ax3.legend(fontsize=11)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(22, 60)

# 右下：年齢別の資産構成
check_ages = [30, 40, 50, 60]
x_pos = np.arange(len(check_ages))
width = 0.25

case1_values = []
case2_values = []
case3_values = []

for age in check_ages:
    idx = np.where(ages == age)[0][0]
    case1_values.append(assets_case1[idx])
    case2_values.append(assets_case2[idx])
    case3_values.append(assets_case3[idx])

bars1 = ax4.bar(x_pos - width, case1_values, width, label='貯金のみ', color='blue', alpha=0.7)
bars2 = ax4.bar(x_pos, case2_values, width, label='控えめ投資', color='orange', alpha=0.7)
bars3 = ax4.bar(x_pos + width, case3_values, width, label='積極投資', color='red', alpha=0.7)

# 数値を表示
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)

ax4.set_xlabel('年齢', fontsize=12)
ax4.set_ylabel('総資産（万円）', fontsize=12)
ax4.set_title('年齢別の資産比較', fontsize=14, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels([f'{age}歳' for age in check_ages])
ax4.legend(fontsize=11)
ax4.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# 詳細な数値出力
print("=== 高年収企業での資産形成シミュレーション ===")
print(f"前提条件：22歳入社、11年目（32歳）でD2グレード（年収1,100万円）")
print(f"\n【60歳時点の資産】")
print(f"ケース1（貯金のみ、年収の20%）: {assets_case1[-1]:,.0f}万円")
print(f"ケース2（控えめ投資、20%を年利4%）: {assets_case2[-1]:,.0f}万円")
print(f"ケース3（積極投資、25%を年利6%）: {assets_case3[-1]:,.0f}万円")
print(f"\n投資による差額：")
print(f"控えめ投資: +{assets_case2[-1] - assets_case1[-1]:,.0f}万円（{(assets_case2[-1] / assets_case1[-1] - 1) * 100:.0f}%増）")
print(f"積極投資: +{assets_case3[-1] - assets_case1[-1]:,.0f}万円（{(assets_case3[-1] / assets_case1[-1] - 1) * 100:.0f}%増）")

# 年代別の詳細
print("\n【年代別の資産推移】")
for check_age in [30, 40, 50, 60]:
    idx = np.where(ages == check_age)[0][0]
    years_worked = check_age - 22
    grade = grade_history[idx]
    salary = annual_salaries[idx]
    print(f"\n{check_age}歳（勤続{years_worked}年、{grade}グレード、年収{salary}万円）")
    print(f"  貯金のみ: {assets_case1[idx]:,.0f}万円")
    print(f"  控えめ投資: {assets_case2[idx]:,.0f}万円")
    print(f"  積極投資: {assets_case3[idx]:,.0f}万円")