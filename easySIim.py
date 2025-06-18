import matplotlib.pyplot as plt
import numpy as np

# 日本語フォントの設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# シンプルな比較
fig, ax = plt.subplots(figsize=(12, 8))

# 時間軸（5年ごと）
years = np.array([0, 5, 10, 15, 20, 25, 30])

# 毎年36万円ずつ積み立てた場合
principal = years * 36  # 元本

# 銀行預金（金利0.001%）
bank = principal.copy()  # ほぼ元本のまま

# 投資（年利6%）の計算
investment = np.zeros_like(years, dtype=float)
for i, year in enumerate(years):
    for y in range(year):
        investment[i] += 36 * (1.06 ** (year - y))

# 積み上げ棒グラフ
bar_width = 1.5
x_pos = np.arange(len(years))

# 元本部分
bars1 = ax.bar(x_pos - bar_width/2, principal, bar_width, 
                label='銀行預金', color='lightblue', edgecolor='darkblue', linewidth=2)

# 投資の元本部分
bars2 = ax.bar(x_pos + bar_width/2, principal, bar_width, 
                label='投資元本', color='lightcoral', edgecolor='darkred', linewidth=2)

# 投資の利益部分
profit = investment - principal
bars3 = ax.bar(x_pos + bar_width/2, profit, bar_width, bottom=principal,
                label='投資利益', color='darkred', alpha=0.7, edgecolor='darkred', linewidth=2)

# 数値を表示
for i in range(len(years)):
    # 銀行預金の金額
    ax.text(x_pos[i] - bar_width/2, principal[i] + 20, f'{int(principal[i])}万円', 
            ha='center', va='bottom', fontsize=9)
    
    # 投資総額
    ax.text(x_pos[i] + bar_width/2, investment[i] + 20, f'{int(investment[i])}万円', 
            ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 差額を表示（10年後以降）
    if years[i] >= 10:
        diff = investment[i] - principal[i]
        ax.text(x_pos[i] + bar_width/2, investment[i] + 100, 
                f'+{int(diff)}万円\n({int(diff/principal[i]*100)}%増)', 
                ha='center', va='bottom', fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

# グラフの装飾
ax.set_xlabel('経過年数', fontsize=14)
ax.set_ylabel('資産総額（万円）', fontsize=14)
ax.set_title('r > g の法則：同じ金額を貯金 vs 投資（年36万円ずつ）', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels([f'{y}年' for y in years])
ax.legend(fontsize=12, loc='upper left')
ax.grid(True, axis='y', alpha=0.3)
ax.set_ylim(0, max(investment) * 1.2)

# 説明文
ax.text(0.02, 0.95, '※銀行金利0.001%、投資利回り6%で計算', 
        transform=ax.transAxes, fontsize=10, 
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow'))

plt.tight_layout()
plt.show()

# 結果のサマリー
print("=== r > g が生み出す差 ===")
print(f"30年間、毎年36万円（月3万円）を積み立てた場合：")
print(f"\n銀行預金: {int(principal[-1])}万円（ほぼ元本のみ）")
print(f"投資運用: {int(investment[-1])}万円")
print(f"差額: {int(investment[-1] - principal[-1])}万円")
print(f"\n投資の方が{int((investment[-1] / principal[-1] - 1) * 100)}%も多い！")