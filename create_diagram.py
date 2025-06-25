import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# 日本語フォントの設定（ご自身の環境に合わせて調整してください）
# Windows: 'Yu Gothic', 'Meiryo'
# Mac: 'Hiragino Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False

# 保存用ディレクトリの作成
save_dir = "seminar_graphs_v2"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# --- シミュレーションデータの生成 ---
# キャリアパスと年収データ
career_data = {
    'age':       [22, 25, 28, 33, 38, 46, 65],
    'std_salary': [344, 402, 506, 686, 850, 1144, 1144],
    'high_salary':[344, 441, 605, 850, 1079, 1144, 1144],
    'low_salary': [344, 362, 417, 522, 686, 1144, 1144]
}

# 1年ごとの詳細データを生成
ages = np.arange(22, 66)
salaries = {
    'std': np.interp(ages, career_data['age'], career_data['std_salary']),
    'high': np.interp(ages, career_data['age'], career_data['high_salary']),
    'low': np.interp(ages, career_data['age'], career_data['low_salary'])
}

# --- 1. 10年後の資産格差イメージ (01_introduction_gap.png) ---
def create_01_introduction_gap():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7), sharey=True)
    
    # 貯金のみの10年後資産
    savings_only = 34.4 * 0.15 * 10 
    
    # 投資ありの10年後資産（標準シナリオ）
    balance = 0
    for i in range(10):
        annual_saving = salaries['std'][i] * 0.15
        balance = balance * 1.05 + annual_saving
    investment_asset = balance

    ax1.bar(['資産'], [savings_only], color='#a2d2ff', width=0.5)
    ax1.text(0, savings_only / 2, '貯金のみ', ha='center', va='center', fontsize=20, fontweight='bold', color='#023047')
    ax1.text(0, savings_only + 50, f'{savings_only:.0f}万円', ha='center', va='center', fontsize=22, color='#023047')
    ax1.set_title('何もしなかった未来', fontsize=16, pad=20)
    ax1.set_ylabel('10年後の資産額（万円）', fontsize=14)
    ax1.get_xaxis().set_visible(False)

    ax2.bar(['資産'], [investment_asset], color='#ffb703', width=0.5)
    ax2.text(0, investment_asset / 2, '投資あり', ha='center', va='center', fontsize=20, fontweight='bold', color='#023047')
    ax2.text(0, investment_asset + 50, f'{investment_asset:.0f}万円', ha='center', va='center', fontsize=22, color='#023047')
    ax2.set_title('正しく行動した未来', fontsize=16, pad=20, color='#ffb703')
    ax2.get_xaxis().set_visible(False)
    
    fig.suptitle('図1: 10年後の資産格差イメージ', fontsize=18, fontweight='bold')
    ax1.set_ylim(0, max(investment_asset, savings_only) * 1.2)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'{save_dir}/01_introduction_gap.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- 2. 理想の給与仕分け (02_money_management_pie.png) ---
def create_02_money_management_pie():
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(aspect="equal"))
    labels = ['消費 (65%)\n15.0万円', '将来への投資 (15%)\n3.4万円', 'お楽しみ (10%)\n2.3万円', '自己投資 (10%)\n2.3万円']
    sizes = [65, 15, 10, 10]
    colors = ['#a2d2ff', '#ffb703', '#fb8500', '#8ecae6']
    explode = (0, 0.1, 0, 0)
    
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, colors=colors, autopct='%1.0f%%',
                                      shadow=True, startangle=140, pctdistance=0.85,
                                      textprops={'fontsize': 14, 'fontweight': 'bold', 'color': 'white'})
    
    ax.legend(wedges, labels, title="項目", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=12)
    
    ax.set_title('図2: 理想の給与仕分け（手取り23万円の場合）', fontsize=18, fontweight='bold', pad=20)
    plt.savefig(f'{save_dir}/02_money_management_pie.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- 3. 生活防衛資金の重要性 (03_emergency_fund_base.png) ---
def create_03_emergency_fund_base():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.3, color='#468faf', alpha=0.8))
    ax.text(0.5, 0.15, '生活防衛資金 (70-140万円)', ha='center', va='center', fontsize=18, fontweight='bold', color='white')
    ax.text(0.5, 0.05, '（普通預金で確保）', ha='center', va='center', fontsize=12, color='white')

    ax.add_patch(plt.Polygon([[0.25, 0.3], [0.75, 0.3], [0.5, 0.5]], color='#ffb703', alpha=0.8))
    ax.text(0.5, 0.38, '投資資産', ha='center', va='center', fontsize=18, fontweight='bold')
    
    ax.text(0.1, 0.7, '市場の嵐\n(経済ショック)', ha='center', va='center', fontsize=14, color='gray', style='italic')
    ax.annotate('', xy=(0.4, 0.5), xytext=(0.2, 0.8),
                arrowprops=dict(arrowstyle='simple,head_length=0.8,head_width=0.8', color='gray', lw=2))
    
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('図3: 生活防衛資金という"心の安全基地"', fontsize=18, fontweight='bold')
    plt.savefig(f'{save_dir}/03_emergency_fund_base.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- 4. 複利の雪だるま効果 (04_compound_interest_snowball.png) ---
def create_04_compound_interest_snowball():
    fig, ax = plt.subplots(figsize=(12, 7))

    years = np.arange(0, 44)
    principal = 3 * 12 * years
    asset_3 = [3*12 if i == 0 else asset * (1.03) + 3*12 for i, asset in enumerate([0] + [0]*(len(years)-1))]
    for i in range(1, len(years)): asset_3[i] = asset_3[i-1] * 1.03 + 3*12
    asset_5 = [3*12 if i == 0 else asset * (1.05) + 3*12 for i, asset in enumerate([0] + [0]*(len(years)-1))]
    for i in range(1, len(years)): asset_5[i] = asset_5[i-1] * 1.05 + 3*12
    
    ax.stackplot(years, principal, [a - p for a, p in zip(asset_5, principal)],
                 labels=['元本', '運用益'], colors=['#a2d2ff', '#ffb703'], alpha=0.8)

    ax.plot(years, asset_5, color='#fb8500', lw=2, label='総資産')
    
    ax.set_xlabel('積立年数', fontsize=14)
    ax.set_ylabel('資産額（万円）', fontsize=14)
    ax.set_title('図4: 複利の雪だるま効果（月3万円積立）', fontsize=18, fontweight='bold')
    ax.legend(loc='upper left', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # 注釈
    ax.annotate(f'10年後: {(principal[10]+(asset_5[10]-principal[10])):.0f}万円\n(運用益: {asset_5[10]-principal[10]:.0f}万円)', 
                xy=(10, asset_5[10]), xytext=(12, asset_5[10]-1000), arrowprops=dict(arrowstyle='->'))
    ax.annotate(f'30年後: {(principal[30]+(asset_5[30]-principal[30])):.0f}万円\n(運用益: {asset_5[30]-principal[30]:.0f}万円)', 
                xy=(30, asset_5[30]), xytext=(32, asset_5[30]-4000), arrowprops=dict(arrowstyle='->'))

    plt.tight_layout()
    plt.savefig(f'{save_dir}/04_compound_interest_snowball.png', dpi=300, bbox_inches='tight')
    plt.close()
    
# --- 5. キャリア登山図 (05_career_mountain.png) ---
def create_05_career_mountain():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(ages, salaries['high'], 'o-', label='上位10%', color='#ffb703', lw=3, ms=8)
    ax.plot(ages, salaries['std'], 's-', label='標準50%', color='#8ecae6', lw=3, ms=8)
    ax.plot(ages, salaries['low'], '^-', label='下位25%', color='#a2d2ff', lw=3, ms=8)
    
    ax.fill_between(ages, salaries['low'], 0, color='#a2d2ff', alpha=0.3)
    ax.fill_between(ages, salaries['std'], salaries['low'], color='#8ecae6', alpha=0.3)
    ax.fill_between(ages, salaries['high'], salaries['std'], color='#ffb703', alpha=0.3)
    
    ax.set_xlabel('年齢', fontsize=14)
    ax.set_ylabel('年収（万円）', fontsize=14)
    ax.set_title('図5: あなたのキャリア登山図', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    ax.text(30, 900, 'Manager / Director', ha='center', fontsize=14, color='#333')
    ax.text(30, 450, 'Professional', ha='center', fontsize=14, color='#333')
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/05_career_mountain.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- 6. 資産形成ロードマップ (06_asset_roadmap_standard.png) ---
def create_06_asset_roadmap_standard():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 標準シナリオの資産推移を計算
    assets = []
    balance = 0
    for i, age in enumerate(ages):
        annual_saving = salaries['std'][i] * 0.20 # 手取りの20%
        balance = balance * 1.05 + annual_saving
        assets.append(balance)

    ax.plot(ages, assets, color='#4ECDC4', lw=4, label='資産額')
    ax.fill_between(ages, 0, assets, color='#4ECDC4', alpha=0.1)
    
    # ライフイベント
    events = {
        30: (890, '結婚 (-300万)'),
        31: (1000, '1000万円達成'),
        35: (1800, '第一子 (-100万)'),
        42: (3500, '3000万円達成'),
        59: (11000, '1億円達成')
    }
    
    for age, (asset, label) in events.items():
        ax.plot([age], [asset], 'o', ms=12, color='#FF6B6B', mec='white', mew=2)
        ax.text(age, asset + 1000, f'{age}歳\n{label}', ha='center', fontsize=12, fontweight='bold')

    ax.set_xlabel('年齢', fontsize=14)
    ax.set_ylabel('資産額（万円）', fontsize=14)
    ax.set_title('図6: あなたの資産形成ロードマップ（標準シナリオ）', fontsize=18, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/06_asset_roadmap_standard.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- 7. 未来分岐シミュレーション（積立額） (07_choice_contribution.png) ---
def create_07_choice_contribution():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    plans = {'保守(10%)': 0.1, '標準(20%)': 0.2, '積極(30%)': 0.3}
    colors = {'保守(10%)': '#a2d2ff', '標準(20%)': '#8ecae6', '積極(30%)': '#ffb703'}
    
    for name, rate in plans.items():
        assets = []
        balance = 0
        for i, age in enumerate(ages):
            annual_saving = salaries['std'][i] * rate
            balance = balance * 1.05 + annual_saving
            assets.append(balance)
        
        ax.plot(ages, assets, label=f'{name}: {assets[-1]/10000:.1f}億円', 
                color=colors[name], lw=4 if name == '標準(20%)' else 2.5)

    ax.set_xlabel('年齢', fontsize=14)
    ax.set_ylabel('資産額（万円）', fontsize=14)
    ax.set_title('図7: 未来分岐シミュレーション（積立額の選択）', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/07_choice_contribution.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- 8. 未来分岐シミュレーション（投資先） (08_choice_return.png) ---
def create_08_choice_return():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    returns = {'保守(3%)': 1.03, '標準(5%)': 1.05, '積極(7%)': 1.07}
    colors = {'保守(3%)': '#a2d2ff', '標準(5%)': '#8ecae6', '積極(7%)': '#ffb703'}
    
    for name, rate in returns.items():
        assets = []
        balance = 0
        for i, age in enumerate(ages):
            annual_saving = salaries['std'][i] * 0.20
            balance = balance * rate + annual_saving
            assets.append(balance)
            
        ax.plot(ages, assets, label=f'{name}: {assets[-1]/10000:.1f}億円', 
                color=colors[name], lw=4 if name == '標準(5%)' else 2.5)

    ax.set_xlabel('年齢', fontsize=14)
    ax.set_ylabel('資産額（万円）', fontsize=14)
    ax.set_title('図8: 未来分岐シミュレーション（投資先の選択）', fontsize=18, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(f'{save_dir}/08_choice_return.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- 9. アクションプラン3ステップ (09_action_plan_3steps.png) ---
def create_09_action_plan_3steps():
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    
    steps = [
        ('1. 口座開設', '楽天証券 or SBI証券\nNISA口座を申し込む', '#a2d2ff'),
        ('2. 商品選択', 'eMAXIS Slim\n全世界株式', '#8ecae6'),
        ('3. 自動設定', '月3万円から\n給与日翌日に設定', '#ffb703')
    ]
    
    for i, (title, desc, color) in enumerate(steps):
        ax = axes[i]
        ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, color=color, alpha=0.2, ec=color, lw=3))
        ax.text(0.5, 0.75, f'STEP {i+1}', ha='center', fontsize=20, fontweight='bold')
        ax.text(0.5, 0.55, title, ha='center', fontsize=22, fontweight='bold', color='#023047')
        ax.text(0.5, 0.3, desc, ha='center', va='top', fontsize=16, linespacing=1.5)
        ax.axis('off')
        
    fig.suptitle('図9: 最初の1時間で未来を変えるアクションプラン', fontsize=18, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f'{save_dir}/09_action_plan_3steps.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- すべてのグラフを生成 ---
if __name__ == '__main__':
    create_01_introduction_gap()
    create_02_money_management_pie()
    create_03_emergency_fund_base()
    create_04_compound_interest_snowball()
    create_05_career_mountain()
    create_06_asset_roadmap_standard()
    create_07_choice_contribution()
    create_08_choice_return()
    create_09_action_plan_3steps()
    
    print(f"9個のグラフが '{save_dir}/' ディレクトリに保存されました。")