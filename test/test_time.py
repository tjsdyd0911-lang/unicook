import pandas as pd
from datetime import datetime
from modules.DBManager import DBManager

def get_product_data(target_time=None):
    if target_time is None:
        target_time = datetime.now()

    hour = target_time.hour
    
    sql = """
    select 
        case 
            when hour(b.btime) between 7 and 10 then 'morning'
            when hour(b.btime) between 11 and 15 then 'lunch'
            when hour(b.btime) between 16 and 19 then 'dinner'
            else 'night'
        end as time_slot,
        i.code,
        i.item_name,
        i.image,
        i.price,
        count(*) as count
    from buy b
    join item i on b.code = i.code
    group by time_slot, i.code, i.item_name, i.image, i.price
    order by time_slot, count desc
    """
    try :
        with DBManager() as db :
            ranking_df = pd.read_sql(sql, db.con)
    except Exception as e:
        print(f"데이터 분석 중 오류 발생: {e}")
    
    if 7 <= hour < 11 : slot = "morning"
    elif 11 <= hour < 16 : slot = "lunch"
    elif 16 <= hour < 20 : slot = "dinner"
    else : slot = "night"
    
    top_data = ranking_df[ranking_df["time_slot"] == slot].head(4)
    return top_data

for h in [8, 13, 17, 23]: # 주요 시간대만 테스트
    test_time = datetime(2026, 1, 1, hour=h)
    product = get_product_data(test_time)
    print(product.index)
    for idx, row in product.iterrows() :
        print(f"[{h:02d}시] 상품명: {row['item_name']}, count: {row['count']}")
    print("=" * 40)
