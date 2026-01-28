#======================================
# 필수 라이브러리 Import
#======================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from scipy.stats import f_oneway, levene, shapiro
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

import warnings
import platform

warnings.filterwarnings('ignore')
#======================================
# 운영체제별 한글 폰트 설정
#======================================
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

# 시각화 기본 설정
plt.rcParams['figure.figsize'] = (12, 4)

# 전역 시드 설정
np.random.seed(42)

#========================================================
# 기본 EDA 함수
#========================================================
def isna_shape(data):
    """
    여러 DataFrame의 shape와 결측치(개수, 비율)를 확인 후 출력
    data: [(df1, "name1"), (df2, "name2"), ...] 형태의 리스트
    """
    for df, name in data:
        print("="*5, name, "="*5)
        print("Shape:", df.shape)
        
        display(df.isna().sum())

def describe_numeric(data):
    '''
    수치형 기술통계
    '''
    for df, name in data:
        print("="*5, name, "="*5)
        display(df.describe())

def describe_object(data):
    '''
    문자형 기술통계
    '''
    for df, name in data:
        print("="*5, name, "="*5)
        display(df.describe(include = "O"))

def type_info(data):
    '''
    타입
    '''
    for df, name in data:
        print("="*5, name, "="*5)
        display(df.info())  
def head5(data):
    for df, name in data:
        print("="*5, name, "="*5)
        display(df.head())

#========================================================
# 전체 데이터 셋 불러오기
#========================================================
df = pd.read_csv("merged_data_inner.csv")
sellers = pd.read_csv("olist_sellers_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
order_reviews = pd.read_csv("olist_order_reviews_dataset.csv")
order_payments = pd.read_csv("olist_order_payments_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
geolocation = pd.read_csv("olist_geolocation_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")

#========================================================
# products['product_weight_g', 'product_length_cm', 'product_height_cm','product_width_cm']
# ols 회귀 모델 사용 여부
# 상관관계, VIF 파악
#========================================================

# 결측치 제거

products_pre = products.copy()
products_pre.dropna(subset=['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'], inplace=True)

#----------------------------------------------------
# 결측치 수가 2개로 매우 적고 표본이 많아 삭제 결정 후 EDA
#----------------------------------------------------


#========================================================
#['product_weight_g', 'product_length_cm', 'product_height_cm','product_width_cm']
# Histogram 시각화
#========================================================
fig, axes = plt.subplots(2,2, figsize = (16,10))

axes[0][0].hist(products_pre['product_weight_g'], bins = 15)
axes[0][0].set_title("상품 무게 히스토그램")

axes[0][1].hist(products_pre['product_length_cm'], bins = 15)
axes[0][1].set_title("상품 길이 히스토그램")

axes[1][0].hist(products_pre['product_height_cm'], bins = 15)
axes[1][0].set_title("상품 높이 히스토그램")

axes[1][1].hist(products_pre['product_width_cm'], bins = 15)
axes[1][1].set_title("상품 너비 히스토그램")

plt.show()

#========================================================
#['product_weight_g', 'product_length_cm', 'product_height_cm','product_width_cm']
# Boxplot 시각화
#========================================================
fig, axes = plt.subplots(2,2, figsize = (16,10))

axes[0][0].boxplot(products_pre['product_weight_g'])
axes[0][0].set_title("상품 무게 박스플롯")

axes[0][1].boxplot(products_pre['product_length_cm'])
axes[0][1].set_title("상품 길이 박스플롯")

axes[1][0].boxplot(products_pre['product_height_cm'])
axes[1][0].set_title("상품 높이 박스플롯")

axes[1][1].boxplot(products_pre['product_width_cm'])
axes[1][1].set_title("상품 너비 박스플롯")

plt.show()

#========================================================
#['product_weight_g', 'product_length_cm', 'product_height_cm','product_width_cm']
# scatterplot 시각화
#========================================================

cols = ['product_weight_g','product_length_cm', 'product_height_cm','product_width_cm']

for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        print("=" *30, f'{cols[i]} VS {cols[j]}', "=" *30)
        sns.scatterplot(x=products_pre[cols[i]], y=products_pre[cols[j]])
        plt.title(f"{cols[i]} vs {cols[j]}")
        plt.show()

#-------------------------------------------------------
# Scatter plot에서 뚜렷하게 상관관계가 보이지 않음 
#-------------------------------------------------------

#========================================================
#['product_weight_g', 'product_length_cm', 'product_height_cm','product_width_cm']
# Pearson, Spearman 상관계수
#========================================================

# 피어슨 상관계수
print("=" * 20, "pearson", "=" * 20)
pearson_corr = products_pre[['product_weight_g','product_length_cm', 'product_height_cm','product_width_cm']].corr(method = 'pearson')
display(pearson_corr)

# 스피어만 상관계수
print("=" * 20, "spearman", "=" * 20)
spearman_corr = products_pre[['product_weight_g','product_length_cm', 'product_height_cm','product_width_cm']].corr(method = 'spearman')
display(spearman_corr)

# Pearson vs Spearman상관 비교
print("=" * 20, "Pearson vs Spearman상관 비교", "=" * 20)
corr_df = []
for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        pearson = products_pre[[cols[i],cols[j]]].corr().iloc[0,1]
        spearman = products_pre[[cols[i],cols[j]]].corr(method= "spearman").iloc[0,1]
        corr_df.append({
            "col1" : cols[i],
            "col2" : cols[j],
            "pearson" : pearson,
            "spearman" : spearman
        })
def corr_(data):
    if data >= 0.7:
        return "강한(+)"
    elif data >= 0.5:
        return "중간(+)"
    elif data >= 0.3:
        return "약한(+)"
    elif data <= -0.7:
        return "강한(-)"
    elif data <= -0.5:
        return "중간(-)"
    elif data <= -0.3:
        return "약한(-)"
    else:
        return "상관 거의 없음"

corr_df = pd.DataFrame(corr_df)
corr_df['pearson 해석'] = corr_df['pearson'].apply(corr_)
corr_df['spearman 해석'] = corr_df['spearman'].apply(corr_)
display(corr_df)

#========================================================
# Pearson vs Spearman 히트맵
#========================================================
print("=" * 20, "Pearson vs Spearman 히트맵", "=" * 20)
fig, axes = plt.subplots(1, 2, figsize = (14, 6))

sns.heatmap(data = pearson_corr, ax = axes[0], annot = True)
axes[0].set_title("Pearson")

sns.heatmap(data = spearman_corr, ax = axes[1], annot = True)
axes[1].set_title("Spearman")

#-------------------------------------------------------
# Spearman이 Pearson 보다 상관계수가 대체로 높음
# Spearman, Pearson 모두 중간 관계의 상관관계의 많음
#-------------------------------------------------------

#========================================================
#['product_weight_g', 'product_length_cm', 'product_height_cm','product_width_cm']
# VIF 확인
#========================================================

from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

# 상수항 추가
X = sm.add_constant(products_pre[cols])
vif = pd.DataFrame()
vif['feature'] = X.columns
vif['vif'] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
display(vif)

#-------------------------------------------------------
# 독립변수 간 심각한 다중공선성 없음
# 모든 변수 그대로 모델 학습 가능
# weight, length, width가 상관이 중간 수준이지만, 다중공선성은 낮아서 유지 가능
#-------------------------------------------------------

#========================================================
# order 테이블 EDA 및 지연일 파악
# 지연일이 재구매에 영향을 미치는가? (통계검정)을 위한 EDA
#========================================================

# orders 결측치 제거
orders_pre = orders.dropna(subset= ['order_delivered_customer_date'])

#-------------------------------------------------------
# 대체할 값이 마땅하지 않고 표본이 많아 결측값 삭제
#-------------------------------------------------------

# order_estimated_delivery_date :: object -> datetime
# order_delivered_customer_date :: object -> datetime
# order_purchase_timestamp:: object -> datetime
orders_pre['order_estimated_delivery_date'] = pd.to_datetime(orders_pre['order_estimated_delivery_date'])
orders_pre['order_delivered_customer_date'] = pd.to_datetime(orders_pre['order_delivered_customer_date'])
orders_pre['order_purchase_timestamp'] = pd.to_datetime(orders_pre['order_purchase_timestamp'])

# 배송 지연일 추가 -> 지연일이 양수
orders_pre['delay_days'] = (orders_pre['order_delivered_customer_date'] - orders_pre['order_estimated_delivery_date']).dt.days

#========================================================
# 지연일 통계 및 시각화
#========================================================

# 지연일 통계
print("=" * 5, "지연일 통계", "="*5)
print("평균" , orders_pre['delay_days'].mean())
print("중앙값" , orders_pre['delay_days'].median())
print("최소" , orders_pre['delay_days'].min())
print("최대" , orders_pre['delay_days'].max())

# 지연일 시각화

fig, axes = plt.subplots(1,4, figsize = (16,4))

# 지연 여부
delay_o = orders_pre['delay_days'] > 0 # 지연
delay_x = orders_pre['delay_days'] <= 0 # 정상도착

# 전체 지연일 분포 - Histogram
axes[0].hist(orders_pre['delay_days'], bins = 30)
axes[0].set_title("지연일 분포")

# 지연여부 - Bar
axes[1].bar(["정상도착", "배송지연"], [delay_x.sum(), delay_o.sum()])
axes[1].set_title("지연여부")

# 지연율 - Pie
axes[2].pie([delay_x.sum(), delay_o.sum()], labels=['정상도착','배송지연'], autopct='%1.1f%%', colors=['green','red'])
axes[2].set_title("지연율")

# 이상치 - Boxplot
delay_o_data = orders_pre.loc[orders_pre['delay_days'] > 0, 'delay_days'] 
delay_x_data = abs(orders_pre.loc[orders_pre['delay_days'] <= 0, 'delay_days'])


axes[3].boxplot([delay_x_data, delay_o_data],
                labels=['정상도착','배송지연'],
                patch_artist=True)

axes[3].set_title("지연")

#-------------------------------------------------------
# 평균 -11.876881296902857
# 중앙값 -12.0
# 최소 -147
# 최대 188
# 지연되지 않고 조기 배송한 건들이 더 많음
#-------------------------------------------------------


# 결측치 제거
orders_pre = orders_pre.dropna(subset =['order_approved_at', 'order_delivered_customer_date'])

# 주문상태에서 고객에게 배달완료만 필터링
cond = orders_pre['order_status'] == "delivered"
orders_pre = orders_pre[cond]

#-------------------------------------------------------
# 배송완료만 필터링 한 이유
# 배송이 실제로 완료되지 않았으므로 지연 계산 불가
# 리뷰가 존재해도 배송 완료와 관련 없는 리뷰일 수 있음 → 분석 왜곡
#-------------------------------------------------------

# 날짜 컬럼 변경

orders_pre['order_purchase_timestamp'] = pd.to_datetime(orders_pre['order_purchase_timestamp'])
orders_pre['order_approved_at'] = pd.to_datetime(orders_pre['order_approved_at'])
orders_pre['order_delivered_carrier_date'] = pd.to_datetime(orders_pre['order_delivered_carrier_date'])

#-------------------------------------------------------
# 배송이 실제로 완료되지 않았으므로 지연 계산 불가
# 리뷰가 존재해도 배송 완료와 관련 없는 리뷰일 수 있음 → 분석 왜곡
#-------------------------------------------------------

#========================================================
# 월별 평균 리뷰 점수
#========================================================

order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])

# 'Y-M'을 문자열로 생성
order_reviews['Y-M_str'] = order_reviews['review_creation_date'].dt.to_period('M').astype(str)

# 월별 평균 리뷰 점수 계산
review_mean = order_reviews.groupby('Y-M_str')['review_score'].mean()

# 시각화
plt.figure(figsize=(12,6))
plt.plot(review_mean.index, review_mean.values, marker='o', linestyle='-', color='skyblue')
plt.title('월별 평균 리뷰 점수')
plt.xlabel('연-월')
plt.ylabel('평균 리뷰 점수')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

#========================================================
# 통계 검정을 위한 reivew_merge.csv 테이블 만들기
#========================================================

# 지연여부
orders_pre['delay_label'] = orders_pre['delay_days'].apply(lambda day : 0 if day <= 0 else 1)

# merge
orders_col = ['order_id', 'delay_days', 'delay_label']
review_cols = ['order_id', 'review_id', 'review_score']

review_merge = pd.merge(orders_pre[orders_col], order_reviews[review_cols], on = 'order_id')

# 저장
review_merge.to_csv("review_merge.csv")

#========================================================
# 통계 검정
# 지연 여부가 리뷰 점수에 영향을 미치는가?
# -----
# 가설
# H0 : 지연여부와 리뷰 점수는 독립적이다.
# H1 : 지연여부와 리뷰 점수는 독립적이지 않다.
# -----
#========================================================

# stats 불러오기
from scipy import stats

# riview_merge 불러오기
review_merge = pd.read_csv("review_merge.csv")

# =====================================
# 리뷰 점수 그룹 분리
# =====================================

delay_x = review_merge['delay_label'] == 0   # 정상 배송
delay_o = review_merge['delay_label'] == 1   # 지연 배송

reviews_normal = review_merge.loc[delay_x, 'review_score']
reviews_delay = review_merge.loc[delay_o, 'review_score']

# =====================================
# 시각화
# =====================================

fig, axes = plt.subplots(1, 2, figsize=(12,5))

# 신뢰구간
means = [reviews_normal.mean(), reviews_delay.mean()]
ses = [stats.sem(reviews_normal)*1.96, stats.sem(reviews_delay)*1.96] 

# 배송 지연 여부별 리뷰 점수 평균 - Bar
axes[0].bar(['정상배송', '지연배송'], means, yerr=ses, capsize=5, color=['skyblue','salmon'])
axes[0].set_ylabel('리뷰 점수 평균')
axes[0].set_title('배송 지연 여부별 리뷰 점수 평균')

# 배송 지연 여부별 리뷰 점수 분포 - Boxplot
sns.boxplot(x='delay_label', y='review_score', data=review_merge, ax=axes[1])
axes[1].set_xticklabels(['정상배송','지연배송'])
axes[1].set_ylabel('리뷰 점수')
axes[1].set_title('배송 지연 여부별 리뷰 점수 분포')

plt.tight_layout()
plt.show()

# ----------------------------------
# 정상 배송: 평균 리뷰 점수가 높음
# 지연 배송: 평균 리뷰 점수가 낮음
# 정상 배송: 중앙값이 높고, 4~5점 비율이 높음
# 지연 배송: 중앙값 낮고, 낮은 점수(1~3점) 비율이 상대적으로 많음
# 분포 차이가 뚜렷하게 나타남 → 지연 여부가 리뷰에 영향
# ----------------------------------

# =====================================
# 통계 검정 -> 카이제곱 검정
# =====================================

# 관측 빈도
ct = pd.crosstab(review_merge['delay_label'], review_merge['review_score'])

# 카이제곱 검정
chi2_stat, p_value, dof, expected = stats.chi2_contingency(ct)

# 효과 크기 (Cramér's V)
n = ct.values.sum()
r, c = ct.shape
cramers_v = np.sqrt(chi2_stat / (n * min(r-1, c-1)))

print("기대빈도 5 이하 셀 : ", (expected <= 5).sum())
print("카이제곱 통계량:", chi2_stat)
print("자유도:", dof)
print("p-value:", p_value)
print("Cramér's V (효과 크기):", cramers_v)

# -------------------------------------
# 배송 지연 여부와 리뷰 점수는 독립이 아님
# 지연 배송은 리뷰 점수에 중간 정도 영향
# 따라서 지연 최소화 → 리뷰 개선 가능
# -------------------------------------

# =====================================
# 종합 테이블 생성
# =====================================

# 전체 데이터 셋 가져오기
sellers = pd.read_csv("olist_sellers_dataset.csv")
products = pd.read_csv("olist_products_dataset.csv")
orders = pd.read_csv("olist_orders_dataset.csv")
order_reviews = pd.read_csv("olist_order_reviews_dataset.csv")
order_payments = pd.read_csv("olist_order_payments_dataset.csv")
order_items = pd.read_csv("olist_order_items_dataset.csv")
geolocation = pd.read_csv("olist_geolocation_dataset.csv")
customers = pd.read_csv("olist_customers_dataset.csv")

# =====================================
# customer
# =====================================

# 중복 제거
customers_pre = customers.drop_duplicates()

# =====================================
# seller
# =====================================

# 중복 제거

sellers_pre = sellers.drop_duplicates()

# =====================================
# geolocation
# =====================================

geolocation_pre = geolocation.drop_duplicates()

# 우편번호 평균값으로 그룹

geolocation_pre = geolocation_pre.groupby('geolocation_zip_code_prefix').agg({
    'geolocation_lat': 'mean',
    'geolocation_lng': 'mean',
    'geolocation_city': 'first',
    'geolocation_state': 'first'
}).reset_index()

# -------------------------------
# 동일한 우편번호 앞자리가 많고 merge 및 모델학습 시 데이터가 과하게 증가함
# -------------------------------

# =====================================
# products
# =====================================

products_pre = products.copy()

# 결측치 제거
products_pre.dropna(inplace = True)

# 로그변환 [길이, 무게, 높이, 너비]

log_cols = ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']

for col in log_cols:
    products_pre[f'log_{col}'] = np.log1p(products_pre[col])

products_pre.head()

# 필요컬럼만 필터링

products_col = ["product_id",
                "log_product_weight_g",
                "log_product_length_cm",
                "log_product_height_cm",
                "log_product_width_cm"
                ]
products_pre = products_pre[products_col]

# =====================================
# items
# =====================================

# 필요 없는 컬럼 삭제
order_items_pre = order_items.drop(columns = ['order_item_id'])

# 데이터형 변환 (object->datetime)
order_items_pre['shipping_limit_date'] = pd.to_datetime(order_items_pre['shipping_limit_date'])

# 로그 변환
order_items_pre['log_price'] = np.log1p(order_items_pre['price'])
order_items_pre['log_freight'] = np.log1p(order_items_pre['freight_value'])

items_cols = ["order_id",
              "product_id" ,
              "seller_id" ,
              "shipping_limit_date",
              'log_freight',
              "log_price"]

items_pre = order_items_pre[items_cols]

# =====================================
# ordrs
# =====================================

# 배송 완료된 주문만 선택
orders_pre = orders[orders['order_status'] == 'delivered'].copy()

# 날짜 컬럼 datetime 변환
date_cols = [
    'order_purchase_timestamp', 
    'order_approved_at', 
    'order_delivered_carrier_date', 
    'order_delivered_customer_date', 
    'order_estimated_delivery_date'
]
for col in date_cols:
    orders_pre[col] = pd.to_datetime(orders_pre[col])

# 결측치 제거
orders_pre = orders_pre.dropna(subset=[
    'order_approved_at', 
    'order_delivered_carrier_date', 
    'order_delivered_customer_date'
])

# 배송일 < 택배사 전달일인 경우 제거
orders_pre = orders_pre[
    orders_pre['order_delivered_customer_date'] >= orders_pre['order_delivered_carrier_date']
]

# 지연일 계산 컬럼 추가
orders_pre['delay_days'] = (
    orders_pre['order_delivered_customer_date'] - orders_pre['order_estimated_delivery_date']
).dt.days

# 지연여부 컬럼 정의
orders_pre['delay_label'] = orders_pre['delay_days'].apply(lambda x: 1 if x > 0 else 0)

orders_cols = ["order_id",
               "customer_id",
               "order_purchase_timestamp",
               "order_approved_at",
               "order_delivered_carrier_date",
               "order_delivered_customer_date",
               "order_estimated_delivery_date",
               "delay_days",
               "delay_label"]

orders_pre = orders_pre[orders_cols]



# =====================================
# payments
# =====================================

payments_pre = order_payments.copy()
payments_pre['log_payment_value'] = np.log(payments_pre['payment_value'] + 1)

# 필요한 컬럼만 추출하여 새로운 데이터프레임 생성
payments_pre = payments_pre[['order_id', 'payment_type', 'payment_installments', 'log_payment_value']]


# =====================================
# reviews
# =====================================

reviews_pre = order_reviews[['order_id','review_score']]

# =====================================
# Merge
# =====================================

# =====================================
# orders + itmems
# =====================================

# 주문별로 어떤 상품이 들어갔는지 연결
# 상품 가격, 배송비, 상품 ID, seller 정보 포함

order_items_merge = pd.merge(orders_pre,
                             items_pre,
                             on = "order_id",
                             how ="left")

# =====================================
# orders + itmems + products
# =====================================

# 상품 특성 추가: 카테고리, 무게, 길이, 높이 등

order_items_products_merge = pd.merge(order_items_merge,
                                      products_pre,
                                      on = "product_id",
                                      how ="left")

# =====================================
# orders + itmems + products + payments
# =====================================

# 결제 정보 추가: 결제 타입, 금액, 할부 정보

order_items_products_payments_merge  = pd.merge(order_items_products_merge,
                                                payments_pre,
                                                on = "order_id",
                                                how ="left")

# =====================================
# orders + itmems + products + payments + reviews
# =====================================

# 리뷰점수 추가
# 최종 주문 테이블

full_orders  = pd.merge(order_items_products_payments_merge,
                                                reviews_pre,
                                                on = "order_id",
                                                how ="left")

# =====================================
# sellers + geolocation 판매자 위치 정보
# =====================================

seller_geo = pd.merge(sellers_pre,
                      geolocation_pre,
                      left_on = "seller_zip_code_prefix",
                      right_on = "geolocation_zip_code_prefix",
                      how ='inner',
                      suffixes = ("_selleor", "_geo"))
seller_geo = seller_geo.drop(columns = "geolocation_zip_code_prefix")

# =====================================
# customers + + geolocation 구매자 위치 정보
# =====================================
customers_geo = pd.merge(customers_pre,
                         geolocation_pre,
                         left_on = "customer_zip_code_prefix",
                         right_on = "geolocation_zip_code_prefix",
                         how ='inner',
                         suffixes = ("_customer", "_geo"))
customers_geo = customers_geo.drop(columns = "geolocation_zip_code_prefix")

# =====================================
# full_orders + seller_geo + customers_geo (최종 테이블)
# =====================================

# -----------------------------------------
# full_orders + seller_geo
# -----------------------------------------
full_orders_geo = pd.merge(
    full_orders,
    seller_geo,          # seller_geo 안에는 seller_id 기준 위치 정보 포함
    on='seller_id',
    how='left'
)
# -----------------------------------------
# full_orders_geo + customers_geo
# -----------------------------------------
full_orders_geo = pd.merge(
    full_orders_geo,
    customers_geo,       # customers_geo 안에는 customer_id 기준 위치 정보 포함
    on='customer_id',
    how='left',
    suffixes=('_seller','_customer') 
)
# =====================================
# 중복 컬럼 제거
# =====================================

full_orders_geo.drop_duplicates(inplace= True)

drop_cols = [
    "geolocation_city_seller", "geolocation_state_seller",
    "geolocation_city_customer", "geolocation_state_customer"
]
full_orders_geo.drop(columns= drop_cols, inplace = True)
#======================================
# 거리 계산
#======================================

# 위도/경도를 라디안으로 변환
lat1 = np.radians(full_orders_geo['geolocation_lat_seller'])
lon1 = np.radians(full_orders_geo['geolocation_lng_seller'])
lat2 = np.radians(full_orders_geo['geolocation_lat_customer'])
lon2 = np.radians(full_orders_geo['geolocation_lng_customer'])

# 위도/경도 차이
dlat = lat2 - lat1
dlon = lon2 - lon1

# Haversine 공식 적용
a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
c = 2 * np.arcsin(np.sqrt(a))

# 거리 계산
full_orders_geo['distance_km'] = 6371 * c
full_orders_geo['road_distance_km'] = full_orders_geo['distance_km'] * 1.26


# =====================================
# 저장
# =====================================
full_orders_geo.to_csv("full_orders_geo.csv", index=False)

# =====================================
# OLS와 모델을 위한 시각화
# =====================================

# 구매자 도시 지연일 평균 상위 30개 시각화 - Bar

city_mean = full_orders_geo.groupby('customer_city')['delay_days'].mean().sort_values(ascending= False).iloc[:30]

plt.bar(city_mean.index, city_mean.values)
plt.xticks(rotation = 55, ha = 'right')
plt.ylabel('평균 지연일 (days)')
plt.title('상위 30개 지연 구매자 도시별 평균 지연일')
plt.show()

# 판매자 도시 지연일 평균 상위 30개 - Bar

city_mean = full_orders_geo.groupby('seller_city')['delay_days'].mean().sort_values(ascending= False).iloc[:30]

plt.bar(city_mean.index, city_mean.values)
plt.xticks(rotation = 55, ha = 'right')
plt.ylabel('평균 지연일 (days)')
plt.title('상위 30개 지연 판매자 도시별 평균 지연일')
plt.show()

# 구매자 X 판매자별 도시 평균 지연일 - Bar
city_mean = full_orders_geo.groupby(['customer_city','seller_city'])['delay_days'].mean()
top_30 = city_mean.sort_values(ascending=False).head(30)

plt.figure(figsize=(12,6))
plt.bar(range(len(top_30)), top_30.values)
plt.xticks(range(len(top_30)), [f"{c[0]}-{c[1]}" for c in top_30.index], rotation=55, ha='right')
plt.ylabel('평균 지연일 (days)')
plt.title('상위 30개 지연 구매자 X 판매자 도시별 평균 지연일')
plt.show()

# 구매자 X 판매자별 주 평균 지연일
state_mean = full_orders_geo.groupby(['customer_state','seller_state'])['delay_days'].mean()
top_30 = state_mean.sort_values(ascending=False).head(30)

plt.figure(figsize=(12,6))
plt.bar(range(len(top_30)), top_30.values)
plt.xticks(range(len(top_30)), [f"{c[0]}-{c[1]}" for c in top_30.index], rotation=55, ha='right')
plt.ylabel('평균 지연일 (days)')
plt.title('상위 30개 지연 구매자 X 판매자 주별 평균 지연일')
plt.show()

# =====================================
# 통계점정 - 카이제곱 검정
# ----------------------
# H₀: 주와 지연여부는 평균은 독립적이다
# H₁: 주별 주와 지연여부는 독립적이지 않다
#-----------------------
# =====================================

df = pd.crosstab(full_orders_geo['delay_label'],full_orders_geo['customer_state'])

print("\n[카이제곱 독립성 검정]")
print("-"*40)

# 가설
print("H₀: 주와 지연여부는 평균은 독립적이다")
print("H₁: 주별 주와 지연여부는 독립적이지 않다")
print("유의수준: α = 0.05")

chi2_stat, p, dof, expected = stats.chi2_contingency(df)
n = df.values.sum()
r, c = df.shape
cramers_v = np.sqrt(chi2_stat / n * min(r-1, c-1))

print("기대빈도 5 이하 셀 : ", (expected <= 5).sum())
print("카이제곱 통계량:", chi2_stat)
print("자유도:", dof)
print("p-value:", p)
print("유의성:", p<=0.05)
print("Cramér's V (효과 크기):", cramers_v)

# =====================================
# OLS 분석
# =====================================

# OLS 변수 선정

# =====================================
# :막대_차트: OLS 배송 지연일 예측 전체 코드
# =====================================
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')
# =====================================
# 1. 데이터 불러오기 및 선택
# =====================================
full_orders_geo = pd.read_csv("full_orders_geo.csv")
cols = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'shipping_limit_date',
    'log_price',
    'log_freight',
    'log_product_weight_g',
    'log_product_length_cm',
    'log_product_height_cm',
    'log_product_width_cm',
    'payment_type',
    'log_payment_value',
    'seller_state',
    'customer_state',
    'delay_days'
]
delay_re = full_orders_geo[cols].copy()
delay_re.drop_duplicates(inplace=True)
delay_re.dropna(inplace=True)
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "shipping_limit_date"
]
# 날짜 변환
for col in date_cols:
    delay_re[col] = pd.to_datetime(delay_re[col], errors='coerce')
# =====================================
# 2. 파생 변수 생성
# =====================================
for col in date_cols:
    delay_re[f'{col}_month'] = delay_re[col].dt.month
    delay_re[f'{col}_dayofweek'] = delay_re[col].dt.dayofweek
    delay_re[f'{col}_hour'] = delay_re[col].dt.hour
# 배송 과정별 소요일수
delay_re['days_to_payment'] = (delay_re['order_approved_at'] - delay_re['order_purchase_timestamp']).dt.days
delay_re['days_to_ship'] = (delay_re['order_delivered_carrier_date'] - delay_re['order_approved_at']).dt.days
delay_re['days_until_limit'] = (delay_re['shipping_limit_date'] - delay_re['order_delivered_carrier_date']).dt.days
# 원본 날짜 컬럼 제거
delay_re.drop(columns=date_cols, inplace=True)
# =====================================
# 3. 이상치 제거 (1.5*IQR)
# =====================================
def remove_outliers_iqr(df, cols, factor=1.5):
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df
num_cols = delay_re.select_dtypes(include='number').columns.tolist()
delay_re = remove_outliers_iqr(delay_re, num_cols, factor=1.5)
# =====================================
# 4. 독립, 종속 변수 설정
# =====================================
X = delay_re.drop(columns=['delay_days'])
y = delay_re['delay_days']
# =====================================
# 5. Train/Test Split
# =====================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# =====================================
# 6. 수치형 변수 스케일링
# =====================================
num_cols = X_train.select_dtypes(include='number').columns
scaler = StandardScaler()
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])
# =====================================
# 7. 범주형 변수 원핫 인코딩
# =====================================
cat_cols = X_train.select_dtypes(include='object').columns
encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
X_train_cat = pd.DataFrame(
    encoder.fit_transform(X_train[cat_cols]),
    columns=encoder.get_feature_names_out(cat_cols),
    index=X_train.index
)
X_test_cat = pd.DataFrame(
    encoder.transform(X_test[cat_cols]),
    columns=encoder.get_feature_names_out(cat_cols),
    index=X_test.index
)
X_train = pd.concat([X_train.drop(columns=cat_cols), X_train_cat], axis=1)
X_test = pd.concat([X_test.drop(columns=cat_cols), X_test_cat], axis=1)
# =====================================
# 8. OLS 학습
# =====================================
X_train_ols = sm.add_constant(X_train)
X_test_ols = sm.add_constant(X_test)
ols_model = sm.OLS(y_train, X_train_ols).fit()
print("="*20, "OLS Summary", "="*20)
display(ols_model.summary())
# =====================================
# 9. 예측 및 평가
# =====================================
y_pred = ols_model.predict(X_test_ols)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print("="*20, "OLS 평가", "="*20)
print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")


# =====================================
# Tree
# =====================================

from sklearn.model_selection import train_test_split, KFold
from sklearn.model_selection import cross_validate

# 1. 사용할 컬럼 정의



cols = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'shipping_limit_date',
    'log_price',
    'log_freight',
    'log_product_weight_g',
    'log_product_length_cm',
    'log_product_height_cm',
    'log_product_width_cm',
    'payment_type',
    'log_payment_value',
    'seller_city',
    'seller_state',
    'customer_state',
    'customer_city',
    'delay_days'
]

# 2. 데이터 불러오기 및 로그 복원


log_cols = [
    'log_price', 'log_freight',
    'log_product_weight_g', 'log_product_length_cm',
    'log_product_height_cm', 'log_product_width_cm',
    'log_payment_value'
]

delay_re = full_orders_geo[cols].copy()
for col in log_cols:
    orig_col = col.replace('log_', '')
    delay_re[orig_col] = np.expm1(delay_re[col])
delay_re.drop(columns=log_cols, inplace=True)


# 3. 날짜 컬럼 파생

date_cols = [
    'order_purchase_timestamp', 'order_approved_at',
    'order_delivered_carrier_date', 'shipping_limit_date'
]
for col in date_cols:
    delay_re[col] = pd.to_datetime(delay_re[col])
    delay_re[f"{col}_month"] = delay_re[col].dt.month
    delay_re[f"{col}_day"] = delay_re[col].dt.day
    delay_re[f"{col}_dayofweek"] = delay_re[col].dt.dayofweek
    delay_re[f"{col}_hour"] = delay_re[col].dt.hour

delay_re.drop(columns=date_cols, inplace=True)


# 4. IQR 기반 이상치 제거 (1.5 기준)

# 타겟
Q1 = delay_re['delay_days'].quantile(0.25)
Q3 = delay_re['delay_days'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
delay_re = delay_re[(delay_re['delay_days'] >= lower) & (delay_re['delay_days'] <= upper)]

# 독립변수 연속형 컬럼
num_cols = ['price', 'freight', 'product_weight_g', 'product_length_cm',
            'product_height_cm', 'product_width_cm', 'payment_value']

for col in num_cols:
    Q1 = delay_re[col].quantile(0.25)
    Q3 = delay_re[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    delay_re = delay_re[(delay_re[col] >= lower) & (delay_re[col] <= upper)]

# 중복제거
delay_re.dropna(inplace= True)

# =========================================
# 모델 선정
# =========================================

from sklearn.model_selection import train_test_split, KFold
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# 결측값 제거
delay_re.dropna(inplace=True)

# 독립변수, 종속변수
X = delay_re.drop(columns=['delay_days'])
y = delay_re['delay_days']

# 카테고리형 컬럼은 문자열로 변환
cat_features = ['payment_type', 'customer_city', 'customer_state', 'seller_state', 'seller_city']
for col in cat_features:
    X[col] = X[col].astype(str)

# train/test 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델과 KFold 설정
model = CatBoostRegressor(random_state=42, verbose=0, thread_count=-1)
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 교차검증 R² 계산
cv_scores = []
for train_idx, val_idx in kf.split(X_train):
    X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

    model.fit(X_tr, y_tr, cat_features=cat_features)
    r2 = model.score(X_val, y_val)  # CatBoostRegressor의 score() = R²
    cv_scores.append(r2)
print("=" * 20, "모델", "=" * 20)
print("CV R² 평균:", np.mean(cv_scores))

# 최종 모델 학습
model.fit(X_train, y_train, cat_features=cat_features)

# 테스트 데이터로 예측
y_pred = model.predict(X_test)

# MSE, RMSE 계산
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")

# ----------------------------------
# CB : (R2 : 0.4353, RMSE : 5.3249)
# ----------------------------------

# city 컬럼 제외 -> 인코딩 넘 많음
delay_re_2 = delay_re.drop(columns=['customer_city', 'seller_city'])
delay_re_2.dropna(inplace=True)

# 독립, 종속 설정
X = delay_re_2.drop(columns=['delay_days'])
y = delay_re_2['delay_days']

# 훈련, 테스트 데이터
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

# 인코딩 변수 지정
encoder_cols = X_train.select_dtypes(include= 'O').columns

# ColumnTransformer 정의
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
    ("encoder", OneHotEncoder(drop = 'first',sparse_output = False, handle_unknown='ignore'), encoder_cols)
    ],
    remainder = 'passthrough'
)

# 모델 정의
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

models ={
    'RF' : Pipeline([
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(random_state= 42, n_jobs=-1))
    ]),
    "GB" : Pipeline([
        ('preprocessor', preprocessor),
        ('model', GradientBoostingRegressor(random_state = 42))
    ]),
    "XGB" : Pipeline([
        ('preprocessor', preprocessor),
        ('model', XGBRegressor(random_state = 42, n_jobs=-1))
    ]),
    "LGBM" : Pipeline([
        ('preprocessor', preprocessor),
        ('model', LGBMRegressor(random_state = 42, n_jobs=-1, verbose=-1))
    ]),
}

# scoring 정의 (R² + RMSE)
from sklearn.metrics import r2_score, mean_squared_error
scoring = {
    'R2': 'r2',
    'RMSE': 'neg_root_mean_squared_error'
}


# cross_validate 수행


from sklearn.model_selection import cross_validate

results = []

for name, model in models.items():
    cv_result = cross_validate(model, X_train, y_train, cv = 5, scoring = scoring)
    cv_result = {
    'name': name,
    'R2 평균': round(cv_result['test_R2'].mean(),4),
    'RMSE 평균': round(-cv_result['test_RMSE'].mean(),4)
    }
    results.append(cv_result)

result_df = pd.DataFrame(results)
display(result_df)

# ----------------------------------
# RF : (R2 : 0.3967, RMSE : 5.5513)
# GB : (R2 : 0.2387, RMSE : 6.2357)
# XGB : (R2 : 0.4013, RMSE : 5.5300)
# LGBM : (R2 : 0.3669, RMSE : 5.6867)
# ----------------------------------

#------------------------------------
# CatBoost 확정
#------------------------------------

# 독립, 종속 변수 설정

X = delay_re.drop(columns=['delay_days'])
y = delay_re['delay_days']

# 훈련, 테스트
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 범주형 지정
cat_features = ['payment_type', 'customer_city', 'customer_state', 'seller_state', 'seller_city']

# 모델 학습
model = CatBoostRegressor(random_state = 42, verbose = 0, thread_count = -1)
model.fit(X_train, y_train, cat_features = cat_features)

#------------------------------------
# 변수 영향력 확인 > Shap
#------------------------------------

import shap
# CatBoost 모델 SHAP 값 계산
explainer = shap.Explainer(model)  # CatBoost는 TreeExplainer 자동 지원
shap_values = explainer(X_train)   # 학습 데이터 기준

# 전체 feature 중요도 시각화
shap.summary_plot(shap_values, X_train, plot_type="bar")

# feature 영향도 분포 시각화 (개별 샘플 포함)
shap.summary_plot(shap_values, X_train)

# 특정 샘플 예측 분석
shap.plots.waterfall(shap_values[0])  # 첫 번째 샘플 기준\

#------------------------------------
# 하이퍼 파라미터 찾기
#------------------------------------

from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostRegressor
from sklearn.metrics import make_scorer, mean_squared_error, r2_score

# 모델 정의
model = CatBoostRegressor(
    random_state=42,
    verbose=0,
    thread_count=-1,
    cat_features=cat_features
)

# 하이퍼파라미터 범위
param_dist = {
    'depth': [6, 8, 10],
    'learning_rate': [0.03, 0.05, 0.07],
    'l2_leaf_reg': [3, 5, 7],
    'iterations': [500, 800],
    'bagging_temperature': [0, 1, 2],
    'random_strength': [0, 1, 2]
}

# RMSE scorer

def rmse_scorer(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

scorer = make_scorer(rmse_scorer, greater_is_better=False)

# RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist,
    n_iter=20,            
    scoring=scorer,
    cv=5,                 
    verbose=2,
    random_state=42,
    n_jobs=-1
)

# 학습
random_search.fit(X_train, y_train)
print("최적 파라미터:", random_search.best_params_)
print("최적 RMSE:", -random_search.best_score_)

#--------------------------------
# 최종 모델
#--------------------------------

model = random_search.best_estimator_

y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("테스트 RMSE:", rmse)

r2 = r2_score(y_test, y_pred)
print("테스트 R²:", r2)

# ==============================================
# OLS와 Tree 변수 city 추가를 제외 하고 동일하게 -> 해석 용이
# ==============================================



import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from catboost import CatBoostRegressor
import warnings
warnings.filterwarnings('ignore')

# =====================================
# 1. 데이터 불러오기 및 선택
# =====================================
cols = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'shipping_limit_date',
    'log_price',
    'log_freight',
    'log_product_weight_g',
    'log_product_length_cm',
    'log_product_height_cm',
    'log_product_width_cm',
    'log_payment_value',
    'payment_type',
    'seller_state',
    'customer_state',
    'customer_city',
    'seller_city',
    'delay_days'
]

delay_re = pd.read_csv("full_orders_geo.csv")[cols].copy()
delay_re.drop_duplicates(inplace=True)
delay_re.dropna(inplace=True)

# =====================================
# 2. 날짜 파생변수 생성
# =====================================
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "shipping_limit_date"
]

for col in date_cols:
    delay_re[col] = pd.to_datetime(delay_re[col], errors='coerce')
    delay_re[f'{col}_month'] = delay_re[col].dt.month
    delay_re[f'{col}_weekday'] = delay_re[col].dt.dayofweek
    delay_re[f'{col}_hour'] = delay_re[col].dt.hour

delay_re['days_to_payment'] = (delay_re['order_approved_at'] - delay_re['order_purchase_timestamp']).dt.days
delay_re['days_to_ship'] = (delay_re['order_delivered_carrier_date'] - delay_re['order_approved_at']).dt.days
delay_re['days_until_limit'] = (delay_re['shipping_limit_date'] - delay_re['order_delivered_carrier_date']).dt.days

delay_re.drop(columns=date_cols, inplace=True)

# =====================================
# 3. 이상치 제거 (1.5*IQR)
# =====================================
num_cols = delay_re.select_dtypes(include='number').columns.tolist()
def remove_outliers_iqr(df, cols, factor=1.5):
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - factor * IQR
        upper = Q3 + factor * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df

delay_re = remove_outliers_iqr(delay_re, num_cols)

# =====================================
# 4. 로그(x+1) 역변환
# =====================================
log_cols = [col for col in delay_re.columns if col.startswith('log_')]
for col in log_cols:
    orig_col = col.replace('log_', '')
    delay_re[orig_col] = np.exp(delay_re[col]) - 1
delay_re.drop(columns=log_cols, inplace=True)

# =====================================
# 5. 독립, 종속 변수 설정
# =====================================
X = delay_re.drop(columns=['delay_days'])
y = delay_re['delay_days']

# =====================================
# 6. Train/Test Split
# =====================================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# =====================================
# 7. 수치형 변수 스케일링
# =====================================
num_cols = X_train.select_dtypes(include='number').columns
scaler = StandardScaler()
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])

# =====================================
# 8. CatBoost 학습 (최적 파라미터 적용)
# =====================================
cat_features = ['payment_type', 'seller_state', 'customer_state', 'customer_city', 'seller_city']
model = CatBoostRegressor(
    iterations=800,
    learning_rate=0.07,
    depth=10,
    l2_leaf_reg=3,
    random_strength=0,
    bagging_temperature=2,
    eval_metric='RMSE',
    random_state=42,
    thread_count=-1,
    verbose=100
)
model.fit(
    X_train, y_train,
    cat_features=cat_features,
    eval_set=(X_test, y_test),
    use_best_model=True
)

# =====================================
# 9. 예측 및 평가
# =====================================
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R²: {r2:.4f}")


import shap
import matplotlib.pyplot as plt

# =====================================
# CatBoost SHAP 분석
# =====================================
explainer = shap.Explainer(model)      # CatBoost는 TreeExplainer 자동 지원
shap_values = explainer(X_train)       # 학습 데이터 기준

# 1. 전체 feature 중요도 시각화 (막대 그래프)
shap.summary_plot(shap_values, X_train, plot_type="bar", show=True)

# 2. feature 영향도 분포 시각화 (개별 샘플 포함)
shap.summary_plot(shap_values, X_train, show=True)

# 3. 특정 샘플 예측 분석 (첫 번째 샘플 기준)
shap.plots.waterfall(shap_values[0], show=True)