# visualization_part1.py
# 基本設定と導入部・現状分析の図表（図1-9）

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['MS Gothic']
plt.rcParams['axes.unicode_minus'] = False


# カラーパレット設定
colors = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'positive': '#2ECC71',
    'negative': '#E74C3C',
    'neutral': '#95A5A6'
}

# 図を保存するディレクトリ
import os
os.makedirs('figures', exist_ok=True)

# ========== 図1: 開始年齢による資産形成の差 ==========
def create_fig1():
    plt.figure(figsize=(12, 8))
    
    # データ準備
    years = np.arange(0, 44)
    monthly_investment = 30000  # 月3万円
    annual_return = 0.05  # 年率5%
    
    # 22歳開始
    age_22 = []
    total = 0
    for year in years:
        if year <= 43:
            total = total * (1 + annual_return) + monthly_investment * 12
        age_22.append(total / 10000)  # 万円単位
    
    # 32歳開始
    age_32 = []
    total = 0
    for year in years:
        if 10 <= year <= 43:
            total = total * (1 + annual_return) + monthly_investment * 12
        age_32.append(total / 10000)
    
    # 42歳開始
    age_42 = []
    total = 0
    for year in years:
        if 20 <= year <= 43:
            total = total * (1 + annual_return) + monthly_investment * 12
        age_42.append(total / 10000)
    
    # プロット
    ages = 22 + years
    plt.plot(ages, age_22, linewidth=3, label='22歳開始', color=colors['primary'])
    plt.plot(ages, age_32, linewidth=3, label='32歳開始', color=colors['secondary'])
    plt.plot(ages, age_42, linewidth=3, label='42歳開始', color=colors['accent'])
    
    # 65歳時点の値を表示
    plt.scatter([65, 65, 65], [age_22[43], age_32[43], age_42[43]], s=100, zorder=5)
    plt.text(65.5, age_22[43], f'{age_22[43]:.0f}万円', fontsize=12, va='center')
    plt.text(65.5, age_32[43], f'{age_32[43]:.0f}万円', fontsize=12, va='center')
    plt.text(65.5, age_42[43], f'{age_42[43]:.0f}万円', fontsize=12, va='center')
    
    plt.xlabel('年齢', fontsize=14)
    plt.ylabel('資産額（万円）', fontsize=14)
    plt.title('図1: 開始年齢による資産形成の差\n（月3万円投資、年率5%運用）', fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(22, 67)
    plt.ylim(0, max(age_22) * 1.1)
    
    plt.tight_layout()
    plt.savefig('figures/fig01_age_difference.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図2: インフレによる現金価値の推移 ==========
def create_fig2():
    plt.figure(figsize=(12, 8))
    
    years = np.arange(0, 31)
    inflation_rate = 0.02  # 年率2%のインフレ
    
    # 現金の実質価値
    cash_value = 100 * (1 - inflation_rate) ** years
    
    # 銀行預金（年率0.001%）
    bank_nominal = 100 * (1.00001) ** years
    bank_real = bank_nominal / ((1 + inflation_rate) ** years) * 100
    
    # 投資（年率5%）
    investment_nominal = 100 * (1.05) ** years
    investment_real = investment_nominal / ((1 + inflation_rate) ** years) * 100
    
    plt.fill_between(years, 100, cash_value, alpha=0.3, color=colors['negative'], label='現金の実質価値')
    plt.plot(years, cash_value, linewidth=3, color=colors['negative'])
    plt.plot(years, bank_real, linewidth=3, color=colors['neutral'], label='銀行預金の実質価値')
    plt.plot(years, investment_real, linewidth=3, color=colors['positive'], label='投資の実質価値（年率5%）')
    
    plt.axhline(y=100, color='black', linestyle='--', alpha=0.5)
    plt.text(15, 102, '初期価値', fontsize=10, ha='center')
    
    plt.xlabel('経過年数', fontsize=14)
    plt.ylabel('実質価値（初期値を100とした場合）', fontsize=14)
    plt.title('図2: インフレによる資産の実質価値推移\n（年率2%のインフレを想定）', fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 30)
    plt.ylim(40, 180)
    
    plt.tight_layout()
    plt.savefig('figures/fig02_inflation_impact.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図3: 人生100年時代の必要資金 ==========
def create_fig3():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左側：支出の内訳
    years = np.arange(65, 101)
    living_cost = np.full(len(years), 25)  # 月25万円
    medical_cost = np.linspace(5, 15, len(years))  # 医療費は年齢とともに増加
    leisure_cost = np.linspace(10, 5, len(years))  # 娯楽費は年齢とともに減少
    
    ax1.fill_between(years, 0, living_cost, alpha=0.7, color=colors['primary'], label='基本生活費')
    ax1.fill_between(years, living_cost, living_cost + medical_cost, alpha=0.7, color=colors['secondary'], label='医療・介護費')
    ax1.fill_between(years, living_cost + medical_cost, living_cost + medical_cost + leisure_cost, alpha=0.7, color=colors['accent'], label='娯楽・趣味費')
    
    ax1.set_xlabel('年齢', fontsize=14)
    ax1.set_ylabel('月額支出（万円）', fontsize=14)
    ax1.set_title('老後の支出内訳', fontsize=14)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(65, 100)
    ax1.set_ylim(0, 50)
    
    # 右側：必要資金と年金のギャップ
    total_cost = (living_cost + medical_cost + leisure_cost) * 12  # 年間支出
    pension = np.full(len(years), 200)  # 年金年額200万円
    gap = total_cost - pension
    cumulative_gap = np.cumsum(gap)
    
    ax2.bar(years[::5], total_cost[::5], width=3, alpha=0.7, color=colors['negative'], label='年間支出')
    ax2.bar(years[::5], pension[::5], width=3, alpha=0.7, color=colors['positive'], label='公的年金')
    
    # 累積不足額を第2軸に
    ax2_twin = ax2.twinx()
    ax2_twin.plot(years, cumulative_gap, linewidth=3, color=colors['accent'], label='累積不足額')
    ax2_twin.set_ylabel('累積不足額（万円）', fontsize=14)
    
    ax2.set_xlabel('年齢', fontsize=14)
    ax2.set_ylabel('年間金額（万円）', fontsize=14)
    ax2.set_title('必要資金と年金のギャップ', fontsize=14)
    ax2.legend(loc='upper left', fontsize=12)
    ax2_twin.legend(loc='upper right', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(65, 100)
    
    plt.suptitle('図3: 人生100年時代の必要資金シミュレーション', fontsize=16)
    plt.tight_layout()
    plt.savefig('figures/fig03_retirement_funds.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図4: 給与明細の詳細解説図 ==========
def create_fig4():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左側：総支給額の内訳
    labels1 = ['基本給\n210,000円', '住宅手当\n80,000円', '固定残業代\n49,300円', '通勤手当\n4,200円']
    sizes1 = [210000, 80000, 49300, 4200]
    colors1 = [colors['primary'], colors['secondary'], colors['accent'], colors['neutral']]
    
    wedges1, texts1, autotexts1 = ax1.pie(sizes1, labels=labels1, colors=colors1, autopct='%1.1f%%',
                                           startangle=90, textprops={'fontsize': 11})
    ax1.set_title('総支給額 343,500円の内訳', fontsize=14)
    
    # 右側：手取り計算
    categories = ['総支給額', '社会保険料', '所得税', '住民税', '手取り額']
    values = [343500, -25000, -12000, -12059, 294441]
    colors2 = [colors['positive'], colors['negative'], colors['negative'], colors['negative'], colors['primary']]
    
    bars = ax2.bar(categories, values, color=colors2, alpha=0.7)
    
    # 値を表示
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 5000 if height > 0 else height - 5000,
                f'{abs(value):,}円', ha='center', va='bottom' if height > 0 else 'top', fontsize=10)
    
    ax2.axhline(y=0, color='black', linewidth=0.5)
    ax2.set_ylabel('金額（円）', fontsize=14)
    ax2.set_title('総支給額から手取り額への計算', fontsize=14)
    ax2.set_ylim(-50000, 400000)
    
    plt.suptitle('図4: 給与明細の詳細解説', fontsize=16)
    plt.tight_layout()
    plt.savefig('figures/fig04_salary_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図5: 推奨支出配分サンキーダイアグラム ==========
def create_fig5():
    # サンキーダイアグラムの代わりに、フロー図風の可視化
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # 手取り額
    take_home = 294441
    
    # 配分
    categories = {
        '生活費': {'amount': 176000, 'color': colors['primary'], 'items': ['家賃: 120,000', '食費: 40,000', '光熱費: 16,000']},
        '自己投資': {'amount': 29000, 'color': colors['secondary'], 'items': ['書籍: 10,000', 'セミナー: 10,000', '資格: 9,000']},
        '娯楽・交際': {'amount': 29000, 'color': colors['accent'], 'items': ['飲み会: 15,000', '趣味: 14,000']},
        '緊急予備': {'amount': 15000, 'color': colors['neutral'], 'items': ['予備費: 15,000']},
        '投資': {'amount': 45441, 'color': colors['positive'], 'items': ['NISA: 45,441']}
    }
    
    # メインの棒グラフ
    y_pos = np.arange(len(categories))
    amounts = [cat['amount'] for cat in categories.values()]
    colors_list = [cat['color'] for cat in categories.values()]
    
    bars = ax.barh(y_pos, amounts, color=colors_list, alpha=0.7)
    
    # カテゴリ名と金額を表示
    for i, (name, data) in enumerate(categories.items()):
        ax.text(-5000, i, name, ha='right', va='center', fontsize=12, fontweight='bold')
        ax.text(data['amount'] + 2000, i, f"{data['amount']:,}円\n({data['amount']/take_home*100:.1f}%)", 
                ha='left', va='center', fontsize=10)
    
    ax.set_xlim(-30000, 200000)
    ax.set_ylim(-0.5, len(categories) - 0.5)
    ax.set_xlabel('金額（円）', fontsize=14)
    ax.set_title(f'図5: 手取り{take_home:,}円の推奨支出配分', fontsize=16, pad=20)
    ax.set_yticks([])
    
    # 縦線で手取り額を表示
    # 縦線で手取り額を表示
    ax.axvline(x=take_home, color='black', linestyle='--', alpha=0.5)
    ax.text(take_home, len(categories), f'手取り額\n{take_home:,}円', ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('figures/fig05_expense_allocation.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図6: 港区・品川区エリアの生活費内訳 ==========
def create_fig6():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左側：生活費の内訳（ドーナツチャート）
    labels = ['家賃', '食費', '光熱費', '通信費', '日用品', 'その他']
    sizes = [120000, 40000, 15000, 10000, 10000, 15000]
    colors_list = [colors['primary'], colors['secondary'], colors['accent'], 
                   colors['positive'], colors['negative'], colors['neutral']]
    
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors_list, autopct='%1.1f%%',
                                       startangle=90, pctdistance=0.85)
    
    # ドーナツチャートにする
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax1.add_artist(centre_circle)
    ax1.text(0, 0, '月額生活費\n210,000円', ha='center', va='center', fontsize=14, fontweight='bold')
    ax1.set_title('港区・品川区エリアの生活費内訳', fontsize=14)
    
    # 右側：エリア別家賃相場比較
    areas = ['港区', '品川区', '渋谷区', '新宿区', '文京区', '23区平均']
    rent_1r = [12.5, 10.8, 11.5, 10.2, 9.5, 8.7]
    
    bars = ax2.bar(areas, rent_1r, color=colors['primary'], alpha=0.7)
    ax2.axhline(y=12, color='red', linestyle='--', alpha=0.7, label='想定家賃')
    
    for bar, rent in zip(bars, rent_1r):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                f'{rent}万円', ha='center', va='bottom', fontsize=10)
    
    ax2.set_ylabel('家賃（万円）', fontsize=14)
    ax2.set_title('エリア別ワンルーム家賃相場', fontsize=14)
    ax2.legend()
    ax2.set_ylim(0, 14)
    
    plt.suptitle('図6: 都内一人暮らしの生活費実態', fontsize=16)
    plt.tight_layout()
    plt.savefig('figures/fig06_living_costs.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図7: 当社の組織ピラミッドと人数分布 ==========
def create_fig7():
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 組織構造データ（仮想的な分布）
    levels = ['部長以上', '課長', '係長', '主任', '一般社員', '新入社員']
    grades = ['D1-D3', 'M1-M3', 'P1-P2', 'P3-P4', 'B1', 'B2']
    counts = [8, 22, 45, 68, 101, 134]  # 合計378名
    percentages = [c/378*100 for c in counts]
    
    # ピラミッド型の可視化
    y_pos = np.arange(len(levels))
    
    # 左右対称のピラミッドを作成
    for i, (level, grade, count, pct) in enumerate(zip(levels, grades, counts, percentages)):
        # バーを中央に配置
        bar = ax.barh(i, count, left=-count/2, height=0.8, 
                     color=colors['primary'], alpha=0.7 - i*0.1)
        
        # ラベルを追加
        ax.text(0, i, f'{level}\n({grade})', ha='center', va='center', 
                fontsize=11, fontweight='bold', color='white')
        ax.text(count/2 + 5, i, f'{count}名\n({pct:.1f}%)', 
                ha='left', va='center', fontsize=10)
    
    ax.set_xlim(-80, 80)
    ax.set_ylim(-0.5, len(levels) - 0.5)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    ax.set_title('図7: 当社の組織構造（全378名）', fontsize=16, pad=20)
    
    # 昇進確率の注釈
    ax.text(0, -1, '※ 新入社員から10年で主任クラスに到達する割合：約60%', 
            ha='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig('figures/fig07_organization_pyramid.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図8: 3つのキャリアパス別年収推移グラフ ==========
def create_fig8():
    plt.figure(figsize=(14, 8))
    
    ages = np.arange(22, 66)
    years_exp = ages - 22
    
    # 上位20%パス（早期昇進）
    top_path = []
    for year in years_exp:
        if year < 3:
            salary = 340  # B2
        elif year < 5:
            salary = 390  # B1
        elif year < 7:
            salary = 480  # P3
        elif year < 10:
            salary = 520  # P2
        elif year < 13:
            salary = 590  # P1
        elif year < 17:
            salary = 700  # M3
        elif year < 22:
            salary = 800  # M2
        elif year < 27:
            salary = 900  # M1
        elif year < 32:
            salary = 980  # D3
        else:
            salary = 1100  # D2
        top_path.append(salary)
    
    # 標準パス
    standard_path = []
    for year in years_exp:
        if year < 3:
            salary = 340  # B2
        elif year < 6:
            salary = 390  # B1
        elif year < 9:
            salary = 430  # P4
        elif year < 13:
            salary = 480  # P3
        elif year < 17:
            salary = 520  # P2
        elif year < 22:
            salary = 590  # P1
        elif year < 28:
            salary = 700  # M3
        elif year < 35:
            salary = 800  # M2
        else:
            salary = 900  # M1
        standard_path.append(salary)
    
    # 保守的パス
    conservative_path = []
    for year in years_exp:
        if year < 4:
            salary = 340  # B2
        elif year < 8:
            salary = 390  # B1
        elif year < 13:
            salary = 430  # P4
        elif year < 18:
            salary = 480  # P3
        elif year < 25:
            salary = 520  # P2
        elif year < 35:
            salary = 590  # P1
        else:
            salary = 700  # M3
        conservative_path.append(salary)
    
    # プロット
    plt.plot(ages, top_path, linewidth=3, label='上位20%パス', color=colors['positive'], marker='o', markersize=4)
    plt.plot(ages, standard_path, linewidth=3, label='標準パス', color=colors['primary'], marker='s', markersize=4)
    plt.plot(ages, conservative_path, linewidth=3, label='保守的パス', color=colors['secondary'], marker='^', markersize=4)
    
    # 主要なマイルストーンをマーク
    plt.axvline(x=30, color='gray', linestyle='--', alpha=0.5)
    plt.text(30, 1150, '30歳', ha='center', fontsize=10)
    plt.axvline(x=40, color='gray', linestyle='--', alpha=0.5)
    plt.text(40, 1150, '40歳', ha='center', fontsize=10)
    plt.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
    plt.text(50, 1150, '50歳', ha='center', fontsize=10)
    
    plt.xlabel('年齢', fontsize=14)
    plt.ylabel('年収（万円）', fontsize=14)
    plt.title('図8: キャリアパス別年収推移シミュレーション', fontsize=16, pad=20)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xlim(22, 65)
    plt.ylim(300, 1200)
    
    plt.tight_layout()
    plt.savefig('figures/fig08_career_salary_paths.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図9: キャリアパス別生涯年収の棒グラフ ==========
def create_fig9():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 生涯年収の計算（22-65歳の43年間）
    paths = ['上位20%パス', '標準パス', '保守的パス']
    gross_income = [3.2, 2.5, 2.0]  # 億円
    net_income = [2.4, 1.9, 1.5]  # 手取り（約75%）
    investment_potential = [0.48, 0.38, 0.30]  # 投資可能額（手取りの20%）
    
    # 左側：生涯年収の比較
    x = np.arange(len(paths))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, gross_income, width, label='額面', color=colors['primary'], alpha=0.7)
    bars2 = ax1.bar(x + width/2, net_income, width, label='手取り', color=colors['secondary'], alpha=0.7)
    
    # 値を表示
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{height:.1f}億円', ha='center', va='bottom', fontsize=10)
    
    ax1.set_ylabel('金額（億円）', fontsize=14)
    ax1.set_title('生涯年収の比較', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(paths)
    ax1.legend()
    ax1.set_ylim(0, 3.5)
    
    # 右側：投資可能額の累計
    bars3 = ax2.bar(paths, investment_potential, color=colors['positive'], alpha=0.7)
    
    for bar, value in zip(bars3, investment_potential):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                f'{value:.2f}億円', ha='center', va='bottom', fontsize=10)
    
    ax2.set_ylabel('投資可能額累計（億円）', fontsize=14)
    ax2.set_title('43年間の投資可能額（手取りの20%）', fontsize=14)
    ax2.set_ylim(0, 0.6)
    
    plt.suptitle('図9: キャリアパス別の生涯収入分析', fontsize=16)
    plt.tight_layout()
    plt.savefig('figures/fig09_lifetime_income.png', dpi=300, bbox_inches='tight')
    plt.close()

# メイン実行部
if __name__ == "__main__":
    print("図表の生成を開始します...")
    
    # 各図を生成
    create_fig1()
    print("図1: 開始年齢による資産形成の差 - 完了")
    
    create_fig2()
    print("図2: インフレによる現金価値の推移 - 完了")
    
    create_fig3()
    print("図3: 人生100年時代の必要資金 - 完了")
    
    create_fig4()
    print("図4: 給与明細の詳細解説図 - 完了")
    
    create_fig5()
    print("図5: 推奨支出配分 - 完了")
    
    create_fig6()
    print("図6: 港区・品川区エリアの生活費内訳 - 完了")
    
    create_fig7()
    print("図7: 当社の組織ピラミッドと人数分布 - 完了")
    
    create_fig8()
    print("図8: キャリアパス別年収推移グラフ - 完了")
    
    create_fig9()
    print("図9: キャリアパス別生涯年収 - 完了")
    
    print("\nPart 1（図1-9）の生成が完了しました！")