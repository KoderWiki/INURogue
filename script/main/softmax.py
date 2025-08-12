import numpy as np

weights = np.random.randn(3, 3)

def softmax(x):
    exps = np.exp(x - np.max(x))
    return exps / np.sum(exps)

def choose_skill(state):
    logits = weights @ state
    probs = softmax(logits)
    skill_index = np.random.choice(3, p=probs)
    return skill_index, probs

def update_weights(state, skill_index, reward, probs, lr=0.01):
    grad = -reward * (1 - probs[skill_index]) * state
    weights[skill_index] -= lr * grad