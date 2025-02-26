# from pyclbr import Function
# from typing import Sequence
# import os
# import numpy as np
# from numpy.core.fromnumeric import mean
# from Class.VMType import VMType,PrivateCloudVMType
# # from Class.PrivateCloudVMType import PrivateCloudVMType
# import math
# import copy
# from Class.Task import Task
# from Class.File import File
# import operator

# class Objectives:
#     def __init__(self):
#         self.Cost = None #{'Cost':None}
#         self.Cmax= None #{'Cmax':None}
#         self.ResourceUtilization = None #{'ResourceUtilization':None}
#         self.NoHiberCost = None #{'NoHiberCost':None}
#         self.AlgorithmRunTime = None #{'AlgorithmRunTime':None}
#         self.NC = None #{'NC':None}
#         self.Speedup = None #{'Speedup':None}
#         self.SLR = None #{'SLR':None}
#         self.ART = None #{'ART':None}
#         self.Energy = None
#         self.missDDL = None
#         self.TotalTardiness = None 


# def SimplifyVMS(VMS):
#     k = 0
#     while True:
#         if k >=len(VMS):
#             break
#         if max(VMS[k].CompleteTime)==0:
#             del VMS[k]
#             k = 0
#         else:
#             k += 1
#     return VMS
 
# def VMStateAdjustment():
#     """
#     VM状态首先是开关机过程中的持续时间，
#     """
#     k = 1


# def caculateMultiWorkflowMakespan_Cost(resultWorkflow,WfDeadline,VMS):
#     PUBLICID  = 0
#     PRIVATEID = 1
#     HYBRIDCLOUD = [PUBLICID,PRIVATEID]
#     VMT = [VMType(),PrivateCloudVMType()]

#     Obj = Objectives()
#     Obj.Cmax = 0 # AWSCOLDSTARTUP  # Cmax 加上启动时间
#     for CloudID in HYBRIDCLOUD:
#         VMNums = len(VMS[CloudID])        
#         for VMnumID in range(VMNums):
#             TaskCoreID = 0
#             if len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])>0:                 
#                 taskID = len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID]) - 1
#                 FinishTime = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]  # 此处默认为单核执行
#                 if Obj.Cmax<FinishTime:
#                     Obj.Cmax = FinishTime
#     Obj.Cmax += AWSCOLDSTARTUP

#     Obj.Cost = 0
#     TTT = 1 # 1024*1024
#     CloudID = PUBLICID# 公有云 计算花费
#     VMNums = len(VMS[CloudID])        
#     for VMnumID in range(VMNums):                               #VM层
#         ProcessingTasks = False
#         for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores):
#             if len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])>0:
#                 ProcessingTasks = True
#                 break 
#         if ProcessingTasks:
#             # tatalData = 0
#             for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores) :        #VM的核层  
#                 time0 = AWSCOLDSTARTUP
#                 HStart0 = 0                   
#                 for taskID in range(len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])):
#                     task = VMS[CloudID][VMnumID].TaskCore[TaskCoreID][taskID]
#                     ## 计算传入传出数据费用
#                     # TransIN = 0
#                     # for preTask in resultWorkflow[task[0]][task[1]].inputs:                                
#                     #     if (resultWorkflow[task[0]][preTask.id].VMnum[0]==PRIVATEID):
#                     #         TransIN += preTask.size
#                     '''20220906修改取消传入费用'''
#                     TransOUT = 0
#                     for sucTask in resultWorkflow[task[0]][task[1]].outputs:                                
#                         if resultWorkflow[task[0]][sucTask.id].VMnum[0]==PRIVATEID:
#                             TransOUT += sucTask.size                           
#                     Obj.Cost += (TransOUT/TTT * VMT[CloudID].price_trans_data['OUT'])  # TransIN/TTT * VMT[CloudID].price_trans_data['IN'] +


#                     taskRunTime = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]
#                     time0 += taskRunTime
#                     # totalRuntimeofTasks += taskRunTime
#                     # tatalData += resultWorkflow[task[0]][task[1]].runtime
#                     if taskID==0:
#                         IdleTime = 0
#                     else:
#                         IdleTime = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID-1][1]
#                     if  (taskID>0) and(VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID-1][1]-HStart0>HibernateInterval)and(IdleTime> HibernateLowerBound ): 
#                         HibernateTime = IdleTime - AWSWARMSTARTUP

#                         Obj.Cost += max(math.ceil(time0)/INTERVAL,60) * (VMT[CloudID].M[VMS[CloudID][VMnumID].id  ] /3600 *INTERVAL)
#                         Obj.Cost += max(math.ceil(HibernateTime)/INTERVAL,60) * (ElasticIP /3600 *INTERVAL)
#                         time0 = AWSWARMSTARTUP
#                         HStart0 = VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]
#                         continue
#                 Obj.Cost += max(math.ceil(time0)/INTERVAL,60) * (VMT[CloudID].M[VMS[CloudID][VMnumID].id] /3600 *INTERVAL)
#                 # Obj.Cost += (tatalData/TTT * VMT[CloudID].price_store_data)

#     Obj.Energy = 0
#     totalTransEnergy = 0
#     for dagNum in range(len(resultWorkflow)):
#         for taskId in range(len(resultWorkflow[dagNum])):
#             VMnum = resultWorkflow[dagNum][taskId].VMnum
#             ## 计算传出数据能耗
#             for sucTask in resultWorkflow[dagNum][taskId].outputs: 
#                 sucVMnum = resultWorkflow[dagNum][sucTask.id].VMnum
#                 if (VMnum == sucVMnum)or((VMnum[0]==PUBLICID)and(sucVMnum[0]==PUBLICID)):
#                     DataTransferTime = 0
#                 else:                      
#                     DataTransferRate = min(VMT[VMnum[0]].B[VMS[VMnum[0]][VMnum[1]].id],  VMT[sucVMnum[0]].B[VMS[sucVMnum[0]][sucVMnum[1]].id]   )
#                     DataTransferTime = (sucTask.size/DataTransferRate * DTT)  #将传输时间放大DTT倍 
#                 totalTransEnergy += DataTransferTime/3600*VMT[PRIVATEID].trans_power
#     totalIdleEnergy = 0
#     totalDynaEnergy = 0
#     CloudID = PRIVATEID
#     VMNums = len(VMS[CloudID])        
#     for VMnumID in range(VMNums):                               #VM层
#         ProcessingTasks = False
#         for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores):
#             if len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])>0:
#                 ProcessingTasks = True
#                 break 
#         if ProcessingTasks:
#             totalRuntimeofTasks = 0 
#             for TaskCoreID in range(VMS[CloudID][VMnumID].NumCores) :     #VM的核层  
#                 for taskID in range(len(VMS[CloudID][VMnumID].TaskCore[TaskCoreID])):
#                     totalRuntimeofTasks += VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][1]-VMS[CloudID][VMnumID].VMTime[TaskCoreID][taskID][0]
#             tatalIdleTime = Obj.Cmax - totalRuntimeofTasks
#             totalDynaEnergy = totalRuntimeofTasks/3600*VMT[CloudID].dynamic_power[VMS[CloudID][VMnumID].id] 
#             totalIdleEnergy = tatalIdleTime/3600* VMT[CloudID].idle_power[VMS[CloudID][VMnumID].id]
#     Obj.Energy = totalTransEnergy + totalIdleEnergy + totalDynaEnergy

#     # Obj.TotalTardiness = 0
#     Tardiness = [] # [0 for i in range(len(resultWorkflow))]
#     for i in range(len(resultWorkflow)):
#         Cmax = 0
#         for j in range(len(resultWorkflow[i])):
#             Cmax = max(Cmax,resultWorkflow[i][j].FinishTime)
#         temp = max(0,Cmax-WfDeadline[i]) # +AWSCOLDSTARTUP
#         Tardiness.append(temp)
#     Obj.TotalTardiness = sum(Tardiness)
#     return Obj 

# def DetermineWhether2Dominate(salpA,salpB): ## Cost   Energy   TotalTardiness
#     ''' salpA 可支配 salpB  '''
#     if ((salpA.objectives.Cost<=salpB.objectives.Cost) and(salpA.objectives.Energy<=salpB.objectives.Energy)
#             and(salpA.objectives.TotalTardiness<=salpB.objectives.TotalTardiness)):
#         if ((salpA.objectives.Cost<salpB.objectives.Cost) or (salpA.objectives.Energy<salpB.objectives.Energy)
#              or (salpA.objectives.TotalTardiness<salpB.objectives.TotalTardiness)):
#             return True
#     return False

# def DetermineWhether2Equal(salpA,salpB): ## Cost   Energy   TotalTardiness
#     ''' salpA 等于 salpB  '''
#     if ((salpA.objectives.Cost==salpB.objectives.Cost) and(salpA.objectives.Energy==salpB.objectives.Energy)
#             and(salpA.objectives.TotalTardiness==salpB.objectives.TotalTardiness)):
#         return True  # 包含相等的
#     return False


# def caculateMakespan_Cost(resultWorkflow,VMS):

#     def breadth_first_search(workflow):#从前往后
#         def bfs():
#             while len(queue)> 0:
#                 node = queue.pop(0)
#                 booleanOrder[node] = True  
#                 for n in DAG[node].outputs:
#                     if (not n.id in booleanOrder) and (not n.id in queue):
#                         queue.append(n.id)
#                         order.append(n.id)     

#         DAG = copy.deepcopy(workflow)
#         DAG[len(DAG)] = Task(len(DAG),name = 'entry')
#         list1 = [taskId for taskId,task in DAG.items()]
#         for taskid in list1: #range(len(DAG)-1):
#             if DAG[taskid].inputs == []:   #原源节点 size = 0  JITCAWorkflow[len(JITCAWorkflow)-1]
#                 tout = File('EntryOut', id = len(DAG)-1)
#                 DAG[taskid].inputs.append(tout)
#                 tout = File('Entry', id = taskid)
#                 DAG[len(DAG)-1].addOutput(tout)

#         root = len(DAG)-1
#         queue = []
#         order = []
#         booleanOrder = {}  
#         queue.append(root)
#         order.append(root)
#         bfs()
#         order.remove(order[0])
#         return order

#     def getCP_MIN(workflow):
#         scheduleOrder = breadth_first_search(workflow)
#         EST = [-1 for each in range(len(workflow))] # {} #
#         EFT = [-1 for each in range(len(workflow))]  #{} #
#         SequentialExecutionTimeFastest_SingleProcessor = 0
#         MET = [0 for each in range(len(workflow))]  # {}#
#         for taskid,task in workflow.items():
#             MET[taskid] =task.runtime/max(VMType().ProcessingCapacity)
#             SequentialExecutionTimeFastest_SingleProcessor += MET[taskid]

#         CostCheapestSchedule_SingleProcessor = 0
#         for taskid,task in workflow.items():
#             CostCheapestSchedule_SingleProcessor += task.runtime/min(VMType().ProcessingCapacity)*min(VMType().M)

#         while True:
#             if scheduleOrder == []:
#                 break    

#             for taskid in scheduleOrder:
#                 parents = workflow[taskid].inputs
#                 if parents != []:
#                     boolean1 = False
#                     for each in parents:
#                         if EST[each.id] == -1:
#                             boolean1 = True
#                             break
#                     if boolean1:
#                         continue
#                     listPEST = [ EST[each.id] + MET[each.id] for each in parents  ]
#                     EST[taskid] = max(listPEST)
#                 else:
#                     EST[taskid] = 0
#                 EFT[taskid] = EST[taskid] + MET[taskid]
#                 scheduleOrder.remove(taskid)
#                 break
#         CP_MIN = max(EFT)
#         return CP_MIN,SequentialExecutionTimeFastest_SingleProcessor,CostCheapestSchedule_SingleProcessor

#     def getART(workflow,VMS,VMT):
#         scheduleOrder = breadth_first_search(workflow)
#         ART_Task = [None for each in range(len(workflow))] # {} #
#         # CT = [-1 for each in range(len(workflow))] # {} #
#         # EFT = [-1 for each in range(len(workflow))]  #{} #
#         while True:
#             if scheduleOrder == []:
#                 break
#             for taskid in scheduleOrder:
#                 parents = workflow[taskid].inputs                 
#                 if parents != []:
#                     FTCT = 0
#                     VMnumID = workflow[taskid].VMnum
#                     for parent in parents:
#                         DataTransferRate = None
#                         if VMnumID == workflow[parent.id].VMnum:
#                             DataTransferRate = 0
#                         elif   VMS[VMnumID].id <= VMS[workflow[parent.id].VMnum].id:
#                             DataTransferRate = VMT.B[VMS[VMnumID].id]
#                         else:
#                             DataTransferRate = VMT.B[VMS[workflow[parent.id].VMnum].id]
#                         TransTime = 0 if DataTransferRate == 0 else (parent.size/DataTransferRate)
#                         FTCT = max(FTCT,workflow[parent.id].FinishTime + TransTime)
#                     ART_Task[taskid] = workflow[taskid].FinishTime - FTCT
#                 else:
#                     ART_Task[taskid] = workflow[taskid].StartTime                
#                 scheduleOrder.remove(taskid)
#                 break        
#         ART = mean(ART_Task)
#         return ART

#     Obj = Objectives()
#     VMT = VMType() 
#     VMNums = len(VMS)
#     Obj.Cost = 0
#     Obj.NoHiberCost = 0
#     Obj.Cmax = 0
#     Obj.ResourceUtilization = 0
#     for VMnumID in range(VMNums):                               #VM层
#         ProcessingTasks = False
#         for TaskCoreID in range(VMS[VMnumID].NumCores):
#             if len(VMS[VMnumID].TaskCore[TaskCoreID])>0:
#                ProcessingTasks = True
#                break 
#         if ProcessingTasks:
#             totalRuntimeofTasks = 0
            
#             for TaskCoreID in range(VMS[VMnumID].NumCores) :        #VM的核层  
#                 time0 = AWSCOLDSTARTUP
#                 HStart0 = 0                   
#                 for taskID in range(len(VMS[VMnumID].TaskCore[TaskCoreID])):
#                     task = VMS[VMnumID].TaskCore[TaskCoreID][taskID]
#                     taskRunTime = VMS[VMnumID].VMTime[TaskCoreID][taskID][1]-VMS[VMnumID].VMTime[TaskCoreID][taskID][0]
#                     time0 += taskRunTime
#                     totalRuntimeofTasks += taskRunTime
#                     IdleTime = VMS[VMnumID].VMTime[TaskCoreID][taskID][0]-VMS[VMnumID].VMTime[TaskCoreID][taskID-1][1]
#                     if  (taskID>0) and(VMS[VMnumID].VMTime[TaskCoreID][taskID-1][1]-HStart0>HibernateInterval)and(
#                         VMS[VMnumID].VMTime[TaskCoreID][taskID][0]-VMS[VMnumID].VMTime[TaskCoreID][taskID-1][1]> HibernateLowerBound ): 
#                         HibernateTime = IdleTime - AWSWARMSTARTUP

#                         Obj.Cost += max(math.ceil(time0)/INTERVAL,60) * (VMT.M[VMnumID%VMT.m] /3600 *INTERVAL)
#                         Obj.Cost += max(math.ceil(HibernateTime)/INTERVAL,60) * (ElasticIP /3600 *INTERVAL)
#                         time0 = AWSWARMSTARTUP
#                         HStart0 = VMS[VMnumID].VMTime[TaskCoreID][taskID][0]
#                         continue
#                 Obj.Cost += max(math.ceil(time0)/INTERVAL,60) * (VMT.M[VMnumID%VMT.m] /3600 *INTERVAL)
#             TaskCoreID = 0
#             taskID = 0
#             StartTime = VMS[VMnumID].VMTime[TaskCoreID][taskID][0]  # 此处默认为单核执行
#             taskID = len(VMS[VMnumID].TaskCore[TaskCoreID]) - 1
#             FinishTime = VMS[VMnumID].VMTime[TaskCoreID][taskID][1]  # 此处默认为单核执行
#             Obj.ResourceUtilization  += (1-totalRuntimeofTasks/(FinishTime-StartTime+AWSCOLDSTARTUP))
#             Obj.NoHiberCost += max(math.ceil((FinishTime-StartTime+AWSCOLDSTARTUP))/INTERVAL,60) * (VMT.M[VMnumID%VMT.m] /3600 *INTERVAL)
#             if Obj.Cmax<FinishTime:
#                 Obj.Cmax = FinishTime  
#     Obj.Cmax += AWSCOLDSTARTUP  # Cmax 加上启动时间
                        
#     CP_MIN,SequentialExecutionTimeFastest_SingleProcessor,CostCheapestSchedule_SingleProcessor = getCP_MIN(resultWorkflow)
#     Obj.SLR = Obj.Cmax/CP_MIN
#     Obj.Speedup = SequentialExecutionTimeFastest_SingleProcessor/Obj.Cmax
#     Obj.NC = Obj.Cost/CostCheapestSchedule_SingleProcessor
#     Obj.ART = getART(resultWorkflow,VMS,VMT)
#     return Obj 
    
#     #.Cost,NoHiberCost,Cmax,ART,Speedup,ResourceUtilization
#     # return Cost,NoHiberCost,Cmax,SLR,Speedup,ResourceUtilization # NoHiberCost 为没有休眠待机模式时的价格
#     # return Cost,NC,Cmax,SLR,Speedup,ResourceUtilization
#           # 小， 小， 小， 小，大，      小

# # global workflow 0 Montage 100.xml  .xml  .xml  Epigenomics_24.xml   CyberShake_30.xml   
# # WorkFlowTestName = 'Montage_25'   #  CyberShake_100  Inspiral_30   Sipht_30                
# DTT = 1                 # 传输时间放大倍数 00
# PUBLICID  = 0
# PRIVATEID = 1
# # VMNums = 2 * len(VMType().ProcessingCapacity)  # 10             # VM的数量  假设可供选择的VM总量为类型的整数倍即 5 10 15 20...
# # minECU = min(VMType().ProcessingCapacity)  # 10             # min ProcessingCapacity
# # maxECU = max(VMType().ProcessingCapacity)
# # minB = min(VMType().B)  # 1                # min 内网带宽
# # maxB = max(VMType().B)

# def STARTUP(CloudID):
#     if CloudID==PUBLICID:
#         return AWSCOLDSTARTUP
#     else:
#         return 0


# minECU = min(PrivateCloudVMType().ProcessingCapacity)  # 10             # min ProcessingCapacity
# maxECU = max(PrivateCloudVMType().ProcessingCapacity)
# minB = min(PrivateCloudVMType().B)  # 1                # min 内网带宽
# maxB = max(PrivateCloudVMType().B)
# NUMofPrivateCloudVM = [3,3,4]   #[1,1,1] # 不能为0   [0 for i in PrivateCloudVMType().P]



# ObjectiveNumbers = ['Cost','ResourceUtilization','NoHiberCost','AlgorithmRunTime']
# AlgorithmNumbers = 5
# ReferenceProcessingCapacity = VMType().ProcessingCapacity[1]

# HibernateLowerBound = 60 # 启动休眠的最低限制
# AWSCOLDSTARTUP = 55.9  # [2021 启动时间] An Empirical Analysis of VM Startup Times in Public IaaS Clouds An Extended Report
# AWSWARMSTARTUP = 34.0
# AWSSTOPPING = 5.6 
# INTERVAL = 1 # 计费时间间隔，单位：秒   # 60 # 更改为60s 原因是每次启动后，最低收取一分钟费用。   
# ElasticIP = 0.005   # Elastic IP (EIP)  您可以免费将一个 Elastic IP (EIP) 地址与运行的实例相关联。
#                     # 如果将其他 EIP 与该实例关联，则需要按比例对每小时与该实例关联的其他 EIP 付费。
#                     # 0.005 USD（按比例每小时与正在运行的实例相关联的额外 IP 地址）
# SuitVM = 1                    
# HibernateInterval = 120 
# repeatTmies = 10


# listWorkflowNum = np.load(os.getcwd()+'/FininaltestInstanceIndex.npy',allow_pickle=True)
# # FininaltestInstanceIndex = []
# # listWorkflowNum2 = np.load(os.getcwd()+'\\testInstanceIndex_Lessthan1000.npy',allow_pickle=True) # 
# # list2 = [3,0,7,6,9,10,15,14]
# # for i in list2:
# #     FininaltestInstanceIndex.append(listWorkflowNum2[i])
# # listWorkflowNum = np.load(os.getcwd()+'\\testInstanceIndex.npy',allow_pickle=True) # _Lessthan1000
# # list0 = [0,3,1,11,9,10,18,19,16]
# # for i in list0:
# #     FininaltestInstanceIndex.append(listWorkflowNum[i])
# # np.save(os.getcwd()+'\\FininaltestInstanceIndex.npy', FininaltestInstanceIndex)
# # k = 1


# # def _init():
# #     global _global_dict
# #     _global_dict = {}
 
# def set_globalvalue(name, value):
#     _global_dict[name] = value
 
# def get_globalvalue(name, defValue=None):
#     try:
#         return _global_dict[name]
#     except KeyError:
#         return defValue
# _global_dict = {}



# class ObjectivesNopermutation:
#     def __init__(self):
#         self.Cost = None #{'Cost':None}
#         self.Cmax= None
#         self.Energy = None
#         self.TotalTardiness = None
#         self.NumPBVMs = None

# def RemovePermutation(tempPF):
#     PF = []
#     PBVMs = []
#     '''NF '''
#     for i in range(len(tempPF)-1):
#         Obj = ObjectivesNopermutation()
#         Obj.Cost =  tempPF[i].objectives.Cost
#         Obj.Cmax =  tempPF[i].objectives.Cmax
#         Obj.Energy =  tempPF[i].objectives.Energy
#         Obj.TotalTardiness =  tempPF[i].objectives.TotalTardiness      

#         Obj.NumPBVMs = 0
#         TaskCoreID = 0
#         for CloudID in [0]: # ,1
#             VMnum = len(tempPF[i].VMSchedule[CloudID])
#             for VMnumID in range(VMnum):
#                 if tempPF[i].VMSchedule[CloudID][VMnumID].CompleteTime[TaskCoreID]>0:
#                     Obj.NumPBVMs += 1
#         PBVMs.append(Obj.NumPBVMs)
#         PF.append(Obj)
#     PF.append({'RunTime':tempPF[len(tempPF)-1], 'AvgPBVMs':math.trunc(np.average(PBVMs))})
#     return PF

