

import os
import numpy as np
from copy import deepcopy
# import GlobalResource
from Class.Task import Task
from Class.File import File
from GPClass.workflowClass import workflowClass # ,DeadlineFactor
from random import randint,seed,random
from GPClass.function_terminal_3D import WORKFLOWTERMINAL_dict,TASKTERMINAL_dict # ,CLOUDPLATFORMTERMINAL_dict
# from GPClass.multiCloudSystem import MULTICLOUDsystem
from Environments.CLOUDFOGsystem import CLOUDFOGsystem
# import matplotlib.pyplot as plt


# DeadlineFactor = 0.85


def getDAGTopologicalLevel_End(tempDAG):  
    '''以下是从根节点起分层 目前的7种工作流结构，
        只有适用于SIPHT工作流，其他工作流不受影响，
        故当SIPHT工作流效果不好时可以使用 '''
    setLevelNode = set() 
    dictNodeLevel = {}
    intflag = 0
    while True:
        for name,task in tempDAG.items():  
            if (not(name in setLevelNode)):
                if (len(task.outputs)==0):         
                    setLevelNode.add(name)
                    dictNodeLevel[name] = 0
                    intflag += 1     
                # elif  (len(task.inputs)==0):   
                #     setLevelNode.add(name)
                #     dictNodeLevel[name] = 0
                #     intflag += 1 
                else:
                    sucNodedict = {}
                    for each in range(len(task.outputs)):
                        if task.outputs[each].id in setLevelNode:
                            sucNodedict[task.outputs[each].id] = dictNodeLevel[task.outputs[each].id]
                        else:
                            break
                    if len(sucNodedict)==len(task.outputs):
                        dictNodeLevel[name] = max(list(sucNodedict.values()))+1
                        setLevelNode.add(name)
                        intflag += 1
        if intflag == len(tempDAG):
            break
    RootNode = []
    for name,task in tempDAG.items():
        if  (len(task.inputs)==0):   
            RootNode.append(name)

    DAGLevel_RootNode = [[] for i in range(max(list(dictNodeLevel.values()))+1)]
    for key1,value1 in dictNodeLevel.items():
        DAGLevel_RootNode[value1].append(key1)
        tempDAG[key1].Level = value1
    return DAGLevel_RootNode,RootNode

# def readWorkflowData_End(fileName):
#     WfW = workflowClass()
#     WfW.name = fileName[0:-4]
#     WfW.DAG = np.load('data_npy/'+fileName,allow_pickle=True).item() # os.getcwd()+'/
#     seed(os.path.getsize('data_npy/'+fileName))  # os.getcwd()+'/
#     WfW.releaseTime = 100*random()  # randint(0,100)  ##### 随机生成工作流的到达时间
#     WfW.deadlineFactor = WfW.DAG.pop('DeadlineFactor')   
#     WfW.deadline = WfW.DAG.pop('Deadline')    
#     WfW.unscheduledTaskNumber = len(WfW.DAG)
#     WfW.DAGLevel = getDAGTopologicalLevel_End(WfW.DAG)    
#     # WfW.terminal_workflow = WORKFLOWTERMINAL_dict()
#     # for name,task in WfW.DAG.items():
#     #     WfW.DAG[name].terminal_task = TASKTERMINAL_dict()
#     WfW.given_DAGLevel(WfW.DAGLevel)   # WfW.__DAGLevel = copy.deepcopy(WfW.DAGLevel) 
#     return WfW

def getDAGTopologicalLevel(tempDAG):  
    setLevelNode = set() 
    dictNodeLevel = {}
    intflag = 0
    while True:
        for name,task in tempDAG.items():  
            if (not(name in setLevelNode)):
                if (len(task.inputs)==0):         
                    setLevelNode.add(name)
                    dictNodeLevel[name] = 0
                    intflag += 1     
                elif  (len(task.outputs)==0):   
                    setLevelNode.add(name)
                    dictNodeLevel[name] = -1
                    intflag += 1 
                else:
                    preNodedict = {}
                    for each in range(len(task.inputs)):
                        if task.inputs[each].id in setLevelNode:
                            preNodedict[task.inputs[each].id] = dictNodeLevel[task.inputs[each].id]
                        else:
                            break
                    if len(preNodedict)==len(task.inputs):
                        dictNodeLevel[name] = max(list(preNodedict.values()))+1
                        setLevelNode.add(name)
                        intflag += 1
        if intflag == len(tempDAG):
            break
    ## 以下是从源节点起分层
    DAGLevel = [[] for i in range(max(dictNodeLevel.values())+2)]  
    for key1,value1 in dictNodeLevel.items():
        if value1 == -1:
            DAGLevel[max(dictNodeLevel.values())+1].append(key1)
            tempDAG[key1].Level = max(dictNodeLevel.values())+1
        else:    
            DAGLevel[value1].append(key1)
            tempDAG[key1].Level = value1

    ## 按执行时间降序排列
    for k in range(len(DAGLevel)):
        for i in range(len(DAGLevel[k])-1):
            for j in range(i+1,len(DAGLevel[k])):
                if tempDAG[DAGLevel[k][i]].runtime<tempDAG[DAGLevel[k][j]].runtime:
                    DAGLevel[k][i],DAGLevel[k][j] = DAGLevel[k][j], DAGLevel[k][i]
    return DAGLevel

def readAlibabaData(fileName):

    WfW = np.load('data_npy/'+fileName,allow_pickle=True).item() # os.getcwd()+'/
    seed(os.path.getsize('data_npy/'+fileName))  # os.getcwd()+'/
    # WfW.releaseTime = 100*random()  # randint(0,100)  ##### 随机生成工作流的到达时间  
    WfW.unscheduledTaskNumber = len(WfW.DAG)
    WfW.DAGLevel = getDAGTopologicalLevel(WfW.DAG)    
    WfW.terminal_workflow = WORKFLOWTERMINAL_dict()
    for name,task in WfW.DAG.items():
        WfW.DAG[name].terminal_task = TASKTERMINAL_dict()
    WfW.given_DAGLevel(WfW.DAGLevel)   # WfW.__DAGLevel = copy.deepcopy(WfW.DAGLevel) 
    return WfW


def readWorkflowData(fileName):
    WfW = workflowClass()
    WfW.name = fileName[0:-4]
    WfW.DAG = np.load('data_npy/'+fileName,allow_pickle=True).item() # os.getcwd()+'/
    seed(os.path.getsize('data_npy/'+fileName))  # os.getcwd()+'/
    WfW.releaseTime = 100*random()  # randint(0,100)  ##### 随机生成工作流的到达时间
    try:
        WfW.deadlineFactor = WfW.DAG.pop('DeadlineFactor')   
    except:
        pass
    WfW.deadline = WfW.DAG.pop('Deadline')    
    WfW.unscheduledTaskNumber = len(WfW.DAG)
    WfW.DAGLevel = getDAGTopologicalLevel(WfW.DAG)    
    WfW.terminal_workflow = WORKFLOWTERMINAL_dict()
    for name,task in WfW.DAG.items():
        WfW.DAG[name].terminal_task = TASKTERMINAL_dict()
    WfW.given_DAGLevel(WfW.DAGLevel)   # WfW.__DAGLevel = copy.deepcopy(WfW.DAGLevel) 
    return WfW

def getMET_SubDeadline(workflow):
    MET = [0 for each in range(len(workflow))]  # {}#
    for taskid,task in workflow.items():
        if task.Category[0]== 'vm':
            MET[taskid] = task.runtime /MULTICLOUDsystem.averageMIPS.vm
        elif task.Category[0]== 'FaaS':
            MET[taskid] = task.runtime /MULTICLOUDsystem.averageMIPS.FaaS  
        elif task.Category[0]== 'Office365':
            MET[taskid] = task.runtime /MULTICLOUDsystem.averageMIPS.Office365 
    return MET

def breadth_first_search_SubDeadline(workflow):#从前往后
    def bfs():
        while len(queue)> 0:
            node = queue.pop(0)
            booleanOrder[node] = True  
            for n in DAG[node].outputs:
                if (not n.id in booleanOrder) and (not n.id in queue):
                    queue.append(n.id)
                    order.append(n.id)     

    DAG = deepcopy(workflow)
    DAG[len(DAG)] = Task(len(DAG),name = 'entry')
    list1 = [taskId for taskId,task in DAG.items()]
    for taskid in list1: 
        if DAG[taskid].inputs == []: 
            tout = File('EntryOut', id = len(DAG)-1)
            DAG[taskid].inputs.append(tout)
            tout = File('Entry', id = taskid)
            DAG[len(DAG)-1].addOutput(tout)

    root = len(DAG)-1
    queue = []
    order = []
    booleanOrder = {}  
    queue.append(root)
    order.append(root)
    bfs()
    order.remove(order[0])
    return order

def getEST_SubDeadline(workflow,MET,scheduleOrder):
    # scheduleOrder = breadth_first_search_SubDeadline(workflow)
    EST = [-1 for each in range(len(workflow))] # {} #
    EFT = deepcopy(EST) # [-1 for each in range(len(workflow))]  #{} #
    while True:
        if scheduleOrder == []:
            break    

        for taskid in scheduleOrder:
            parents = workflow[taskid].inputs
            if parents != []:
                boolean1 = False
                for each in parents:
                    if EST[each.id] == -1:
                        boolean1 = True
                        break
                if boolean1:
                    continue
                listPEST = [ EST[each.id] + MET[each.id] + each.size/CLOUDFOGsystem.bandwidth_Fog for each in parents  ] #GlobalResource.maxB
                EST[taskid] = max(listPEST)
            else:
                EST[taskid] = 0
            EFT[taskid] = EST[taskid] + MET[taskid]
            scheduleOrder.remove(taskid)
            break
    return EST,EFT

def getLFT(workflow,Deadline,scheduleOrder):
    # scheduleOrder = breadth_first_search_SubDeadline(workflow)
    scheduleOrder.reverse()
    LFT = [-1 for each in range(len(workflow))]  #{} #
    LST = [-1 for each in range(len(workflow))]  #{} #
    while True:
        if scheduleOrder == []:
            break
        for taskid in scheduleOrder:
            child_1 = workflow[taskid].outputs
            if child_1 != []:
                boolean1 = False
                for each in child_1:
                    if LFT[each.id] == -1:
                        boolean1 = True
                        break
                if boolean1:
                    continue                    
                listCLFT = [ (LFT[each.id] - workflow[each.id].getRuntime(CLOUDFOGsystem.representativeType().ECU, CLOUDFOGsystem.representativeType().Memory) - each.size/CLOUDFOGsystem.bandwidth_Fog) for each in child_1  ] # GlobalResource.maxB
                LFT[taskid] = min(listCLFT)
            else:
                LFT[taskid] = Deadline  
            LST[taskid] = LFT[taskid] - workflow[taskid].getRuntime(CLOUDFOGsystem.representativeType().ECU, CLOUDFOGsystem.representativeType().Memory)
            scheduleOrder.remove(taskid)
            break
    return LFT,LST

def getRank_u(workflow,scheduleOrder):
    # scheduleOrder = breadth_first_search_SubDeadline(workflow)
    scheduleOrder.reverse()
    Rank_u = [-1 for each in range(len(workflow))] 
    while True:
        if scheduleOrder == []:
            break
        for taskid in scheduleOrder:
            child_1 = workflow[taskid].outputs
            if child_1 != []:
                boolean1 = False
                for each in child_1:
                    if Rank_u[each.id] == -1:
                        boolean1 = True
                        break
                if boolean1:
                    continue
                Rank_u[taskid] = workflow[taskid].getRuntime(CLOUDFOGsystem.representativeType().ECU, CLOUDFOGsystem.representativeType().Memory) + max([(Rank_u[each.id] + each.size/CLOUDFOGsystem.bandwidth_Fog) for each in child_1] ) # GlobalResource.maxB
            else:
                Rank_u[taskid] = workflow[taskid].getRuntime(CLOUDFOGsystem.representativeType().ECU, CLOUDFOGsystem.representativeType().Memory)
            scheduleOrder.remove(taskid)
            break
    return Rank_u

def getSubDeadline(workflow,releaseTime,Deadline,DeadlineFactor):
    scheduleOrder = breadth_first_search_SubDeadline(workflow)
    categoryList = ["00","01","10","11"]  
    TASKCATEGORY = {}
    for i in range(len(categoryList)):
        TASKCATEGORY[categoryList[i] ] = i+1

    # MET = getMET_SubDeadline(workflow)
    # # EST,EFT = getEST_SubDeadline(workflow,MET,deepcopy(scheduleOrder))  #  /GlobalResource.maxB
    # # # Deadline = max(EFT)*DeadlineFactor
    LFT,LST = getLFT(workflow,Deadline,deepcopy(scheduleOrder))
    Rank_u = getRank_u(workflow,deepcopy(scheduleOrder))
    for taskid,task in workflow.items():
        if workflow[taskid].outputs ==[]: 
            workflow[taskid].XFT = LFT[taskid]
        else:
            workflow[taskid].XFT = 0.95*LFT[taskid]  # # 对 sub-deadline 缩放
        workflow[taskid].LFT = LFT[taskid]
        workflow[taskid].terminal_task.SUBDEADLINE = workflow[taskid].XFT + releaseTime
        workflow[taskid].terminal_task.NUMBERSCHILDREN = len(workflow[taskid].outputs)
        workflow[taskid].terminal_task.NUMBERSFATHER = len(workflow[taskid].inputs)
        workflow[taskid].terminal_task.EXECUTETIME = workflow[taskid].getRuntime(CLOUDFOGsystem.representativeType().ECU, CLOUDFOGsystem.representativeType().Memory)
        workflow[taskid].terminal_task.MINCPU = workflow[taskid].minCPU
        workflow[taskid].terminal_task.MINMEMORY = workflow[taskid].minMEM
        workflow[taskid].terminal_task.TASKCATEGORY = TASKCATEGORY[workflow[taskid].Category[0]]

        # if workflow[taskid].Category[0]== 'vm':
        #     # MULTICLOUDsystem.bandwidth_in1Cloud
        #     workflow[taskid].terminal_task.EXECUTETIME = workflow[taskid].runtime /MULTICLOUDsystem.averageMIPS.vm  #GlobalResource.maxECU MULTICLOUDsystem.bandwidth_in1Cloud
        # elif workflow[taskid].Category[0]== 'FaaS':
        #     workflow[taskid].terminal_task.EXECUTETIME = workflow[taskid].runtime /MULTICLOUDsystem.averageMIPS.FaaS  #GlobalResource.maxECU MULTICLOUDsystem.bandwidth_in1Cloud
        # elif workflow[taskid].Category[0]== 'Office365':
        #     workflow[taskid].terminal_task.EXECUTETIME = workflow[taskid].runtime /MULTICLOUDsystem.averageMIPS.Office365  #GlobalResource.maxECU MULTICLOUDsystem.bandwidth_in1Cloud
        
        aveCT = np.average( [each.size/CLOUDFOGsystem.bandwidth_Fog for each in workflow[taskid].outputs] ) if len(workflow[taskid].outputs)!= 0 else 0   # GlobalResource.maxB
        workflow[taskid].terminal_task.AVERAGECOMMUNICATIONTIME = aveCT
        workflow[taskid].terminal_task.UPWARDRANK = Rank_u[taskid]
    # return Deadline
    # k = 1


# def ResetDeadline(workflow,DeadlineFactor):
#     MET = getMET_SubDeadline(workflow)          #  /GlobalResource.maxECU
#     EST,EFT = getEST_SubDeadline(workflow,MET)  #  /GlobalResource.maxB
#     Deadline = max(EFT)*DeadlineFactor
#     return Deadline

def getEFT_Deadline(workflow,scheduleOrder):
    # scheduleOrder = breadth_first_search_SubDeadline(workflow)
    EST = [-1 for each in range(len(workflow))] # {} #
    EFT = deepcopy(EST) # [-1 for each in range(len(workflow))]  #{} #
    while True:
        if scheduleOrder == []:
            break    

        for taskid in scheduleOrder:
            parents = workflow[taskid].inputs
            if parents != []:
                boolean1 = False
                for each in parents:
                    if EST[each.id] == -1:
                        boolean1 = True
                        break
                if boolean1:
                    continue
                
                listPEST = [ EST[each.id] + workflow[each.id].getRuntime(CLOUDFOGsystem.representativeType().ECU, CLOUDFOGsystem.representativeType().Memory) + each.size/CLOUDFOGsystem.bandwidth_Fog for each in parents  ] #GlobalResource.maxB
                EST[taskid] = max(listPEST)
            else:
                EST[taskid] = 0
            EFT[taskid] = EST[taskid] + workflow[taskid].getRuntime(CLOUDFOGsystem.representativeType().ECU, CLOUDFOGsystem.representativeType().Memory)  # MET[taskid]
            scheduleOrder.remove(taskid)
            break
    return EFT


def getDeadline(workflow,DeadlineFactor):
    scheduleOrder = breadth_first_search_SubDeadline(workflow)
    EFT = getEFT_Deadline(workflow,deepcopy(scheduleOrder))  #  /GlobalResource.maxB
    Deadline = max(EFT)*DeadlineFactor
    return Deadline




# TASKTERMINAL = {'SUBDEADLINE':0, 'NUMBERSCHILDREN':0, 'UPWARDRANK':0,
#                 'EXECUTETIME':0, 'AVERAGECOMMUNICATIONTIME':0,} 






# task = Task(id=1)
# task.AET = 10
# task.StartTime = 10
# k =1


