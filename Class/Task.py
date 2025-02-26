'''
Created on 15-Mar-2017

@author: itadmin
'''
# from GPClass.function_terminal import *
from copy import deepcopy
import math
# from GPClass.multiCloudSystem import InstanceList

class Task:
    
    def __init__(self, id, name=None,namespace = None, jobsetname= None, 
                 inputs=[], outputs = [],runtime=0, MI=0,
                 terminal_task = None,Category =None,configuration_Container = [],FinishTime = None, ):
        self.id = id               #parents=[], storage=0 ,core=None,deepcopy(TASKTERMINAL_dict)
        self.name = name
        self.namespace = namespace
        self.Category = Category
        self.jobsetname = jobsetname
        self.runtime = runtime  # 等于权重
        self.Invocations = None
        self.MI = MI
        # self.weight = None
        self.inputs =list(inputs)
        self.outputs =list(outputs)
        # self.storage =  storage
        # self.core = core
        self.terminal_task = terminal_task #deepcopy(TASKTERMINAL_dict)  # deepcopy(TASKTERMINAL)
            # # SUBDEADLINE                 #  子截止时间
            # # NUMBERSCHILDREN             #  子任务的个数
            # # UPWARDRANK                  #  HEFT rank值
            # # EXECUTETIME                 #  执行时间
            # # AVERAGECOMMUNICATIONTIME    #  平均通讯时间
            # # WAITINGTIME                 #  等待时间 
            # # 对于任务，其执行时间正比于执行花费，故不在考虑其花费。考虑了与父任务的平均通信时间
        # self.averageET = None   # 平均执行时间
        
        # self._instanceTerminal = deepcopy(INSTANCETERMINAL)       
        self.minCPU = None
        self.minMEM = None
        self.runtimePerCPU_Memory = None
        self._given_runtime = None

        self.configuration_Container = configuration_Container

        self.EST = None         # 最早开始时间
        self.EFT = None         # 最早完成时间
        self.LFT = None         # 最晚完成时间
        self.Assigned = None       # 是否已调度
        self.Level = None       # 所在拓扑层
        # self.SubDeadline = None 
        self.XFT = 0
        self.MET= 0

        # self.currentCompletionTime = 0
        self.VMnum = None
        self.schedulingTime = None # which includes the time to caculate the priority parameters and the time to select the appraopriate instance.
        # self.VMcore = None
        self.StartTime = None 
        self.AET = None   # 实际执行时间  
        self.FinishTime = FinishTime
        # self.StatusTable = None
        self._given_start_time = None
        self._given_end_time = None 
        self._given_plan_cpu = None 
        self._given_plan_mem = None
        self._given_instance_num = None  
    def __repr__(self):
        return self.name#"<File %s>" %     
    # @property
    # def FinishTime(self):
    #     return self.configuration_Container[-1].FinishTime # self.StartTime + self.AET
    @property
    def subDeadline(self):
        return self.LFT
    @property
    def weight(self):
        return self.runtime

    def calculateRunTime(self,MIPS):
        return self.weight/MIPS

    # def assignTask(self,)

    def addjobsetname(self, jobsetname):
        self.jobsetname = jobsetname

    def addInput(self, file_):
        self.inputs.append(file_) #add(file_)#
    
    def addOutput(self, file_):
        self.outputs.append(file_) #add(file_)#

    def getRuntime(self,CPU,Memory):
        if self.minCPU<=CPU and self.minMEM<=Memory:
            if self.Category[0]=='00':
                return self.runtimePerCPU_Memory/(self.minCPU * self.minMEM)
            elif self.Category[0]=='01':
                return self.runtimePerCPU_Memory/(self.minCPU * Memory)
            elif self.Category[0]=='10':
                return self.runtimePerCPU_Memory/(CPU * self.minMEM)
            elif self.Category[0]=='11':
                return self.runtimePerCPU_Memory/(CPU * Memory)
        else:
            return False

    # def getAverageRuntime(self,CPU,Memory):
    #     aveCPU = math.ceil(CPU)/2
    #     aveMemory = math.ceil(Memory)/2
    #     if self.minCPU<=aveCPU and self.minMEM<=aveMemory:
    #         if self.Category[0]=='00':
    #             return self.runtimePerCPU_Memory/(self.minCPU * self.minMEM)
    #         elif self.Category[0]=='01':
    #             return self.runtimePerCPU_Memory/(self.minCPU * aveMemory)
    #         elif self.Category[0]=='10':
    #             return self.runtimePerCPU_Memory/(aveCPU * self.minMEM)
    #         elif self.Category[0]=='11':
    #             return self.runtimePerCPU_Memory/(aveCPU * aveMemory)
    #     else:
    #         return False




        # return self.runtime

# class DAGTask:    
#     def __init__(self, id):
#         self.id = id         
#         self.VMnum = None
#         self.VMcore = None
#         self.runtime = 0
#         self.StartTime = 0   
#         self.FinishTime = 0   
#     def __repr__(self):
#         return self.id  

# class caculateCmax_Cost():
#     def __init__(self, StartTime,FinishTime):
#         for taskID,task in self.items():

