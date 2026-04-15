"""
상품추천 처리 클래스
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

from modules.DBManager   import DBManager
from modules.RecommendVO import RecommendVO

class RecommendDAO  :    
    def GetByFrequency(self,month,n) :
        """
        최근 1개월 구매이력을 이용한 추천
        """
        items = []
        with DBManager() as db :
            
            #전체 건수
            sql  = "select count(product_id) as total "
            sql += "from orders "
            sql += f"where order_date  >= date_sub(now(), interval {month} month) "
            db.Select(sql)
            total  = int(db.GetValue(0,"total"))
            
            #추천 상품
            sql  = "select product_id,count(product_id) as count,"
            sql += "(select name from product where product_id = orders.product_id) as name,"
            sql += "(select price from product where product_id = orders.product_id) as price,"
            sql += "(select weight from product where product_id = orders.product_id) as weight,"
            sql += "(select category_id from product where product_id = orders.product_id) as category_id,"
            sql += "(select category from product where product_id = orders.product_id) as category,"
            sql += "(select image_url from product where product_id = orders.product_id) as image_url "
            sql += "from orders "
            sql += f"where order_date  >= date_sub(now(), interval {month} month) "
            sql += "group by product_id "
            sql += "order by count desc "
            sql += f"limit 0,{ n } "
            count = db.Select(sql)
            for i in range(0,count) :
                product_id  = db.GetValue(i,"product_id")
                count  = db.GetValue(i,"count")            
                name        = db.GetValue(i,"name")
                price       = int(db.GetValue(i,"price"))
                weight      = db.GetValue(i,"weight")
                category_id = db.GetValue(i,"category_id")
                category    = db.GetValue(i,"category")
                image_url   = db.GetValue(i,"image_url")
                data = { "product_id" : product_id, "count" : count,
                        "name" : name , "price" : price, "weight" : weight,
                        "category_id" : category_id, "category" : category,
                        "image_url" : image_url}
                items.append(data)
        return total,items
    
    def GetByUserFrequency(self, userid, n = 8, algo_type = "main"):
        """
        회원에 대한 상품 추천 알고리즘 구축 (메인화면)
        """
        items = []
        with DBManager() as db :
            #전체 건수
            sql  = "select count(code) as total "
            sql += "from score "
            sql += f"where id = '{userid}' and algo_type = '{algo_type}' "
            db.Select(sql)
            total  = int(db.GetValue(0,"total"))
            
            #추천 상품
            sql  = "select code, score, "
            sql += "(select item_name from item where code = score.code) as name,"
            sql += "(select price from item where code = score.code) as price,"
            sql += "(select weight from item where code = score.code) as weight,"
            sql += "(select category_id from item where code = score.code) as category_id,"
            sql += "(select category from item where code = score.code) as category,"
            sql += "(select image from item where code = score.code) as image "
            sql += "from score "
            sql += f"where id = '{userid}' and algo_type = '{algo_type}' "
            sql += "order by score desc "
            sql += f"limit 0,{ n } "
            count = db.Select(sql)
            for i in range(0,count) :
                code        = db.GetValue(i,"code")
                score       = db.GetValue(i,"score")            
                name        = db.GetValue(i,"name")
                price       = int(db.GetValue(i,"price"))
                weight      = db.GetValue(i,"weight")
                category_id = db.GetValue(i,"category_id")
                category    = db.GetValue(i,"category")
                image   = db.GetValue(i,"image")
                data = { "code" : code, "score" : score,
                        "name" : name , "price" : price, "weight" : weight,
                        "category_id" : category_id, "category" : category,
                        "image" : image}
                items.append(data)
        return total,items
    
        
    def MakeUserFrequency(self,userid, top_k=10, algo_type="cosine"):
        """
        회원에 대한 상품 추천 알고리즘 구축 (메인화면)
        
        현재 코드는 "해당 상품을 구매한 모든 사용자"를 대상으로 계산하고 있는데, 이는 엄밀히 말하면
        KNN(K-Nearest Neighbors) 기반의 협업 필터링이 아닌 전체 가중 평균 방식이다.
        
        노이즈 제거: 나와 취향이 전혀 다른(유사도가 매우 낮은) 사람이 구매한 데이터까지 계산에 포함되면 추천의 정확도가 떨어진다.
        계산 효율성: 모든 유저가 아닌, 유사도가 높은 상위 K명(예: 5명~20명)의 데이터만 참조함으로써 계산 속도를 높일 수 있다.
        
        top_k 파라미터 추가: 나랑 가장 비슷한 몇 명을 볼 것인지 정합니다. (일반적으로 5~10명이 적당합니다.)
        """        
        # 1. 구매내역을 DB로부터 가져오기
        with DBManager() as db :
            sql  = "select user_id,product_id,quantity "
            sql += "from orders "        
            count = db.Select(sql)
            user_id    = []
            product_id = []
            quantity   = []
            for i in range(0,count) :
                user_id.append(db.GetValue(i,"user_id"))
                product_id.append(db.GetValue(i,"product_id"))
                quantity.append(db.GetValue(i,"quantity"))
            
            
            data = {
                'user_id': user_id,
                'product_id': product_id,
                'quantity': quantity
            }
            df = pd.DataFrame(data)        
            
            # 2. 사용자-상품 매트릭스 생성
            user_item_matrix = df.pivot_table(index='user_id', columns='product_id', values='quantity', fill_value=0)
            
            # 3. 사용자 간 코사인 유사도 계산
            user_sim = cosine_similarity(user_item_matrix)
            user_sim_df = pd.DataFrame(user_sim, index=user_item_matrix.index, columns=user_item_matrix.index)
            
            # 4. 대상 사용자와 유사한 이웃 '상위 K명' 찾기 (sim_users 활용!)
            # 자기 자신 제외, 유사도 높은 순으로 K명 추출
            sim_users = user_sim_df[userid].sort_values(ascending=False)[1:top_k+1]
            top_sim_user_ids = sim_users.index # 유사한 유저들의 ID 리스트
            
            # 5. 추천 점수 계산 (가중 평균 방식 - 상위 K명의 데이터만 사용)
            target_user_series = user_item_matrix.loc[userid]
            unbought_products = target_user_series[target_user_series == 0].index
            
            predictions = []
            
            for product in unbought_products:
                nom = 0 # 분자 (유사도 * 수량)
                den = 0 # 분모 (유사도의 합)
                
                for other_user in top_sim_user_ids: # 전체 유저가 아닌 상위 K명만 순회
                    sim = user_sim_df.loc[userid, other_user]
                    quantity = user_item_matrix.loc[other_user, product]
                    
                    if quantity > 0: # 유사한 유저가 해당 상품을 구매한 경우만 반영
                        nom += sim * quantity
                        den += sim
                    
                if den > 0:
                    score = nom / den
                    predictions.append({
                        'user_id': userid,
                        'product_id': product,
                        'score': round(float(score), 4),
                        'algo_type': algo_type
                    })
        
            ndf = pd.DataFrame(predictions).sort_values(by='score', ascending=False)
            
            #기존 추천정보 삭제
            sql  = "delete from score "
            sql += f"where user_id = '{userid}' and algo_type = '{algo_type}'"
            db.RunSQL(sql)
            
            for i in range(0,len(ndf)) :
                product_id = ndf.iloc[i]["product_id"]
                score = ndf.iloc[i]["score"]
                sql  = "insert into score "
                sql += "(user_id,product_id,score,algo_type) "
                sql += "values "
                sql += f"('{userid}','{product_id}','{score}','{algo_type}') "
                #print(sql)
                db.RunSQL(sql)

        return ndf
    
    def MakeItemFrequency(self,target_user_id, target_product_id, n_components=12, algo_type = "view"):
        """
        회원에 대한 상품 추천 알고리즘 구축 (상품정보)
        
        SVD(Singular Value Decomposition, 특잇값 분해)를 활용한 추천은 잠재 요인(Latent Factor)을 
        분석하여 "이 상품을 선택한 사람들의 숨겨진 취향"을 파악하는 데 매우 강력하다.
        특정 상품(5049242)을 기준으로, SVD로 압축된 잠재 공간에서 가장 유사한 연관 관계를 가진 상품들을 
        찾아 user_001에게 추천하는 코드이다.
        이 코드는 scikit-learn의 TruncatedSVD를 사용하여 아이템 간의 유사도를 계산한다.        
        """     
        # 1. 구매내역을 DB로부터 가져오기
        with DBManager() as db :
            sql  = "select user_id,product_id,quantity "
            sql += "from orders "        
            count = db.Select(sql)
            user_id    = []
            product_id = []
            quantity   = []
            for i in range(0,count) :
                user_id.append(db.GetValue(i,"user_id"))
                product_id.append(db.GetValue(i,"product_id"))
                quantity.append(db.GetValue(i,"quantity"))
            
            
            data = {
                'user_id': user_id,
                'product_id': product_id,
                'quantity': quantity
            }
            df = pd.DataFrame(data) 
            
            # --- [수정] 데이터 타입 통일: 모든 product_id를 문자열로 변환 ---
            df = df.copy()
            df['product_id'] = df['product_id'].astype(str)
            target_product_id = str(target_product_id)
            # ---------------------------------------------------------
        
            # 1. 사용자-상품 피벗 테이블 생성
            user_item_matrix = df.pivot_table(index='user_id', columns='product_id', values='quantity', fill_value=0)
            
            # 2. 아이템 간 유사도 계산을 위해 행렬 전치 (행: 상품, 열: 사용자)
            item_user_matrix = user_item_matrix.T
            
            # 3. SVD 차원 축소
            SVD = TruncatedSVD(n_components=n_components, random_state=42)
            matrix_reduced = SVD.fit_transform(item_user_matrix)
            
            # 4. 잠재 요인 공간에서의 상관계수 계산
            corr = np.corrcoef(matrix_reduced)
            item_ids = item_user_matrix.index.tolist() # 이제 item_ids는 문자열 리스트임
            
            # 5. 대상 상품 인덱스 찾기 (타입이 같으므로 int 변환 없이 바로 조회)
            try:
                target_idx = item_ids.index(target_product_id)
            except ValueError:
                db.DBClose()
                return f"상품 코드 {target_product_id}를 데이터에서 찾을 수 없습니다."
            
            # 6. 상관관계 점수 추출
            similarities = corr[target_idx]
            
            # 7. 결과 데이터프레임 구성
            recom_df = pd.DataFrame({
                'product_id': item_ids,
                'score': similarities
            })
            
            # 8. 필터링 로직
            # - 자기 자신 제외
            # - 해당 유저가 이미 구매한 상품 제외
            bought_list = df[df['user_id'] == target_user_id]['product_id'].unique()
            
            final_recom = recom_df[
                (~recom_df['product_id'].isin(bought_list)) & 
                (recom_df['product_id'] != target_product_id)
            ].sort_values(by='score', ascending=False).head(10)
            
            # 9. 최종 score 테이블 형식 가공
            final_recom['user_id'] = target_user_id
            final_recom['algo_type'] = 'svd'
            final_recom['score'] = final_recom['score'].apply(lambda x: round(float(x), 4))
                    
            ndf = final_recom[['user_id', 'product_id', 'score', 'algo_type']]        
            
            #기존 추천정보 삭제
            sql  = "delete from score "
            sql += f"where user_id = '{target_user_id}' and algo_type = '{algo_type}'"
            db.RunSQL(sql)
            
            for i in range(0,len(ndf)) :
                product_id = ndf.iloc[i]["product_id"]
                score = ndf.iloc[i]["score"]
                sql  = "insert into score "
                sql += "(user_id,product_id,score,algo_type) "
                sql += "values "
                sql += f"('{target_user_id}','{product_id}','{score}','{algo_type}') "
                #print(sql)
                db.RunSQL(sql)       
        
        return ndf
    
    def MakeCartRecommendations(self,target_user_id,algo_type = "cart"):
        """
        현재 맥락(Context) 반영:
        유저가 장바구니에 '치킨텐더'와 '치즈스틱'을 담았다면, 이 유저는 현재 '냉동 간식'이나 
        '맥주 안주'를 찾고 있을 확률이 높습니다. 
        이 알고리즘은 과거 구매 데이터를 통해 치킨텐더와 함께 자주 팔렸던 다른 간식류(예: 감자튀김, 닭강정 등)를 
        즉각적으로 찾아냅니다.
        데이터 희소성 극복:
        유저 개개인의 과거 데이터가 부족하더라도, '치킨텐더'라는 상품 자체의 판매 패턴은 데이터가 풍부하기 때문에 훨씬 안정적인 추천이 가능합니다.
        교차 판매(Cross-selling) 극대화:
        장바구니에 담긴 모든 아이템의 유사도를 합산하므로, 담긴 아이템 전체와 조화로운 상품이 추천 리스트 상단에 오게 됩니다.
        
        df_orders: 주문내역 데이터프레임
        df_cart: 현재 장바구니 데이터프레임 (columns: user_id, product_id, quantity)        
        """
        # 1. 구매내역을 DB로부터 가져오기
        with DBManager() as db :
            sql  = "select user_id,product_id,quantity "
            sql += "from orders "        
            count = db.Select(sql)
            user_id    = []
            product_id = []
            quantity   = []
            for i in range(0,count) :
                user_id.append(db.GetValue(i,"user_id"))
                product_id.append(db.GetValue(i,"product_id"))
                quantity.append(db.GetValue(i,"quantity"))
            
            
            data = {
                'user_id': user_id,
                'product_id': product_id,
                'quantity': quantity
            }
            df_orders = pd.DataFrame(data) 
            
            # 2. 장바구니를 DB로부터 가져오기
            sql  = "select user_id,product_id,quantity "
            sql += "from cart "
            sql += f"where user_id = '{target_user_id}' "
            count = db.Select(sql)
            user_id    = []
            product_id = []
            quantity   = []
            for i in range(0,count) :
                user_id.append(db.GetValue(i,"user_id"))
                product_id.append(db.GetValue(i,"product_id"))
                quantity.append(db.GetValue(i,"quantity"))
            
            
            data = {
                'user_id': user_id,
                'product_id': product_id,
                'quantity': quantity
            }
            df_cart = pd.DataFrame(data)         
    
            #기존 추천정보 삭제
            sql  = "delete from score "
            sql += f"where user_id = '{target_user_id}' and algo_type = '{algo_type}'"
            db.RunSQL(sql)
            
            # 0. 데이터 전처리: product_id를 문자열로 통일
            df_orders = df_orders.copy()
            df_orders['product_id'] = df_orders['product_id'].astype(str)
            df_cart = df_cart.copy()
            df_cart['product_id'] = df_cart['product_id'].astype(str)
            
            # 1. 사용자-상품 매트릭스 생성 (구매 여부 기반)
            # 수량(quantity)을 사용하거나, 단순히 샀으면 1, 안 샀으면 0으로 처리 (여기선 1/0 권장)
            user_item_matrix = df_orders.pivot_table(index='user_id', columns='product_id', values='quantity', fill_value=0)
            user_item_matrix = user_item_matrix.applymap(lambda x: 1 if x > 0 else 0)
            
            # 2. 아이템 간 유사도 계산 (상품 간 코사인 유사도)
            # 상품이 행으로 와야 하므로 행렬을 전치(T)함
            item_sim = cosine_similarity(user_item_matrix.T)
            item_sim_df = pd.DataFrame(item_sim, index=user_item_matrix.columns, columns=user_item_matrix.columns)
            
            # 3. 로그인 유저의 현재 장바구니 아이템 가져오기
            current_cart_items = df_cart[df_cart['user_id'] == target_user_id]['product_id'].tolist()
            
            if not current_cart_items:
                db.DBClose()
                return "장바구니가 비어 있어 추천할 수 없습니다."
        
            # 4. 장바구니 아이템들과 유사한 상품들의 점수 합계 구하기
            # 장바구니에 담긴 상품들이 다른 상품들과 갖는 유사도를 모두 더함
            recom_scores = item_sim_df[current_cart_items].sum(axis=1)
            
            # 5. 결과 데이터프레임 생성
            recom_df = recom_scores.reset_index()
            recom_df.columns = ['product_id', 'score']
            
            # 6. 필터링 로직
            # - 이미 장바구니에 담긴 상품 제외
            # - 이미 과거에 주문했던 상품 제외 (선택 사항, 여기선 제외함)
            ordered_items = df_orders[df_orders['user_id'] == target_user_id]['product_id'].unique()
            
            exclude_items = set(current_cart_items) | set(ordered_items)
            
            final_recom = recom_df[~recom_df['product_id'].isin(exclude_items)]
            final_recom = final_recom.sort_values(by='score', ascending=False).head(10)
            
            # 7. score 테이블 형식으로 가공
            final_recom['user_id'] = target_user_id
            final_recom['algo_type'] = algo_type
            final_recom['score'] = final_recom['score'].apply(lambda x: round(float(x), 4))
            
            ndf = final_recom[['user_id', 'product_id', 'score', 'algo_type']]    
    
            #기존 추천정보 등록
            for i in range(0,len(ndf)) :
                product_id = ndf.iloc[i]["product_id"]
                score = ndf.iloc[i]["score"]
                sql  = "insert into score "
                sql += "(user_id,product_id,score,algo_type) "
                sql += "values "
                sql += f"('{target_user_id}','{product_id}','{score}','{algo_type}') "
                #print(sql)
                db.RunSQL(sql) 
            
        return ndf
    
    def MakePersonalBestRecommendations(self,target_user_id,algo_type = "best"):
        """
        구매내역 추천 알고리즘
        
        이 알고리즘은 사용자의 '충성도(Loyalty)'와 '반복 구매 습관'을 분석하는 로직입니다.
        단순히 수량만 계산하면 한 번에 대량 구매한 상품이 상단에 오기 때문에, 
        "얼마나 자주(빈도)"와 "얼마나 많이(수량)"를 적절히 조합하여 '인생템 점수'를 산출하는 
        것이 핵심입니다.
        
        개인별 최애 상품(Personal Best) 추천 알고리즘
        이 코드는 다음 로직으로 점수를 계산합니다:
        구매 빈도(Frequency): 해당 상품을 몇 번의 주문(bno)에 걸쳐 샀는가? (주문 횟수)
        누적 수량(qty): 가입 이후 총 몇 개를 샀는가?
        가중치 점수: (빈도 * 0.7) + (수량 * 0.3) 등으로 가중치를 두어 최종 점수를 계산하고 0~1 사이로 정규화합니다.        
        """
        # 1. 구매내역을 DB로부터 가져오기
        with DBManager() as db :
            sql  = "select bno, id, code, qty "
            sql += "from buy "  
            sql += f"where id = '{target_user_id}' "
            count = db.Select(sql)
            bno   = []
            id    = []
            code = []
            qty   = []
            for i in range(0,count) :
                bno.append(db.GetValue(i,"bno"))
                id.append(db.GetValue(i,"id"))
                code.append(db.GetValue(i,"code"))
                qty.append(db.GetValue(i,"qty"))
            
            
            data = {
                'bno': bno,
                'id': id,
                'code': code,
                'qty': qty
            }
            df_orders = pd.DataFrame(data) 
    
            #기존 추천정보 삭제
            sql  = "delete from score "
            sql += f"where id = '{target_user_id}' and algo_type = '{algo_type}'"
            db.RunSQL(sql)
            
            # 0. 데이터 전처리: code를 문자열로 변환
            df_orders = df_orders.copy()
            df_orders['code'] = df_orders['code'].astype(str)
            
            # 1. 특정 사용자의 구매 내역만 필터링
            user_orders = df_orders[df_orders['id'] == target_user_id]
            
            if user_orders.empty:
                return "구매 이력이 없습니다."
        
            # 2. 상품별 구매 빈도와 누적 수량 계산
            # frequency: 서로 다른 주문번호의 개수 (얼마나 자주 찾았나)
            # total_qty: 수량의 합계 (얼마나 많이 샀나)
            best_stats = user_orders.groupby('code').agg(
                frequency=('bno', 'nunique'),
                total_qty=('qty', 'sum')
            ).reset_index()
        
            # 3. 가중치 점수 계산 (인생템 지수)
            # 빈도에 더 높은 가중치(0.7)를 두어 반복적으로 구매한 습관을 중시함
            best_stats['raw_score'] = (best_stats['frequency'] * 0.7) + (best_stats['total_qty'] * 0.3)
        
            # 4. score 테이블 저장을 위해 0~1 사이로 정규화 (Min-Max Scaling)
            # 추천 점수는 상대적이므로 가장 점수가 높은 상품을 1점으로 만듦
            max_score = best_stats['raw_score'].max()
            min_score = best_stats['raw_score'].min()
            
            if max_score == min_score:
                best_stats['score'] = 1.0  # 모든 상품 점수가 같으면 1점으로 통일
            else:
                best_stats['score'] = (best_stats['raw_score'] - min_score) / (max_score - min_score)
        
            # 5. score 테이블 형식으로 가공
            best_stats['id'] = target_user_id
            best_stats['algo_type'] = algo_type
            best_stats['score'] = best_stats['score'].apply(lambda x: round(float(x), 4))
            
            # 점수 높은 순으로 정렬하여 상위 4개 반환
            result = best_stats[['id', 'code', 'score', 'algo_type']]
            ndf =  result.sort_values(by='score', ascending=False).head(4)  
            
            
            #기존 추천정보 등록
            for i in range(0,len(ndf)) :
                code = ndf.iloc[i]["code"]
                score = ndf.iloc[i]["score"]
                sql  = "insert into score "
                sql += "(id,code,score,algo_type) "
                sql += "values "
                sql += f"('{target_user_id}','{code}','{score}','{algo_type}') "
                #print(sql)
                db.RunSQL(sql)         
        
        return ndf

    def UpdateRecommand(self,userid) :
        """
        상품 추천 알고리즘을 업데이트한다.
        """
        print(f"{userid}를 위한 상품 추천 정보 갱신 시작 =================")
        self.MakeUserFrequency(userid,top_k=10, algo_type="main")
        print(f"{userid}를 위한 상품 추천 정보 갱신 종료 =================")

    def RecommendItem(self, userid, algo_type) :
        item = []
        with DBManager() as db :
            conditions = []
            params     = []
            conditions.append("algo_type = %s")
            params.append(algo_type)
            if userid :
                conditions.append("id = %s")
                params.append(userid)
            sql  = "select i.code, i.image, i.item_name, i.price "
            sql += "from score s "
            sql += "join item  i "
            sql += "on s.code = i.code "
            if conditions :
                sql += "where " + " AND ".join(conditions)
            sql += " order by score desc "
            
            count = db.Select(sql, params)
            for n in range(count) :
                vo = RecommendVO()
                vo.code      = db.GetValue(n, "code")
                vo.image     = db.GetValue(n, "image")
                vo.item_name = db.GetValue(n, "item_name")
                vo.price     = f"{db.GetValue(n, 'price'):,}원"
                item.append(vo)
        return item
    
"""
target_user = "user_001"        
dao = RecommendDAO()
df = dao.MakePersonalBestRecommendations(target_user)
print(df)
"""
    
    