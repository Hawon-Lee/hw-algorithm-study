# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# 1. age 컬럼의 결측치를 중앙값으로 채우세요.
# 2. sex 컬럼을 male=0, female=1로 인코딩하세요.
# 3. 피처는 ['pclass', 'sex', 'age', 'fare'], 타겟은 survived로 설정하세요.
# 4. train_test_split으로 test_size=0.2, random_state=42로 분리하세요.
# 5. Pytorch LogisticRegression으로 학습시키세요. (max_iter=1000)
# 6. test set에 대한 accuracy를 반환하세요.
# 7. loss plot 을 그려보세요.

import seaborn as sns
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from tqdm import tqdm

import torch.optim as optim

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

class LogisticRegression(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.layer = nn.Linear(input_dim, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        out = self.layer(x)
        out = self.sigmoid(out)
        return out.squeeze()

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
    scaler = StandardScaler()
    X_tr = scaler.fit_transform(X_tr)
    X_ts = scaler.transform(X_ts)

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    X_tr = torch.tensor(X_tr, dtype=torch.float).to(device)
    X_ts = torch.tensor(X_ts, dtype=torch.float).to(device)
    y_tr = torch.tensor(y_tr.values, dtype=torch.float).to(device)
    y_ts = torch.tensor(y_ts.values, dtype=torch.float)
    

    # 5번
    bce_loss = nn.BCELoss()
    model = LogisticRegression(X.shape[1]).to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)

    model.train()
    loss_ls = []
    pbar = tqdm(range(1000))
    for _ in pbar:
        y_pred = model(X_tr)
        loss = bce_loss(y_pred, y_tr)

        optimizer.zero_grad()
        loss.backward()

        loss_item = round(loss.item(), 4)
        loss_ls.append(loss_item)
        pbar.set_postfix(loss=loss_item)
        optimizer.step()

    # 6번
    model.eval()
    with torch.no_grad():
        y_hat = model(X_ts).cpu()
        accuracy = accuracy_score(y_ts, y_hat > 0.5)

    # 7번
    plt.plot(loss_ls)
    plt.savefig("outputs/260704_titanic_logistic_pytorch_loss.png")

    return accuracy

if __name__ == "__main__":
    df = sns.load_dataset('titanic')
    result = solution(df)
    print(f"Accuracy: {result:.4f}")