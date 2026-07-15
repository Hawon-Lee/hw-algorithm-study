# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# 2D 데이터(반달 모양, sklearn make_moons)에 대해 아주 단순한 Diffusion 모델을 구현합니다.
#
# 1. sklearn의 make_moons(n_samples=1000, noise=0.05, random_state=42)로 데이터를 만드세요.
# 2. Forward process: timestep T=50, beta는 1e-4에서 0.02까지 선형으로 증가하도록 설정하세요.
#    (beta_t를 이용해 alpha_t = 1 - beta_t, alpha_bar_t = alpha_1 * alpha_2 * ... * alpha_t 를 미리 계산)
# 3. 임의의 timestep t에서 노이즈를 추가한 데이터를 만드는 함수를 작성하세요.
#    x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * noise   (noise는 표준정규분포)
# 4. 모델은 (x_t, t)를 입력받아 노이즈(epsilon)를 예측하는 간단한 MLP로 만드세요.
#    (t는 정수 그대로 넣지 말고, 스칼라 값을 float으로 변환해 x_t와 concat)
# 5. loss = MSE(예측한 noise, 실제 noise)
# 6. 매 스텝마다 배치 데이터, 무작위 timestep t를 뽑아 학습시키세요. (500 iteration, Adam, lr=1e-3)
# 7. 최종 평균 loss(마지막 50 iteration 평균)를 반환하세요.

import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim

from sklearn.datasets import make_moons

def visualize_samples(model, X_real, device, save_path="./outputs/260715_diffusion_samples.png"):
    model.eval()
    n_samples = X_real.shape[0]

    with torch.no_grad():
        x = torch.randn(n_samples, 2, device=device)  # t=T 순수 노이즈에서 시작
        for t in reversed(range(50)):
            t_batch = torch.full((n_samples, 1), t, device=device, dtype=torch.float) / 50
            noise_pred = model.mlp(torch.cat([x, t_batch], dim=1))

            alpha_t = 1 - torch.linspace(1e-4, 0.02, steps=50, device=device)[t]
            alpha_bar_t = model.alpha_bar[t]

            if t > 0:
                z = torch.randn(n_samples, 2, device=device)
            else:
                z = torch.zeros(n_samples, 2, device=device)

            beta_t = 1 - alpha_t
            x = (1 / torch.sqrt(alpha_t)) * (x - (beta_t / torch.sqrt(1 - alpha_bar_t)) * noise_pred) + torch.sqrt(beta_t) * z

    generated = x.cpu().numpy()
    real = X_real.cpu().numpy()

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].scatter(real[:, 0], real[:, 1], s=8, alpha=0.6)
    axes[0].set_title("real data")
    axes[1].scatter(generated[:, 0], generated[:, 1], s=8, alpha=0.6, color="orange")
    axes[1].set_title("generated samples")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    model.train()

class Diffusion(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        beta = torch.linspace(1e-4, 0.02, steps=50)
        alpha = torch.ones(50) - beta
        alpha_bar = torch.cumprod(alpha, dim=0)
        self.register_buffer("alpha_bar", alpha_bar)
        self.mlp = nn.Sequential(
            nn.Linear(input_dim+1, input_dim*32),
            nn.ReLU(),
            nn.Linear(input_dim*32, input_dim*16),
            nn.ReLU(),
            nn.Linear(input_dim*16, input_dim)
        )
        self.mse_criterion = nn.MSELoss()

    def forward(self, x_0, t):
        noise = torch.randn(x_0.shape).to(x_0.device)
        
        x_t = torch.sqrt(self.alpha_bar[t]) * x_0 + torch.sqrt(1 - self.alpha_bar[t]) * noise

        # time embedding
        t = t.to(torch.float) / 50
        x_t = torch.concat([x_t, t], dim=1)
        noise_pred = self.mlp(x_t)
        return self.mse_criterion(noise_pred, noise)

def solution():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    iter = 10000
    batch_size = 32
    
    data = make_moons(n_samples=1000, noise=0.05, random_state=42)
    X, y = data[0], data[1]
    X = torch.from_numpy(X).to(torch.float)
    X = X.to(device)

    model = Diffusion(input_dim=2)
    model = model.to(device)
    adam = optim.Adam(model.parameters(), lr=1e-3)
    
    mse_last50_ls = []
    for i in range(iter):
        batch_idx = torch.randperm(len(X))[:batch_size]
        x_0 = X[batch_idx]
        t = torch.randint(low=0, high=50, size=(batch_size, 1)).to(device)

        mse_loss = model(x_0, t)
        
        adam.zero_grad()
        mse_loss.backward()
        adam.step()

        if i % 100 == 0:
            print(f"iter: {i}/{iter} | mse:", round(mse_loss.item(), 4))
        if i >= iter - 50:
            mse_last50_ls.append(mse_loss.item())
    avg_loss = sum(mse_last50_ls) / len(mse_last50_ls)
    return avg_loss, model, X, device

if __name__ == "__main__":
    result, model, X, device = solution()
    visualize_samples(model, X, device)
    print(f"Avg loss: {result:.4f}")