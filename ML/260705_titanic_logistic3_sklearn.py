# venv: sandbox
# cursor json 세팅으로 자동완성 꺼놓음!

# [ 문제 ]
# 1. age 컬럼의 결측치를 중앙값으로 채우세요.
# 2. sibsp + parch를 더해서 family_size 컬럼을 새로 만드세요.
# 3. pclass, sex 컬럼을 sklearn의 OneHotEncoder로 인코딩하세요.
# 4. 피처는 인코딩된 pclass/sex + age, fare, family_size, 타겟은 survived로 설정하세요.
# 5. train_test_split으로 test_size=0.2, random_state=42, stratify 옵션을 사용해 분리하세요.
# 6. LogisticRegression으로 학습시키세요. (class_weight='balanced', max_iter=1000)
# 7. test set에 대한 roc_auc_score를 반환하세요. (predict_proba 사용)

def solution(df):

    return auc

if __name__ == "__main__":
    df = sns.load_dataset('titanic')
    result = solution(df)
    print(f"AUC: {result:.4f}")