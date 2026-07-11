# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# 1. age 컬럼의 결측치를 중앙값으로 채우세요.
# 2. sibsp + parch를 더해서 family_size 컬럼을 새로 만드세요.
# 3. pclass, sex 컬럼을 원-핫 인코딩하세요.
# 4. 피처는 인코딩된 pclass/sex + age, fare, family_size, 타겟은 survived로 설정하세요.
# 5. train_test_split으로 test_size=0.2, random_state=42, stratify 옵션을 사용해 분리하세요.
# 6. PyTorch로 로지스틱 회귀를 학습시키세요. 단, 클래스 불균형을 보정하기 위해
#    BCEWithLogitsLoss의 pos_weight 인자를 활용하세요.
# 7. test set에 대한 roc_auc_score를 반환하세요.

import seaborn as sns
import pandas as pd

import torch
import torch.nn as nn
import torch.optim as optim

from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def solution(df):
    df = df.copy()

    # 1
    df.fillna(value={"age": df["age"].median()}, inplace=True)

    # 2
    df["family_size"] = df["sibsp"] + df["parch"]

    # 3
    df[["pclass_2", "pclass_3"]] = pd.get_dummies(df["pclass"], drop_first=True)
    df[["is_male"]] = pd.get_dummies(df["sex"], drop_first=True)

    # 4
    X = df[["pclass_2", "pclass_3", "is_male", "fare", "family_size"]].values.astype(float)
    y = df["survived"].values.astype(float)
    
    # 5
    X_tr, X_ts, y_tr, y_ts = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    X_tr, X_ts, y_tr, y_ts = torch.tensor(X_tr, dtype=torch.float), torch.tensor(X_ts, dtype=torch.float), torch.tensor(y_tr, dtype=torch.float), torch.tensor(y_ts, dtype=torch.float)

    # 6
    model = nn.Sequential(
        nn.Linear(X_tr.shape[1], 1),
        # nn.Sigmoid()
    )

    pos_weight = (y_tr == 0).sum() / (y_tr == 1).sum()
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    adam = optim.Adam(model.parameters(), lr=1e-3)
    
    model.train()
    for i in tqdm(range(1000)):
        adam.zero_grad()
        y_tr_pred = model(X_tr).squeeze()
        loss = criterion(y_tr_pred, y_tr)
        loss.backward()
        adam.step()

        if i % 100 == 0:
            print(round(loss.item(), 4))

    model.eval()
    with torch.no_grad():
        y_ts_pred = model(X_ts)
    
    return roc_auc_score(y_ts, y_ts_pred)

if __name__ == "__main__":
    df = sns.load_dataset('titanic')
    result = solution(df)
    print(f"AUC: {result:.4f}")