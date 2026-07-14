# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# sklearn의 load_digits (8x8 손글씨 숫자 이미지, 64차원으로 펼침)를 사용합니다.
#
# 1. 데이터를 0~1 범위로 정규화하세요. (원본은 0~16 범위)
# 2. train_test_split으로 test_size=0.2, random_state=42로 분리하세요.
# 3. VAE를 구현하세요.
#    - Encoder: 64 -> 32 -> (mu, logvar), 각각 latent_dim=8
#    - Reparameterization trick 사용 (mu + eps * std)
#    - Decoder: 8 -> 32 -> 64, 마지막은 Sigmoid로 0~1 복원
# 4. Loss = 재구성 손실(BCE, reduction='sum') + KL divergence
#    KL divergence 공식: -0.5 * sum(1 + logvar - mu^2 - exp(logvar))
# 5. 100 epoch 학습시키세요. (Adam, lr=1e-3)
# 6. test set에 대한 평균 재구성 손실(reconstruction loss만, KL 제외)을 반환하세요.

import matplotlib.pyplot as plt
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

def visualize_reconstruction(X_ts, X_ts_pred, n_show=8, save_path="vae_reconstruction.png"):
    originals = X_ts[:n_show].cpu().numpy()
    recons = X_ts_pred[:n_show].cpu().numpy()

    fig, axes = plt.subplots(2, n_show, figsize=(n_show * 1.5, 3))
    for i in range(n_show):
        axes[0, i].imshow(originals[i].reshape(8, 8), cmap="gray")
        axes[0, i].axis("off")
        axes[1, i].imshow(recons[i].reshape(8, 8), cmap="gray")
        axes[1, i].axis("off")

    axes[0, 0].set_title("original", loc="left", fontsize=9)
    axes[1, 0].set_title("reconstructed", loc="left", fontsize=9)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

class VAE(nn.Module):
    def __init__(self, input_dim, h1, h2):
        super().__init__()
        
        # encoder
        self.enc = nn.Linear(input_dim, h1)
        self.enc_mu = nn.Linear(h1, h2)
        self.enc_logvar = nn.Linear(h1, h2)
        
        # decoder
        self.dec_1 = nn.Linear(h2, h1)
        self.dec_2 = nn.Linear(h1, input_dim)

        # activation
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.enc(x)

        mu = self.enc_mu(out)
        logvar = self.enc_logvar(out)

        # sampling
        std = torch.exp(0.5 * logvar)
        eps = torch.randn(std.size()).to(mu.device)
        latent = mu + eps * std

        # decoding
        out = self.dec_1(latent)
        out = self.dec_2(out)

        out = self.sigmoid(out)

        return out, mu, logvar

class CustomDataset(Dataset):
    def __init__(self, X, y):
        super().__init__()
        self.X = X
        self.y = y
        
    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.X)

def solution():
    # 변수 정의
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    epoch = 100

    # 데이터 로드
    digits = load_digits(return_X_y=True)
    data, target = digits
    
    # 정규화
    mm = MinMaxScaler()
    data = mm.fit_transform(data)
    data = torch.from_numpy(data).to(torch.float32)
    data = data.to(device)

    # 분할
    X_tr, X_ts, y_tr, y_ts = train_test_split(data, target, test_size=0.2, random_state=42)

    tr_loader = DataLoader(
        CustomDataset(X_tr, y_tr),
        shuffle=True,
        batch_size=32
    )

    # 학습
    model = VAE(input_dim=64, h1=48, h2=32)
    model = model.to(device)
    bce_criterion = nn.BCELoss(reduction="sum")
    kl_criterion = nn.KLDivLoss()
    adam = optim.Adam(model.parameters(), lr=1e-3)

    model.train()
    kl_loss_ls = []
    bce_loss_ls = []
    total_loss_ls = []
    for i in tqdm(range(epoch)):
        bce_loss_sum = 0
        kl_loss_sum = 0
        total_loss_sum = 0
        for j, (X, y) in tqdm(enumerate(tr_loader)): # j means step index
            X_pred, mu, logvar = model(X)
            
            bce_loss = bce_criterion(X_pred, X)
            bce_loss_sum += bce_loss
            kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
            kl_loss_sum += kl_loss
            total_loss = bce_loss + kl_loss
            total_loss_sum += total_loss

            adam.zero_grad()
            total_loss.backward()
            adam.step()

        bce_loss_ls.append(bce_loss_sum.item())
        kl_loss_ls.append(kl_loss_sum.item())
        total_loss_ls.append(total_loss_sum.item())
        
        print(f"BCE={sum(bce_loss_ls)/len(bce_loss_ls)}, KL={sum(kl_loss_ls)/len(kl_loss_ls)}, total={sum(total_loss_ls)/len(total_loss_ls)}")

    # evaluation
    model.eval()
    test_bce_criterion = nn.BCELoss(reduction="mean")
    with torch.no_grad():
        X_ts_pred, _, _ = model(X_ts)
        avg_recon_loss = test_bce_criterion(X_ts_pred, X_ts)
    return avg_recon_loss, X_ts, X_ts_pred

if __name__ == "__main__":
    result, X_ts, X_ts_pred = solution()
    print(f"Avg reconstruction loss: {result:.4f}")
    visualize_reconstruction(X_ts, X_ts_pred, save_path="outputs/260714_VAE_reconstruction.png")