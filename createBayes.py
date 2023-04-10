

import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.models import BayesianNetwork
import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

#构建网络
model = BayesianNetwork([('免疫力低下', '流感'),
                              ('免疫力低下', '感冒'),
                              ('着凉', '流感'),
                              ('着凉', '感冒'),
                              ('流感', '头疼'),
                              ('流感', '发烧'),
                              ('感冒', '头疼'),
                              ('感冒', '发烧')])
#设置参数
from pgmpy.factors.discrete import TabularCPD
cpd_m = TabularCPD(variable='免疫力低下', variable_card=2,
                      values=[[0.9], [0.1]])
cpd_c = TabularCPD(variable='着凉', variable_card=2,
                       values=[[0.3], [0.7]])
cpd_f= TabularCPD(variable='流感', variable_card=2,
                        values=[[0.72,0.80,0.13,0.08],
                                [0.28,0.20,0.87,0.92]],
                        evidence=['免疫力低下', '着凉'],
                        evidence_card=[2, 2])
cpd_cold= TabularCPD(variable='感冒', variable_card=2,
                        values=[[0.94,0.54,0.30,0.02],
                                [0.06,0.46,0.70,0.98]],
                        evidence=['免疫力低下', '着凉'],
                        evidence_card=[2, 2])

cpd_h = TabularCPD(variable='头疼', variable_card=2,
                      values=[[0.77,0.24,0.12,0.08], 
                              [0.23,0.76,0.88,0.92]],
                      evidence=['流感','感冒'], evidence_card=[2,2])
cpd_fev = TabularCPD(variable='发烧', variable_card=2,
                      values=[[0.86,0.45,0.49,0.91], 
                              [0.14,0.55,0.51,0.09]],
                      evidence=['流感','感冒'], evidence_card=[2,2])   
model.add_cpds(cpd_m, cpd_c, cpd_f,cpd_cold, cpd_h, cpd_fev)
#测试网络结构是否正确
print(model.check_model())

#可视化网络
G = nx.DiGraph([('免疫力低下', '流感'),
                              ('免疫力低下', '感冒'),
                              ('着凉', '流感'),
                              ('着凉', '感冒'),
                              ('流感', '头疼'),
                              ('流感', '发烧'),
                              ('感冒', '头疼'),
                              ('感冒', '发烧')])

#网络结构大致分为左右结构
left_nodes = ['头疼', '流感' , '免疫力低下']
right_nodes = ['发烧','感冒', '着凉' ]

options = {
    "font_size": 10,
    "node_size": 3000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5,
}
# 设置节点位置
pos = {n: (0, i) for i, n in enumerate(left_nodes)}
pos.update({n: (2, i +0.2) for i, n in enumerate(right_nodes)})
nx.draw_networkx(G, pos, **options)

# 设置轴的边距，以便不剪裁节点
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
plt.savefig('static/bayes.png',dpi=60)
plt.show()

#变量消除法
from pgmpy.inference import VariableElimination
infer = VariableElimination(model)
ret = infer.query(variables=['流感'], evidence={'免疫力低下': 0})
print(ret)





