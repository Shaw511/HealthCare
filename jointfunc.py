import numpy as np
'''
    nodes = ['感冒', '头疼', '发烧']
    edges = {'感冒': ['头疼','发烧'], '头疼': ['感冒'], '发烧': ['感冒']}
    probs = {'感冒': np.array([0.1, 0.9]), '头疼': np.array([[0.8, 0.2], [0.4, 0.6]]), '发烧': np.array([[0.7, 0.3], [0.5, 0.5]])}
'''
class JointTree:
    def __init__(self, nodes, edges,probs):
        self.nodes = nodes
        self.edges = edges
        self.messages = {}

        # 初始化节点的消息
        for node in self.nodes:
            self.messages[node] = {}
            for neighbor in self.edges[node]:
                self.messages[node][neighbor] = probs[neighbor]

        #调试
        for node in self.nodes:
            print("node:", node)
            print("edges[node]:", self.edges[node])
            for neighbor in self.edges[node]:
                print("neighbor:", neighbor)
                print("self.messages[node]:", self.messages[node])
                print("self.messages[neighbor]:", self.messages[neighbor])

        # 执行消息传递算法
        #self.message_passing()

    def marginal_prob(self, node):
        """
        计算节点的边缘概率
        """
        factors = []
        for neighbor in self.edges[node]:
            factors.append(self.messages[neighbor][node])

        # 将所有因子相乘得到联合概率
        joint_prob = np.prod(factors, axis=0)

        # 计算节点的边缘概率
        marginal_prob = joint_prob.sum(axis=0)
        return marginal_prob / marginal_prob.sum()

    def message_passing(self, max_iterations=100, tolerance=1e-6):
        """
        执行消息传递算法
        """
        for i in range(max_iterations):
            max_diff = 0
            for node in self.nodes:
                for neighbor in self.edges[node]:#neighbor=[['头疼','发烧'],["感冒"],["感冒"]]
                    old_message = self.messages[node][neighbor]
                    incoming_messages = []
                    for other_neighbor in self.edges[node]:
                        if other_neighbor != neighbor:
                            incoming_messages.append(self.messages[other_neighbor][node])

                    # 将所有传入消息相乘得到新消息
                    new_message = np.prod(incoming_messages, axis=0)

                    # 对新消息进行归一化
                    new_message /= new_message.sum()

                    # 计算消息差异
                    diff = np.abs(new_message - old_message).sum()

                    # 更新消息
                    self.messages[node][neighbor] = new_message

                    # 记录最大差异
                    max_diff = max(max_diff, diff)

            # 如果消息差异小于容忍度，则停止迭代
            if max_diff < tolerance:
                break

if __name__ == '__main__':
    # 定义节点和边
    nodes = ['感冒', '头疼', '发烧']
    edges = {'感冒': ['头疼','发烧'], '头疼': ['感冒'], '发烧': ['感冒']}

    # 定义病症概率表
    probs = {'感冒': np.array([0.1, 0.9]), '头疼': np.array([[0.1, 0.9], [0.4, 0.6]]), '发烧': np.array([[0.1, 0.9], [0.5, 0.5]])}

    # 创建联合树
    joint_tree = JointTree(nodes, edges,probs)
    
    # 计算并输出边缘概率
    print('症状1概率：', joint_tree.marginal_prob('发烧'))


