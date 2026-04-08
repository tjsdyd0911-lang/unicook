"""
상품추천 처리 클래스
"""

import pandas as pd
from datetime import datetime
from modules.DBManager import DBManager

class TimeDAO :
    def time_analyze(self) :
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
            now_hour = datetime.now().hour
        except Exception as e:
            print(f"데이터 분석 중 오류 발생: {e}")
            return [], "error"
        
        if 7 <= now_hour < 11 : slot = "morning"
        elif 11 <= now_hour < 16 : slot = "lunch"
        elif 16 <= now_hour < 20 : slot = "dinner"
        else : slot = "night"
        
        top_data = ranking_df[ranking_df["time_slot"] == slot].head(4)
        
        if not top_data.empty:
            top_data['price'] = top_data['price'].apply(lambda x: "{:,}원".format(x))
            return top_data.to_dict('records'), slot
        else:
            return [], slot
        