#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
板块罗盘 - 主力资金流向分析工具
基于 AKShare 数据源

运行方式:
    python sector_compass.py

输出：符合筛选条件的板块列表，最多3个
"""

import akshare as ak
import pandas as pd
from datetime import datetime

def get_sector_data(period="5日"):
    """
    获取板块资金流向数据
    period: "今日", "3日", "5日", "10日"
    """
    try:
        df = ak.stock_sector_fund_flow_rank(indicator=period)
        return df
    except Exception as e:
        print(f"获取{period}数据失败: {e}")
        return None

def analyze_sectors():
    """
    分析板块数据，筛选符合条件的板块
    """
    print("=" * 60)
    print("🧭 板块罗盘 - 主力资金流向分析")
    print(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 获取不同周期的数据
    print("\n📊 正在获取板块数据...")
    
    df_5d = get_sector_data("5日")
    df_10d = get_sector_data("10日")
    
    if df_5d is None or df_10d is None:
        print("❌ 数据获取失败，请检查网络连接")
        return
    
    # 计算排名（百分位）
    total_sectors = len(df_5d)
    df_5d['5日排名'] = df_5d['5日涨跌幅'].rank(ascending=False)
    df_5d['5日排名百分位'] = df_5d['5日排名'] / total_sectors * 100
    
    df_10d['10日排名'] = df_10d['10日涨跌幅'].rank(ascending=False)
    df_10d['10日排名百分位'] = df_10d['10日排名'] / total_sectors * 100
    
    # 合并数据
    df = pd.merge(df_5d, df_10d[['名称', '10日涨跌幅', '10日排名', '10日排名百分位']], on='名称', how='left')
    
    # 筛选条件
    # 1. 5日涨幅排名在前30%
    # 2. 10日/20日涨幅排名在前40%（用10日近似20日）
    # 3. 主力净流入 > 1亿
    # 4. 上涨家数占比 > 60%（此字段需要额外获取，暂用净流入占比>0替代）
    
    print(f"\n📈 共获取 {total_sectors} 个板块数据")
    print("\n🔍 筛选条件:")
    print("   • 5日涨幅排名在前30%")
    print("   • 10日涨幅排名在前40%")
    print("   • 主力净流入 > 1亿元")
    print("   • 净流入占比 > 0")
    
    # 数据清洗
    df['5日主力净流入-净额'] = pd.to_numeric(df['5日主力净流入-净额'], errors='coerce')
    df['5日主力净流入-净占比'] = pd.to_numeric(df['5日主力净流入-净占比'], errors='coerce')
    
    # 应用筛选
    filtered = df[
        (df['5日排名百分位'] <= 30) &  # 前30%
        (df['10日排名百分位'] <= 40) &  # 前40%
        (df['5日主力净流入-净额'] > 100000000) &  # >1亿
        (df['5日主力净流入-净占比'] > 0)  # 净流入为正
    ].copy()
    
    # 按净流入排序，取前3
    filtered = filtered.sort_values('5日主力净流入-净额', ascending=False).head(3)
    
    print(f"\n✅ 符合条件板块: {len(filtered)} 个")
    print("=" * 60)
    
    if len(filtered) == 0:
        print("\n⚠️ 暂无板块满足所有筛选条件")
        print("\n建议放宽条件或查看完整榜单：")
        print("\n📋 5日涨幅前10板块:")
        top10 = df.nsmallest(10, '5日排名')[['名称', '5日涨跌幅', '5日主力净流入-净额', '5日主力净流入-净占比']]
        for idx, row in top10.iterrows():
            print(f"   {row['名称']:8s} | 5日: {row['5日涨跌幅']:+.2f}% | 净流入: {row['5日主力净流入-净额']/1e8:.2f}亿 | 占比: {row['5日主力净流入-净占比']:+.2f}%")
        return
    
    # 输出结果
    for idx, (_, row) in enumerate(filtered.iterrows(), 1):
        sector_name = row['名称']
        change_5d = row['5日涨跌幅']
        change_10d = row['10日涨跌幅']
        fund_inflow = row['5日主力净流入-净额'] / 1e8  # 转为亿
        fund_ratio = row['5日主力净流入-净占比']
        rank_5d = row['5日排名']
        rank_10d = row['10日排名']
        
        # 判断阶段标签
        if change_5d < 5 and fund_ratio > 2:
            label = "底部集中"
            label_desc = "主力在吸筹，值得重点关注"
        elif change_5d < 10 and change_10d < 15:
            label = "低位换手"
            label_desc = "筹码在换，观察为主"
        elif change_5d > 5 and change_10d > 10:
            label = "中继抬升"
            label_desc = "趋势健康，可跟踪"
        elif change_5d > 15:
            label = "高位锁仓"
            label_desc = "主力没走，但空间不大"
        else:
            label = "过渡状态"
            label_desc = "方向不明，先不看"
        
        print(f"\n{idx}. 📌 {sector_name}")
        print(f"   ├─ 核心逻辑: {label_desc}")
        print(f"   ├─ 阶段标签: {label}")
        print(f"   ├─ 5日涨幅: {change_5d:+.2f}% (排名: {int(rank_5d)}/{total_sectors})")
        print(f"   ├─ 10日涨幅: {change_10d:+.2f}% (排名: {int(rank_10d)}/{total_sectors})")
        print(f"   ├─ 主力净流入: {fund_inflow:.2f}亿元")
        print(f"   ├─ 净流入占比: {fund_ratio:+.2f}%")
        
        # 风险提示
        if change_5d > 15:
            risk = "⚠️ 短期涨幅过大，注意回调风险"
        elif fund_ratio > 5:
            risk = "⚠️ 资金过度集中，可能即将分化"
        elif change_10d > 30:
            risk = "⚠️ 中期涨幅已高，谨慎追高"
        else:
            risk = "✅ 风险相对可控"
        
        print(f"   └─ 风险提示: {risk}")
    
    print("\n" + "=" * 60)
    print("💡 使用建议:")
    print("   • 优先关注'底部集中'和'中继抬升'板块")
    print("   • 结合个股基本面进一步筛选")
    print("   • 设置止损位，控制仓位风险")
    print("=" * 60)

def save_full_list():
    """
    保存完整板块列表到CSV
    """
    df_5d = get_sector_data("5日")
    if df_5d is not None:
        df_5d = df_5d.sort_values('5日涨跌幅', ascending=False)
        filename = f"sector_fund_flow_{datetime.now().strftime('%Y%m%d')}.csv"
        df_5d.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 完整数据已保存至: {filename}")

if __name__ == "__main__":
    # 分析板块
    analyze_sectors()
    
    # 可选：保存完整数据
    # save_full_list()
    
    print("\n✨ 分析完成!")