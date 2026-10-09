#!/usr/bin/env python3
"""Profiling trung thực file nguồn L6; không thay đổi CSV.
Chạy từ root repo: python scripts/profile_sales.py --data-dir data/raw
"""
import argparse,csv,collections,json
from pathlib import Path

def read(path):
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def main():
    p=argparse.ArgumentParser();p.add_argument('--data-dir',default='data/raw'); args=p.parse_args()
    base=Path(args.data_dir)
    names=['orders_2024_2026.csv','order_items.csv','products.csv','stores.csv','customers_raw.csv']
    result={'file_overview':{},'sales_reconciliation':{}}
    for name in names:
        path=base/name
        if not path.exists():
            print(f'Chưa có {path}; bỏ qua.');continue
        rows=read(path)
        result['file_overview'][name]={'rows':len(rows),'columns':list(rows[0]) if rows else [],'missing':{k:sum(not (r.get(k) or '').strip() for r in rows) for k in (rows[0].keys() if rows else [])}}
    items_path=base/'order_items.csv'
    if items_path.exists():
        rows=read(items_path); outcomes=collections.Counter();calc_total=reported_total=0;bad=[]
        for idx,r in enumerate(rows,2):
            try:
                calc=int(r['so_luong'])*int(r['don_gia']);real=int(r['thanh_tien'])
                calc_total+=calc;reported_total+=real
                if calc==real:outcomes['MATCH']+=1
                elif 10*real==11*calc:outcomes['PLUS_10_PERCENT']+=1
                elif 10*real==9*calc:outcomes['MINUS_10_PERCENT']+=1
                else:outcomes['OTHER_DIFF']+=1
            except (ValueError,KeyError) as exc:
                bad.append({'line':idx,'reason':str(exc)})
        duplicates=len(rows)-len({tuple(r.items()) for r in rows})
        result['sales_reconciliation']={'outcomes':dict(outcomes),'calculated_sum':calc_total,'reported_sum':reported_total,'difference':reported_total-calc_total,'exact_duplicate_excess':duplicates,'parse_errors':bad[:20]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
