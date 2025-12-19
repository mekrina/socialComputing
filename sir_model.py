import numpy as np
import networkx as nx
from tqdm import tqdm
from community_risk import calculate_community_risk_optimized
from intervention import apply_nonlinear_intervention

def optimized_SIR_model(G, beta_0, gamma_0, intervention, total_resources, communities=None, steps=100):
    S = {node: 1 for node in G.nodes()}  # 全部为易感
    I = {node: 0 for node in G.nodes()}  # 全部为未感染
    R = {node: 0 for node in G.nodes()}  # 全部为未恢复
    infected = np.random.choice(list(G.nodes()), size=10, replace=False)  # 随机初始化感染者
    for node in infected:
        I[node] = 1  # 初始感染者
        S[node] = 0  # 感染者不再是易感
    
    # 资源分配
    r_u = {}  # 记录每个节点的资源消耗比例
    
    if intervention == "uniform":
        # 均匀分配资源
        for node in G.nodes():
            r_u[node] = total_resources / len(G.nodes())
    
    elif intervention == "degree":
        # 按度数分配资源
        for node in G.nodes():
            r_u[node] = G.degree(node) / sum(dict(G.degree()).values()) * total_resources
            
    elif intervention == "community" and communities is not None:
        # 基于社区发现分配资源
        community_risk = calculate_community_risk_optimized(G, communities)
        total_community_risk = sum(community_risk.values())
        
        node_to_community = {}
        for comm, nodes in communities.items():
            for node in nodes:
                node_to_community[node] = comm
                
        community_resources = {}
        community_degree_sums = {}
        
        for comm, nodes in communities.items():
            community_resources[comm] = (community_risk[comm] / total_community_risk) * total_resources
            community_degree_sums[comm] = sum(G.degree(node) for node in nodes) / 2
        
        # 社区内按节点度分配资源
        for node in G.nodes():
            comm = node_to_community[node]
            resource_total = community_resources[comm]
            degree_sum = community_degree_sums[comm]
            
            if degree_sum <= 0:
                r_u[node] = resource_total / len(communities[comm])
            else:
                r_u[node] = (G.degree(node) / degree_sum) * resource_total
            
        
    # 计算每个节点的实际感染和康复概率（非线性）
    beta = {}
    gamma = {}
    for node in G.nodes():
        beta[node], gamma[node] = apply_nonlinear_intervention(beta_0, gamma_0, r_u[node]/total_resources)

    # SIR仿真
    infected_count = []
    
    np.random.seed(100)
    
    for step in tqdm(range(steps), desc=f"Simulation Progress of strategy {intervention}".ljust(42), ncols=100):
        new_infected = []
        for node in G.nodes():
            if S[node] == 1:  # 只有易感者才会被感染
                infection_probability = sum([I[neighbor] * beta[node] for neighbor in G.neighbors(node)]) / G.degree(node)
                if np.random.rand() < infection_probability:
                    new_infected.append(node)
                    S[node] = 0  # 转为感染
                    I[node] = 1
        
        # 更新康复者
        for node in G.nodes():
            if I[node] == 1:
                if np.random.rand() < gamma[node]:
                    I[node] = 0  # 转为恢复
                    R[node] = 1
        
        infected_count.append(sum(I.values()))
    
    return infected_count
