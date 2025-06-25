# visualization_part3.py
# シミュレーション、リスク管理、実践編の図表（図16-27）

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle, Circle
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch

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

# ========== 図16: 標準シナリオの資産推移グラフ ==========
def create_fig16():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), height_ratios=[3, 1])

    # 年齢と年数の設定
    ages = np.arange(22, 66)
    years = ages - 22

    # 収入の推移（標準パス）
    income = []
    for age in ages:
        if age < 25:
            annual_income = 344
        elif age < 28:
            annual_income = 390
        elif age < 31:
            annual_income = 430
        elif age < 35:
            annual_income = 480
        elif age < 39:
            annual_income = 520
        elif age < 44:
            annual_income = 590
        elif age < 50:
            annual_income = 700
        elif age < 57:
            annual_income = 800
        else:
            annual_income = 900
        income.append(annual_income)

    # 投資額の計算（手取りの20%）
    monthly_investment = [inc * 0.75 * 0.2 / 12 for inc in income]  # 手取り75%の20%

    # 資産推移の計算
    asset_balance = []
    principal = []
    total_asset = 0
    total_principal = 0

    for i, monthly in enumerate(monthly_investment):
        total_asset = total_asset * 1.05 + monthly * 12  # 年率5%
        total_principal += monthly * 12
        asset_balance.append(total_asset / 10000)  # 万円単位
        principal.append(total_principal / 10000)

    # ライフイベント
    life_events = {
        30: '結婚',
        32: '第一子誕生',
        35: '第二子誕生',
        40: 'マイホーム購入',
        50: '子供の大学入学',
        65: 'リタイア'
    }

    # 上段：資産推移
    ax1.fill_between(ages, 0, principal, alpha=0.5, color=colors['neutral'], label='投資元本')
    ax1.fill_between(ages, principal, asset_balance, alpha=0.5, color=colors['positive'], label='運用益')
    ax1.plot(ages, asset_balance, linewidth=3, color=colors['primary'], label='総資産')

    # ライフイベントをマーク
    for age, event in life_events.items():
        if 22 <= age <= 65:
            idx = age - 22
            if idx < len(asset_balance):
                y_position = asset_balance[idx]
                ax1.axvline(x=age, color='gray', linestyle='--', alpha=0.5)
                ax1.text(age, y_position + max(asset_balance) * 0.05, event, rotation=45,
                        ha='left', fontsize=9)

    # マイルストーン
    milestones = [1000, 3000, 5000, 10000]
    achieved_milestones = set()
    for milestone in milestones:
        for i, balance in enumerate(asset_balance):
            if balance >= milestone and milestone not in achieved_milestones:
                achievement_age = ages[i]
                ax1.plot(achievement_age, milestone, 'o', markersize=10,
                        color=colors['accent'], zorder=5) # zorderで点を前面に
                ax1.text(achievement_age + 0.5, milestone, f'{milestone}万円達成',
                        fontsize=9, va='center')
                achieved_milestones.add(milestone)
                break # 達成したら次のマイルストーンへ

    ax1.set_ylabel('資産額（万円）', fontsize=14)
    ax1.set_title('標準シナリオでの資産推移（手取りの20%を年率5%で運用）', fontsize=14)
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(22, 65)

    if len(asset_balance) > 0:
        ax1.set_ylim(0, max(asset_balance) * 1.1)
    else:
        ax1.set_ylim(0, 15000)

    # 下段：年間投資額の推移
    annual_investment = [m * 12 for m in monthly_investment]
    ax2.bar(ages, annual_investment, color=colors['primary'], alpha=0.7)
    ax2.set_xlabel('年齢', fontsize=14)
    ax2.set_ylabel('年間投資額（万円）', fontsize=12)
    ax2.set_title('年間投資額の推移', fontsize=12)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_xlim(22, 65)

    plt.suptitle('図16: あなたの資産形成ストーリー', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96]) # suptitleとの重なりを調整

    # 原因3の対策：保存先をカレントディレクトリに変更
    plt.savefig('figures/fig16_standard_scenario.png', dpi=300, bbox_inches='tight')
    
    # 原因1の対策：表示する場合はこの行をコメントアウトする
    # plt.close()


# ========== 図17: 年齢別資産構成の推移 ==========
def create_fig17():
    plt.figure(figsize=(14, 8))
    
    ages = np.arange(22, 66, 2)  # 2歳刻み
    
    # 年齢に応じた資産配分
    stock_ratio = []
    bond_ratio = []
    cash_ratio = []
    
    for age in ages:
        if age < 30:
            stock = 80
            bond = 15
            cash = 5
        elif age < 40:
            stock = 70
            bond = 20
            cash = 10
        elif age < 50:
            stock = 60
            bond = 30
            cash = 10
        elif age < 60:
            stock = 50
            bond = 35
            cash = 15
        else:
            stock = 40
            bond = 40
            cash = 20
        
        stock_ratio.append(stock)
        bond_ratio.append(bond)
        cash_ratio.append(cash)
    
    # 積み上げ面グラフ
    plt.fill_between(ages, 0, cash_ratio, alpha=0.7, color=colors['neutral'], label='現金・預金')
    plt.fill_between(ages, cash_ratio, np.array(cash_ratio) + np.array(bond_ratio), 
                     alpha=0.7, color=colors['secondary'], label='債券')
    plt.fill_between(ages, np.array(cash_ratio) + np.array(bond_ratio), 100, 
                     alpha=0.7, color=colors['primary'], label='株式')
    
        # リバランスポイント
    rebalance_ages = [30, 40, 50, 60]
    for age in rebalance_ages:
        plt.axvline(x=age, color='red', linestyle='--', alpha=0.7, linewidth=2)
        plt.text(age, 102, 'リバランス', rotation=0, ha='center', fontsize=9)
    
    plt.xlabel('年齢', fontsize=14)
    plt.ylabel('資産配分（%）', fontsize=14)
    plt.title('図17: 年齢に応じた資産配分の推移', fontsize=16, pad=20)
    plt.legend(fontsize=12, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True, alpha=0.3, axis='y')
    plt.xlim(22, 65)
    plt.ylim(0, 105)
    
    # 配分の説明を追加
    plt.text(26, 50, '20代\n積極運用', ha='center', fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    plt.text(35, 50, '30代\nバランス重視', ha='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    plt.text(45, 50, '40代\n安定性向上', ha='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    plt.text(55, 50, '50代\nリスク抑制', ha='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('figures/fig17_age_asset_allocation.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図18: 3つのシナリオの比較チャート ==========
def create_fig18():
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    ages = np.arange(22, 66)
    
    # 3つのシナリオ設定
    scenarios = {
        '保守的': {'monthly': 30000, 'return': 0.03, 'color': colors['secondary']},
        '標準': {'monthly': 50000, 'return': 0.05, 'color': colors['primary']},
        '積極的': {'monthly': 70000, 'return': 0.07, 'color': colors['positive']}
    }
    
    # 各シナリオの計算
    results = {}
    for name, params in scenarios.items():
        balance = []
        total = 0
        for year in range(len(ages)):
            total = total * (1 + params['return']) + params['monthly'] * 12
            balance.append(total / 10000)
        results[name] = balance
    
    # 左上：資産推移の比較
    ax1 = axes[0, 0]
    for name, balance in results.items():
        ax1.plot(ages, balance, linewidth=3, label=name, color=scenarios[name]['color'])
    
    ax1.set_xlabel('年齢', fontsize=12)
    ax1.set_ylabel('資産額（万円）', fontsize=12)
    ax1.set_title('資産推移の比較', fontsize=14)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # 右上：65歳時点の資産額
    ax2 = axes[0, 1]
    final_values = [results[name][-1] for name in scenarios.keys()]
    bars = ax2.bar(scenarios.keys(), final_values, 
                   color=[scenarios[name]['color'] for name in scenarios.keys()], alpha=0.7)
    
    for bar, value in zip(bars, final_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                f'{value:.0f}万円', ha='center', fontsize=11)
    
    ax2.set_ylabel('資産額（万円）', fontsize=12)
    ax2.set_title('65歳時点の資産額', fontsize=14)
    ax2.set_ylim(0, max(final_values) * 1.2)
    
    # 左下：月間投資額と必要な手取り
    ax3 = axes[1, 0]
    monthly_amounts = [s['monthly']/10000 for s in scenarios.values()]
    required_income = [s['monthly']/0.2/0.75 for s in scenarios.values()]  # 手取りの20%として逆算
    
    x = np.arange(len(scenarios))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, monthly_amounts, width, label='月間投資額', 
                    color=colors['primary'], alpha=0.7)
    bars2 = ax3.bar(x + width/2, [r/10000 for r in required_income], width, 
                    label='必要な月収（額面）', color=colors['accent'], alpha=0.7)
    
    ax3.set_ylabel('金額（万円）', fontsize=12)
    ax3.set_title('必要投資額と収入の関係', fontsize=14)
    ax3.set_xticks(x)
    ax3.set_xticklabels(scenarios.keys())
    ax3.legend(fontsize=11)
    
    # 右下：投資総額vs最終資産
    ax4 = axes[1, 1]
    total_invested = [s['monthly'] * 12 * 43 / 10000 for s in scenarios.values()]
    
    # 積み上げ棒グラフ
    bars1 = ax4.bar(scenarios.keys(), total_invested, label='投資元本', 
                   color=colors['neutral'], alpha=0.7)
    bars2 = ax4.bar(scenarios.keys(), [final_values[i] - total_invested[i] for i in range(3)], 
                   bottom=total_invested, label='運用益', color=colors['positive'], alpha=0.7)
    
    ax4.set_ylabel('金額（万円）', fontsize=12)
    ax4.set_title('投資元本と運用益の内訳', fontsize=14)
    ax4.legend(fontsize=11)
    
    plt.suptitle('図18: 3つのシナリオの詳細比較', fontsize=16)
    plt.tight_layout()
    plt.savefig('figures/fig18_scenario_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図19: 変数別の感度分析ヒートマップ ==========
def create_fig19():
    plt.figure(figsize=(12, 10))
    
    # パラメータ設定
    monthly_amounts = np.arange(3, 8) * 10000  # 3-7万円
    annual_returns = np.arange(3, 8) / 100  # 3-7%
    
    # 65歳時点の資産額を計算（43年間）
    final_assets = np.zeros((len(annual_returns), len(monthly_amounts)))
    
    for i, return_rate in enumerate(annual_returns):
        for j, monthly in enumerate(monthly_amounts):
            total = 0
            for year in range(43):
                total = total * (1 + return_rate) + monthly * 12
            final_assets[i, j] = total / 10000000  # 億円単位
    
    # ヒートマップ
    sns.heatmap(final_assets, 
                xticklabels=[f'{m/10000:.0f}万円' for m in monthly_amounts],
                yticklabels=[f'{r*100:.0f}%' for r in annual_returns],
                annot=True, fmt='.2f', cmap='YlOrRd', 
                cbar_kws={'label': '資産額（億円）'})
    
    plt.xlabel('月間投資額', fontsize=14)
    plt.ylabel('年間リターン', fontsize=14)
    plt.title('図19: 投資額×リターンによる65歳時点の資産額\n（22歳から43年間投資）', fontsize=16, pad=20)
    
    # 目標ゾーンを囲む
    rect = Rectangle((1.5, 1.5), 2, 2, linewidth=3, edgecolor=colors['positive'], 
                    facecolor='none')
    plt.gca().add_patch(rect)
    plt.text(2.5, 2.5, '推奨\nゾーン', ha='center', va='center', 
            fontsize=12, fontweight='bold', color=colors['positive'])
    
    plt.tight_layout()
    plt.savefig('figures/fig19_sensitivity_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図20: 過去の暴落と回復パターン ==========
def create_fig20():
    # カラー定義（colors変数が未定義の場合）
    colors = {
        'primary': '#2E86AB',
        'secondary': '#A23B72',
        'positive': '#2ECC71',
        'negative': '#E74C3C',
        'neutral': '#95A5A6'
    }
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # リーマンショックのシミュレーション
    ax1 = axes[0, 0]
    months = np.arange(0, 60)  # 5年間
    
    # 市場の動き（簡略化）
    market = np.ones(60) * 100
    market[12:24] = 100 * np.exp(-0.5 * (np.arange(12) / 12))  # 暴落
    market[24:48] = market[23] * np.exp(0.3 * (np.arange(24) / 24))  # 回復
    market[48:] = market[47] * 1.05 ** (np.arange(12) / 12)  # 通常成長
    
    ax1.plot(months, market, linewidth=2, color=colors['primary'], label='市場価格')
    ax1.axhspan(50, 100, alpha=0.2, color=colors['negative'])
    ax1.text(18, 70, 'リーマンショック\n最大50%下落', ha='center', fontsize=10)
    ax1.set_xlabel('経過月数', fontsize=12)
    ax1.set_ylabel('指数（開始時=100）', fontsize=12)
    ax1.set_title('リーマンショック時の市場動向', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 積立投資 vs 一括投資
    ax2 = axes[0, 1]
    
    # 一括投資（開始時に1200万円）
    lump_sum = 1200 * market / 100
    
    # 積立投資（月20万円）
    dollar_cost = []
    units = 0
    for i, price in enumerate(market):
        units += 20 / price * 100  # 20万円分購入
        dollar_cost.append(units * price / 100)
    
    dollar_cost = np.array(dollar_cost)
    
    ax2.plot(months, lump_sum, linewidth=2, label='一括投資', color=colors['negative'])
    ax2.plot(months, dollar_cost, linewidth=2, label='積立投資', color=colors['positive'])
    ax2.set_xlabel('経過月数', fontsize=12)
    ax2.set_ylabel('資産額（万円）', fontsize=12)
    ax2.set_title('投資方法による資産推移の違い', fontsize=14)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # 各危機の下落率と回復期間
    ax3 = axes[1, 0]
    crises = ['ITバブル\n(2000)', 'リーマン\n(2008)', 'コロナ\n(2020)']
    max_drawdown = [-45, -50, -35]
    recovery_months = [84, 24, 6]
    
    x = np.arange(len(crises))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, max_drawdown, width, label='最大下落率(%)', 
                    color=colors['negative'], alpha=0.7)
    
    ax3_twin = ax3.twinx()
    bars2 = ax3_twin.bar(x + width/2, recovery_months, width, label='回復期間(月)', 
                        color=colors['primary'], alpha=0.7)
    
    ax3.set_ylabel('最大下落率（%）', fontsize=12)
    ax3_twin.set_ylabel('回復期間（月）', fontsize=12)
    ax3.set_title('過去の主要な市場危機', fontsize=14)
    ax3.set_xticks(x)
    ax3.set_xticklabels(crises)
    ax3.legend(loc='lower left', fontsize=10)
    ax3_twin.legend(loc='lower right', fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # 継続投資の効果
    ax4 = axes[1, 1]
    
    # 暴落時に投資を止めた場合vs継続した場合
    stop_investing = []
    continue_investing = []
    
    for i in range(60):
        if i < 12:  # 暴落前
            stop_investing.append(i * 20)
            continue_investing.append(i * 20)
        elif i < 24:  # 暴落中（止めた場合は投資停止）
            if i == 12:
                stop_investing.append(stop_investing[-1] * market[i] / market[i-1])
                continue_investing.append(continue_investing[-1] * market[i] / market[i-1] + 20)
            else:
                stop_investing.append(stop_investing[-1] * market[i] / market[i-1])
                continue_investing.append(continue_investing[-1] * market[i] / market[i-1] + 20)
        else:  # 回復後
            stop_investing.append(stop_investing[-1] * market[i] / market[i-1])
            continue_investing.append(continue_investing[-1] * market[i] / market[i-1] + 20)
    
    stop_investing = np.array(stop_investing)
    continue_investing = np.array(continue_investing)
    
    ax4.plot(months, stop_investing, linewidth=2, label='暴落時に投資停止', 
            color=colors['negative'])
    ax4.plot(months, continue_investing, linewidth=2, label='投資継続', 
            color=colors['positive'])
    
    final_diff = continue_investing[-1] - stop_investing[-1]
    ax4.text(50, (continue_investing[-1] + stop_investing[-1])/2, 
            f'差額\n{final_diff:.0f}万円', ha='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
    ax4.set_xlabel('経過月数', fontsize=12)
    ax4.set_ylabel('資産額（万円）', fontsize=12)    
    ax4.set_title('投資継続 vs 投資停止の比較', fontsize=14)
    ax4.legend(fontsize=11)
    ax4.grid(True, alpha=0.3)

    # plt.sutitle → plt.suptitle に修正
    plt.suptitle('図20: 市場暴落への対処法', fontsize=16, y=0.98)
    plt.tight_layout()
    
    # ディレクトリが存在しない場合は作成
    import os
    os.makedirs('figures', exist_ok=True)
    
    plt.savefig('figures/fig20_market_crash_patterns.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図21: 年齢別推奨アセットアロケーション ==========
def create_fig21():
    fig = plt.figure(figsize=(16, 10))
    
    # レーダーチャート用の設定
    categories = ['国内株式', '先進国株式', '新興国株式', '国内債券', '先進国債券', '現金・預金']
    
    # 年代別の配分（%）
    allocations = {
        '20代': [20, 40, 20, 5, 10, 5],
        '30代': [20, 35, 15, 10, 10, 10],
        '40代': [20, 30, 10, 15, 15, 10],
        '50代': [15, 25, 10, 20, 15, 15],
        '60代': [10, 20, 10, 25, 15, 20]
    }
    
    # サブプロットの配置
    positions = [(0, 0), (0, 1), (0, 2), (1, 0.5), (1, 1.5)]
    
    for idx, (age, allocation) in enumerate(allocations.items()):
        ax = plt.subplot(2, 3, idx + 1, projection='polar')
        
        # データの準備
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        allocation += allocation[:1]  # 閉じるため
        angles += angles[:1]
        
        # プロット
        ax.plot(angles, allocation, 'o-', linewidth=2, color=colors['primary'])
        ax.fill(angles, allocation, alpha=0.3, color=colors['primary'])
        
        # 軸の設定
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=9)
        ax.set_ylim(0, 45)
        ax.set_yticks([10, 20, 30, 40])
        ax.set_yticklabels(['10%', '20%', '30%', '40%'], size=8)
        ax.set_title(f'{age}', fontsize=14, pad=20)
        
        # グリッド
        ax.grid(True)
    
    # 全体のタイトル
    plt.suptitle('図21: 年齢別推奨アセットアロケーション', fontsize=16)
    
    # 凡例用の説明
    fig.text(0.5, 0.02, '※ 各年代でリスク許容度に応じて株式比率を調整', 
             ha='center', fontsize=11, style='italic')
    
    plt.tight_layout()
    plt.savefig('figures/fig21_age_asset_allocation_radar.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図22: 最悪シナリオでの資産推移 ==========
def create_fig22():
    plt.figure(figsize=(14, 8))
    
    years = np.arange(0, 44)  # 22歳から65歳まで
    
    # 通常シナリオ（年率5%）
    normal_scenario = []
    normal_total = 0
    
    # 最悪シナリオ（最初の10年間マイナス成長）
    worst_scenario = []
    worst_total = 0
    
    monthly_investment = 50000  # 月5万円
    
    for year in years:
        # 通常シナリオ
        normal_total = normal_total * 1.05 + monthly_investment * 12
        normal_scenario.append(normal_total / 10000)
        
        # 最悪シナリオ
        if year < 10:
            # 最初の10年間は年率-2%
            worst_total = worst_total * 0.98 + monthly_investment * 12
        else:
            # その後は年率7%で回復
            worst_total = worst_total * 1.07 + monthly_investment * 12
        worst_scenario.append(worst_total / 10000)
    
    # 投資元本
    principal = [monthly_investment * 12 * year / 10000 for year in years]
    
    # プロット
    plt.plot(22 + years, normal_scenario, linewidth=3, label='通常シナリオ（年率5%）', 
             color=colors['primary'])
    plt.plot(22 + years, worst_scenario, linewidth=3, label='最悪シナリオ（10年間マイナス後回復）', 
             color=colors['negative'], linestyle='--')
    plt.plot(22 + years, principal, linewidth=2, label='投資元本', 
             color=colors['neutral'], linestyle=':')
    
    # 危機期間を塗りつぶし
    plt.axvspan(22, 32, alpha=0.2, color=colors['negative'])
    plt.text(27, 1000, '低迷期\n10年間', ha='center', fontsize=11,
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # 最終値を表示
    plt.text(65, normal_scenario[-1], f'{normal_scenario[-1]:.0f}万円', 
             ha='left', va='bottom', fontsize=11)
    plt.text(65, worst_scenario[-1], f'{worst_scenario[-1]:.0f}万円', 
             ha='left', va='top', fontsize=11)
    
    plt.xlabel('年齢', fontsize=14)
    plt.ylabel('資産額（万円）', fontsize=14)
    plt.title('図22: 最悪シナリオでも継続投資の効果は大きい', fontsize=16, pad=20)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(22, 67)
    plt.ylim(0, max(normal_scenario) * 1.1)
    
    plt.tight_layout()
    plt.savefig('figures/fig22_worst_case_scenario.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図23: 最初の1年間のロードマップ ==========
def create_fig23():
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # 月別タスク
    months = ['4月\n入社', '5月', '6月', '7月', '8月', '9月', 
              '10月', '11月', '12月', '1月', '2月', '3月']
    
    tasks = {
        '口座開設': {'start': 0, 'duration': 1, 'color': colors['primary']},
        'NISA申請': {'start': 0.5, 'duration': 1, 'color': colors['primary']},
        '投資開始': {'start': 1, 'duration': 11, 'color': colors['positive']},
        '知識習得': {'start': 0, 'duration': 12, 'color': colors['secondary']},
        '家計管理': {'start': 0, 'duration': 12, 'color': colors['neutral']},
        '初回見直し': {'start': 3, 'duration': 0.5, 'color': colors['accent']},
        '半年見直し': {'start': 6, 'duration': 0.5, 'color': colors['accent']},
        '年度末評価': {'start': 11, 'duration': 1, 'color': colors['accent']},
    }
    
    # ガントチャート
    y_pos = 0
    for task, info in tasks.items():
        ax.barh(y_pos, info['duration'], left=info['start'], height=0.5,
                color=info['color'], alpha=0.7, edgecolor='black')
        ax.text(-0.5, y_pos, task, ha='right', va='center', fontsize=11)
        y_pos += 1
    
    # マイルストーン
    milestones = {
        1: '投資スタート',
        3: '初回評価',
        6: '半期評価',
        11: '年度評価'
    }
    
    for month, milestone in milestones.items():
        ax.axvline(x=month, color='red', linestyle='--', alpha=0.5)
        ax.text(month, len(tasks) + 0.5, milestone, rotation=45, 
                ha='left', fontsize=9)
    
    # 月別の目標金額
    ax2 = ax.twinx()
    cumulative_investment = [i * 3 for i in range(12)]  # 月3万円
    ax2.plot(range(12), cumulative_investment, 'o-', color=colors['positive'], 
             linewidth=2, markersize=8)
    ax2.set_ylabel('累計投資額（万円）', fontsize=12)
    ax2.set_ylim(0, 40)
    
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-0.5, len(tasks))
    ax.set_xticks(range(12))
    ax.set_xticklabels(months)
    ax.set_yticks([])
    ax.set_xlabel('月', fontsize=14)
    ax.set_title('図23: 新入社員1年目の資産形成ロードマップ', fontsize=16, pad=20)
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('figures/fig23_first_year_roadmap.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図24: 初心者向け投資信託の比較表 ==========
def create_fig24():
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # 投資信託データ
    funds = {
        'eMAXIS Slim\n全世界株式': {
            'expense': 0.1133, 'size': 3000, 'return': 15.2, 
            'risk': 18, 'rating': 5
        },
        'eMAXIS Slim\n米国株式': {
            'expense': 0.0968, 'size': 2500, 'return': 18.5, 
            'risk': 20, 'rating': 5
        },
        'eMAXIS Slim\nバランス': {
            'expense': 0.154, 'size': 1500, 'return': 10.3, 
            'risk': 12, 'rating': 4
        },
        '楽天VT': {
            'expense': 0.192, 'size': 2000, 'return': 14.8, 
            'risk': 17, 'rating': 4
        },
        'SBI・V・S&P500': {
            'expense': 0.0938, 'size': 1800, 'return': 19.2, 
            'risk': 21, 'rating': 5
        }
    }
    
    # バブルチャート
    for i, (name, data) in enumerate(funds.items()):
        # バブルのサイズは純資産総額に比例
        size = data['size'] / 10
        
        # 色は評価に応じて
        if data['rating'] == 5:
            color = colors['positive']
        elif data['rating'] == 4:
            color = colors['primary']
        else:
            color = colors['neutral']
        
        ax.scatter(data['risk'], data['return'], s=size, alpha=0.6, 
                  color=color, edgecolors='black', linewidth=2)
        
        # ラベル
        ax.annotate(f"{name}\n信託報酬:{data['expense']:.3f}%", 
                   (data['risk'], data['return']), 
                   xytext=(0, -40), textcoords='offset points', 
                   ha='center', fontsize=9,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.7))
    
    # 推奨ゾーン
    rect = Rectangle((10, 8), 12, 8, linewidth=3, edgecolor=colors['positive'], 
                    facecolor=colors['positive'], alpha=0.1)
    ax.add_patch(rect)
    ax.text(16, 12, '初心者\n推奨ゾーン', ha='center', va='center', 
            fontsize=14, fontweight='bold', color=colors['positive'])
    
    ax.set_xlabel('リスク（標準偏差 %）', fontsize=14)
    ax.set_ylabel('過去3年リターン（%）', fontsize=14)
    ax.set_title('図24: 初心者向け主要投資信託の比較', fontsize=16, pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(8, 24)
    ax.set_ylim(5, 22)
    
    # 凡例
    legend_elements = [
        plt.scatter([], [], s=100, color=colors['positive'], alpha=0.6, label='評価★5'),
        plt.scatter([], [], s=100, color=colors['primary'], alpha=0.6, label='評価★4'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
                   markersize=15, label='バブルサイズ=純資産額')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('figures/fig24_fund_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図25: 自動化システムの構築図 ==========
def create_fig25():
    fig, ax = plt.subplots(figsize=(14, 10))
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # フローチャートの要素
    # 給与振込
    salary_box = FancyBboxPatch((1, 8), 2, 1, boxstyle="round,pad=0.1",
                               facecolor=colors['primary'], alpha=0.7)
    ax.add_patch(salary_box)
    ax.text(2, 8.5, '給与振込\n（25日）', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='white')
    
    # 自動振替1（生活費）
    living_box = FancyBboxPatch((0.5, 5.5), 2, 1, boxstyle="round,pad=0.1",
                               facecolor=colors['neutral'], alpha=0.7)
    ax.add_patch(living_box)
    ax.text(1.5, 6, '生活費口座\n自動振替', ha='center', va='center', 
            fontsize=11, color='white')
    
    # 自動振替2（投資）
    invest_box = FancyBboxPatch((3, 5.5), 2, 1, boxstyle="round,pad=0.1",
                               facecolor=colors['positive'], alpha=0.7)
    ax.add_patch(invest_box)
    ax.text(4, 6, '証券口座\n自動振替', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # NISA自動積立
    nisa_box = FancyBboxPatch((3, 3), 2, 1, boxstyle="round,pad=0.1",
                             facecolor=colors['secondary'], alpha=0.7)
    ax.add_patch(nisa_box)
    ax.text(4, 3.5, 'NISA\n自動積立', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # 投資実行
    execute_box = FancyBboxPatch((3, 0.5), 2, 1, boxstyle="round,pad=0.1",
                                facecolor=colors['accent'], alpha=0.7)
    ax.add_patch(execute_box)
    ax.text(4, 1, '投資信託\n購入完了', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    
    # 矢印
    arrows = [
        ((2, 8), (1.5, 6.5)),  # 給与→生活費
        ((2, 8), (4, 6.5)),    # 給与→投資
        ((4, 5.5), (4, 4)),    # 投資口座→NISA
        ((4, 3), (4, 1.5))     # NISA→購入
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=3, color='black'))
    
    # 金額表示
    ax.text(0.5, 7.2, '17.6万円', fontsize=10, ha='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))
    ax.text(5, 7.2, '4.4万円', fontsize=10, ha='center',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white'))
    
    # タイミング表示
    timing_box = FancyBboxPatch((6, 5), 3, 4, boxstyle="round,pad=0.1",
                               facecolor='lightgray', alpha=0.3)
    ax.add_patch(timing_box)
    ax.text(7.5, 8, '自動化タイミング', fontsize=12, ha='center', fontweight='bold')
    ax.text(7.5, 7.2, '25日: 給与振込', fontsize=10, ha='center')
    ax.text(7.5, 6.6, '26日: 自動振替', fontsize=10, ha='center')
    ax.text(7.5, 6, '27日: NISA積立設定', fontsize=10, ha='center')
    ax.text(7.5, 5.4, '月初: 投資信託購入', fontsize=10, ha='center')
    
    ax.set_title('図25: 給与から投資まで完全自動化システム', fontsize=16, pad=20)
    
    plt.tight_layout()
    plt.savefig('figures/fig25_automation_system.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図26: 65歳時点でのライフスタイル比較 ==========
def create_fig26():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # 左側：資産額による可能な生活レベル
    lifestyles = ['最低限の生活', '標準的な生活', 'ゆとりある生活', '豊かな生活']
    required_assets = [2000, 4000, 6000, 10000]  # 万円
    
    # 3つのシナリオでの到達資産
    scenarios = {
        '貯金のみ': 1500,
        '保守的投資': 3000,
        '標準投資': 8500,
        '積極的投資': 18000
    }
    
    # 生活レベルのバー
    bars = ax1.barh(lifestyles, required_assets, color=colors['neutral'], alpha=0.3)
    
    # 各シナリオの到達点
    for i, (name, amount) in enumerate(scenarios.items()):
        y_pos = amount / 2500  # スケーリング
        if y_pos > 3.5:
            y_pos = 3.5
        ax1.scatter(amount, y_pos, s=200, label=name, zorder=5)
        ax1.text(amount, y_pos - 0.3, f'{amount:,}万円', ha='center', fontsize=9)
    
    ax1.set_xlabel('必要資産額（万円）', fontsize=14)
    ax1.set_title('実現可能な生活レベル', fontsize=14)
    ax1.legend(loc='lower right', fontsize=10)
    ax1.set_xlim(0, 12000)
    
    # 右側：具体的な生活イメージ
    ax2.axis('off')
    
    # 標準投資（8,500万円）で実現できること
    y_positions = [0.9, 0.75, 0.6, 0.45, 0.3, 0.15]
    items = [
        '✓ 年金+月20万円の取り崩し',
        '✓ 年2回の海外旅行',
        '✓ 趣味や習い事を自由に',
        '✓ 孫への教育資金援助',
        '✓ 高級老人ホームも選択可',
        '✓ 相続で次世代に資産を残せる'
    ]
    
    ax2.text(0.5, 0.95, '標準投資で実現できる老後', fontsize=16, 
            ha='center', fontweight='bold', transform=ax2.transAxes)
    
    for y, item in zip(y_positions, items):
        ax2.text(0.1, y, item, fontsize=12, transform=ax2.transAxes)
    
    # 貯金のみの場合
    ax2.text(0.5, 0.5, 'vs', fontsize=20, ha='center', transform=ax2.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['accent'], alpha=0.7))
    
    y_positions2 = [0.35, 0.25, 0.15, 0.05]
    items2 = [
        '✗ 年金だけでは生活費不足',
        '✗ 医療費の増加に不安',
        '✗ 趣味や旅行は我慢',
        '✗ 子供に頼る可能性'
    ]
    
    ax2.text(0.5, 0.4, '貯金のみの老後', fontsize=16, 
            ha='center', fontweight='bold', transform=ax2.transAxes,
            color=colors['negative'])
    
    for y, item in zip(y_positions2, items2):
        ax2.text(0.1, y, item, fontsize=12, transform=ax2.transAxes,
                color=colors['negative'])
    
    plt.suptitle('図26: 投資の有無で変わる65歳以降の人生', fontsize=18)
    plt.tight_layout()
    plt.savefig('figures/fig26_retirement_lifestyle.png', dpi=300, bbox_inches='tight')
    plt.close()

# ========== 図27: 資産形成成功者の共通要素 ==========
def create_fig27():
    fig, ax = plt.subplots(figsize=(14, 10))
    
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axis('off')
    
    # 中心：成功
    center = Circle((0, 0), 2, facecolor=colors['positive'], alpha=0.8)
    ax.add_patch(center)
    ax.text(0, 0, '資産形成\n成功', ha='center', va='center', 
            fontsize=16, fontweight='bold', color='white')
    
    # 5つの要素
    elements = [
        {'name': '早期開始', 'angle': 0, 'detail': '20代から\nスタート'},
        {'name': '継続性', 'angle': 72, 'detail': '市場変動に\n動じない'},
        {'name': '知識', 'angle': 144, 'detail': '基礎を\n理解'},
        {'name': 'シンプル', 'angle': 216, 'detail': 'インデックス\n投資'},
        {'name': '長期視点', 'angle': 288, 'detail': '10年以上の\n投資期間'}
    ]
    
    for elem in elements:
        # 角度をラジアンに変換
        angle_rad = np.radians(elem['angle'])
        x = 5 * np.cos(angle_rad)
        y = 5 * np.sin(angle_rad)
        
        # 要素の円
        elem_circle = Circle((x, y), 1.5, facecolor=colors['primary'], alpha=0.7)
        ax.add_patch(elem_circle)
        ax.text(x, y + 0.3, elem['name'], ha='center', va='center', 
                fontsize=12, fontweight='bold', color='white')
        ax.text(x, y - 0.3, elem['detail'], ha='center', va='center', 
                fontsize=9, color='white')
        
        # 中心への矢印
        ax.annotate('', xy=(x * 0.4, y * 0.4), xytext=(x * 0.65, y * 0.65),
                   arrowprops=dict(arrowstyle='->', lw=2, color='gray'))
    
    # 現在地マーカー
    your_position = Circle((-3, -6), 0.5, facecolor=colors['accent'], alpha=0.8)
    ax.add_patch(your_position)
    ax.text(-3, -7, 'あなたは\nここ！', ha='center', va='top', fontsize=11,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # スタートへの矢印
    ax.annotate('', xy=(4, 0), xytext=(-2.5, -5.5),
               arrowprops=dict(arrowstyle='->', lw=3, color=colors['accent'],
                             connectionstyle="arc3,rad=0.3"))
    ax.text(-0.5, -3, '第一歩は\n「早期開始」', ha='center', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=colors['accent'], alpha=0.3))
    
    ax.set_title('図27: 資産形成成功への5つの要素', fontsize=18, pad=20)
    
    plt.tight_layout()
    plt.savefig('figures/fig27_success_factors.png', dpi=300, bbox_inches='tight')
    plt.close()

# メイン実行部
if __name__ == "__main__":
    print("Part 3の図表生成を開始します...")
    
    create_fig16()
    print("図16: 標準シナリオの資産推移グラフ - 完了")
    
    create_fig17()
    print("図17: 年齢別資産構成の推移 - 完了")
    
    create_fig18()
    print("図18: 3つのシナリオの比較チャート - 完了")
    
    create_fig19()
    print("図19: 変数別の感度分析ヒートマップ - 完了")
    
    create_fig20()
    print("図20: 過去の暴落と回復パターン - 完了")
    
    create_fig21()
    print("図21: 年齢別推奨アセットアロケーション - 完了")
    
    create_fig22()
    print("図22: 最悪シナリオでの資産推移 - 完了")
    
    create_fig23()
    print("図23: 最初の1年間のロードマップ - 完了")
    
    create_fig24()
    print("図24: 初心者向け投資信託の比較表 - 完了")
    
    create_fig25()
    print("図25: 自動化システムの構築図 - 完了")
    
    create_fig26()
    print("図26: 65歳時点でのライフスタイル比較 - 完了")
    
    create_fig27()
    print("図27: 資産形成成功者の共通要素 - 完了")
    
    print("\nPart 3（図16-27）の生成が完了しました！")
    print("\n全27図の生成が完了しました！")