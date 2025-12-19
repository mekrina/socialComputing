import community as community_louvain

def community_detection(G):
    print("运行louvain进行社区发现算法...")
    partition = community_louvain.best_partition(G)
    communities = {}
    for node, comm in partition.items():
        if comm not in communities:
            communities[comm] = []
        communities[comm].append(node)
    return communities

