import numpy as np
import networkx as nx

def create_sbm_network(sizes, p_in, p_out):
    print("正在创建sbm网络...")
    blocks = np.full((len(sizes), len(sizes)), p_out) 
    np.fill_diagonal(blocks, p_in)  # 对角线设置为p_in，即社区内部连接概率
    G = nx.stochastic_block_model(sizes, blocks)  # 创建SBM网络
    return G

def create_watts_network(N, k, p):
    print("创建Watts-Strogatz小世界模型...")
    G = nx.watts_strogatz_graph(N, k, p)
    return G

def create_random_network(N, p):
    print("创建Erdős–Rényi随机图模型...")
    G = nx.erdos_renyi_graph(N, p)  
    return G