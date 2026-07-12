# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# 1. age 컬럼의 결측치를 중앙값으로 채우세요.
# 2. sex 컬럼을 male=0, female=1로 인코딩하세요.
# 3. 피처는 pclass, sex, age, fare, 타겟은 survived로 설정하세요.
# 4. train_test_split으로 test_size=0.2, random_state=42, stratify 옵션을 사용해 분리하세요.
# 5. 피처를 표준화(StandardScaler)하세요.
# 6. PyTorch로 로지스틱 회귀를 학습시키세요. 단, 매 100 epoch마다 learning rate를
#    절반으로 줄이는 스케줄러(StepLR)를 사용하세요. (총 500 epoch, 초기 lr=0.1)
# 7. test set에 대한 accuracy를 반환하세요.