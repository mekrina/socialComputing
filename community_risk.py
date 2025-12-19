import numpy as np
import networkx as nx

def calculate_community_risk_optimized(G, communities):
    print("计算社区风险....（图规模比较大时计算聚类系数耗时可能比较长(10000节点约10min)）")
    if(len(G.nodes()) >= 5000): # 使用估算的方法加速
        return calculate_community_risk_approximate(G, communities)
        
    community_risk = {}
    
    clustering_dict = nx.clustering(G) # 复杂度较高
    
    for comm, nodes in communities.items():
        if len(nodes) == 0:
            community_risk[comm] = 0
            continue
        
        degrees = [G.degree(node) for node in nodes]
        internal_degree = np.mean(degrees)
        
        # 平均聚类系数
        clustering_coeffs = [clustering_dict[node] for node in nodes]
        clustering_coefficient = np.mean(clustering_coeffs)
        
        # 2. 计算跨社区传播潜力指标
        # 计算社区边界连接数
        cross_edges = 0
        nodes_set = set(nodes)
        for u in nodes:
            for v in G.neighbors(u):
                if v not in nodes_set:  # 邻居节点不在同一社区
                    cross_edges += 1
        
        # 标准化为每节点平均跨社区连接数
        cross_edges_normalized = cross_edges / len(nodes)
        
        # 3. 计算综合风险评分
        risk_score = (1.0 * internal_degree + 
                      2.0 * clustering_coefficient + 
                      0.5 * cross_edges_normalized)
        
        community_risk[comm] = risk_score
    
    return community_risk

def calculate_community_risk_approximate(G, communities, sample_fraction=0.1):
    # 使用抽样方法近似计算社区风险
    community_risk = {}
    
    for comm, nodes in communities.items():
        if len(nodes) == 0:
            community_risk[comm] = 0
            continue
        
        # 确定抽样数量（至少保证1个节点）
        sample_size = min(1000, max(1, int(len(nodes) * sample_fraction)))
        sampled_nodes = np.random.choice(nodes, size=sample_size, replace=False)
        
        # 1. 基于样本计算内部传播潜力指标
        # 平均度数（基于样本）
        degrees = [G.degree(node) for node in sampled_nodes]
        internal_degree = np.mean(degrees)
        
        # 2. 批量计算样本节点的聚类系数
        # 创建一个子图，只包含样本节点和它们的邻居，用于计算聚类系数
        # 首先收集所有相关节点：样本节点及其邻居
        relevant_nodes = set(sampled_nodes)
        for node in sampled_nodes:
            relevant_nodes.update(G.neighbors(node))
        
        # 创建诱导子图
        subgraph = G.subgraph(relevant_nodes)
        
        # 批量计算子图中样本节点的聚类系数
        clustering_coeffs = []
        for node in sampled_nodes:
            if node in subgraph:
                clustering_coeffs.append(nx.clustering(subgraph, node))
        
        clustering_coefficient = np.mean(clustering_coeffs) if clustering_coeffs else 0
        
        # 3. 基于样本计算跨社区传播潜力
        # 为每个样本节点计算跨社区连接数
        cross_edges_per_node = []
        nodes_set = set(nodes)
        
        for u in sampled_nodes:
            cross_count = 0
            for v in G.neighbors(u):
                if v not in nodes_set:
                    cross_count += 1
            cross_edges_per_node.append(cross_count)
        
        cross_edges_normalized = np.mean(cross_edges_per_node) if cross_edges_per_node else 0
        
        # 4. 计算综合风险评分
        risk_score = (1.0 * internal_degree + 
                      2.0 * clustering_coefficient + 
                      0.5 * cross_edges_normalized)
        
        community_risk[comm] = risk_score
    
    return community_risk