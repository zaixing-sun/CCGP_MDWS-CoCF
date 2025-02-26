from random import choice, randint, shuffle
from statistics import mean
from copy import deepcopy
from GPClass.function_terminal_3D import INSTANCETERMINAL_dict,CONTAINERTERMINAL_dict,expression_evaluator
# from GPClass.function_terminal_3D import INSTANCETERMINAL_SET,TASKTERMINAL_SET,CONTAINERTERMINAL_SET
# from GPClass.Tree import Node
# import GlobalResource
# from GPClass.multiCloudSystem import multiCloudSystem,InstanceList,MULTICLOUDsystem,InstanceState_Dict
from GPClass.EventClass import *
import random,math
import numpy as np
from Class.commonFunctionClass import Objectives

from Environments.CLOUDFOGsystem import CloudFogSystem,InstanceList,Configuration_Container,Utilisation_Instance
import time
# from numba import njit, jit

import ctypes

# @jit(nopython=True) # , parallel=True
def protected_div(left, right):
    with np.errstate(divide='ignore', invalid='ignore'):
        x = np.divide(left, right)
        if isinstance(x, np.ndarray):
            x[np.isinf(x)] = 1
            x[np.isnan(x)] = 1
        elif np.isinf(x) or np.isnan(x):
            x = 1
    return x   


 
from deap.gp import PrimitiveTree, Primitive, Terminal
def treeNode_R(expr: PrimitiveTree,index, terminal):
    
    var_names, var_values = terminal.names_values
    
    var_names_ctypes = (ctypes.c_char_p * len(var_names))(*var_names)
    var_values_ctypes = (ctypes.c_double * len(var_values))(*var_values)

    # 调用 C++ 函数
    result = expression_evaluator.evaluate_expression_from_python(str(expr).encode('ASCII'), var_names_ctypes, var_values_ctypes, len(var_names))

    return result

    # def eval_context(name, args):
    #     if name == 'protected_div':
    #         return protected_div(*args)
    #     elif name == 'add':
    #         return np.add(*args)
    #     elif name == 'subtract':
    #         return np.subtract(*args)
    #     elif name == 'multiply':
    #         return np.multiply(*args)
    #     elif name == 'maximum':
    #         return np.maximum(*args)
    #     elif name == 'minimum':
    #         return np.minimum(*args)
    # start_time = time.time()
    # result = None
    # stack = []
    # for node in expr:
    #     stack.append((node, []))
    #     while len(stack[-1][1]) == stack[-1][0].arity:
    #         prim, args = stack.pop()
    #         if isinstance(prim, Primitive):
    #             result = eval_context(prim.name, args) # pset.context[prim.name](*args)
    #         elif isinstance(prim, Terminal):
    #             result = eval('terminal.'+prim.value)   # prim.value
    #         else:
    #             raise Exception
    #         if len(stack) == 0:
    #             break  # 栈为空代表所有节点都已经被访问
    #         stack[-1][1].append(result)

    # end_time = time.time()
    # Time_GP = end_time-start_time
    # # print('Time_GP:',end_time-start_time)

    # start_time = time.time()
    # var_names, var_values = terminal.names_values
    # # var_names, var_values = names_values[0], names_values[1]
    # var_names_ctypes = (ctypes.c_char_p * len(var_names))(*var_names)
    # var_values_ctypes = (ctypes.c_double * len(var_values))(*var_values)

    # # 调用 C++ 函数
    # result2 = expression_evaluator.evaluate_expression_from_python(str(expr).encode('ASCII'), var_names_ctypes, var_values_ctypes, len(var_names))
    # end_time = time.time()
    # Time_C = end_time-start_time    
    # # print('Time_C++:',end_time-start_time)

    # if Time_GP/Time_C>50:
    #     print('Time_GP:',Time_GP,'Time_C++:',Time_C)

    # if result != result2:
    #     print('Error:',result,result2)
    # return result

class Individual:
    def __init__(self): 
        self.fitness = deepcopy(Objectives()) 
        self.multiWorkflows = []
        self.MCSPSystem = deepcopy(CloudFogSystem())  # []
        # self.CloudFogSystem = CloudFogSystem()  # []
        self.EVENT = deepcopy(EventClass())

        self.workflowRoot = None # Node()
        self.workflowQueue = [] 
        self.workflowPriority = [] 
        self.workflowWaitQueue = []


        self.taskRoot = None # Node()
        self.taskQueue = [] 
        self.taskPriority = [] 

        self.instanceRoot = None # Node()
        # self.instanceQueue = [] 
        # self.instancePriority = []


        self.booleanPriority = False # True: max; False: min
        self.throughput = 0
        self.numJobsRecorded = 0
        self.seed = 484215
    # @property
    # def workflowWaitQueue(self):
    #     WaitQueue = []
    #     for each in range(len(self.multiWorkflows)):
    #         if not self.multiWorkflows[each].scheduledBoolean:
    #             WaitQueue.append(each)
    #     return WaitQueue



    # def __lt__(self, other):
    #     return self.fitness < other.fitness

    def grow(self, depth):
        # self.workflowRoot.growWorkflow(depth)
        self.taskRoot.growTask(depth)
        self.instanceRoot.growInatance(depth)

    def full(self, depth):
        # self.workflowRoot.fullWorkflow(depth)
        self.taskRoot.fullTask(depth)
        self.instanceRoot.fullInatance(depth)



        # def recombine(self, other):
        #     self.workflowRoot.recombine(other.workflowRoot)

        
        
        # def sortWorkflowQueue(self,):
        #     for i in range(len(self.workflowPriority)-1):
        #         for j in range(i+1,len(self.workflowPriority)):
        #             if self.workflowPriority[i]<self.workflowPriority[j]:
        #                 self.workflowPriority[i],self.workflowPriority[j] = self.workflowPriority[j],self.workflowPriority[i]
        #                 self.workflowQueue[i],self.workflowQueue[j] = self.workflowQueue[j],self.workflowQueue[i]
    
    def sortTaskQueue_addEventQueue(self,Time):
        # #  Computing task terminal
        self.updateTaskWorkflowTerminal()
        # #  sort queue based on taskPriority
        self.taskPriority = [] 
        for each in self.taskQueue:  # range(len())
            Priority = treeNode_R(self.taskRoot, "Task", self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)      # self.taskRoot.evaluateTree(self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)
            self.taskPriority.append(Priority)
        # self.sortTaskQueue()
        # ##################  Get the workflow and corresponding tasks to be scheduled.    #############

        for i in range(len(self.taskPriority)-1):
            for j in range(i+1,len(self.taskPriority)):
                if self.taskPriority[i]<self.taskPriority[j]:
                    self.taskPriority[i],self.taskPriority[j] = self.taskPriority[j],self.taskPriority[i]
                    self.taskQueue[i],self.taskQueue[j] = self.taskQueue[j],self.taskQueue[i]     
        while self.taskQueue!=[]:
            priorityIndex = 0 if self.booleanPriority else -1
            each = self.taskQueue[priorityIndex]
            self.sub_TaskQueue_1(each[0],each[1])
            # self.subTaskNumberinWorkflow(each[0],each[1])
            self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_READY'],TRIGERTIME=Time,OBJECT=Object(workflowID=each[0],taskID=each[1]))) 
        # k =1

    def sortTaskQueue(self,):

        # #  Computing task terminal
        self.updateTaskWorkflowTerminal()
        # #  sort queue based on taskPriority
        self.taskPriority = [] 
        for each in self.taskQueue:  # range(len())
            Priority = treeNode_R(self.taskRoot, "Task", self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)      #  self.taskRoot.evaluateTree(self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)
            self.taskPriority.append(Priority)
        # self.sortTaskQueue()
        # ##################  Get the workflow and corresponding tasks to be scheduled.    #############

        for i in range(len(self.taskPriority)-1):
            for j in range(i+1,len(self.taskPriority)):
                if self.taskPriority[i]<self.taskPriority[j]:
                    self.taskPriority[i],self.taskPriority[j] = self.taskPriority[j],self.taskPriority[i]
                    self.taskQueue[i],self.taskQueue[j] = self.taskQueue[j],self.taskQueue[i]                    
        # # def updateWorkflowQueue(self,systemTime,):
        # #     for wfID in range(len(self.multiWorkflow)):
        # #         if ((wfID not in self.workflowQueue) and (self.multiWorkflow[wfID].releaseTime<=systemTime)
        # #             and(not self.multiWorkflow[wfID].scheduledBoolean)):
        # #             self.workflowQueue += [wfID]
        # #             ## 为新增到队列中的工作流  添加任务队列：首层拓扑层的任务
        # #             self.multiWorkflow[wfID].add_TaskQueue(self.multiWorkflow[wfID].DAGLevel[0]) 
        # def updateWorkflowQueue(self,):  # mCSystem,
        #     while True: 
        #         for wfID in range(len(self.multiWorkflows)):
        #             if ((wfID not in self.workflowQueue) and (self.multiWorkflows[wfID].releaseTime<=self.MCSPSystem.systemTime)
        #                 and(not self.multiWorkflows[wfID].scheduledBoolean)):
        #                 self.workflowQueue += [wfID]
        #                 ## 为新增到队列中的工作流  添加任务队列：首层拓扑层的任务
        #                 self.add_TaskQueue(wfID) 
        #                 # self.multiWorkflow[wfID].add_TaskQueue(self.multiWorkflow[wfID].DAGLevel[0]) 
        #         if self.workflowQueue==[]:
        #             self.MCSPSystem.systemTime += 10  # mCSystem.systemTime #  等价于系统休眠10秒钟
        #         else:
        #             break
    
    def updateTaskWorkflowTerminal(self,):
        # self.multiWorkflows = _updateTaskWorkflowTerminal(self.taskQueue,self.multiWorkflows)
        for each in self.taskQueue:
            wfID,taID = each[0],each[1]
            self.multiWorkflows[wfID].DAG[taID].terminal_task.TOTALEXECUTETIMEQUEUE = self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE
            self.multiWorkflows[wfID].DAG[taID].terminal_task.NUMBERTASKSQUEUE = self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE
            self.multiWorkflows[wfID].DAG[taID].terminal_task.TOTALEXECUTETIMEREMAININGTASKS = self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEREMAININGTASKS
            self.multiWorkflows[wfID].DAG[taID].terminal_task.NUMBERREMAININGTASKS = self.multiWorkflows[wfID].terminal_workflow.NUMBERREMAININGTASKS
        # k = 1

    def add_TaskQueue_FirstLevel(self,wfID):  
        '''Only applicable when the workflow has just been submitted'''        
        for each in self.multiWorkflows[wfID].DAGLevel[0]:
            self.taskQueue.append([wfID,each])
            self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE += self.multiWorkflows[wfID].DAG[each].terminal_task.EXECUTETIME     # .runtimePerCPU_Memory
            # self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_LIST['TASK_READY'],TRIGERTIME=Time,OBJECT=Object(workflowID=wfID,taskID=each))) 
        self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE += len( self.multiWorkflows[wfID].DAGLevel[0])

    def add_TaskQueue_List(self,taskList):      
        for eachtask in taskList:
            wfID,each = eachtask[0],eachtask[1]
            self.taskQueue.append([wfID,each])
            self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE += self.multiWorkflows[wfID].DAG[each].terminal_task.EXECUTETIME
            # self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_LIST['TASK_READY'],TRIGERTIME=Time,OBJECT=Object(workflowID=wfID,taskID=each))) 
            self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE += 1

    # def add_TaskQueue_1(self,wfID,taskID):  
    #     self.taskQueue.append([wfID,taskID])
    #     self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE += self.multiWorkflows[wfID].DAG[taskID].terminal_task.EXECUTETIME
    #     self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE += 1      
    
    def sub_TaskQueue_1(self,wfID,taskID):  
        self.taskQueue.remove([wfID,taskID])      
        # self.subTaskNumberinWorkflow(wfID,taskID)
        self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE -= self.multiWorkflows[wfID].DAG[taskID].terminal_task.EXECUTETIME
        self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEREMAININGTASKS -= self.multiWorkflows[wfID].DAG[taskID].terminal_task.EXECUTETIME
        self.multiWorkflows[wfID].terminal_workflow.NUMBERREMAININGTASKS -= 1
        self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE -= 1 # len( self.taskQueue)


    # def sub_TaskQueue(self,taskList):  
    #     for each1 in taskList:
    #         wfID,each = each1[0],each1[1]
    #         self.taskQueue.remove(each1)
    #         self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE -= self.multiWorkflows[wfID].DAG[each].runtime
    #         self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEREMAININGTASKS -= self.multiWorkflows[wfID].DAG[each].runtime
    #         self.multiWorkflows[wfID].terminal_workflow.NUMBERREMAININGTASKS -= 1
    #         self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE -= 1 # len( self.taskQueue)

    def caculateTransmissionCost(self,wfID,taskID,CloudProvider):
        cost1 = 0
        if CloudProvider == 'FogSever':
            for each in self.multiWorkflows[wfID].DAG[taskID].inputs:
                if self.multiWorkflows[wfID].DAG[each.id].Assigned.CloudProvider!= CloudProvider:
                    cost1 += each.size/1024*self.MCSPSystem.TransmissionUnitGBPrice
        return cost1


    def eventTriger_WORKFLOW_SUBMITTED(self,event):
        EventScheduled = [event]
        while self.EVENT.EVENTQUEUE[0].EVENTTYPE==EVENTTYPE_DICT['WORKFLOW_SUBMITTED'] and self.EVENT.EVENTQUEUE[0].TRIGERTIME == self.MCSPSystem.systemTime:
            EventScheduled.append(self.EVENT.EVENTQUEUE.pop(0))
        for each in EventScheduled:
            self.multiWorkflows[each.OBJECT.workflowID].objectives.cost = 0.0
            # self.multiWorkflows[each.OBJECT.workflowID].objectives.cost_VM = 0.0
            # self.multiWorkflows[each.OBJECT.workflowID].objectives.cost_FaaS = 0.0
            self.multiWorkflows[each.OBJECT.workflowID].objectives.cost_Trans = 0.0
            self.multiWorkflows[each.OBJECT.workflowID].NUMBERTASKINCLOUD= [0 for each in range(len(self.MCSPSystem.platform))]
            self.add_TaskQueue_FirstLevel(each.OBJECT.workflowID)
        self.sortTaskQueue_addEventQueue(self.MCSPSystem.systemTime)        

        # self.add_TaskQueue_First(event.OBJECT.workflowID,self.MCSPSystem.systemTime)


    def calculateCommunicationTime(self,wfID,taskID,temp_Instance):
        maxCommunicationTime = 0
        maxFatherFinishTimeplusCT = 0
        for father_ofchild in self.multiWorkflows[wfID].DAG[taskID].inputs:  
            if self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned.ID != temp_Instance.ID:
                if (self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned.CloudProvider == temp_Instance.CloudProvider) and temp_Instance.CloudProvider == 'FogSever':
                    CommunicationTime= father_ofchild.size/self.MCSPSystem.bandwidth_Fog
                else:
                    CommunicationTime= father_ofchild.size/self.MCSPSystem.bandwidth_Cloud
                maxCommunicationTime = max(maxCommunicationTime,CommunicationTime)
                maxFatherFinishTimeplusCT = max(maxFatherFinishTimeplusCT,self.multiWorkflows[wfID].DAG[father_ofchild.id].FinishTime +  CommunicationTime)              
        return maxCommunicationTime,maxFatherFinishTimeplusCT
       
    def determineWhetherItsSubtaskReady(self,time1,wfID,taskID):
        childList = []
        for child in self.multiWorkflows[wfID].DAG[taskID].outputs:
            finish_Boolean = True
            for father_ofchild in self.multiWorkflows[wfID].DAG[child.id].inputs:
                # if self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned==None or self.multiWorkflows[wfID].DAG[father_ofchild.id].configuration_Container[-1].state== 'running':
                if self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned==None or self.multiWorkflows[wfID].DAG[father_ofchild.id].FinishTime==None:
                    finish_Boolean = False
                    break
            if finish_Boolean: # Child can be set Ready and add to Event.
                childList.append([wfID,child.id])
        if len(childList)>1:
            self.add_TaskQueue_List(childList)
            self.sortTaskQueue_addEventQueue(time1) 
            # self.sortTaskQueue_addEventQueue(self.multiWorkflows[wfID].DAG[taskID].StartTime)   
        elif len(childList)==1:
            # self.subTaskNumberinWorkflow(wfID,childList[0][1])     FinishTime
            '''  2024 01 07 zaixing added the following 2 lines'''
            self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEREMAININGTASKS -= self.multiWorkflows[wfID].DAG[taskID].terminal_task.EXECUTETIME
            self.multiWorkflows[wfID].terminal_workflow.NUMBERREMAININGTASKS -= 1

            self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_READY'],TRIGERTIME = time1, # self.multiWorkflows[wfID].DAG[taskID].StartTime,
                                                        OBJECT=Object(workflowID=childList[0][0],taskID=childList[0][1])))
                # self.taskQueue.append([wfID,child.id])
                # self.add_TaskQueue_1(wfID,child.id)                 

    def subTaskNumberinWorkflow(self,time1, wfID,taskID):
        self.multiWorkflows[wfID].DAGLevel[self.multiWorkflows[wfID].DAG[taskID].Level].remove(taskID)        
        self.multiWorkflows[wfID].unscheduledTaskNumber-=1
        if  self.multiWorkflows[wfID].unscheduledTaskNumber==0:       
            self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['WORKFLOW_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].FinishTime,
                                                        OBJECT=Object(workflowID=wfID)))
        else:
            self.determineWhetherItsSubtaskReady(time1,wfID,taskID)
            
    def sort_availableServiceInstance(self,availableServiceInstance):
        for i in range(len(availableServiceInstance)-1):
            for j in range(i+1,len(availableServiceInstance)):
                if availableServiceInstance[i].Priority<availableServiceInstance[j].Priority:
                    availableServiceInstance[i], availableServiceInstance[j] = availableServiceInstance[j], availableServiceInstance[i]
        return availableServiceInstance
    
    def selectOneCloud(self,availableServiceInstance):
        priorityIndex = 0 if self.booleanPriority else -1
        # step = 1 if priorityIndex==0 else -1
        list1 = []
        # if step ==1:availableServiceInstance[priorityIndex]
        for each in range(len(availableServiceInstance)):            
            if availableServiceInstance[each].Priority==availableServiceInstance[priorityIndex].Priority:
               list1.append(each)
        if len(list1)>1:
            random.seed(self.seed +1000)
            return random.choice(list1)
            r1 = randint(0,len(list1)-1)
            if priorityIndex==0:
                print('   ', [each.CloudProvider for each in availableServiceInstance], '##select:', availableServiceInstance[-(r1+1)].CloudProvider)
                return r1
            else:
                print('   ', [each.CloudProvider for each in availableServiceInstance], '##select:', availableServiceInstance[-(r1+1)].CloudProvider)
                return -(r1+1)
        else:
            return priorityIndex
        
    def selectOneInstance(self,task_deadline,availableServiceInstance):
        priorityIndex = 0 if self.booleanPriority else -1
        meetDL = []
        for each in availableServiceInstance:            
            if each.TerminalInstance.ACTUALAVAILABLETIME + each.TerminalInstance.MINEXECUTETIME <= task_deadline:
               meetDL.append(each)
        if meetDL == []:
            time1 = np.inf
            for each in availableServiceInstance:            
                if each.TerminalInstance.ACTUALAVAILABLETIME + each.TerminalInstance.MINEXECUTETIME <time1:
                    time1 = each.TerminalInstance.ACTUALAVAILABLETIME + each.TerminalInstance.MINEXECUTETIME
                    selected = each 
            # print('     np.inf')
            return selected  ## choice one min(finish time) 
        else:
            list1 = []
            for each in range(len(meetDL)):            
                if meetDL[each].Priority==meetDL[priorityIndex].Priority:
                    list1.append(each)

            if len(list1)>1:
                list_NoNeedCreate =[]
                for each in list1:
                    if not meetDL[each].NewlyCreated:
                        list_NoNeedCreate.append(each)
                random.seed(self.seed)
                if list_NoNeedCreate !=[]:
                    return meetDL[random.choice(list_NoNeedCreate) ]   
                else:
                    return meetDL[random.choice(list1)]
            else:
                return meetDL[priorityIndex]



        # # step = 1 if priorityIndex==0 else -1
        # list1 = []
        # # if step ==1:availableServiceInstance[priorityIndex]
        # for each in range(len(availableServiceInstance)):            
        #     if availableServiceInstance[each].Priority==availableServiceInstance[priorityIndex].Priority:
        #        list1.append(each)

        # if len(list1)>1:
        #     list_NoNeedCreate =[]
        #     for each in list1:
        #         if not availableServiceInstance[each].NewlyCreated:
        #             list_NoNeedCreate.append(each)
        #     if list_NoNeedCreate !=[]:
        #         return random.choice(list_NoNeedCreate)    
        #     else:
        #         return random.choice(list1)
        #         r1 = randint(0,len(list1)-1)
        #         if priorityIndex==0:
        #             print('   ', [each.CloudProvider for each in availableServiceInstance], '##select:', availableServiceInstance[-(r1+1)].CloudProvider)
        #             return r1
        #         else:
        #             print('   ', [each.CloudProvider for each in availableServiceInstance], '##select:', availableServiceInstance[-(r1+1)].CloudProvider)
        #             return -(r1+1)
        # else:
        #     return priorityIndex


    def eventProcessReady_1Task(self,Time1,wfID,taskID):
        priorityIndex = 0 if self.booleanPriority else -1
        task_deadline = self.multiWorkflows[wfID].DAG[taskID].terminal_task.SUBDEADLINE
        
        availableServiceInstance = []
        for eachPlstformID in range(len(self.MCSPSystem.platform)):  
            ComCost = self.caculateTransmissionCost(wfID,taskID,self.MCSPSystem.platform[eachPlstformID].CloudProvider)               
            for i in range(len(self.MCSPSystem.platform[eachPlstformID].VMPlatform)): #  have been created
                temp_Instance = self.MCSPSystem.platform[eachPlstformID].VMPlatform[i]
                CommunicationTime,maxFatherFinishTimeplusCT = self.calculateCommunicationTime(wfID,taskID,temp_Instance)
                # delay = self.MCSPSystem.vmColdStartup['ColdStartup'] if self.MCSPSystem.platform[eachPlstformID].CloudProvider == 'CloudSever' else self.MCSPSystem.vmColdStartup['delay']
                temp_Instance.TerminalInstance.ACTUALAVAILABLETIME = max(Time1 + self.MCSPSystem.platform[eachPlstformID].delay, temp_Instance.createdFinishTime,maxFatherFinishTimeplusCT)
                
                temp_Instance.TerminalInstance.COMMUNICATIONCOST = ComCost
                temp_Instance.TerminalInstance.SLACKTIME = temp_Instance.TerminalInstance.ACTUALAVAILABLETIME - task_deadline
                temp_Instance.TerminalInstance.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 

                temp_Instance.TerminalInstance.CPU_CONFIGURATION = temp_Instance.Configuration_instance.ECU
                temp_Instance.TerminalInstance.MEMORY_CONFIGURATION = temp_Instance.Configuration_instance.Memory
                temp_Instance.TerminalInstance.PRICE_CONFIGURATION = temp_Instance.Configuration_instance.Price_Given
                temp_Instance.TerminalInstance.STATICPOWER_CONFIGURATION = temp_Instance.Configuration_instance.StaticPower
                temp_Instance.TerminalInstance.COMMUNICATIONTIME = CommunicationTime

                cpu_all, mem_all, sameType, otherTypeList = 0,0,0,set()
                category = self.multiWorkflows[wfID].DAG[taskID].Category[0]
                for ea in temp_Instance.allTask:
                    eachTask = self.multiWorkflows[ea[0]].DAG[ea[1]]
                    if eachTask.Category[0] == category:
                        sameType = 4
                    else:
                        otherTypeList.add(eachTask.Category[0])
                    cpu_all += eachTask.minCPU
                    mem_all += eachTask.minMEM
                temp_Instance.TerminalInstance.CURRENTLYCPU_INSTANCE = temp_Instance.TerminalInstance.CPU_CONFIGURATION - cpu_all
                temp_Instance.TerminalInstance.CURRENTLYMEMORY_INSTANCE = temp_Instance.TerminalInstance.MEMORY_CONFIGURATION - mem_all
                if temp_Instance.TerminalInstance.CURRENTLYCPU_INSTANCE<self.multiWorkflows[wfID].DAG[taskID].minCPU or temp_Instance.TerminalInstance.CURRENTLYMEMORY_INSTANCE<self.multiWorkflows[wfID].DAG[taskID].minMEM:
                    continue
    
                temp_Instance.TerminalInstance.WEIGHT_TASK_CATEGORY = sameType + len(otherTypeList)
                temp_Instance.TerminalInstance.MINEXECUTETIME = self.multiWorkflows[wfID].DAG[taskID].getRuntime(temp_Instance.TerminalInstance.CURRENTLYCPU_INSTANCE,temp_Instance.TerminalInstance.CURRENTLYMEMORY_INSTANCE)

                temp_Instance.Priority = treeNode_R(self.instanceRoot, "Instance", temp_Instance.TerminalInstance)
                availableServiceInstance.append(temp_Instance)                     
            
            for i in range(self.MCSPSystem.platform[eachPlstformID].Numbers): #  test new Creat Instance
                if self.MCSPSystem.platform[eachPlstformID].eachTypeNumbers_Used[i]<self.MCSPSystem.platform[eachPlstformID].eachTypeNumbers[i]:
                    temp_Instance= deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[eachPlstformID].CloudProvider,typeID =i,
                                            Configuration_instance=self.MCSPSystem.platform[eachPlstformID].Type[i],  NewlyCreated=True, TerminalInstance = INSTANCETERMINAL_dict(),
                                            )) # remainingECU=self.MCSPSystem.platform[eachPlstformID].Type[i].ECU, remainingMemory=self.MCSPSystem.platform[eachPlstformID].Type[i].Memory,
                    CommunicationTime,maxFatherFinishTimeplusCT = self.calculateCommunicationTime(wfID,taskID,temp_Instance)
                    delay = self.MCSPSystem.vmColdStartup['ColdStartup'] if self.MCSPSystem.platform[eachPlstformID].CloudProvider == 'CloudSever' else self.MCSPSystem.vmColdStartup['delay']
                    
                    temp_Instance.TerminalInstance.ACTUALAVAILABLETIME = max(Time1 + delay, maxFatherFinishTimeplusCT)
                    # temp_Instance.TerminalInstance.EXECUTECOST = (self.MCSPSystem.platform[eachPlstformID].VMType.caculateCost(
                    #                                         temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID]) + 
                    #                                         self.MCSPSystem.platform[eachPlstformID].VMType.bootingCost(i))
                    temp_Instance.TerminalInstance.COMMUNICATIONCOST = ComCost
                    # temp_Instance.TerminalInstance.ACTUALEXECUTETIME = self.MCSPSystem.platform[eachPlstformID].VMType.caculateExecuteTime(temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID]) # self.multiWorkflows[wfID].DAG[taskID].runtime
                    # temp_Instance.TerminalInstance.INSTANCEAVAILABLETIME = Time1 + self.MCSPSystem.vmColdStartup
                    temp_Instance.TerminalInstance.SLACKTIME = temp_Instance.TerminalInstance.ACTUALAVAILABLETIME - task_deadline
                    temp_Instance.TerminalInstance.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 

                    temp_Instance.TerminalInstance.CPU_CONFIGURATION = temp_Instance.Configuration_instance.ECU
                    temp_Instance.TerminalInstance.MEMORY_CONFIGURATION = temp_Instance.Configuration_instance.Memory
                    temp_Instance.TerminalInstance.PRICE_CONFIGURATION = temp_Instance.Configuration_instance.Price_Given
                    temp_Instance.TerminalInstance.STATICPOWER_CONFIGURATION = temp_Instance.Configuration_instance.StaticPower
                    temp_Instance.TerminalInstance.COMMUNICATIONTIME = CommunicationTime

                    cpu_all, mem_all, sameType, otherTypeList = 0,0,0,set()
                    # category = self.multiWorkflows[wfID].DAG[taskID].Category[0]
                    # for ea in temp_Instance.allTask:
                    #     eachTask = self.multiWorkflows[ea[0]].DAG[ea[1]]
                    #     if eachTask.Category[0] == category:
                    #         sameType = 4
                    #     else:
                    #         otherTypeList.add(eachTask.Category[0])
                    #     cpu_all += eachTask.minCPU
                    #     mem_all += eachTask.minMEM
                    temp_Instance.TerminalInstance.CURRENTLYCPU_INSTANCE = temp_Instance.TerminalInstance.CPU_CONFIGURATION - cpu_all
                    temp_Instance.TerminalInstance.CURRENTLYMEMORY_INSTANCE = temp_Instance.TerminalInstance.MEMORY_CONFIGURATION - mem_all
                    if temp_Instance.TerminalInstance.CURRENTLYCPU_INSTANCE<self.multiWorkflows[wfID].DAG[taskID].minCPU or temp_Instance.TerminalInstance.CURRENTLYMEMORY_INSTANCE<self.multiWorkflows[wfID].DAG[taskID].minMEM:
                        continue
                    
                    
                    temp_Instance.TerminalInstance.WEIGHT_TASK_CATEGORY = sameType + len(otherTypeList)
                    temp_Instance.TerminalInstance.MINEXECUTETIME = self.multiWorkflows[wfID].DAG[taskID].getRuntime(temp_Instance.TerminalInstance.CURRENTLYCPU_INSTANCE,temp_Instance.TerminalInstance.CURRENTLYMEMORY_INSTANCE)

                    temp_Instance.Priority = treeNode_R(self.instanceRoot, "Instance", temp_Instance.TerminalInstance)
                    availableServiceInstance.append(temp_Instance)

        availableServiceInstance = self.sort_availableServiceInstance(availableServiceInstance)
        selectedInstance = self.selectOneInstance(task_deadline,availableServiceInstance) 

        CloudProviderID = self.MCSPSystem.getCloudProviderID(selectedInstance.CloudProvider)
            
        if selectedInstance.NewlyCreated:
            selectedInstance.ID = len(self.MCSPSystem.platform[CloudProviderID].VMPlatform)
            Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=selectedInstance.CloudProvider,instance=selectedInstance.ID)
            
        else:
            Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=selectedInstance.CloudProvider,instance=selectedInstance.ID)

        # self.multiWorkflows[wfID].DAG[taskID].Assigned = deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[CloudProviderID].CloudProvider,
        #                                                                 ID=selectedInstance.ID,typeID= selectedInstance.typeID,))
        self.multiWorkflows[wfID].DAG[taskID].Assigned = deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[CloudProviderID].CloudProvider,
                                                                               typeID =selectedInstance.typeID, ID=selectedInstance.ID, 
                                                                               Configuration_instance=self.MCSPSystem.platform[CloudProviderID].Type[selectedInstance.typeID],))
                                                                            #    remainingECU=self.MCSPSystem.platform[CloudProviderID].Type[selectedInstance.typeID].ECU,
                                                                            #    remainingMemory=self.MCSPSystem.platform[CloudProviderID].Type[selectedInstance.typeID].Memory,
        self.multiWorkflows[wfID].DAG[taskID].StartTime = selectedInstance.TerminalInstance.ACTUALAVAILABLETIME
        self.multiWorkflows[wfID].DAG[taskID].FinishTime = None
        # self.multiWorkflows[wfID].DAG[taskID].AET=  selectedInstance.TerminalInstance.ACTUALEXECUTETIME  # self.multiWorkflows[wfID].DAG[taskID].runtime / selectedInstance.
        
        # self.multiWorkflows[wfID].DAG[taskID].configuration_Container = [deepcopy(Configuration_Container(index=0,ECU=0, Memory=0, 
        #                                                                 remainingWeightofTask=self.multiWorkflows[wfID].DAG[taskID].runtimePerCPU_Memory, 
        #                                                                 latestFinishTime= math.inf,terminal_container = CONTAINERTERMINAL_dict(), 
        #                                                                 task= [wfID, taskID]  ) ) ] 
        
        self.multiWorkflows[wfID].NUMBERTASKINCLOUD[CloudProviderID] += 1
        # self.fitness.Cost += selectedInstance.TerminalInstance.COMMUNICATIONCOST + selectedInstance.TerminalInstance.EXECUTECOST
        # self.fitness.cost_VM += selectedInstance.TerminalInstance.EXECUTECOST
        # # self.fitness.cost_FaaS += 
        self.fitness.cost_Trans +=  selectedInstance.TerminalInstance.COMMUNICATIONCOST            
        # self.multiWorkflows[wfID].objectives.cost += selectedInstance.TerminalInstance.COMMUNICATIONCOST + selectedInstance.TerminalInstance.EXECUTECOST
        # self.multiWorkflows[wfID].objectives.cost_VM += selectedInstance.TerminalInstance.EXECUTECOST
        # # self.multiWorkflows[wfID].objectives.cost_FaaS += 
        self.multiWorkflows[wfID].objectives.cost_Trans +=  selectedInstance.TerminalInstance.COMMUNICATIONCOST


        selectedInstance.waitingTask.append([wfID,taskID])

        # # selectedInstance.taskSequence.append([wfID,taskID])
        # selectedInstance.timeTable.append([self.multiWorkflows[wfID].DAG[taskID].StartTime,self.multiWorkflows[wfID].DAG[taskID].FinishTime])
        # selectedInstance.CompleteTime = max(selectedInstance.CompleteTime,self.multiWorkflows[wfID].DAG[taskID].FinishTime)
        
        if selectedInstance.NewlyCreated:
            selectedInstance.NewlyCreated = False    
            selectedInstance.createdFinishTime = selectedInstance.TerminalInstance.ACTUALAVAILABLETIME

            self.MCSPSystem.platform[CloudProviderID].VMPlatform.append(selectedInstance)
            self.MCSPSystem.platform[CloudProviderID].eachTypeNumbers_Used[selectedInstance.typeID] += 1

            # self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['BOOTING_INSTANCE_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime-self.MCSPSystem.vmColdStartup,OBJECT=Object_Temp)) 
            # self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['BOOTING_INSTANCE_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 
        else:
            self.MCSPSystem.platform[CloudProviderID].VMPlatform[selectedInstance.ID] = selectedInstance

        # CCT,gg = self.calculateCommunicationTime(wfID,taskID,selectedInstance)
        # if CCT!=0:
        #     self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime-CCT,OBJECT=Object_Temp)) 
        #     self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 

        self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime, OBJECT=Object_Temp)) 
        # self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].FinishTime,OBJECT=Object_Temp)) 

    def adjust_CPU_AllContainer_AllRunningTasks(self, boolean, time1, remECU, RunningTasks):
    
        def generate_RandomSumlist(NUM, SUM):
            result = [0] * NUM
            current_sum = 0  
            while current_sum < SUM:
                idx = random.randint(0, NUM - 1)
                result[idx] += 0.5
                current_sum += 0.5
            return result
        def generate_uniform_list(NUM, SUM):
            a1, a2 = (2*SUM)//NUM, (2*SUM)%NUM                              # Average distribution scheme
            eachPartition = []
            for i in range(NUM):
                if i < a2:
                    eachPartition.append(a1+1)
                else:
                    eachPartition.append(a1)
            return [each/2 for each in eachPartition]
        
        
        taskNum,Nums = len(RunningTasks), remECU

        
        containerList = []
        # categoryList = set()
        for each in RunningTasks:
            wfID,taskID = int(each.split('-')[0]), int(each.split('-')[1])            # each[0],each[1]
            # categoryList.append(self.multiWorkflows[wfID].DAG[taskID].Category[0] )    #  = 
            temp_container = deepcopy(self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1]) 
            
            temp_container.terminal_container.ASSIGNED_CPU_MEMORY = temp_container.ECU
            temp_container.terminal_container.MIN_CPU_MEMORY_TASK = self.multiWorkflows[wfID].DAG[taskID].minCPU
            temp_container.terminal_container.SLACKTIME = time1 - self.multiWorkflows[wfID].DAG[taskID].terminal_task.SUBDEADLINE
            temp_container.terminal_container.NUMBERSCHILDREN = self.multiWorkflows[wfID].DAG[taskID].terminal_task.NUMBERSCHILDREN
            
            if temp_container.index == 0:
                temp_container.terminal_container.REMAININGWEIGHT = temp_container.remainingWeightofTask                
            else:
                # temp_container.index += 1
                temp_container.remainingWeightofTask = temp_container.remainingWeightofTask - temp_container.ECU*temp_container.Memory * (time1 - temp_container.StartTime)
                temp_container.terminal_container.REMAININGWEIGHT = temp_container.remainingWeightofTask
                if boolean[each]:
                    Object_Temp = Object(workflowID=wfID,taskID=taskID,cloudProvider=self.multiWorkflows[wfID].DAG[taskID].Assigned.CloudProvider,instance=self.multiWorkflows[wfID].DAG[taskID].Assigned.ID)
                    delEvent = EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=temp_container.latestFinishTime,OBJECT=Object_Temp)  
                    self.EVENT.delOneTerminateEnventinQueue(delEvent)
            if boolean[each]:
                temp_container.index += 1
            self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].FinishTime = time1

            temp_container.Priority = treeNode_R(self.containerRoot, "Container", temp_container.terminal_container)
            containerList.append(temp_container)
        containerList = self.sort_availableServiceInstance(containerList)
        # taskList = [ each.task for each in containerList ]
        pro = random.random()
        if pro<0.2:    
            # a1, a2 = Nums//taskNum, Nums%taskNum                              # Average distribution scheme
            # eachPartition = []
            # for i in range(taskNum):
            #     if i < a2:
            #         eachPartition.append(a1+1)
            #     else:
            #         eachPartition.append(a1)
            eachPartition = generate_uniform_list(taskNum, Nums)
            # return taskList, eachPartition
        elif pro<0.4:           # Random distribution scheme
            eachPartition = generate_RandomSumlist(taskNum, Nums)
            # return taskList, eachPartition
        # elif pro<0.7:
        #     eachPartition = generate_RandomSumlist(taskNum, Nums)
        #     eachPartition.sort()
        #     # return taskList, eachPartition.sort()
        else:
            eachPartition = generate_RandomSumlist(taskNum, Nums)
            eachPartition.sort(reverse=True)
            # return taskList, eachPartition.sort(reverse=True)
        for eachContainer,partition in zip(containerList,eachPartition):            
            wfID,taskID = eachContainer.task[0],eachContainer.task[1]
            eachContainer.ECU = self.multiWorkflows[wfID].DAG[taskID].minCPU + partition
            if (eachContainer.Memory ==0) or boolean['%s-%s'%(wfID,taskID)]:              
                eachContainer.Memory = self.multiWorkflows[wfID].DAG[taskID].minMEM
            eachContainer.StartTime = time1
            eachContainer.latestFinishTime = time1 + eachContainer.remainingWeightofTask/(eachContainer.ECU*eachContainer.Memory)

            if boolean['%s-%s'%(wfID,taskID)]:
                self.multiWorkflows[wfID].DAG[taskID].configuration_Container.append(eachContainer)
            else:
                self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1] = eachContainer
            # self.multiWorkflows[wfID].DAG[taskID].configuration_Container.append(eachContainer)






    def adjust_MEM_AllContainer_AllRunningTasks(self,boolean, time1, remMEM, RunningTasks):
    
        def generate_RandomSumlist(NUM, SUM):
            result = [0] * NUM
            current_sum = 0  
            while current_sum < SUM:
                idx = random.randint(0, NUM - 1)
                result[idx] += 0.5
                current_sum += 0.5
            return result
        def generate_uniform_list(NUM, SUM):
            a1, a2 = (2*SUM)//NUM, (2*SUM)%NUM                              # Average distribution scheme
            eachPartition = []
            for i in range(NUM):
                if i < a2:
                    eachPartition.append(a1+1)
                else:
                    eachPartition.append(a1)
            return [each/2 for each in eachPartition] 
        
        taskNum,Nums = len(RunningTasks), remMEM

        
        containerList = []
        # categoryList = set()
        for each in RunningTasks:
            wfID,taskID = int(each.split('-')[0]), int(each.split('-')[1])            # each[0],each[1]
            # categoryList.append(self.multiWorkflows[wfID].DAG[taskID].Category[0] )    #  = 
            temp_container = deepcopy(self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1]) 
            
            temp_container.terminal_container.ASSIGNED_CPU_MEMORY = temp_container.Memory
            temp_container.terminal_container.MIN_CPU_MEMORY_TASK = self.multiWorkflows[wfID].DAG[taskID].minMEM
            temp_container.terminal_container.SLACKTIME = time1 - self.multiWorkflows[wfID].DAG[taskID].terminal_task.SUBDEADLINE
            temp_container.terminal_container.NUMBERSCHILDREN = self.multiWorkflows[wfID].DAG[taskID].terminal_task.NUMBERSCHILDREN
            
            if temp_container.index == 0:
                temp_container.terminal_container.REMAININGWEIGHT = temp_container.remainingWeightofTask                
            else:
                
                temp_container.remainingWeightofTask = temp_container.remainingWeightofTask - temp_container.ECU*temp_container.Memory * (time1 - temp_container.StartTime)
                temp_container.terminal_container.REMAININGWEIGHT = temp_container.remainingWeightofTask
                if boolean[each]:
                    Object_Temp = Object(workflowID=wfID,taskID=taskID,cloudProvider=self.multiWorkflows[wfID].DAG[taskID].Assigned.CloudProvider,instance=self.multiWorkflows[wfID].DAG[taskID].Assigned.ID)
                    delEvent = EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=temp_container.latestFinishTime,OBJECT=Object_Temp)  
                    self.EVENT.delOneTerminateEnventinQueue(delEvent)
            if boolean[each]:
                temp_container.index += 1
            self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].FinishTime = time1

            temp_container.Priority = treeNode_R(self.containerRoot, "Container", temp_container.terminal_container)
            containerList.append(temp_container)
        containerList = self.sort_availableServiceInstance(containerList)
        # taskList = [ each.task for each in containerList ]
        pro = random.random()
        if pro<0.2:    
            # a1, a2 = Nums//taskNum, Nums%taskNum                              # Average distribution scheme
            # eachPartition = []
            # for i in range(taskNum):
            #     if i < a2:
            #         eachPartition.append(a1+1)
            #     else:
            #         eachPartition.append(a1)
            eachPartition = generate_uniform_list(taskNum, Nums)
            # return taskList, eachPartition
        elif pro<0.4:           # Random distribution scheme
            eachPartition = generate_RandomSumlist(taskNum, Nums)
            # return taskList, eachPartition
        # elif pro<0.7:
        #     eachPartition = generate_RandomSumlist(taskNum, Nums)
        #     eachPartition.sort()
        #     # return taskList, eachPartition.sort()
        else:
            eachPartition = generate_RandomSumlist(taskNum, Nums)
            eachPartition.sort(reverse=True)
            # return taskList, eachPartition.sort(reverse=True)
        # for [wfID,taskID],config in zip(taskList,eachPartition):
        
        for eachContainer,partition in zip(containerList,eachPartition):            
            wfID,taskID = eachContainer.task[0],eachContainer.task[1]
            eachContainer.Memory = self.multiWorkflows[wfID].DAG[taskID].minMEM + partition
            if (eachContainer.ECU ==0) or boolean['%s-%s'%(wfID,taskID)]:                
                eachContainer.ECU = self.multiWorkflows[wfID].DAG[taskID].minCPU
            eachContainer.StartTime = time1
            eachContainer.latestFinishTime = time1 + eachContainer.remainingWeightofTask/(eachContainer.ECU*eachContainer.Memory)
            if boolean['%s-%s'%(wfID,taskID)]:
                self.multiWorkflows[wfID].DAG[taskID].configuration_Container.append(eachContainer)
            else:
                self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1] = eachContainer


            # Object_Temp = Object(workflowID=wfID,taskID=taskID,cloudProvider=self.multiWorkflows[wfID].DAG[taskID].Assigned.CloudProvider,instance=self.multiWorkflows[wfID].DAG[taskID].Assigned.ID)
            # delEvent = EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=temp_container.latestFinishTime,OBJECT=Object_Temp)  
            # self.EVENT.addtoEventQueue(delEvent) 



    def eventTriger_ContainerConfiguration(self,Event):
        priorityIndex = 0 if self.booleanPriority else -1
        instance =  deepcopy(self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(Event.OBJECT.cloudProvider)].VMPlatform[Event.OBJECT.instance])  
        
        wfID,taskID = Event.OBJECT.workflowID,Event.OBJECT.taskID
        if Event.EVENTTYPE == EVENTTYPE_DICT['TASK_STARTED']:
            # wfID = Event.OBJECT.workflowID
            # taskID = Event.OBJECT.taskID

            if self.multiWorkflows[wfID].DAG[taskID].Category[0] == '00':
                self.multiWorkflows[wfID].DAG[taskID].AET = self.multiWorkflows[wfID].DAG[taskID].getRuntime(self.multiWorkflows[wfID].DAG[taskID].minCPU,self.multiWorkflows[wfID].DAG[taskID].minMEM)
                # self.multiWorkflows[wfID].DAG[taskID].FinishTime = Event.TRIGERTIME + self.multiWorkflows[wfID].DAG[taskID].AET
                self.multiWorkflows[wfID].DAG[taskID].configuration_Container = [deepcopy(Configuration_Container(index=0,ECU=self.multiWorkflows[wfID].DAG[taskID].minCPU, Memory=self.multiWorkflows[wfID].DAG[taskID].minMEM, 
                                                                                remainingWeightofTask=self.multiWorkflows[wfID].DAG[taskID].runtimePerCPU_Memory, 
                                                                                StartTime = self.multiWorkflows[wfID].DAG[taskID].StartTime,
                                                                                # FinishTime = self.multiWorkflows[wfID].DAG[taskID].FinishTime,
                                                                                # latestFinishTime = self.multiWorkflows[wfID].DAG[taskID].FinishTime,
                                                                                latestFinishTime = Event.TRIGERTIME + self.multiWorkflows[wfID].DAG[taskID].AET,
                                                                                task= [wfID, taskID],state= 'running'  ) ) ]  
                Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=instance.CloudProvider,instance=instance.ID)
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=Event.TRIGERTIME + self.multiWorkflows[wfID].DAG[taskID].AET,OBJECT=Object_Temp))       
            else:
                self.multiWorkflows[wfID].DAG[taskID].configuration_Container = [deepcopy(Configuration_Container(index=0,ECU=0, Memory=0, 
                                                                            remainingWeightofTask=self.multiWorkflows[wfID].DAG[taskID].runtimePerCPU_Memory,
                                                                            StartTime = self.multiWorkflows[wfID].DAG[taskID].StartTime,
                                                                            # FinishTime = self.multiWorkflows[wfID].DAG[taskID].StartTime, 
                                                                            latestFinishTime= math.inf,terminal_container = CONTAINERTERMINAL_dict(), 
                                                                            task= [wfID, taskID]  ,state= 'running') ) ]
            # self.multiWorkflows[wfID].DAG[taskID].FinishTime = None
            instance.waitingTask.remove([wfID,taskID]) 
            instance.runningTask.append([wfID,taskID]) 
            instance.taskSequence.append([wfID,taskID])
        elif Event.EVENTTYPE == EVENTTYPE_DICT['TASK_COMPLETED']:
            # wfID = Event.OBJECT.workflowID
            # taskID = Event.OBJECT.taskID
            self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].FinishTime = Event.TRIGERTIME
            self.multiWorkflows[wfID].DAG[taskID].FinishTime = Event.TRIGERTIME

            # t1 = Event.TRIGERTIME - self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].StartTime
            # if t1 * self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].ECU * self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].Memory != self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].remainingWeightofTask:
            if Event.TRIGERTIME != self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].latestFinishTime:
                print('error')
            self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].state= 'terminate'
            instance.runningTask.remove([wfID,taskID]) 


        needAdjustCPU, needAdjustMEM = [],[]
        summinCPU, summinMEM = 0,0
        for each in instance.runningTask:
            wfID,taskID = each[0],each[1]
            str1 = '%s-%s'%(wfID,taskID)
            if self.multiWorkflows[wfID].DAG[taskID].Category[0] == '01':
                needAdjustMEM.append(str1)
            elif self.multiWorkflows[wfID].DAG[taskID].Category[0] == '10':
                needAdjustCPU.append(str1)
            elif self.multiWorkflows[wfID].DAG[taskID].Category[0] == '11':
                needAdjustCPU.append(str1)
                needAdjustMEM.append(str1)
            summinCPU += self.multiWorkflows[wfID].DAG[taskID].minCPU
            summinMEM += self.multiWorkflows[wfID].DAG[taskID].minMEM
        
        if (set(needAdjustCPU)& set(needAdjustMEM)) == set():
            booleanDict = { }
            for each in needAdjustCPU:
                booleanDict[each] = True
            for each in needAdjustMEM:
                booleanDict[each] = True
            if needAdjustCPU != []:
                self.adjust_CPU_AllContainer_AllRunningTasks(booleanDict,Event.TRIGERTIME,instance.Configuration_instance.ECU-summinCPU, needAdjustCPU)
            if needAdjustMEM != []:
                self.adjust_MEM_AllContainer_AllRunningTasks(booleanDict,Event.TRIGERTIME,instance.Configuration_instance.Memory-summinMEM, needAdjustMEM)
        else:
            if summinCPU/instance.Configuration_instance.ECU < summinMEM/instance.Configuration_instance.Memory:
                booleanDict = { }
                for each in needAdjustCPU:
                    booleanDict[each] = True
                self.adjust_CPU_AllContainer_AllRunningTasks(booleanDict,Event.TRIGERTIME,instance.Configuration_instance.ECU-summinCPU, needAdjustCPU)
                booleanDict = { }
                for each in needAdjustMEM:
                    if each not in needAdjustCPU:
                        booleanDict[each] = True
                    else:
                        booleanDict[each] = False
                self.adjust_MEM_AllContainer_AllRunningTasks(booleanDict,Event.TRIGERTIME,instance.Configuration_instance.Memory-summinMEM, needAdjustMEM)
            else:
                booleanDict = { }
                for each in needAdjustMEM:
                    booleanDict[each] = True

                self.adjust_MEM_AllContainer_AllRunningTasks(booleanDict,Event.TRIGERTIME,instance.Configuration_instance.Memory-summinMEM, needAdjustMEM)
                booleanDict = { }
                for each in needAdjustCPU:
                    if each not in needAdjustMEM:
                        booleanDict[each] = True
                    else:
                        booleanDict[each] = False
                self.adjust_CPU_AllContainer_AllRunningTasks(booleanDict,Event.TRIGERTIME,instance.Configuration_instance.ECU-summinCPU, needAdjustCPU)
            
        list1 = list(set(needAdjustCPU) | set(needAdjustMEM))
        for eachTask in list1: 
            wfID,taskID = int(eachTask.split('-')[0]), int(eachTask.split('-')[1]) 

            Object_Temp = Object(workflowID=wfID,taskID=taskID,cloudProvider=self.multiWorkflows[wfID].DAG[taskID].Assigned.CloudProvider,instance=self.multiWorkflows[wfID].DAG[taskID].Assigned.ID)
            eachContainer = self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1]
            addEvent = EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=eachContainer.latestFinishTime,OBJECT=Object_Temp)  
            self.EVENT.addtoEventQueue(addEvent) 


        summinCPU, summinMEM = 0,0
        for each in instance.runningTask:
            wfID,taskID = each[0],each[1]
            summinCPU += self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].ECU
            summinMEM += self.multiWorkflows[wfID].DAG[taskID].configuration_Container[-1].Memory
        # instance.remainingECU = instance.Configuration_instance.ECU - summinCPU
        # instance.remainingMemory = instance.Configuration_instance.Memory - summinMEM
        Uti_Ins = Utilisation_Instance(time=Event.TRIGERTIME, ECU=summinCPU/instance.Configuration_instance.ECU, Memory=summinMEM/instance.Configuration_instance.Memory)
        instance.Utilisation.append(Uti_Ins)

        self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(Event.OBJECT.cloudProvider)].VMPlatform[Event.OBJECT.instance] = deepcopy(instance) 
        del instance

        # k = 1

        # task_deadline = self.multiWorkflows[wfID].DAG[taskID].terminal_task.SUBDEADLINE
        
        # availableServiceInstance = []
        # for eachPlstformID in range(len(self.MCSPSystem.platform)):  
        #     ComCost = self.caculateTransmissionCost(wfID,taskID,self.MCSPSystem.platform[eachPlstformID].CloudProvider)               
        #     for i in range(len(self.MCSPSystem.platform[eachPlstformID].VMPlatform)):



    def EvaluateFitness(self,):
        # print('{:12}'.format('Triger time:'),
        #         '{:30}'.format('Event type:'),
        #         '{:12}'.format('Workflow ID:'),
        #         '{:8}'.format('Task ID:'),
        #         '{:12}'.format('Cloud provider:'),
        #         '{:12}'.format('Instance ID:'))                  
        # eventNumbers = 0

        # for eachPlatform in self.MCSPSystem.platform:
        #     for eachType in eachPlatform.eachTypeNumbers:
        #         if eachType!=math.inf:   
        #             # instance = deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[eachPlstformID].CloudProvider,
        #             #                                 typeID =i,NewlyCreated=True,TerminalInstance = INSTANCETERMINAL_dict()))
        #             eachPlatform.VMPlatform.append(instance)



        
        # self.fitness.cost_VM = 0.0
        # self.fitness.cost_FaaS = 0.0
        self.fitness.cost_Trans = 0.0



        self.EVENT.eventHistory = []
        while not self.EVENT.empty() and self.throughput <= self.numJobsRecorded:
            '''
                'WORKFLOW_SUBMITTED'  'WORKFLOW_COMPLETED'
                'TASK_READY' 'TASK_STARTED' 'TASK_COMPLETED', 
                'BOOTING_INSTANCE_STARTED' 'BOOTING_INSTANCE_COMPLETED',
                'DATA_TRANSMISSION_STARTED' 'DATA_TRANSMISSION_COMPLETED'                    
            '''

            event = self.EVENT.EVENTQUEUE.pop(0) 
            # self.EVENT.eventHistory.append(event)            
            '''
            WORKFLOW_SUBMITTED First;
            TASK_READY: Assign task to service instace. 
            '''
            match event.EVENTTYPE:
                case 'WORKFLOW_SUBMITTED':
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                    self.eventTriger_WORKFLOW_SUBMITTED(event)
                case 'TASK_READY':
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                    self.eventProcessReady_1Task(self.MCSPSystem.systemTime,event.OBJECT.workflowID,event.OBJECT.taskID)  
                    # self.determineWhetherItsSubtaskReady(event.OBJECT.workflowID,event.OBJECT.taskID)
                case 'TASK_STARTED':
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                    self.eventTriger_ContainerConfiguration(event)
                    self.EVENT.eventHistory.append(event)

                case 'TASK_COMPLETED':
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                    self.eventTriger_ContainerConfiguration(event)
                    self.subTaskNumberinWorkflow(self.MCSPSystem.systemTime,event.OBJECT.workflowID,event.OBJECT.taskID)
             
                # case 'BOOTING_INSTANCE_STARTED':
                #     self.MCSPSystem.systemTime = event.TRIGERTIME
                #     self.EVENT.eventHistory.append(event)
                # case 'BOOTING_INSTANCE_COMPLETED':      
                #     self.MCSPSystem.systemTime = event.TRIGERTIME
                # case 'DATA_TRANSMISSION_STARTED':
                #     self.MCSPSystem.systemTime = event.TRIGERTIME
                # case 'DATA_TRANSMISSION_COMPLETED':
                #     self.MCSPSystem.systemTime = event.TRIGERTIME   
                case 'WORKFLOW_COMPLETED':   
                    self.MCSPSystem.systemTime = event.TRIGERTIME 
                    self.multiWorkflows[event.OBJECT.workflowID].objectives.Cmax = event.TRIGERTIME 
                    self.multiWorkflows[event.OBJECT.workflowID].objectives.missDDL = self.multiWorkflows[event.OBJECT.workflowID].systemDeadline-event.TRIGERTIME
                    self.throughput += 1
                # case 'INSTANCE_WhetherTerminate':   
                #     self.MCSPSystem.systemTime = event.TRIGERTIME 
                # case 'INSTANCE_Terminate':   
                #     self.MCSPSystem.systemTime = event.TRIGERTIME 


        self.fitness.Cost = 0.0 + self.fitness.cost_Trans
        self.fitness.Cmax = self.MCSPSystem.systemTime 
        self.fitness.Energy = 0.0
        # self.fitness.ResourceUtilization = 0.0
        # CPU_RU, MEM_RU = 0,0
        RU_CloudSever, RU_FogSever = [],[]
        for eachPlatform in self.MCSPSystem.platform:
            if eachPlatform.CloudProvider == 'CloudSever':
                # self.fitness.cost_FaaS += eachPlatform.cost_FaaS
                for eachInstance in eachPlatform.VMPlatform:
                    unitPrice = eachInstance.Configuration_instance.unitPrice
                    UtilisationList = eachInstance.Utilisation
                    RU_CloudSever.append(0)
                    for k in range(1,len(UtilisationList)):
                        t1 = UtilisationList[k].time
                        t0 = UtilisationList[k-1].time
                        # CPU_RU += (t1-t0) * UtilisationList[k-1].ECU
                        # MEM_RU += (t1-t0) * UtilisationList[k-1].Memory
                        RU_CloudSever[-1] += (t1-t0) * (UtilisationList[k-1].ECU + UtilisationList[k-1].Memory)/2
                        if UtilisationList[k-1].ECU*UtilisationList[k-1].Memory != 0:
                            self.fitness.Cost += (t1-t0) * unitPrice
                    RU_CloudSever[-1] = RU_CloudSever[-1]/(UtilisationList[len(UtilisationList)-1].time - UtilisationList[0].time)
            elif eachPlatform.CloudProvider == 'FogSever':
                for eachInstance in eachPlatform.VMPlatform:
                    # unitPrice = eachInstance.Configuration_instance.unitPrice
                    StaticPower = eachInstance.Configuration_instance.StaticPower
                    CPU_basedDynamicPower = eachInstance.Configuration_instance.CPU_basedDynamicPower
                    MEM_basedDynamicPower = eachInstance.Configuration_instance.Memory_basedDynamicPower
                    UtilisationList = eachInstance.Utilisation
                    RU_FogSever.append(0)
                    for k in range(1,len(UtilisationList)):
                        t1 = UtilisationList[k].time
                        t0 = UtilisationList[k-1].time
                        # CPU_RU += (t1-t0) * UtilisationList[k-1].ECU
                        # MEM_RU += (t1-t0) * UtilisationList[k-1].Memory
                        RU_FogSever[-1] += (t1-t0) * (UtilisationList[k-1].ECU + UtilisationList[k-1].Memory)/2
                        self.fitness.Energy += (t1-t0) * (StaticPower + CPU_basedDynamicPower*UtilisationList[k-1].ECU + MEM_basedDynamicPower*UtilisationList[k-1].Memory)
                    RU_FogSever[-1] = RU_FogSever[-1]/(UtilisationList[len(UtilisationList)-1].time - UtilisationList[0].time)
                self.fitness.Energy = self.fitness.Energy/(3600*1000)
        if len(RU_CloudSever) == 0:
            aveRU_CloudSever = 0
        else:
            aveRU_CloudSever = sum(RU_CloudSever)/len(RU_CloudSever)
        if len(RU_FogSever) == 0:
            aveRU_FogSever = 0
        else:
            aveRU_FogSever = sum(RU_FogSever)/len(RU_FogSever)
        if aveRU_FogSever*aveRU_CloudSever == 0:
            self.fitness.ResourceUtilization = aveRU_CloudSever + aveRU_FogSever
        else:
            # aveRU_CloudSever = sum(RU_CloudSever)/len(RU_CloudSever)
            # aveRU_FogSever = sum(RU_FogSever)/len(RU_FogSever)
            self.fitness.ResourceUtilization = (aveRU_CloudSever + aveRU_FogSever)/2
                        

        

        k,d = 0,0
        self.fitness.TotalTardiness = 0.0
        for each in self.multiWorkflows:
            d -= (each.objectives.missDDL/each.deadline)
            if each.objectives.missDDL>0:
                k += 1
                self.fitness.TotalTardiness += each.objectives.missDDL
        self.fitness.successfulrate = k/len(self.multiWorkflows)
        self.fitness.deadlineDeviation = d/len(self.multiWorkflows)

        # del RU_CloudSever, RU_FogSever
        # del eachPlatform, eachInstance, UtilisationList
        # del aveRU_CloudSever, aveRU_FogSever
        del self.multiWorkflows, self.MCSPSystem, self.EVENT
        
        return self.fitness # .Cost

