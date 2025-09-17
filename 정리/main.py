# import my_module

# result = my_module.add(1,2)
# print(result)

# print(my_module.PI)


# from my_module import add, PI
# print(add(10,20))
# print(PI)

import pandas as pd

# 딕셔너리 형태로 데이터 생성
data = {
    "name": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "age": [25, 32, 18, 47, 29],
    "city": ["Seoul", "Busan", "Incheon", "Daegu", "Seoul"],
    "score": [85, 92, 78, 64, 90]
}

# DataFrame 만들기
df = pd.DataFrame(data)

print(df)       # 페이지 소스 출력