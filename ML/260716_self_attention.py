# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# generate_data()로 만든 서열 분류 문제를 self-attention 기반 모델로 풀어보세요.
# (임베딩 문제 때와 같은 태스크지만, mean pooling 대신 self-attention을 사용합니다.)
#
# 1. 각 문자(A,C,G,T)를 정수 인덱스로 변환하고, nn.Embedding으로 embed_dim=16 벡터로 바꾸세요.
# 2. Q, K, V를 각각 별도의 Linear layer로 생성하세요. (bias 없이)
# 3. Single-head self-attention을 직접 구현하세요. (마스킹 불필요, 공식은 스스로 떠올려보세요)
# 4. attention 출력을 시퀀스 축으로 평균(mean)내서 서열 하나를 벡터로 압축하세요.
# 5. 압축된 벡터로 이진 분류하는 Linear layer를 추가하세요.
# 6. train_test_split으로 test_size=0.2, random_state=42로 분리하세요.
# 7. BCEWithLogitsLoss로 300 epoch 학습시키세요. (Adam, lr=1e-3)
# 8. test set에 대한 accuracy를 반환하세요.

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

class SelfAttnClassifier(nn.Module):
    def __init__(self, hidden_dim=16, out_dim=1):
        super().__init__()
        self.embedding = nn.Embedding(num_embeddings=4, embedding_dim=hidden_dim)
        self.Q_proj = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.K_proj = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.V_proj = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.ffn = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim//2),
            nn.ReLU(),
            nn.Linear(hidden_dim//2, hidden_dim//4),
            nn.ReLU(),
            nn.Linear(hidden_dim//4, out_dim),
        )

    def attention(self, Q, K, V):
        attn_score = F.softmax( 
            (Q @ K.transpose(1, 2)) / (Q.size(-1) ** 0.5), dim=-1
        )
        out = attn_score @ V
        return out

    def forward(self, x):
        x = self.embedding(x) # [B, 20, hidden_dim]
        Q = self.Q_proj(x)
        K = self.K_proj(x)
        V = self.V_proj(x)
        
        out = self.attention(Q, K, V)
        out = self.ffn(out + x)
        out = out.mean(dim=1)
        out = self.head(out)
        return out.squeeze()


def solution(sequences, labels):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    epochs = 300
    lr = 1e-3

    seq_dict = {"A":0, "C":1, "G":2, "T":3}
    sequences = [
        [seq_dict[char] for char in seq] for seq in sequences
    ]

    sequences = torch.tensor(sequences).to(device)
    labels = torch.tensor(labels, dtype=torch.float).to(device)
    x_tr, x_ts, y_tr, y_ts = train_test_split(sequences, labels, test_size=0.2, random_state=42)

    
    model = SelfAttnClassifier(hidden_dim=192, out_dim=1).to(device)
    adam = optim.Adam(model.parameters(), lr=lr)
    # calc pose weight
    n_pos = y_tr.sum()
    n_neg = len(y_tr) - n_pos
    bce_criterion = nn.BCEWithLogitsLoss(pos_weight=(n_neg/n_pos).to(device))

    model.train()
    for i in range(epochs):
        y_tr_pred = model(x_tr)
        bce_loss = bce_criterion(y_tr_pred, y_tr)

        adam.zero_grad()
        bce_loss.backward()
        adam.step()
        if i % 50 == 0:
            print(f"Epoch {i} | Loss {round(bce_loss.item(), 4)}")

    model.eval()
    with torch.no_grad():
        y_ts_pred = model(x_ts)
        y_ts_pred = y_ts_pred > 0.5
    f1 = f1_score(y_ts.cpu(), y_ts_pred.cpu())
    return f1

def generate_data(n=1000, seq_len=20, seed=42):
    import random
    random.seed(seed)
    chars = "ACGT"
    sequences, labels = [], []
    for _ in range(n):
        seq = "".join(random.choice(chars) for _ in range(seq_len))
        # 라벨 규칙: "GATA" 모티프가 서열에 포함되어 있으면 1
        label = 1 if "GATA" in seq else 0
        sequences.append(seq)
        labels.append(label)
    return sequences, labels

if __name__ == "__main__":
    sequences, labels = generate_data()
    result = solution(sequences, labels)
    print(f"F1 score: {result:.4f}")