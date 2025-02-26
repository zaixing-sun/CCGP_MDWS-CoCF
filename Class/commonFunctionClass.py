import os
import numpy as np
from copy import deepcopy
# import GlobalResource
# from Class.Task import Task
# from Class.File import File
# from GPClass.workflowClass import workflowClass
from random import randint,seed,random
# from GPClass.function_terminal_3D import WORKFLOWTERMINAL_dict,TASKTERMINAL_dict # ,CLOUDPLATFORMTERMINAL_dict
# from GPClass.multiCloudSystem_3D import MULTICLOUDsystem
# import matplotlib.pyplot as plt



class Objectives:
    def __init__(self):
        self.Cost = None
        self.Cmax= None 
        self.ResourceUtilization = None 
        self.AlgorithmRunTime = None
        self.Speedup = None
        self.SLR = None
        self.Energy = None
        self.missDDL = None
        self.TotalTardiness = None
        self.cost_VM = None
        self.cost_FaaS = None
        self.cost_Trans = None
        self.successfulrate = None
        self.deadlineDeviation = None
    def __repr__(self):
        return 'Objectives'
    @property
    def TotalCost(self):
        return self.Cost
    @property
    def Makespan(self):
        return self.Cmax
    @property
    def AverageResourceUtilization(self):
        return self.ResourceUtilization
    @property
    def TotalEnergyConsumption(self):
        return self.Energy




# NUMGENERATION = 51  # 迭代次数
# POPSIZE = 11 # 种群规模 300
# MAXDEPTH = 6            # 树的最大深度
# MINDEPTH = 2            # 树的最小深度
# seed(10)
# def depthLimit():
#     return randint(MINDEPTH,MAXDEPTH)
# RATECROSSOVER = 0.85
# RATEMUTATION = 0.1
# REPRODUCTION = 0.05