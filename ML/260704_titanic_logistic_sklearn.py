# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# 1. age 컬럼의 결측치를 중앙값으로 채우세요.
# 2. sex 컬럼을 male=0, female=1로 인코딩하세요.
# 3. 피처는 ['pclass', 'sex', 'age', 'fare'], 타겟은 survived로 설정하세요.
# 4. train_test_split으로 test_size=0.2, random_state=42로 분리하세요.
# 5. sklearn의 LogisticRegression으로 학습시키세요. (max_iter=1000)
# 6. test set에 대한 accuracy를 반환하세요.

import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def solution(df):
    # 1번
    df = df.copy()
    df.fillna(value={"age":df["age"].median()}, inplace=True)

    # 2번
    sex_mapping_dict = {"male": 0, "female": 1}
    df["sex"] = df["sex"].map(sex_mapping_dict)

    # 3번
    X = df[["pclass", "sex", "age", "fare"]]
    y = df["survived"]

    # 4번
    X_tr, X_ts, y_tr, y_ts = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5번
    model = LogisticRegression(max_iter=1000)
    model.fit(X_tr, y_tr)

    # 6번
    y_hat = model.predict(X_ts)
    accuracy = accuracy_score(y_ts, y_hat)
    return accuracy

if __name__ == "__main__":
    df = sns.load_dataset('titanic')
    result = solution(df)
    print(f"Accuracy: {result:.4f}")