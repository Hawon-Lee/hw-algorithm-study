# venv: insite
# json 세팅으로 자동완성을 꺼놓음.

# [ 문제 ]
# 1. fare 컬럼의 결측치를 평균으로 채우세요.
# 2. embarked 컬럼을 원-핫 인코딩하세요.
# 3. 피처는 pclass, age, fare, 원-핫 인코딩된 embarked 컬럼들, 타겟은 survived로 설정하세요.
# 4. test_size=0.25, random_state=0, stratify 옵션을 사용해 데이터를 분리하세요.
# 5. 로지스틱 회귀로 학습시키세요. (max_iter=1000)
# 6. test set에 대한 정확도를 반환하세요.

import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def solution(df):
    # 1
    df = df.copy()
    df.fillna(
        value={
            "fare": df["fare"].mean(),
            # "age": df["age"].median()
        }, inplace=True
    )
    df.dropna(axis=0, subset=["age"], inplace=True)

    # 2
    df[["Q", "S"]] = pd.get_dummies(df["embarked"], drop_first=True)

    # 3 
    X = df[["pclass", "age", "fare", "Q", "S"]]
    y = df["survived"]

    # 4
    X_tr, X_ts, y_tr, y_ts = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

    # 5
    model = LogisticRegression(max_iter=1000)
    model.fit(X_tr, y_tr)
    
    # 6
    y_pred = model.predict(X_ts)
    accuracy = accuracy_score(y_ts, y_pred)
    return accuracy

if __name__ == "__main__":
    df = sns.load_dataset('titanic')
    result = solution(df)
    print(f"Accuracy: {result:.4f}")