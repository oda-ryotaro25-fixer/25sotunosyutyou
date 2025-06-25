# visualization_part2.py
# 投資基礎とNISA関連の図表（図10-15）

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

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

# ========== 図10: 単利vs複利の成長曲線 ==========
def create_fig10():
    plt.figure(figsize=(12, 8))
    
    years = np.arange(0, 31)
    principal = 100  # 100万円
    rate = 0.05  # 年率5%
    
    # 単利計算
    simple_interest = principal + (principal * rate * years)
    
    # 複利計算
    compound_interest = principal * (1 + rate) ** years
    
    plt.plot(years, simple_interest, linewidth=3, label='単利（年率5%）', 
             color=colors['secondary'], linestyle='--')
    plt.plot(years, compound_interest, linewidth=3, label='複利（年率5%）', 
             color=colors['primary'])
    
    # 差額を塗りつぶし
    plt.fill_between(years, simple_interest, compound_interest, 
                     alpha=0.3, color=colors['positive'])
    
    # 主要ポイントにマーカー
    for year in [10, 20, 30]:
        diff = compound_interest[year] - simple_interest[year]
        plt.annotate(f'差額: {diff:.0f}万円', 
                    xy=(year, compound_interest[year]), 
                    xytext=(year+2, compound_interest[year]+20),
                    arrowprops=dict(arrowstyle='->', color='black', alpha=0.5),
                    fontsize=10)
    
    plt.xlabel('運用年数', fontsize=14)
    plt.ylabel('資産額（万円）', fontsize=14)
    plt.title('図10: 単利と複利の違い（元本100万円、年率5%）', fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 30)
    plt.ylim(80, 450)
    
    plt.tight_layout()
    plt.savefig('figures/fig10_simple_vs_compound.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図11: 主要投資商品のリスク・リターン散布図 ==========
def create_fig11():
    plt.figure(figsize=(12, 10))
    
    # 投資商品データ
    products = {
        '普通預金': {'risk': 0.1, 'return': 0.001, 'color': colors['neutral']},
        '定期預金': {'risk': 0.2, 'return': 0.01, 'color': colors['neutral']},
        '国債': {'risk': 1, 'return': 0.5, 'color': colors['secondary']},
        '社債': {'risk': 3, 'return': 2, 'color': colors['secondary']},
        'バランス型投信': {'risk': 8, 'return': 4, 'color': colors['primary']},
        '国内株式': {'risk': 15, 'return': 6, 'color': colors['accent']},
        '先進国株式': {'risk': 18, 'return': 7, 'color': colors['accent']},
        '新興国株式': {'risk': 25, 'return': 9, 'color': colors['negative']},
        '仮想通貨': {'risk': 40, 'return': 15, 'color': colors['negative']},
    }
    
    # 散布図
    for name, data in products.items():
        plt.scatter(data['risk'], data['return'], s=300, alpha=0.7, 
                   color=data['color'], edgecolors='black', linewidth=2)
        plt.annotate(name, (data['risk'], data['return']), 
                    xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    # 効率的フロンティア（仮想的な曲線）
    eff_risk = np.linspace(0, 25, 100)
    eff_return = 0.3 * np.sqrt(eff_risk)
    plt.plot(eff_risk, eff_return, 'k--', alpha=0.5, linewidth=2, 
             label='効率的フロンティア')
    
    # 初心者推奨ゾーン
    rect = Rectangle((5, 2), 15, 6, linewidth=3, edgecolor=colors['positive'], 
                    facecolor=colors['positive'], alpha=0.2)
    plt.gca().add_patch(rect)
    plt.text(12.5, 5, '初心者\n推奨ゾーン', ha='center', va='center', 
             fontsize=14, fontweight='bold', color=colors['positive'])
    
    plt.xlabel('リスク（標準偏差 %）', fontsize=14)
    plt.ylabel('期待リターン（%）', fontsize=14)
    plt.title('図11: 主要投資商品のリスク・リターンマップ', fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(-2, 45)
    plt.ylim(-1, 17)
    
    plt.tight_layout()
    plt.savefig('figures/fig11_risk_return_map.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図12: 分散投資によるリスク低減効果 ==========
def create_fig12():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # 左側：銘柄数とリスクの関係
    n_stocks = np.arange(1, 31)
    # リスクは銘柄数の平方根に反比例
    individual_risk = 25  # 個別株のリスク
    systematic_risk = 10  # 市場全体のリスク
    total_risk = systematic_risk + individual_risk / np.sqrt(n_stocks)
    
    ax1.plot(n_stocks, total_risk, linewidth=3, color=colors['primary'])
    ax1.axhline(y=systematic_risk, color=colors['secondary'], linestyle='--', 
                label='システマティックリスク（分散不可）')
    ax1.fill_between(n_stocks, systematic_risk, total_risk, alpha=0.3, 
                     color=colors['accent'], label='非システマティックリスク（分散可能）')
    
    ax1.set_xlabel('保有銘柄数', fontsize=14)
    ax1.set_ylabel('ポートフォリオのリスク（%）', fontsize=14)
    ax1.set_title('銘柄数増加によるリスク低減', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1, 30)
    ax1.set_ylim(0, 40)
    
    # 右側：地域分散の効果
    regions = ['日本のみ', '日本+米国', '日本+米国\n+欧州', '全世界']
    risk_levels = [20, 15, 12, 10]
    returns = [5, 6, 6.5, 7]
    
    scatter = ax2.scatter(risk_levels, returns, s=500, alpha=0.7, 
                         c=range(len(regions)), cmap='viridis')
    
    for i, region in enumerate(regions):
        ax2.annotate(region, (risk_levels[i], returns[i]), 
                    xytext=(0, -30), textcoords='offset points', 
                    ha='center', fontsize=10)
    
    # 矢印で分散の流れを表示
    for i in range(len(regions)-1):
        ax2.annotate('', xy=(risk_levels[i+1], returns[i+1]), 
                    xytext=(risk_levels[i], returns[i]),
                    arrowprops=dict(arrowstyle='->', lw=2, color='gray', alpha=0.5))
    
    ax2.set_xlabel('リスク（%）', fontsize=14)
    ax2.set_ylabel('期待リターン（%）', fontsize=14)
    ax2.set_title('地域分散による効率性向上', fontsize=14)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(8, 22)
    ax2.set_ylim(4, 8)
    
    plt.suptitle('図12: 分散投資の効果', fontsize=16)
    plt.tight_layout()
    plt.savefig('figures/fig12_diversification_effect.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図13: 新NISA制度の構造図 ==========
def create_fig13():
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # 背景
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # タイトル
    ax.text(5, 9.5, '新NISA制度の全体像', fontsize=20, ha='center', fontweight='bold')
    
    # つみたて投資枠
    tsumitate_box = FancyBboxPatch((0.5, 5), 4, 3, boxstyle="round,pad=0.1", 
                                   facecolor=colors['primary'], alpha=0.7, 
                                   edgecolor='black', linewidth=2)
    ax.add_patch(tsumitate_box)
    ax.text(2.5, 7.5, 'つみたて投資枠', fontsize=16, ha='center', fontweight='bold', color='white')
    ax.text(2.5, 6.8, '年間上限：120万円', fontsize=12, ha='center', color='white')
    ax.text(2.5, 6.3, '対象：投資信託・ETF', fontsize=12, ha='center', color='white')
    ax.text(2.5, 5.8, '特徴：長期積立向け', fontsize=12, ha='center', color='white')
    ax.text(2.5, 5.3, '金融庁認定商品のみ', fontsize=12, ha='center', color='white')
    
    # 成長投資枠
    growth_box = FancyBboxPatch((5.5, 5), 4, 3, boxstyle="round,pad=0.1", 
                               facecolor=colors['secondary'], alpha=0.7, 
                               edgecolor='black', linewidth=2)
    ax.add_patch(growth_box)
    ax.text(7.5, 7.5, '成長投資枠', fontsize=16, ha='center', fontweight='bold', color='white')
    ax.text(7.5, 6.8, '年間上限：240万円', fontsize=12, ha='center', color='white')
    ax.text(7.5, 6.3, '対象：株式・投資信託等', fontsize=12, ha='center', color='white')
    ax.text(7.5, 5.8, '特徴：自由度が高い', fontsize=12, ha='center', color='white')
    ax.text(7.5, 5.3, '個別株投資も可能', fontsize=12, ha='center', color='white')
    
    # 共通事項
    common_box = FancyBboxPatch((2, 1), 6, 3, boxstyle="round,pad=0.1", 
                               facecolor=colors['positive'], alpha=0.3, 
                               edgecolor='black', linewidth=2)
    ax.add_patch(common_box)
    ax.text(5, 3.5, '共通のメリット', fontsize=16, ha='center', fontweight='bold')
    ax.text(5, 2.8, '✓ 運用益が非課税（通常は約20%の税金）', fontsize=12, ha='center')
    ax.text(5, 2.3, '✓ 非課税期間は無期限', fontsize=12, ha='center')
    ax.text(5, 1.8, '✓ 売却後の枠の再利用可能', fontsize=12, ha='center')
    ax.text(5, 1.3, '✓ 生涯投資上限：1,800万円', fontsize=12, ha='center')
    
    # 年間上限
    ax.text(5, 4.5, '年間投資上限：360万円（併用可能）', fontsize=14, 
            ha='center', fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['accent'], alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('figures/fig13_new_nisa_structure.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図14: NISA利用vs通常口座の資産推移比較 ==========
def create_fig14():
    plt.figure(figsize=(14, 8))
    
    years = np.arange(0, 31)
    monthly_investment = 50000  # 月5万円
    annual_return = 0.05  # 年率5%
    tax_rate = 0.2  # 20%の税率
    
    # NISA口座（非課税）
    nisa_balance = []
    nisa_total = 0
    for year in years:
        nisa_total = nisa_total * (1 + annual_return) + monthly_investment * 12
        nisa_balance.append(nisa_total / 10000)  # 万円単位
    
    # 通常口座（課税）
    normal_balance = []
    normal_total = 0
    invested_principal = 0
    for year in years:
        # 利益に対して課税
        profit = normal_total - invested_principal
        if profit > 0:
            tax = profit * annual_return * tax_rate
            normal_total = normal_total * (1 + annual_return) - tax + monthly_investment * 12
        else:
            normal_total = normal_total * (1 + annual_return) + monthly_investment * 12
        invested_principal += monthly_investment * 12
        normal_balance.append(normal_total / 10000)
    
    # 投資元本
    principal = [monthly_investment * 12 * year / 10000 for year in years]
    
        # プロット
    plt.plot(years, nisa_balance, linewidth=3, label='NISA口座（非課税）', color=colors['positive'])
    plt.plot(years, normal_balance, linewidth=3, label='通常口座（課税あり）', color=colors['secondary'])
    plt.plot(years, principal, linewidth=2, label='投資元本', color=colors['neutral'], linestyle='--')
    
    # 差額を塗りつぶし
    plt.fill_between(years, normal_balance, nisa_balance, alpha=0.3, color=colors['accent'])
    
    # 最終的な差額を表示
    final_diff = nisa_balance[-1] - normal_balance[-1]
    plt.annotate(f'30年後の差額\n{final_diff:.0f}万円', 
                xy=(30, (nisa_balance[-1] + normal_balance[-1])/2),
                xytext=(25, (nisa_balance[-1] + normal_balance[-1])/2 + 500),
                arrowprops=dict(arrowstyle='->', color='black', lw=2),
                fontsize=12, ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    plt.xlabel('運用年数', fontsize=14)
    plt.ylabel('資産額（万円）', fontsize=14)
    plt.title('図14: NISA vs 通常口座の資産推移比較\n（月5万円投資、年率5%運用）', fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 30)
    plt.ylim(0, max(nisa_balance) * 1.1)
    
    plt.tight_layout()
    plt.savefig('figures/fig14_nisa_vs_normal.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図15: ライフステージ別NISA配分戦略 ==========
def create_fig15():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # 上段：年齢別の推奨配分
    age_groups = ['20代', '30代', '40代', '50代', '60代']
    tsumitate_ratio = [80, 60, 40, 30, 20]
    growth_ratio = [20, 40, 60, 70, 80]
    
    x = np.arange(len(age_groups))
    width = 0.6
    
    p1 = ax1.bar(x, tsumitate_ratio, width, label='つみたて投資枠', 
                 color=colors['primary'], alpha=0.8)
    p2 = ax1.bar(x, growth_ratio, width, bottom=tsumitate_ratio, 
                 label='成長投資枠', color=colors['secondary'], alpha=0.8)
    
    # パーセンテージを表示
    for i in range(len(age_groups)):
        # つみたて投資枠
        if tsumitate_ratio[i] > 10:
            ax1.text(i, tsumitate_ratio[i]/2, f'{tsumitate_ratio[i]}%', 
                    ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        # 成長投資枠
        if growth_ratio[i] > 10:
            ax1.text(i, tsumitate_ratio[i] + growth_ratio[i]/2, f'{growth_ratio[i]}%', 
                    ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    
    ax1.set_ylabel('配分比率（%）', fontsize=14)
    ax1.set_title('年代別NISA枠の推奨配分', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(age_groups)
    ax1.legend(fontsize=12)
    ax1.set_ylim(0, 100)
    
    # 下段：具体的な金額配分例
    total_annual = 360  # 年間360万円
    ages = ['22歳\n(新入社員)', '30歳\n(結婚)', '40歳\n(子育て)', '50歳\n(教育費)', '60歳\n(退職前)']
    
    # 各年代の投資可能額（実態に合わせて調整）
    possible_amounts = [60, 120, 240, 300, 360]  # 年間投資額（万円）
    tsumitate_amounts = [48, 72, 96, 90, 72]
    growth_amounts = [12, 48, 144, 210, 288]
    
    x2 = np.arange(len(ages))
    
    bars1 = ax2.bar(x2 - width/2, tsumitate_amounts, width/2, 
                    label='つみたて投資枠', color=colors['primary'], alpha=0.8)
    bars2 = ax2.bar(x2, growth_amounts, width/2, 
                    label='成長投資枠', color=colors['secondary'], alpha=0.8)
    
    # 合計額を表示
    for i in range(len(ages)):
        total = tsumitate_amounts[i] + growth_amounts[i]
        ax2.text(i, max(tsumitate_amounts[i], growth_amounts[i]) + 10, 
                f'年間{total}万円', ha='center', fontsize=10)
    
    ax2.set_xlabel('年齢・ライフステージ', fontsize=14)
    ax2.set_ylabel('年間投資額（万円）', fontsize=14)
    ax2.set_title('ライフステージ別の具体的な投資額例', fontsize=14)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(ages)
    ax2.legend(fontsize=12)
    ax2.set_ylim(0, 350)
    
    plt.suptitle('図15: ライフステージ別NISA活用戦略', fontsize=16)
    plt.tight_layout()
    plt.savefig('figures/fig15_nisa_lifecycle_strategy.png', dpi=300, bbox_inches='tight')
    plt.close()

# メイン実行部
if __name__ == "__main__":
    print("Part 2の図表生成を開始します...")
    
    create_fig10()
    print("図10: 単利vs複利の成長曲線 - 完了")
    
    create_fig11()
    print("図11: 主要投資商品のリスク・リターンマップ - 完了")
    
    create_fig12()
    print("図12: 分散投資によるリスク低減効果 - 完了")
    
    create_fig13()
    print("図13: 新NISA制度の構造図 - 完了")
    
    create_fig14()
    print("図14: NISA利用vs通常口座の資産推移比較 - 完了")
    
    create_fig15()
    print("図15: ライフステージ別NISA配分戦略 - 完了")
    
    print("\nPart 2（図10-15）の生成が完了しました！")