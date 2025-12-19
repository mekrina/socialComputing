import argparse
from visualization import evaluate_and_plot

def parse_args():
    parser = argparse.ArgumentParser(description="SIR模型与网络干预模拟")
    parser.add_argument('--N', type=int, default=1000, help="节点的总数")
    parser.add_argument('--per_comm_size', type=int, default=100, help="每个社区的大小")
    parser.add_argument('--pin', type=float, default=0.8, help="社区内的连接概率")
    parser.add_argument('--pout', type=float, default=0.1, help="社区间的连接概率")
    parser.add_argument('--beta_0', type=float, default=0.2, help="初始感染率")
    parser.add_argument('--gamma_0', type=float, default=0.1, help="初始恢复率")
    parser.add_argument('--steps', type=int, default=100, help="仿真步骤数")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    print(f"总节点数：{args.N}")
    print(f"每个社区的大小：{args.per_comm_size}")
    print(f"社区内的连接概率：{args.pin}")
    print(f"社区间的连接概率：{args.pout}")
    print(f"初始感染率：{args.beta_0}")
    print(f"初始恢复率：{args.gamma_0}")
    print(f"仿真步骤数：{args.steps}")
    
    if(args.N <= 5000):
        print("\033[33m⚠ 节点数过少可能导致仿真结果不稳定\033[0m")
    
    sizes = [args.per_comm_size] * (args.N // args.per_comm_size)
    evaluate_and_plot(sizes, args.pin, args.pout, args.beta_0, args.gamma_0, args.steps)
