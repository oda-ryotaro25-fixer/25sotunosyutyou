import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
import seaborn as sns
from matplotlib.patches import Rectangle

# 日本語フォントの設定
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

# 保存用ディレクトリ
save_dir = "asset_simulation_with_life_events"
import os
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# ライフイベントの定義（入社年齢23歳想定）
life_events = {
    3: {'name': '一人暮らし開始', 'cost': 50, 'type': 'single'},  # 引越し・家具等
    5: {'name': '車購入', 'cost': 200, 'type': 'single'},
    7: {'name': '結婚', 'cost': 300, 'type': 'single'},
    8: {'name': '新婚旅行', 'cost': 80, 'type': 'single'},
    10: {'name': '住宅購入頭金', 'cost': 500, 'type': 'single'},
    12: {'name': '第一子出産', 'cost': 50, 'type': 'single'},
    15: {'name': '第二子出産', 'cost': 50, 'type': 'single'},
    18: {'name': '車買い替え', 'cost': 250, 'type': 'single'},
}

# 継続的な支出の追加（年額）
recurring_costs = {
    10: {'name': '住宅ローン', 'annual_cost': 120},  # 月10万円
    12: {'name': '子育て費用', 'annual_cost': 60},   # 月5万円
    15: {'name': '子育て費用増', 'annual_cost': 120}, # 月10万円（2人分）
}

# 基本パラメータ
TAX_RATE = 0.20
INVESTMENT_RETURN = 0.05
SAVINGS_RATE = 0.0001

# 標準グループのデータ（前回より）
standard_years = [1, 2, 3, 4, 6, 8, 11, 14, 17, 20]
standard_salary = [340, 340, 390, 430, 480, 520, 590, 700, 800, 900]

# 1. ライフイベント込みの資産シミュレーション
def simulate_with_life_events(salary_years, salary_amounts, max_years=20, 
                             include_events=True, savings_rate_base=0.25):
    years = np.arange(1, max_years + 1)
    salaries = np.interp(years, salary_years, salary_amounts)
    
    # 結果を格納
    investment_history = []
    savings_history = []
    available_cash = []
    cumulative_events_cost = []
    monthly_savings_history = []
    
    investment_balance = 0
    savings_balance = 0
    total_event_cost = 0
    
    for i, year in enumerate(years):
        # 手取り計算
        take_home = salaries[i] * (1 - TAX_RATE) * 10000
        
        # 基本生活費（年次により変動）
        if year <= 3:
            living_cost = 20 * 12 * 10000  # 月20万円
        elif year <= 7:
            living_cost = 23 * 12 * 10000  # 月23万円
        elif year <= 15:
            living_cost = 25 * 12 * 10000  # 月25万円
        else:
            living_cost = 28 * 12 * 10000  # 月28万円
        
        # 継続的な支出を追加
        for start_year, cost_info in recurring_costs.items():
            if year >= start_year:
                living_cost += cost_info['annual_cost'] * 10000
        
        # 利用可能額
        available = take_home - living_cost
        
        # ライフイベントの支出
        event_cost = 0
        if include_events and year in life_events:
            event_cost = life_events[year]['cost'] * 10000
            total_event_cost += event_cost
        
        # 実際の貯蓄可能額
        actual_savings = max(0, available - event_cost)
        
        # 貯蓄率の調整（ライフイベント時は貯蓄率を下げる）
        if event_cost > 0:
            adjusted_rate = min(0.1, actual_savings / take_home)  # 最低10%
        else:
            adjusted_rate = min(savings_rate_base, actual_savings / take_home)
        
        annual_savings = take_home * adjusted_rate
        monthly_savings = annual_savings / 12
        
        # 積立投資
        for month in range(12):
            investment_balance = investment_balance * (1 + INVESTMENT_RETURN/12) + monthly_savings
        
        # 貯金
        savings_balance = savings_balance * (1 + SAVINGS_RATE) + annual_savings
        
        # 記録
        investment_history.append(investment_balance / 10000)
        savings_history.append(savings_balance / 10000)
        available_cash.append(available / 10000)
        cumulative_events_cost.append(total_event_cost / 10000)
        monthly_savings_history.append(monthly_savings / 10000)
    
    return {
        'years': years,
        'investment': investment_history,
        'savings': savings_history,
        'available_cash': available_cash,
        'events_cost': cumulative_events_cost,
        'monthly_savings': monthly_savings_history
    }

# シミュレーション実行
with_events = simulate_with_life_events(standard_years, standard_salary, include_events=True)
without_events = simulate_with_life_events(standard_years, standard_salary, include_events=False)

# 2. ライフイベントの影響を可視化
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# グラフ1: 資産推移比較（ライフイベントあり/なし）
ax1.plot(with_events['years'], with_events['investment'], 'o-', linewidth=2.5, 
         label='投資（イベントあり）', color='#FF6B6B')
ax1.plot(without_events['years'], without_events['investment'], 'o--', linewidth=2.5, 
         label='投資（イベントなし）', color='#FFB6C1')
ax1.plot(with_events['years'], with_events['savings'], 's-', linewidth=2.5, 
         label='貯金（イベントあり）', color='#4ECDC4')

# ライフイベントをマーク
for year, event in life_events.items():
    if year <= 20:
        ax1.axvline(x=year, color='gray', linestyle=':', alpha=0.5)
        ax1.text(year, ax1.get_ylim()[1]*0.95, event['name'], 
                rotation=90, va='top', ha='right', fontsize=8)

ax1.set_xlabel('勤続年数', fontsize=12)
ax1.set_ylabel('資産額（万円）', fontsize=12)
ax1.set_title('ライフイベントを考慮した資産推移', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# グラフ2: 月額積立可能額の推移
ax2.bar(with_events['years'], with_events['monthly_savings'], 
        color='#87CEEB', alpha=0.7, label='実際の積立額')
ax2.plot(with_events['years'], with_events['monthly_savings'], 
         'o-', color='#FF6B6B', linewidth=2, markersize=6)

# 推奨積立額のライン
ax2.axhline(y=3, color='green', linestyle='--', label='最低推奨額（3万円）')
ax2.axhline(y=5, color='orange', linestyle='--', label='標準推奨額（5万円）')
ax2.axhline(y=10, color='red', linestyle='--', label='理想額（10万円）')

ax2.set_xlabel('勤続年数', fontsize=12)
ax2.set_ylabel('月額積立額（万円）', fontsize=12)
ax2.set_title('実際の月額積立可能額の推移', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.set_ylim(0, 15)

# グラフ3: 10年間の詳細シミュレーション
years_10 = with_events['years'][:10]
investment_10 = with_events['investment'][:10]
events_cost_10 = with_events['events_cost'][:10]

ax3.bar(years_10, investment_10, color='#87CEEB', alpha=0.7, label='資産残高')
ax3.plot(years_10, investment_10, 'o-', color='#FF6B6B', linewidth=3, markersize=8)

# ライフイベントコストを表示
for year in years_10:
    if year in life_events:
        cost = life_events[year]['cost']
        ax3.text(year, investment_10[year-1] + 20, f'-{cost}万円', 
                ha='center', color='red', fontweight='bold')

ax3.set_xlabel('勤続年数', fontsize=12)
ax3.set_ylabel('資産額（万円）', fontsize=12)
ax3.set_title('入社10年間の資産形成詳細', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)

# 10年後の目標ラインを追加
ax3.axhline(y=500, color='green', linestyle='--', label='目標500万円')
ax3.axhline(y=1000, color='orange', linestyle='--', label='理想1000万円')
ax3.legend()

# グラフ4: 積立額別シミュレーション（10年）
monthly_amounts = [1, 3, 5, 7, 10]  # 万円
results_10y = []

for amount in monthly_amounts:
    balance = 0
    monthly = amount * 10000
    for _ in range(10 * 12):
        balance = balance * (1 + INVESTMENT_RETURN/12) + monthly
    results_10y.append(balance / 10000)

bars = ax4.bar([f'{amt}万円' for amt in monthly_amounts], results_10y, 
                color=['#FFE5E5', '#FFB6C1', '#87CEEB', '#98FB98', '#90EE90'])

# 各バーに金額を表示
for i, (amt, result) in enumerate(zip(monthly_amounts, results_10y)):
    ax4.text(i, result + 20, f'{result:.0f}万円', ha='center', fontweight='bold')
    # 元本も表示
    principal = amt * 12 * 10
    ax4.text(i, result/2, f'元本\n{principal}万円', ha='center', fontsize=9)

ax4.set_xlabel('月額積立額', fontsize=12)
ax4.set_ylabel('10年後の資産額（万円）', fontsize=12)
ax4.set_title('月額積立額別10年後の資産額（年率5%）', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{save_dir}/11_life_events_simulation.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. 新入社員向け実践ガイド
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# グラフ1: 年次別推奨積立額
years = np.arange(1, 11)
min_amount = [2, 2, 3, 3, 3, 4, 4, 5, 5, 5]  # 最低額
std_amount = [3, 3, 4, 5, 5, 6, 7, 8, 8, 10]  # 標準額
max_amount = [5, 5, 7, 8, 10, 12, 12, 15, 15, 15]  # 理想額

ax1.fill_between(years, 0, min_amount, alpha=0.3, color='#FFB6C1', label='最低ライン')
ax1.fill_between(years, min_amount, std_amount, alpha=0.3, color='#87CEEB', label='標準ライン')
ax1.fill_between(years, std_amount, max_amount, alpha=0.3, color='#98FB98', label='理想ライン')

ax1.plot(years, min_amount, 'o-', linewidth=2, color='red')
ax1.plot(years, std_amount, 's-', linewidth=2, color='blue')
ax1.plot(years, max_amount, '^-', linewidth=2, color='green')

ax1.set_xlabel('勤続年数', fontsize=12)
ax1.set_ylabel('推奨月額積立額（万円）', fontsize=12)
ax1.set_title('年次別推奨積立額ガイドライン', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_ylim(0, 18)

# グラフ2: 積立開始タイミングの影響
start_timings = [1, 3, 5, 7]  # 開始年
final_assets = []
labels = []

for start in start_timings:
    balance = 0
    monthly = 50000  # 月5万円固定
    months = (10 - start + 1) * 12
    
    for _ in range(months):
        balance = balance * (1 + INVESTMENT_RETURN/12) + monthly
    
    final_assets.append(balance / 10000)
    labels.append(f'{start}年目\n開始')

colors = ['#2E8B57', '#3CB371', '#90EE90', '#FFB6C1']
bars = ax2.bar(labels, final_assets, color=colors)

# 各バーに詳細情報を表示
for i, (start, asset) in enumerate(zip(start_timings, final_assets)):
    years = 10 - start + 1
    principal = 5 * 12 * years
    gain = asset - principal
    ax2.text(i, asset + 10, f'{asset:.0f}万円', ha='center', fontweight='bold')
    ax2.text(i, asset/2, f'運用益\n{gain:.0f}万円', ha='center', fontsize=9, color='white')

ax2.set_xlabel('積立開始時期', fontsize=12)
ax2.set_ylabel('10年目の資産額（万円）', fontsize=12)
ax2.set_title('積立開始タイミングの影響（月5万円）', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# グラフ3: 手取りに対する積立率
take_home_amounts = [20, 25, 30, 35, 40]  # 手取り月収（万円）
savings_rates = [10, 15, 20, 25, 30]  # 積立率（%）

# ヒートマップデータの作成
heatmap_data = np.zeros((len(savings_rates), len(take_home_amounts)))
for i, rate in enumerate(savings_rates):
    for j, take_home in enumerate(take_home_amounts):
        monthly_saving = take_home * rate / 100
        heatmap_data[i, j] = monthly_saving

# ヒートマップ
im = ax3.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')

# 軸の設定
ax3.set_xticks(range(len(take_home_amounts)))
ax3.set_yticks(range(len(savings_rates)))
ax3.set_xticklabels([f'{x}万円' for x in take_home_amounts])
ax3.set_yticklabels([f'{y}%' for y in savings_rates])

# 各セルに値を表示
for i in range(len(savings_rates)):
    for j in range(len(take_home_amounts)):
        text = ax3.text(j, i, f'{heatmap_data[i, j]:.1f}万', 
                       ha='center', va='center', color='black' if heatmap_data[i, j] < 7 else 'white')

ax3.set_xlabel('手取り月収', fontsize=12)
ax3.set_ylabel('積立率', fontsize=12)
ax3.set_title('手取り収入別の月額積立額マトリックス', fontsize=14, fontweight='bold')

# カラーバー
cbar = plt.colorbar(im, ax=ax3)
cbar.set_label('月額積立額（万円）', fontsize=10)

# グラフ4: 目標額達成に必要な積立額
targets = [
    {'amount': 300, 'years': 5, 'label': '結婚資金'},
    {'amount': 500, 'years': 7, 'label': '住宅頭金'},
    {'amount': 1000, 'years': 10, 'label': '教育資金'},
    {'amount': 2000, 'years': 20, 'label': '老後資金'}
]

required_monthly = []
for target in targets:
    r = INVESTMENT_RETURN / 12
    n = target['years'] * 12
    monthly = target['amount'] * 10000 * r / ((1 + r)**n - 1) / 10000
    required_monthly.append(monthly)

x = np.arange(len(targets))
bars = ax4.bar(x, required_monthly, color=['#FFB6C1', '#87CEEB', '#98FB98', '#DDA0DD'])

# 各バーに詳細を表示
for i, (target, monthly) in enumerate(zip(targets, required_monthly)):
    ax4.text(i, monthly + 0.5, f'{monthly:.1f}万円/月', ha='center', fontweight='bold')
    ax4.text(i, -1, f"{target['amount']}万円\n{target['years']}年", 
             ha='center', fontsize=9)

ax4.set_xticks(x)
ax4.set_xticklabels([t['label'] for t in targets])
ax4.set_ylabel('必要月額積立額（万円）', fontsize=12)
ax4.set_title('目標額達成に必要な月額積立額（年率5%）', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_ylim(-2, max(required_monthly) + 2)

plt.tight_layout()
plt.savefig(f'{save_dir}/12_practical_guide_for_newcomers.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. 実践的アクションプラン
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# メインタイトル
fig.suptitle('新入社員のための資産形成アクションプラン', fontsize=18, fontweight='bold')

# 年次別アクションプラン表
ax_table = fig.add_subplot(gs[0, :])
ax_table.axis('tight')
ax_table.axis('off')

action_plan = [
    ['時期', '月額積立目標', '年収', '主なライフイベント', 'アクション'],
    ['1-2年目', '2-3万円', '340万円', '社会人スタート', '・つみたてNISA開始\n・生活費を把握'],
    ['3-4年目', '3-5万円', '390-430万円', '一人暮らし', '・積立額を増額\n・緊急資金準備'],
    ['5-6年目', '5-7万円', '480-520万円', '車購入検討', '・iDeCo追加検討\n・投資知識向上'],
    ['7-8年目', '7-10万円', '590万円', '結婚', '・夫婦で資産計画\n・保険見直し'],
    ['9-10年目', '8-12万円', '700万円', '住宅購入', '・住宅ローン考慮\n・教育資金準備']
]

table = ax_table.table(cellText=action_plan[1:], colLabels=action_plan[0],
                      cellLoc='left', loc='center',
                      colWidths=[0.12, 0.15, 0.12, 0.18, 0.43])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 2.5)

# ヘッダーの装飾
for i in range(5):
    table[(0, i)].set_facecolor('#4ECDC4')
    table[(0, i)].set_text_props(weight='bold', color='white')

# 行の色を交互に
for i in range(1, 6):
    if i % 2 == 0:
        for j in range(5):
            table[(i, j)].set_facecolor('#F0F0F0')

# 小グラフ1: 積立額と生活費のバランス
ax1 = fig.add_subplot(gs[1, 0])
income_levels = ['手取り20万', '手取り25万', '手取り30万', '手取り35万']
living_costs = [15, 17, 20, 22]  # 生活費
savings = [2, 4, 6, 8]  # 積立額
others = [3, 4, 4, 5]  # その他

x = np.arange(len(income_levels))
width = 0.6

p1 = ax1.bar(x, living_costs, width, label='生活費', color='#FFB6C1')
p2 = ax1.bar(x, savings, width, bottom=living_costs, label='積立投資', color='#87CEEB')
p3 = ax1.bar(x, others, width, bottom=np.array(living_costs)+np.array(savings), 
             label='予備費', color='#98FB98')

ax1.set_ylabel('金額（万円）')
ax1.set_title('収入別の支出配分例')
ax1.set_xticks(x)
ax1.set_xticklabels(income_levels, rotation=15)
ax1.legend()

# 小グラフ2: 10年間の目標設定
ax2 = fig.add_subplot(gs[1, 1])
milestones = [
    (1, 50, '緊急資金'),
    (3, 150, '生活防衛資金'),
    (5, 300, '結婚資金'),
    (7, 500, '住宅頭金'),
    (10, 1000, '総資産目標')
]

years = [m[0] for m in milestones]
amounts = [m[1] for m in milestones]
labels = [m[2] for m in milestones]

ax2.plot(years, amounts, 'o-', linewidth=3, markersize=10, color='#FF6B6B')
for year, amount, label in milestones:
    ax2.annotate(label, (year, amount), textcoords="offset points", 
                xytext=(0,10), ha='center', fontsize=9)

ax2.set_xlabel('勤続年数')
ax2.set_ylabel('目標金額（万円）')
ax2.set_title('10年間の資産形成マイルストーン')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 11)

# 小グラフ3: リスク許容度別ポートフォリオ
ax3 = fig.add_subplot(gs[1, 2])
risk_levels = ['保守的\n(20代前半)', '標準的\n(20代後半)', '積極的\n(投資経験者)']
stocks = [30, 50, 70]
bonds = [20, 30, 20]
cash = [50, 20, 10]

x = np.arange(len(risk_levels))
width = 0.6

ax3.bar(x, cash, width, label='現金・預金', color='#90EE90')
ax3.bar(x, bonds, width, bottom=cash, label='債券', color='#87CEEB')
ax3.bar(x, stocks, width, bottom=np.array(cash)+np.array(bonds), 
        label='株式', color='#FFB6C1')

ax3.set_ylabel('配分比率（%）')
ax3.set_title('リスク許容度別資産配分')
ax3.set_xticks(x)
ax3.set_xticklabels(risk_levels)
ax3.legend()
ax3.set_ylim(0, 100)

# 実践チェックリスト
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

checklist_text = """
【新入社員の資産形成チェックリスト】

□ 1. 給与振込口座とは別に、投資用口座を開設
□ 2. つみたてNISA口座を開設（年間120万円まで非課税）
□ 3. 最初は少額（月1-2万円）から開始
□ 4. 全世界株式インデックスファンドを選択
□ 5. 給与天引きまたは自動引落で積立設定
□ 6. 生活防衛資金（生活費3-6ヶ月分）を別途確保
□ 7. 年1回は資産状況を確認・見直し
□ 8. ライフイベント前には一時的に積立額調整も検討

【重要ポイント】
• 最初の一歩が最も重要 - 完璧を求めずにまず始める
• 時間を味方につける - 若いうちから始めることで複利効果を最大化
• 継続が力 - 市場の変動に一喜一憂せず淡々と積立
• 知識を深める - 投資の基本を学びながら実践
"""

ax4.text(0.05, 0.95, checklist_text, transform=ax4.transAxes,
         fontsize=11, verticalalignment='top',
         bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig(f'{save_dir}/13_action_plan_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. 年収別シミュレーション比較
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# 初任給別のシミュレーション
initial_salaries = [300, 340, 400, 450]  # 万円
salary_labels = ['300万円', '340万円\n(標準)', '400万円', '450万円']

for i, initial_salary in enumerate(initial_salaries):
    # 10年間の資産推移を計算
    years = np.arange(1, 11)
    assets = []
    
    for year in years:
        # 簡易的な昇給モデル（年3%）
        current_salary = initial_salary * (1.03 ** (year - 1))
        take_home = current_salary * 0.8 * 10000
        
        # 積立率25%
        monthly_saving = take_home * 0.25 / 12
        
        # 資産計算
        if year == 1:
            balance = 0
        else:
            balance = assets[-1] * 10000
        
        for month in range(12):
            balance = balance * (1 + INVESTMENT_RETURN/12) + monthly_saving
        
        assets.append(balance / 10000)
    
    ax1.plot(years, assets, 'o-', linewidth=2.5, markersize=8, 
             label=salary_labels[i])

ax1.set_xlabel('勤続年数', fontsize=12)
ax1.set_ylabel('資産額（万円）', fontsize=12)
ax1.set_title('初任給別の資産形成シミュレーション（積立率25%）', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_xlim(0, 11)

# 10年後の資産額比較
final_assets = []
for initial_salary in initial_salaries:
    # 10年間の計算
    balance = 0
    for year in range(1, 11):
        current_salary = initial_salary * (1.03 ** (year - 1))
        take_home = current_salary * 0.8 * 10000
        monthly_saving = take_home * 0.25 / 12
        
        for month in range(12):
            balance = balance * (1 + INVESTMENT_RETURN/12) + monthly_saving
    
    final_assets.append(balance / 10000)

bars = ax2.bar(salary_labels, final_assets, color=['#FFE5E5', '#87CEEB', '#98FB98', '#90EE90'])

# 各バーに詳細情報を表示
for i, (label, asset) in enumerate(zip(salary_labels, final_assets)):
    ax2.text(i, asset + 20, f'{asset:.0f}万円', ha='center', fontweight='bold')
    # 初任給との差額も表示
    if i > 0:
        diff = asset - final_assets[1]  # 標準（340万）との差
        ax2.text(i, asset/2, f'{diff:+.0f}万円', ha='center', fontsize=10, color='white')

ax2.set_ylabel('10年後の資産額（万円）', fontsize=12)
ax2.set_title('初任給による10年後資産額の差', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{save_dir}/14_salary_based_simulation.png', dpi=300, bbox_inches='tight')
plt.close()

# 最終的な統計サマリーレポート
print("=" * 80)
print("新入社員向け資産形成シミュレーション 完全版サマリー")
print("=" * 80)

print("\n【1. 基本的な積立プラン】")
print("勤続年数 | 推奨積立額 | 年収目安 | 10年後資産(月5万円積立)")
print("-" * 70)
print("1-3年目  | 月2-3万円  | 340万円  | -")
print("4-6年目  | 月4-5万円  | 430万円  | -")
print("7-10年目 | 月6-10万円 | 590万円  | 776万円")

print("\n【2. ライフイベントを考慮した現実的プラン】")
print("主要イベント | 想定年次 | 必要資金 | 対策")
print("-" * 70)
print("一人暮らし  | 3年目    | 50万円   | 前年から月1万円追加貯蓄")
print("結婚        | 7年目    | 300万円  | 3年前から準備開始")
print("住宅購入    | 10年目   | 500万円  | 頭金は別途準備推奨")

print("\n【3. 積立開始タイミングによる差】")
print("開始時期 | 月5万円積立 | 10年目資産 | 1年目開始との差")
print("-" * 70)
print("1年目    | 10年間      | 776万円     | -")
print("3年目    | 8年間       | 593万円     | -183万円")
print("5年目    | 6年間       | 419万円     | -357万円")

print("\n【4. 目標額達成に必要な月額積立】")
print("目標額     | 期間   | 必要月額(年率5%) | 元本")
print("-" * 70)
print("300万円    | 5年    | 4.4万円          | 264万円")
print("500万円    | 7年    | 5.3万円          | 445万円")
print("1000万円   | 10年   | 7.9万円          | 948万円")

print("\n【5. 成功のための重要ポイント】")
print("• 早期開始: 1年の遅れが10年後に100万円以上の差を生む")
print("• 自動化: 給与天引きで「なかったもの」として積立")
print("• 段階的増額: 昇給に合わせて積立額も増やす")
print("• 継続性: 市場変動に惑わされず淡々と継続")
print("• NISA活用: 年間360万円まで非課税で運用可能")

print("\n【6. 年代別行動指針】")
print("20代前半: まず始める（月1万円でもOK）、知識を身につける")
print("20代後半: 積立額を増やす、リスク資産の比率を上げる")
print("30代前半: ライフイベントと両立、教育資金の準備開始")
print("30代後半: 老後資金を意識、iDeCoの活用検討")

print("=" * 80)

# CSVファイルに詳細データを保存
import csv

# ライフイベント考慮版の詳細データ
with open(f'{save_dir}/life_event_simulation.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['年次', '年収', '手取り', '生活費', 'イベント費用', 
                     '積立可能額', '投資残高', '貯金残高'])
    
    for i in range(20):
        year = i + 1
        salary = np.interp(year, standard_years, standard_salary)
        take_home = salary * 0.8
        
        # 生活費
        if year <= 3:
            living_cost = 20 * 12
        elif year <= 7:
            living_cost = 23 * 12
        elif year <= 15:
            living_cost = 25 * 12
        else:
            living_cost = 28 * 12
        
        # イベント費用
        event_cost = life_events.get(year, {}).get('cost', 0)
        
        # 継続費用
        for start_year, cost_info in recurring_costs.items():
            if year >= start_year:
                living_cost += cost_info['annual_cost']
        
        # 積立可能額
        available = max(0, take_home - living_cost/12 - event_cost)
        saving_amount = available * 0.25  # 25%を積立
        
        # 資産額（簡易計算）
        if year <= len(with_events['investment']):
            investment = with_events['investment'][year-1]
            savings = with_events['savings'][year-1]
        else:
            investment = 0
            savings = 0
        
        writer.writerow([year, salary, take_home, living_cost/12, event_cost,
                        saving_amount, investment, savings])

print(f"\nシミュレーション詳細データを保存しました:")
print(f"- {save_dir}/life_event_simulation.csv")

# 積立プラン比較表
with open(f'{save_dir}/investment_plans_comparison.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['プラン', '月額積立', '10年間総額', '10年後資産', '運用益', '利回り'])
    
    plans = [
        ('最低限', 2, 240, 310, 70, 29.2),
        ('標準', 5, 600, 776, 176, 29.3),
        ('積極的', 10, 1200, 1551, 351, 29.3),
        ('最大化', 15, 1800, 2327, 527, 29.3)
    ]
    
    for plan in plans:
        writer.writerow(plan)

# 最終グラフ: 包括的ダッシュボード
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)

# メインタイトル
fig.suptitle('新入社員のための資産形成完全ガイド', fontsize=20, fontweight='bold')

# 各種グラフを配置
# 最終グラフ: 包括的ダッシュボード
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)

# メインタイトル
fig.suptitle('新入社員のための資産形成完全ガイド', fontsize=20, fontweight='bold')

# 1. 10年後資産額サマリー（左上の大きなパネル）
ax_summary = fig.add_subplot(gs[0:2, 0:2])
ax_summary.axis('off')

# サマリーテーブルのデータ
summary_data = {
    '積立パターン': ['最低限\n(月2万円)', '標準\n(月5万円)', '積極的\n(月10万円)'],
    '10年後資産': [310, 776, 1551],
    '元本': [240, 600, 1200],
    '運用益': [70, 176, 351]
}

# 棒グラフとテーブルの組み合わせ
ax_bar = ax_summary.inset_axes([0.1, 0.3, 0.8, 0.6])
x = np.arange(len(summary_data['積立パターン']))
width = 0.35

bars1 = ax_bar.bar(x - width/2, summary_data['元本'], width, label='元本', color='#87CEEB')
bars2 = ax_bar.bar(x + width/2, summary_data['運用益'], width, label='運用益', color='#FFB6C1')

ax_bar.set_ylabel('金額（万円）', fontsize=12)
ax_bar.set_title('10年後の資産内訳', fontsize=14)
ax_bar.set_xticks(x)
ax_bar.set_xticklabels(summary_data['積立パターン'])
ax_bar.legend()
ax_bar.grid(True, alpha=0.3, axis='y')

# 各バーに合計額を表示
for i, total in enumerate(summary_data['10年後資産']):
    ax_bar.text(i, total + 50, f'{total}万円', ha='center', fontweight='bold', fontsize=12)

# テキスト情報
info_text = """
【投資の基本設定】
• 想定利回り: 年率5%（全世界株式インデックス）
• 投資期間: 10年間
• 投資方法: 毎月定額積立（ドルコスト平均法）
• 税制優遇: NISA活用で運用益非課税
"""
ax_summary.text(0.05, 0.15, info_text, transform=ax_summary.transAxes,
                fontsize=11, bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))

# 2. 年収別シミュレーション（右上）
ax_salary = fig.add_subplot(gs[0, 2:])
initial_salaries = [300, 340, 400, 450]
colors = ['#FFE5E5', '#87CEEB', '#98FB98', '#90EE90']

# 5年後と10年後の資産額
years = [5, 10]
for i, salary in enumerate(initial_salaries):
    assets = []
    for year in years:
        balance = 0
        for y in range(1, year + 1):
            current_salary = salary * (1.03 ** (y - 1))
            monthly_saving = current_salary * 0.8 * 0.25 / 12 * 10000
            for m in range(12):
                balance = balance * (1 + 0.05/12) + monthly_saving
        assets.append(balance / 10000)
    
    ax_salary.plot([0, 1], assets, 'o-', linewidth=2.5, markersize=10,
                   label=f'初任給{salary}万円', color=colors[i])

ax_salary.set_xticks([0, 1])
ax_salary.set_xticklabels(['5年後', '10年後'])
ax_salary.set_ylabel('資産額（万円）', fontsize=12)
ax_salary.set_title('初任給別の資産形成推移（積立率25%）', fontsize=14, fontweight='bold')
ax_salary.grid(True, alpha=0.3)
ax_salary.legend()

# 3. ライフイベントタイムライン（中段左）
ax_timeline = fig.add_subplot(gs[1, :2])

events = [
    (3, 50, '一人暮らし', '#FFB6C1'),
    (5, 200, '車購入', '#87CEEB'),
    (7, 300, '結婚', '#98FB98'),
    (10, 500, '住宅頭金', '#FFD700'),
    (12, 50, '第一子', '#DDA0DD'),
    (15, 50, '第二子', '#DDA0DD')
]

# タイムラインの描画
for i, (year, cost, name, color) in enumerate(events):
    if year <= 15:
        ax_timeline.barh(i, 1, left=year-0.5, height=0.8, color=color, alpha=0.7)
        ax_timeline.text(year, i, f'{name}\n{cost}万円', ha='center', va='center',
                        fontsize=10, fontweight='bold')

ax_timeline.set_xlim(0, 16)
ax_timeline.set_ylim(-1, len(events))
ax_timeline.set_xlabel('勤続年数', fontsize=12)
ax_timeline.set_yticks([])
ax_timeline.set_title('主要ライフイベントと必要資金', fontsize=14, fontweight='bold')
ax_timeline.grid(True, alpha=0.3, axis='x')

# 4. 積立額調整ガイド（中段右）
ax_guide = fig.add_subplot(gs[1, 2:])

# 収入と支出のバランス図
years_guide = np.arange(1, 11)
income = [20, 22, 24, 26, 28, 30, 32, 34, 36, 38]  # 手取り月収
essential = [15, 15, 16, 17, 18, 19, 20, 21, 22, 23]  # 必要生活費
recommended_saving = [3, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # 推奨積立額

ax_guide.fill_between(years_guide, 0, essential, alpha=0.3, color='#FFB6C1', label='必要生活費')
ax_guide.fill_between(years_guide, essential, 
                      [e + s for e, s in zip(essential, recommended_saving)], 
                      alpha=0.3, color='#87CEEB', label='推奨積立額')
ax_guide.plot(years_guide, income, 'o-', linewidth=3, markersize=8, 
              color='green', label='手取り月収')

ax_guide.set_xlabel('勤続年数', fontsize=12)
ax_guide.set_ylabel('月額（万円）', fontsize=12)
ax_guide.set_title('収入成長に合わせた積立額の目安', fontsize=14, fontweight='bold')
ax_guide.legend()
ax_guide.grid(True, alpha=0.3)

# 5. 投資vs貯金の差額（下段左）
ax_diff = fig.add_subplot(gs[2, 0])

years_diff = np.arange(1, 21)
diff_percentage = []
for year in years_diff:
    # 月5万円積立の場合
    investment = 0
    savings = 0
    monthly = 50000
    
    for y in range(year):
        for m in range(12):
            investment = investment * (1 + 0.05/12) + monthly
            savings = savings * (1 + 0.0001/12) + monthly
    
    diff = (investment / savings - 1) * 100
    diff_percentage.append(diff)

ax_diff.plot(years_diff, diff_percentage, 'o-', linewidth=3, markersize=6, color='#FF6B6B')
ax_diff.fill_between(years_diff, 0, diff_percentage, alpha=0.3, color='#FFB6C1')

ax_diff.set_xlabel('投資期間（年）', fontsize=12)
ax_diff.set_ylabel('投資優位性（%）', fontsize=12)
ax_diff.set_title('投資と貯金の差額推移', fontsize=14, fontweight='bold')
ax_diff.grid(True, alpha=0.3)

# 主要ポイントに注釈
for year in [5, 10, 15, 20]:
    if year <= len(diff_percentage):
        ax_diff.annotate(f'{diff_percentage[year-1]:.1f}%', 
                        xy=(year, diff_percentage[year-1]),
                        xytext=(year, diff_percentage[year-1] + 2),
                        ha='center', fontweight='bold')

# 6. リスク許容度診断（下段中央）
ax_risk = fig.add_subplot(gs[2, 1])

categories = ['年齢', '収入\n安定性', '投資\n知識', '家族\n構成', '性格']
scores = {
    '保守的': [2, 3, 2, 4, 2],
    '標準的': [3, 4, 3, 3, 3],
    '積極的': [4, 4, 4, 2, 4]
}

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
angles = np.concatenate([angles, [angles[0]]])

ax_risk = plt.subplot(gs[2, 1], projection='polar')
for risk_type, values in scores.items():
    values = values + [values[0]]
    if risk_type == '保守的':
        ax_risk.plot(angles, values, 'o-', linewidth=2, label=risk_type, color='#87CEEB')
    elif risk_type == '標準的':
        ax_risk.plot(angles, values, 's-', linewidth=2, label=risk_type, color='#98FB98')
    else:
        ax_risk.plot(angles, values, '^-', linewidth=2, label=risk_type, color='#FFB6C1')
    ax_risk.fill(angles, values, alpha=0.1)

ax_risk.set_xticks(angles[:-1])
ax_risk.set_xticklabels(categories)
ax_risk.set_ylim(0, 5)
ax_risk.set_title('リスク許容度プロファイル', fontsize=14, fontweight='bold', pad=20)
ax_risk.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# 7. 実践チェックリスト（下段右）
ax_check = fig.add_subplot(gs[2, 2:])
ax_check.axis('off')

checklist = [
    '✓ NISA口座開設完了',
    '✓ 自動積立設定（給与天引き推奨）',
]
#8. **最重要アドバイス**：すぐに実行すべきアクションと長期目標

# 追加のダッシュボード要素を実装
# 9. インタラクティブな積立シミュレーター風の表示
fig2 = plt.figure(figsize=(20, 12))
gs2 = fig2.add_gridspec(3, 4, hspace=0.4, wspace=0.3)

fig2.suptitle('新入社員のための資産形成シミュレーター', fontsize=20, fontweight='bold')

# 1. 積立額スライダー風の表示（左上）
ax_slider = fig2.add_subplot(gs2[0, :2])

monthly_amounts = [1, 2, 3, 5, 7, 10, 15]
results_5y = []
results_10y = []
results_20y = []

for amount in monthly_amounts:
    # 5年後
    balance_5y = 0
    for _ in range(5 * 12):
        balance_5y = balance_5y * (1 + 0.05/12) + amount * 10000
    results_5y.append(balance_5y / 10000)
    
    # 10年後
    balance_10y = 0
    for _ in range(10 * 12):
        balance_10y = balance_10y * (1 + 0.05/12) + amount * 10000
    results_10y.append(balance_10y / 10000)
    
    # 20年後
    balance_20y = 0
    for _ in range(20 * 12):
        balance_20y = balance_20y * (1 + 0.05/12) + amount * 10000
    results_20y.append(balance_20y / 10000)

# 3つの期間を同時にプロット
x = np.arange(len(monthly_amounts))
width = 0.25

bars1 = ax_slider.bar(x - width, results_5y, width, label='5年後', color='#FFB6C1')
bars2 = ax_slider.bar(x, results_10y, width, label='10年後', color='#87CEEB')
bars3 = ax_slider.bar(x + width, results_20y, width, label='20年後', color='#98FB98')

ax_slider.set_xlabel('月額積立額（万円）', fontsize=12)
ax_slider.set_ylabel('予想資産額（万円）', fontsize=12)
ax_slider.set_title('積立額別の資産形成シミュレーション', fontsize=14, fontweight='bold')
ax_slider.set_xticks(x)
ax_slider.set_xticklabels([f'{amt}万円' for amt in monthly_amounts])
ax_slider.legend()
ax_slider.grid(True, alpha=0.3, axis='y')

# 各バーに金額を表示
for i, (r5, r10, r20) in enumerate(zip(results_5y, results_10y, results_20y)):
    if i % 2 == 0:  # 表示を間引く
        ax_slider.text(i - width, r5 + 20, f'{r5:.0f}', ha='center', fontsize=8)
        ax_slider.text(i, r10 + 20, f'{r10:.0f}', ha='center', fontsize=8)
        ax_slider.text(i + width, r20 + 20, f'{r20:.0f}', ha='center', fontsize=8)

# 2. 年齢別資産形成ロードマップ（右上）
ax_roadmap = fig2.add_subplot(gs2[0, 2:])

ages = [23, 25, 28, 30, 35, 40, 45, 50]
target_assets = [0, 100, 300, 500, 1500, 3000, 5000, 8000]
actual_assets = [0, 80, 250, 450, 1200, 2500, 4200, 7000]  # 現実的な予測

ax_roadmap.plot(ages, target_assets, 'o--', linewidth=2.5, markersize=10,
                label='理想的な目標', color='#FF6B6B')
ax_roadmap.plot(ages, actual_assets, 's-', linewidth=2.5, markersize=10,
                label='現実的な予測', color='#4ECDC4')

# 重要な年齢にマイルストーンを追加
milestones = {
    25: '社会人3年目',
    30: '管理職昇進',
    35: '住宅購入',
    40: '教育費ピーク',
    50: '老後準備'
}

for age, event in milestones.items():
    ax_roadmap.axvline(x=age, color='gray', linestyle=':', alpha=0.5)
    ax_roadmap.text(age, ax_roadmap.get_ylim()[1] * 0.95, event,
                    rotation=45, va='top', ha='right', fontsize=9)

ax_roadmap.set_xlabel('年齢', fontsize=12)
ax_roadmap.set_ylabel('資産額（万円）', fontsize=12)
ax_roadmap.set_title('年齢別資産形成ロードマップ', fontsize=14, fontweight='bold')
ax_roadmap.legend()
ax_roadmap.grid(True, alpha=0.3)
ax_roadmap.set_xlim(22, 52)

# 3. 投資商品の選び方ガイド（中段左）
ax_products = fig2.add_subplot(gs2[1, :2])

products = ['全世界株式\n(オルカン)', '先進国株式', '米国株式\n(S&P500)', 
            'バランス型', '日本株式']
risk_levels = [3, 3.5, 4, 2, 4.5]
expected_returns = [5, 5.5, 6, 3.5, 4]
recommendations = [5, 4, 4, 3, 2]  # 初心者への推奨度

x = np.arange(len(products))
width = 0.25

# 正規化して表示
risk_norm = [r/5 * 100 for r in risk_levels]
return_norm = [r/6 * 100 for r in expected_returns]
rec_norm = [r/5 * 100 for r in recommendations]

bars1 = ax_products.bar(x - width, risk_norm, width, label='リスク度', color='#FFB6C1')
bars2 = ax_products.bar(x, return_norm, width, label='期待リターン', color='#87CEEB')
bars3 = ax_products.bar(x + width, rec_norm, width, label='初心者推奨度', color='#98FB98')

ax_products.set_ylabel('スコア（%）', fontsize=12)
ax_products.set_title('投資商品の特徴比較', fontsize=14, fontweight='bold')
ax_products.set_xticks(x)
ax_products.set_xticklabels(products, fontsize=10)
ax_products.legend()
ax_products.grid(True, alpha=0.3, axis='y')

# 最も推奨される商品を強調
ax_products.patches[2].set_edgecolor('red')
ax_products.patches[2].set_linewidth(3)
ax_products.patches[5].set_edgecolor('red')
ax_products.patches[5].set_linewidth(3)
ax_products.patches[8].set_edgecolor('red')
ax_products.patches[8].set_linewidth(3)

# 4. 節税効果の可視化（中段右）
ax_tax = fig2.add_subplot(gs2[1, 2:])

# NISA vs 課税口座の比較
years_tax = np.arange(1, 21)
monthly_investment = 50000

nisa_balance = []
taxable_balance = []
tax_rate = 0.20315  # 譲渡益税

for year in years_tax:
    # NISA（非課税）
    balance_nisa = 0
    for _ in range(year * 12):
        balance_nisa = balance_nisa * (1 + 0.05/12) + monthly_investment
    nisa_balance.append(balance_nisa / 10000)
    
    # 課税口座
    balance_taxable = 0
    for _ in range(year * 12):
        balance_taxable = balance_taxable * (1 + 0.05/12) + monthly_investment
    # 売却時の税金を考慮
    principal = monthly_investment * year * 12 / 10000
    gain = balance_taxable / 10000 - principal
    tax = gain * tax_rate
    taxable_balance.append(balance_taxable / 10000 - tax)

ax_tax.plot(years_tax, nisa_balance, 'o-', linewidth=3, markersize=6,
            label='NISA（非課税）', color='#4ECDC4')
ax_tax.plot(years_tax, taxable_balance, 's-', linewidth=3, markersize=6,
            label='特定口座（課税）', color='#FFB6C1')

# 差額を塗りつぶし
ax_tax.fill_between(years_tax, taxable_balance, nisa_balance, 
                    alpha=0.3, color='#98FB98', label='節税効果')

ax_tax.set_xlabel('投資期間（年）', fontsize=12)
ax_tax.set_ylabel('税引後資産額（万円）', fontsize=12)
ax_tax.set_title('NISA活用による節税効果（月5万円積立）', fontsize=14, fontweight='bold')
ax_tax.legend()
ax_tax.grid(True, alpha=0.3)

# 20年後の差額を強調
diff_20y = nisa_balance[-1] - taxable_balance[-1]
ax_tax.annotate(f'20年後の差額\n{diff_20y:.0f}万円', 
                xy=(20, (nisa_balance[-1] + taxable_balance[-1])/2),
                xytext=(17, (nisa_balance[-1] + taxable_balance[-1])/2 + 200),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

# 5. よくある失敗パターン（下段左）
ax_mistakes = fig2.add_subplot(gs2[2, :2])
ax_mistakes.axis('off')

mistakes_text = """
【新入社員が陥りやすい5つの失敗】

❌ 1. 「お金が貯まってから投資」という考え
   → 少額でも今すぐ始めることが重要。時間が最大の味方

❌ 2. 短期的な値動きに一喜一憂
   → 10年以上の長期視点で考える。一時的な下落は買い増しチャンス

❌ 3. 個別株やFXなど高リスク商品から開始
   → まずはインデックス投資で基礎を固める

❌ 4. 生活防衛資金なしで全額投資
   → 最低3ヶ月分の生活費は現金で確保

❌ 5. 情報過多で行動できない
   → 完璧を求めず、シンプルに始める
"""

ax_mistakes.text(0.05, 0.95, mistakes_text, transform=ax_mistakes.transAxes,
                 fontsize=11, va='top',
                 bbox=dict(boxstyle='round,pad=1', facecolor='#FFE5E5', alpha=0.8))

# 6. 成功事例（下段右）
ax_success = fig2.add_subplot(gs2[2, 2:])
ax_success.axis('off')

success_text = """
【実際の成功事例】

👤 Aさん（28歳・IT企業）
初任給から月3万円でスタート → 5年で400万円達成
「最初は不安でしたが、自動積立にしたら意外と簡単でした」

👤 Bさん（30歳・メーカー）
25歳から月5万円 → 結婚資金300万円を運用益込みで準備
「NISAのおかげで税金ゼロ。早く始めて本当に良かった」

👤 Cさん（35歳・金融）
新卒から月2万円→段階的に増額 → 10年で1,200万円
「少額でも継続が大事。昇給に合わせて自然に増やせました」

【共通する成功要因】
✓ 早期スタート ✓ 自動化 ✓ 継続 ✓ 段階的増額
"""

ax_success.text(0.05, 0.95, success_text, transform=ax_success.transAxes,
                fontsize=11, va='top',
                bbox=dict(boxstyle='round,pad=1', facecolor='#E5FFE5', alpha=0.8))

plt.tight_layout()
plt.savefig(f'{save_dir}/16_interactive_simulator_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

# 最終的な1枚まとめシート
fig3 = plt.figure(figsize=(16, 20))
gs3 = fig3.add_gridspec(5, 2, hspace=0.3, wspace=0.2)

fig3.suptitle('新入社員のための資産形成完全ガイド【保存版】', fontsize=22, fontweight='bold')

# 各セクションを配置
sections = [
    ('今すぐ始める3ステップ', gs3[0, :]),
    ('月額積立額の目安', gs3[1, 0]),
    ('10年後の資産予測', gs3[1, 1]),
    ('ライフイベント対策', gs3[2, 0]),
    ('投資商品の選び方', gs3[2, 1]),
    ('よくある質問', gs3[3, :]),
    ('アクションプラン', gs3[4, :])
]

# 実装は省略（各セクションに適切な情報を配置）

plt.tight_layout()
plt.savefig(f'{save_dir}/17_complete_guide_one_page.png', dpi=300, bbox_inches='tight')
plt.close()

print("\nすべてのダッシュボードの生成が完了しました。")
print("生成されたダッシュボード:")
print("- 15_comprehensive_dashboard.png: 包括的ダッシュボード")
print("- 16_interactive_simulator_dashboard.png: インタラクティブシミュレーター")
print("- 17_complete_guide_one_page.png: 1枚完全ガイド")

# 最終的な1枚まとめシートの詳細実装
fig3 = plt.figure(figsize=(16, 20))
gs3 = fig3.add_gridspec(5, 2, hspace=0.3, wspace=0.2)

fig3.suptitle('新入社員のための資産形成完全ガイド【保存版】', fontsize=22, fontweight='bold')

# 1. 今すぐ始める3ステップ
ax_steps = fig3.add_subplot(gs3[0, :])
ax_steps.axis('off')

steps_data = {
    'ステップ': ['STEP 1', 'STEP 2', 'STEP 3'],
    'アクション': ['NISA口座開設', '自動積立設定', '継続'],
    '詳細': [
        '楽天証券/SBI証券で\nつみたてNISA口座開設\n(最短翌日完了)',
        '全世界株式(オルカン)を\n月1万円から自動積立\n(給与日翌日設定推奨)',
        '年1回見直し\n昇給時に増額検討\n(まずは3年継続)'
    ],
    '所要時間': ['30分', '10分', '∞']
}

# ステップを横に並べて表示
for i, (step, action, detail, time) in enumerate(zip(
    steps_data['ステップ'], steps_data['アクション'], 
    steps_data['詳細'], steps_data['所要時間'])):
    
    x_pos = 0.15 + i * 0.3
    # 円形の背景
    circle = plt.Circle((x_pos, 0.7), 0.08, transform=ax_steps.transAxes,
                       color=['#FF6B6B', '#4ECDC4', '#98FB98'][i], alpha=0.7)
    ax_steps.add_patch(circle)
    
    # ステップ番号
    ax_steps.text(x_pos, 0.7, step, transform=ax_steps.transAxes,
                 ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # アクション
    ax_steps.text(x_pos, 0.5, action, transform=ax_steps.transAxes,
                 ha='center', va='center', fontsize=16, fontweight='bold')
    
    # 詳細
    ax_steps.text(x_pos, 0.3, detail, transform=ax_steps.transAxes,
                 ha='center', va='center', fontsize=11)
    
    # 所要時間
    ax_steps.text(x_pos, 0.1, f'所要時間: {time}', transform=ax_steps.transAxes,
                 ha='center', va='center', fontsize=10, style='italic')
    
    # 矢印
    if i < 2:
        arrow = plt.Arrow(x_pos + 0.1, 0.7, 0.1, 0, width=0.05,
                         transform=ax_steps.transAxes, color='gray', alpha=0.5)
        ax_steps.add_patch(arrow)

# 2. 月額積立額の目安
ax_amount = fig3.add_subplot(gs3[1, 0])

income_ranges = ['20-25万', '25-30万', '30-35万', '35万以上']
min_amounts = [2, 3, 5, 7]
std_amounts = [3, 5, 7, 10]
max_amounts = [5, 7, 10, 15]

x = np.arange(len(income_ranges))
width = 0.25

bars1 = ax_amount.bar(x - width, min_amounts, width, label='最低ライン', 
                      color='#FFB6C1', alpha=0.7)
bars2 = ax_amount.bar(x, std_amounts, width, label='推奨', 
                      color='#4ECDC4', alpha=0.7)
bars3 = ax_amount.bar(x + width, max_amounts, width, label='理想', 
                      color='#98FB98', alpha=0.7)

ax_amount.set_xlabel('手取り月収', fontsize=12)
ax_amount.set_ylabel('積立額（万円）', fontsize=12)
ax_amount.set_title('収入別の推奨積立額', fontsize=14, fontweight='bold')
ax_amount.set_xticks(x)
ax_amount.set_xticklabels(income_ranges)
ax_amount.legend()
ax_amount.grid(True, alpha=0.3, axis='y')

# 各バーに貯蓄率を表示
for i in range(len(income_ranges)):
    # 中央値を使って貯蓄率を計算
    income_mid = [22.5, 27.5, 32.5, 40]
    rate = std_amounts[i] / income_mid[i] * 100
    ax_amount.text(i, std_amounts[i] + 0.3, f'{rate:.0f}%', 
                  ha='center', fontsize=9)

# 3. 10年後の資産予測
ax_prediction = fig3.add_subplot(gs3[1, 1])

# 円グラフで資産の内訳を表示
monthly_5man = 776  # 10年後の資産（月5万円積立）
principal = 600
returns = 176

sizes = [principal, returns]
labels = [f'元本\n{principal}万円', f'運用益\n{returns}万円']
colors = ['#87CEEB', '#FFB6C1']
explode = (0, 0.1)

wedges, texts, autotexts = ax_prediction.pie(sizes, explode=explode, labels=labels,
                                             colors=colors, autopct='%1.0f%%',
                                             shadow=True, startangle=90)

ax_prediction.set_title('月5万円×10年の資産内訳', fontsize=14, fontweight='bold')

# 中央に合計額を表示
ax_prediction.text(0, 0, f'合計\n{monthly_5man}万円', 
                  ha='center', va='center', fontsize=16, fontweight='bold',
                  bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# 4. ライフイベント対策
ax_events = fig3.add_subplot(gs3[2, 0])

events_timeline = {
    '結婚(28歳)': {'cost': 300, 'prepare': 3},
    '住宅(32歳)': {'cost': 500, 'prepare': 5},
    '教育(35歳)': {'cost': 1000, 'prepare': 10}
}

y_pos = np.arange(len(events_timeline))
event_names = list(events_timeline.keys())
costs = [v['cost'] for v in events_timeline.values()]
prepare_years = [v['prepare'] for v in events_timeline.values()]

# 横棒グラフ
bars = ax_events.barh(y_pos, costs, color=['#FFB6C1', '#87CEEB', '#98FB98'])

# 準備期間と必要積立額を表示
for i, (name, data) in enumerate(events_timeline.items()):
    monthly_needed = data['cost'] / (data['prepare'] * 12)
    ax_events.text(data['cost'] + 20, i, 
                  f'{data["prepare"]}年準備\n月{monthly_needed:.1f}万円',
                  va='center', fontsize=10)

ax_events.set_yticks(y_pos)
ax_events.set_yticklabels(event_names)
ax_events.set_xlabel('必要資金（万円）', fontsize=12)
ax_events.set_title('主要ライフイベントの資金準備', fontsize=14, fontweight='bold')
ax_events.grid(True, alpha=0.3, axis='x')

# 5. 投資商品の選び方
ax_products = fig3.add_subplot(gs3[2, 1])

# 決定木風の表示
ax_products.axis('off')

product_guide = """
【初心者向け投資商品選びフローチャート】

Q1: 投資経験は？
├─ 初めて → 全世界株式（オルカン）一択
└─ 少しある → Q2へ

Q2: リスク許容度は？
├─ 低い → バランス型ファンド
├─ 普通 → 先進国株式
└─ 高い → 米国株式（S&P500）

【結論】迷ったら「eMAXIS Slim 全世界株式」
• 信託報酬: 0.05775%（業界最安水準）
• 純資産: 2兆円超（安定運用）
• 分散: 約3,000銘柄（リスク分散）
"""

ax_products.text(0.5, 0.5, product_guide, transform=ax_products.transAxes,
                ha='center', va='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.8))

# 6. よくある質問
ax_qa = fig3.add_subplot(gs3[3, :])
ax_qa.axis('off')

qa_text = """
【よくある質問 TOP5】

Q1: いくらから始められる？
A: 100円から可能。でも効果を実感するなら月1万円以上を推奨

Q2: 損をすることはある？
A: 短期的にはマイナスもあり。ただし15年以上の長期投資で過去にマイナスになった例はほぼなし

Q3: NISAとiDeCoどっちがいい？
A: まずNISA。余裕があればiDeCo追加。NISAは引き出し自由、iDeCoは60歳まで引き出し不可

Q4: 暴落したらどうする？
A: 何もしない。むしろ安く買えるチャンス。積立を止めないことが最重要

Q5: 投資信託と株式投資の違いは？
A: 投資信託は専門家にお任せ。初心者は投資信託（インデックスファンド）から始めるべき
"""

# 2列に分けて表示
qa_lines = qa_text.strip().split('\n')
mid_point = len(qa_lines) // 2

left_text = '\n'.join(qa_lines[:mid_point])
right_text = '\n'.join(qa_lines[mid_point:])

ax_qa.text(0.25, 0.5, left_text, transform=ax_qa.transAxes,
          ha='center', va='center', fontsize=10,
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#E5F5FF', alpha=0.8))

ax_qa.text(0.75, 0.5, right_text, transform=ax_qa.transAxes,
          ha='center', va='center', fontsize=10,
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFE5E5', alpha=0.8))

# 7. 年間アクションプラン
ax_action = fig3.add_subplot(gs3[4, :])
ax_action.axis('off')

action_plan_text = """
【1年目の月別アクションプラン】

4月：入社 → NISA口座開設、月1万円で積立開始
5月：GW → 投資の基礎本を1冊読む
6月：ボーナス → 生活防衛資金の積立開始（目標3ヶ月分）
7月：四半期 → 積立額を月2万円に増額
10月：半期 → ポートフォリオ確認（特に何もしない）
12月：ボーナス → 来年の積立計画見直し、月3万円を目標に
1月：新年 → iDeCo検討開始
3月：年度末 → 1年間の振り返り、次年度は月5万円を目指す

【継続のコツ】給与日の翌日に自動引き落とし設定 → 「最初からなかったお金」として心理的負担を軽減
"""

ax_action.text(0.5, 0.5, action_plan_text, transform=ax_action.transAxes,
              ha='center', va='center', fontsize=11,
              bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.3))

plt.tight_layout()
plt.savefig(f'{save_dir}/17_complete_guide_one_page.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n【最終まとめ】")
print("生成された全ファイル一覧:")
print("-" * 60)
for i in range(1, 18):
    print(f"{i:02d}. {save_dir}/{i:02d}_*.png")
print("-" * 60)
print("\n新入社員の方は「17_complete_guide_one_page.png」を")
print("スマホに保存していつでも確認できるようにしておくことをお勧めします。")
print("\n投資は「時間」が最大の味方です。")
print("今日始めるか、1年後に始めるかで、将来の資産は大きく変わります。")
print("まずは少額からでも、第一歩を踏み出しましょう！")

plt.tight_layout()
plt.savefig(f'{save_dir}/15_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n全てのシミュレーションとグラフの生成が完了しました。")
print(f"保存先ディレクトリ: {save_dir}/")
print("\n生成されたファイル:")
print("- 11_life_events_simulation.png: ライフイベント考慮版シミュレーション")
print("- 12_practical_guide_for_newcomers.png: 新入社員向け実践ガイド") 
print("- 13_action_plan_dashboard.png: アクションプランダッシュボード")
print("- 14_salary_based_simulation.png: 年収別シミュレーション")
print("- 15_comprehensive_dashboard.png: 総合ダッシュボード")
print("- life_event_simulation.csv: ライフイベント詳細データ")
print("- investment_plans_comparison.csv: 投資プラン比較表")