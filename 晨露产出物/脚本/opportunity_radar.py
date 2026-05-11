#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
板块机会雷达 - 短线热点追踪工具
专门抓主升浪、起爆点、资金异动

运行: python opportunity_radar.py
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def get_sector_data(period):
    """获取板块数据"""
    try:
        df = ak.stock_sector_fund_flow_rank(indicator=period)
        return df
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def get_sector_stocks(sector_name):
    """获取板块内个股列表"""
    try:
        # 尝试获取板块成分股
        df = ak.stock_board_industry_name_ths()
        if sector_name in df['name'].values:
            stocks = ak.stock_board_industry_cons_ths(symbol=sector_name)
            return stocks
    except:
        pass
    return None

def analyze_opportunities():
    """
    分析短线机会
    核心逻辑：找资金正在疯狂涌入的板块
    """
    print("=" * 70)
    print("🚀 板块机会雷达 - 短线热点追踪")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    
    # 获取数据
    print("\n📊 获取实时数据...")
    df_today = get_sector_data("今日")
    df_3d = get_sector_data("3日")
    df_5d = get_sector_data("5日")
    
    if df_today is None or df_3d is None:
        print("❌ 数据获取失败")
        return
    
    # 合并数据
    df = pd.merge(df_today, df_3d[['名称', '3日涨跌幅', '3日主力净流入-净额']], on='名称', how='left')
    df = pd.merge(df, df_5d[['名称', '5日涨跌幅', '5日主力净流入-净额']], on='名称', how='left')
    
    # 数据清洗
    numeric_cols = ['今日涨跌幅', '今日主力净流入-净额', '今日主力净流入-净占比',
                    '3日涨跌幅', '3日主力净流入-净额', 
                    '5日涨跌幅', '5日主力净流入-净额']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    total = len(df)
    print(f"✅ 共获取 {total} 个板块数据\n")
    
    opportunities = []
    
    # 机会类型1: 今日起爆（当日大涨+资金涌入）
    print("🔥 机会类型1: 今日起爆板")
    print("-" * 70)
    type1 = df[
        (df['今日涨跌幅'] > 2) &  # 今日涨幅>2%
        (df['今日主力净流入-净额'] > 50000000) &  # 净流入>5000万
        (df['今日主力净流入-净占比'] > 1)  # 资金占比>1%
    ].sort_values('今日主力净流入-净额', ascending=False).head(3)
    
    for _, row in type1.iterrows():
        opportunities.append({
            'name': row['名称'],
            'type': '今日起爆',
            'today_change': row['今日涨跌幅'],
            'fund_inflow': row['今日主力净流入-净额'] / 1e8,
            'fund_ratio': row['今日主力净流入-净占比'],
            'score': row['今日涨跌幅'] * 0.5 + row['今日主力净流入-净占比'] * 2
        })
        print(f"📈 {row['名称']:10s} | 今日 {row['今日涨跌幅']:+5.2f}% | 主力 {row['今日主力净流入-净额']/1e8:5.2f}亿 | 占比 {row['今日主力净流入-净占比']:+.2f}%")
    
    if len(type1) == 0:
        print("   暂无符合条件的板块\n")
    
    # 机会类型2: 3日加速（短期趋势形成）
    print("\n🚀 机会类型2: 3日加速")
    print("-" * 70)
    type2 = df[
        (df['3日涨跌幅'] > 5) &  # 3日涨幅>5%
        (df['今日涨跌幅'] > 0.5) &  # 今日继续上涨
        (df['3日主力净流入-净额'] > 100000000)  # 3日净流入>1亿
    ].sort_values('3日涨跌幅', ascending=False).head(3)
    
    for _, row in type2.iterrows():
        opportunities.append({
            'name': row['名称'],
            'type': '3日加速',
            'change_3d': row['3日涨跌幅'],
            'today_change': row['今日涨跌幅'],
            'fund_3d': row['3日主力净流入-净额'] / 1e8,
            'score': row['3日涨跌幅'] + row['3日主力净流入-净额'] / 1e8
        })
        print(f"📈 {row['名称']:10s} | 3日 {row['3日涨跌幅']:+5.2f}% | 今日 {row['今日涨跌幅']:+5.2f}% | 3日主力 {row['3日主力净流入-净额']/1e8:5.2f}亿")
    
    if len(type2) == 0:
        print("   暂无符合条件的板块\n")
    
    # 机会类型3: 资金暗涌（今日调整但资金仍在买）
    print("\n💎 机会类型3: 资金暗涌（低吸机会）")
    print("-" * 70)
    type3 = df[
        (df['今日涨跌幅'] < 0) &  # 今日下跌
        (df['今日涨跌幅'] > -3) &  # 但跌幅不大(<3%)
        (df['今日主力净流入-净额'] > 30000000) &  # 资金仍在流入
        (df['3日涨跌幅'] > 0)  # 3日整体还是涨的
    ].sort_values('今日主力净流入-净额', ascending=False).head(2)
    
    for _, row in type3.iterrows():
        opportunities.append({
            'name': row['名称'],
            'type': '资金暗涌',
            'today_change': row['今日涨跌幅'],
            'fund_inflow': row['今日主力净流入-净额'] / 1e8,
            'change_3d': row['3日涨跌幅'],
            'score': abs(row['今日涨跌幅']) + row['今日主力净流入-净额'] / 1e8
        })
        print(f"📉 {row['名称']:10s} | 今日 {row['今日涨跌幅']:+5.2f}% | 主力仍买 {row['今日主力净流入-净额']/1e8:5.2f}亿 | 3日累计 {row['3日涨跌幅']:+5.2f}%")
    
    if len(type3) == 0:
        print("   暂无符合条件的板块\n")
    
    # 综合评分排序
    print("\n" + "=" * 70)
    print("🏆 今日机会排行 TOP 5")
    print("=" * 70)
    
    # 去重并排序
    seen = set()
    unique_opps = []
    for opp in opportunities:
        if opp['name'] not in seen:
            seen.add(opp['name'])
            unique_opps.append(opp)
    
    unique_opps.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    for i, opp in enumerate(unique_opps[:5], 1):
        print(f"\n{i}. ⭐ {opp['name']}")
        print(f"   类型: {opp['type']}")
        
        if opp['type'] == '今日起爆':
            print(f"   今日涨幅: {opp['today_change']:+.2f}%")
            print(f"   主力净流入: {opp['fund_inflow']:.2f}亿")
            print(f"   💡 策略: 关注明天开盘，若高开则追，低开则等5日线")
            
        elif opp['type'] == '3日加速':
            print(f"   3日涨幅: {opp['change_3d']:+.2f}%")
            print(f"   今日涨幅: {opp['today_change']:+.2f}%")
            print(f"   💡 策略: 趋势已形成，回调到5日线低吸")
            
        elif opp['type'] == '资金暗涌':
            print(f"   今日跌幅: {opp['today_change']:+.2f}%")
            print(f"   主力净流入: {opp['fund_inflow']:.2f}亿")
            print(f"   💡 策略: 洗盘概率大，明天若企稳可低吸")
    
    print("\n" + "=" * 70)
    print("⚠️ 风险提示:")
    print("   • 以上仅为数据分析，不构成投资建议")
    print("   • 短线交易风险高，请控制仓位")
    print("   • 建议设置止损位，单票不超过总仓位10%")
    print("=" * 70)

if __name__ == "__main__":
    analyze_opportunities()