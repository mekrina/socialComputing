# visualization.py

import matplotlib.pyplot as plt
from sir_model import optimized_SIR_model
from network_creation import create_sbm_network
from community_detection import community_detection

def evaluate_and_plot(sizes, pin, pout, beta_0, gamma_0, steps=100):
    """
    运行仿真并可视化实验结果
    """
    total_resources = 1 # 设定总资源量固定
    G = create_sbm_network(sizes, pin, pout)
    
    # 进行社区发现
    communities = community_detection(G)
    
    # 进行实验：不同干预策略
    interventions = ["uniform", "degree", "community"]
    
    plt.figure(figsize=(12, 6))
    
    print("开始仿真评估...")
    
    for intervention in interventions:
        infected_count = optimized_SIR_model(G, beta_0, gamma_0, intervention, total_resources, communities, steps)
        plt.plot(infected_count, label=f"Intervention: {intervention}")
    
    plt.title("SIR Model with Resource Interventions and Community Detection")
    plt.xlabel("Time steps")
    plt.ylabel("Infected count")
    plt.legend()
    plt.show()
