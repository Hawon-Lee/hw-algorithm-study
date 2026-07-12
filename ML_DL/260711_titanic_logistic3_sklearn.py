# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# 1. age 컬럼의 결측치를 중앙값으로 채우세요.
# 2. embarked 컬럼의 결측치는 최빈값으로 채우세요.
# 3. 수치형(age, fare)과 범주형(sex, embarked, pclass) 컬럼을 각각 다르게 전처리하는 파이프라인을 구성하세요.
#    (수치형: 표준화 / 범주형: 원-핫 인코딩)
# 4. 피처는 pclass, sex, age, fare, embarked, 타겟은 survived로 설정하세요.
# 5. train_test_split으로 test_size=0.2, random_state=42, stratify 옵션을 사용해 분리하세요.
# 6. 전처리와 모델을 하나의 파이프라인으로 묶어 학습시키세요. (LogisticRegression, max_iter=1000)
# 7. 5-fold 교차검증으로 train set에 대한 평균 accuracy를 출력하세요.
# 8. test set에 대한 accuracy를 반환하세요.

import seaborn as sns
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def solution(df):
    df = df.copy()
    # 1
    df.fillna(value={"age":df["age"].median()}, inplace=True)
    # 2
    df.fillna(value={"embarked":df["embarked"].mode()[0]}, inplace=True)
    # 3-1 (범주형)
    df["pclass"] = df["pclass"].astype(str)
    df[["sex_male", "embarked_Q", "embarked_S", "pclass_2", "pclass_3"]] = pd.get_dummies(df[["sex", "embarked", "pclass"]], drop_first=True)
    X = df[["pclass_2", "pclass_3", "sex_male", "age", "fare", "embarked_Q", "embarked_S"]]
    y = df["survived"]
    # 4
    X_tr, X_ts, y_tr, y_ts = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    # 3-2 (수치형)
    sc = StandardScaler().set_output(transform = "pandas") # Standard scaler 출력을 pandas로 변경
    X_tr[["age", "fare"]] = sc.fit_transform(X_tr[["age", "fare"]])
    X_ts[["age", "fare"]] = sc.transform(X_ts[["age", "fare"]])
    X_tr = X_tr.values
    y_tr = y_tr.values
    X_ts = X_ts.values
    y_ts = y_ts.values
    # 5
    kf = KFold(n_splits=5, random_state=42, shuffle=True)
    val_values = []
    for i, (tr_i, ts_i) in enumerate(kf.split(X_tr)):
        model = LogisticRegression(max_iter=1000)
        model.fit(X_tr[tr_i], y_tr[tr_i])
        y_val_pred = model.predict(X_tr[ts_i])
        val_acc = accuracy_score(y_tr[ts_i], y_val_pred)
        val_values.append(val_acc)
        print(f"{i}th validation acc. = {val_acc}")
    print(f"5-split mean val acc. = {sum(val_values)/len(val_values)}")

    final_model = LogisticRegression(max_iter=1000)
    final_model.fit(X_tr, y_tr)
    y_ts_pred = final_model.predict(X_ts)
    return accuracy_score(y_ts, y_ts_pred)

if __name__ == "__main__":
    df = sns.load_dataset('titanic')
    result = solution(df)
    print(f"Accuracy: {result:.4f}")