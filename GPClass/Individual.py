from random import choice, randint, shuffle
from statistics import mean
from copy import deepcopy
from GPClass.function_terminal import INSTANCETERMINAL_dict
# from GPClass.Tree import Node
# import GlobalResource
from GPClass.multiCloudSystem import multiCloudSystem,InstanceList,MULTICLOUDsystem
from GPClass.EventClass import *
import random
import numpy as np
from Class.commonFunctionClass import Objectives





def protected_div(left, right):
    with np.errstate(divide='ignore', invalid='ignore'):
        x = np.divide(left, right)
        if isinstance(x, np.ndarray):
            x[np.isinf(x)] = 1
            x[np.isnan(x)] = 1
        elif np.isinf(x) or np.isnan(x):
            x = 1
    return x   
# # @cache
# def treeNode_R(tree, index, terminal):   
#     def recursiveFunction(index):
#         if index in recursiveFunction.cache:
#             return recursiveFunction.cache[index]
#         match tree[index].arity:
#             case 2:
#                 match tree[index].name: 
#                     case 'add':
#                         return recursiveFunction.cache.setdefault(index,recursiveFunction(index+1) + recursiveFunction(index+2))
#                     case 'subtract':
#                         return recursiveFunction.cache.setdefault(index,recursiveFunction(index+1) - recursiveFunction(index+2))
#                     case 'multiply':
#                         return recursiveFunction.cache.setdefault(index,recursiveFunction(index+1) * recursiveFunction(index+2))
#                     case 'protected_div':
#                         return recursiveFunction.cache.setdefault(index,protected_div(recursiveFunction(index+1), recursiveFunction(index+2)))
#                     case 'maximum':
#                         return recursiveFunction.cache.setdefault(index,np.maximum(recursiveFunction(index+1), recursiveFunction(index+2)))
#                     case 'minimum':
#                         return recursiveFunction.cache.setdefault(index,np.minimum(recursiveFunction(index+1), recursiveFunction(index+2)))
#                     case _:
#                         None
#             case 0:
#                 match  tree[index].name:
#                     case 'NUMBERTASKSQUEUE':
#                         return terminal.NUMBERTASKSQUEUE
#                     case 'TOTALEXECUTETIMEQUEUE':
#                         return terminal.TOTALEXECUTETIMEQUEUE
#                     case 'NUMBERREMAININGTASKS':
#                         return terminal.NUMBERREMAININGTASKS
#                     case 'TOTALEXECUTETIMEREMAININGTASKS':
#                         return terminal.TOTALEXECUTETIMEREMAININGTASKS
#                     case 'SLACKTIME':
#                         return terminal.SLACKTIME
#                     # # task  
#                     case 'SUBDEADLINE':
#                         return terminal.SUBDEADLINE
#                     case 'NUMBERSCHILDREN':
#                         return terminal.NUMBERSCHILDREN
#                     case 'NUMBERSFATHER':
#                         return terminal.NUMBERSFATHER        
#                     case 'UPWARDRANK':
#                         return terminal.UPWARDRANK    
#                     case 'EXECUTETIME':
#                         return terminal.EXECUTETIME
#                     case 'AVERAGECOMMUNICATIONTIME':
#                         return terminal.AVERAGECOMMUNICATIONTIME
#                     # # instance
#                     case 'ACTUALAVAILABLETIME':
#                         return terminal.ACTUALAVAILABLETIME
#                     case 'EXECUTECOST':
#                         return terminal.EXECUTECOST
#                     case 'COMMUNICATIONCOST':
#                         return terminal.COMMUNICATIONCOST
#                     case 'ACTUALEXECUTETIME':
#                         return terminal.ACTUALEXECUTETIME
#                     case 'AVERAGESLACKTIME':
#                         return terminal.AVERAGESLACKTIME
#                     case 'INSTANCEAVAILABLETIME':
#                         return terminal.INSTANCEAVAILABLETIME
#                     case 'NUMBERTASKINCLOUD':
#                         return terminal.NUMBERTASKINCLOUD                   
#                     case 'AVERAGEEXECUTECOST':
#                         return terminal.AVERAGEEXECUTECOST 
#                     case 'AVERAGEEXECUTETIME':
#                         return terminal.AVERAGEEXECUTETIME 
#                     case 'AVERAGEACTUALAVAILABLETIME':
#                         return terminal.AVERAGEACTUALAVAILABLETIME 
#                     case 'AVERAGEINSTANCEAVAILABLETIME':
#                         return terminal.AVERAGEINSTANCEAVAILABLETIME 
#                     case _:
#                         None
#             case _:
#                 None                
    
#     recursiveFunction.cache = {}
#     result = recursiveFunction(index)
#     del recursiveFunction.cache
#     return result
   
def treeNode_R(tree, index, terminal):   
    tree_String = str(tree)
    tree_String = tree_String.replace('add','np.add')
    tree_String = tree_String.replace('subtract','np.subtract')
    tree_String = tree_String.replace('multiply','np.multiply')
    tree_String = tree_String.replace('protected_div','protected_div')
    tree_String = tree_String.replace('maximum','np.maximum')
    tree_String = tree_String.replace('minimum','np.minimum')
    try:
        tree_String = tree_String.replace("'NUMBERTASKSQUEUE'",str(terminal.NUMBERTASKSQUEUE))
    except:
        pass
    try:
        tree_String = tree_String.replace("'TOTALEXECUTETIMEQUEUE'",str(terminal.TOTALEXECUTETIMEQUEUE))
    except:
        pass
    try:
        tree_String = tree_String.replace("'NUMBERREMAININGTASKS'",str(terminal.NUMBERREMAININGTASKS))
    except:
        pass
    try:        
        tree_String = tree_String.replace("'TOTALEXECUTETIMEREMAININGTASKS'",str(terminal.TOTALEXECUTETIMEREMAININGTASKS))
    except:
        pass
    try:
        tree_String = tree_String.replace("'SLACKTIME'",str(terminal.SLACKTIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'SUBDEADLINE'",str(terminal.SUBDEADLINE))
    except:
        pass
    try:
        tree_String = tree_String.replace("'NUMBERSCHILDREN'",str(terminal.NUMBERSCHILDREN))
    except:
        pass
    try:
        tree_String = tree_String.replace("'NUMBERSFATHER'",str(terminal.NUMBERSFATHER))
    except:
        pass
    try:
        tree_String = tree_String.replace("'UPWARDRANK'",str(terminal.UPWARDRANK))
    except:
        pass
    try:
        tree_String = tree_String.replace("'EXECUTETIME'",str(terminal.EXECUTETIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'AVERAGECOMMUNICATIONTIME'",str(terminal.AVERAGECOMMUNICATIONTIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'ACTUALAVAILABLETIME'",str(terminal.ACTUALAVAILABLETIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'EXECUTECOST'",str(terminal.EXECUTECOST))
    except:
        pass
    try:
        tree_String = tree_String.replace("'COMMUNICATIONCOST'",str(terminal.COMMUNICATIONCOST))
    except:
        pass
    try:
        tree_String = tree_String.replace("'ACTUALEXECUTETIME'",str(terminal.ACTUALEXECUTETIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'AVERAGESLACKTIME'",str(terminal.AVERAGESLACKTIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'INSTANCEAVAILABLETIME'",str(terminal.INSTANCEAVAILABLETIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'NUMBERTASKINCLOUD'",str(terminal.NUMBERTASKINCLOUD))
    except:
        pass
    try:
        tree_String = tree_String.replace("'AVERAGEEXECUTECOST'",str(terminal.AVERAGEEXECUTECOST))
    except:
        pass
    try:
        tree_String = tree_String.replace("'AVERAGEEXECUTETIME'",str(terminal.AVERAGEEXECUTETIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'AVERAGEACTUALAVAILABLETIME'",str(terminal.AVERAGEACTUALAVAILABLETIME))
    except:
        pass
    try:
        tree_String = tree_String.replace("'AVERAGEINSTANCEAVAILABLETIME'",str(terminal.AVERAGEINSTANCEAVAILABLETIME))
    except:
        pass
    result = eval(tree_String)
    return result
   

class Individual:
    def __init__(self): 
        self.fitness = Objectives()
        self.multiWorkflows = []
        self.MCSPSystem = multiCloudSystem()  # []
        self.EVENT = EventClass()

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



    # # def __lt__(self, other):
    # #     return self.fitness < other.fitness

    # def grow(self, depth):
    #     # self.workflowRoot.growWorkflow(depth)
    #     self.taskRoot.growTask(depth)
    #     self.instanceRoot.growInatance(depth)

    # def full(self, depth):
    #     # self.workflowRoot.fullWorkflow(depth)
    #     self.taskRoot.fullTask(depth)
    #     self.instanceRoot.fullInatance(depth)



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
            Priority = treeNode_R(self.taskRoot, 0, self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)      # self.taskRoot.evaluateTree(self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)
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
            Priority = treeNode_R(self.taskRoot, 0, self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)      #  self.taskRoot.evaluateTree(self.multiWorkflows[each[0]].DAG[each[1]].terminal_task)
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
            self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE += self.multiWorkflows[wfID].DAG[each].runtimePerCPU_Memory
            # self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_LIST['TASK_READY'],TRIGERTIME=Time,OBJECT=Object(workflowID=wfID,taskID=each))) 
        self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE += len( self.multiWorkflows[wfID].DAGLevel[0])

    def add_TaskQueue_List(self,taskList):      
        for eachtask in taskList:
            wfID,each = eachtask[0],eachtask[1]
            self.taskQueue.append([wfID,each])
            self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE += self.multiWorkflows[wfID].DAG[each].runtimePerCPU_Memory
            # self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_LIST['TASK_READY'],TRIGERTIME=Time,OBJECT=Object(workflowID=wfID,taskID=each))) 
            self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE += 1

    def add_TaskQueue_1(self,wfID,taskID):  
        self.taskQueue.append([wfID,taskID])
        self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE += self.multiWorkflows[wfID].DAG[taskID].runtimePerCPU_Memory
        self.multiWorkflows[wfID].terminal_workflow.NUMBERTASKSQUEUE += 1      
    
    def sub_TaskQueue_1(self,wfID,taskID):  
        self.taskQueue.remove([wfID,taskID])      
        # self.subTaskNumberinWorkflow(wfID,taskID)
        self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEQUEUE -= self.multiWorkflows[wfID].DAG[taskID].runtimePerCPU_Memory
        self.multiWorkflows[wfID].terminal_workflow.TOTALEXECUTETIMEREMAININGTASKS -= self.multiWorkflows[wfID].DAG[taskID].runtimePerCPU_Memory
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
            self.multiWorkflows[each.OBJECT.workflowID].objectives.cost_VM = 0.0
            self.multiWorkflows[each.OBJECT.workflowID].objectives.cost_FaaS = 0.0
            self.multiWorkflows[each.OBJECT.workflowID].objectives.cost_Trans = 0.0            
            self.multiWorkflows[each.OBJECT.workflowID].NUMBERTASKINCLOUD= [0 for each in range(len(self.MCSPSystem.platform))]
            self.add_TaskQueue_FirstLevel(each.OBJECT.workflowID)
        self.sortTaskQueue_addEventQueue(self.MCSPSystem.systemTime)        

        # self.add_TaskQueue_First(event.OBJECT.workflowID,self.MCSPSystem.systemTime)


    def calculateCommunicationTime(self,wfID,taskID,temp_Instance):
        CommunicationTime = 0
        maxFatherFinishTimeplusCT = 0
        for father_ofchild in self.multiWorkflows[wfID].DAG[taskID].inputs:                
            if (self.multiWorkflows[wfID].DAG[taskID].Category[0]==self.multiWorkflows[wfID].DAG[father_ofchild.id].Category[0]):
                if self.multiWorkflows[wfID].DAG[taskID].Category[0]==self.MCSPSystem.Category[2].Category: #['Office365']:
                    continue
                elif (self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned.CloudProvider == temp_Instance.CloudProvider):
                    if self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned.ID== temp_Instance.ID:
                        continue
                    else:
                        CommunicationTime= max(CommunicationTime,father_ofchild.size/self.MCSPSystem.bandwidth_in1Cloud)
                else:
                    CommunicationTime= max(CommunicationTime,father_ofchild.size/self.MCSPSystem.bandwidth_Clouds)
            elif (self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned.CloudProvider == temp_Instance.CloudProvider):
                CommunicationTime= max(CommunicationTime,father_ofchild.size/self.MCSPSystem.bandwidth_in1Cloud)
            else:
                CommunicationTime= max(CommunicationTime,father_ofchild.size/self.MCSPSystem.bandwidth_Clouds) 
            maxFatherFinishTimeplusCT = max(maxFatherFinishTimeplusCT,self.multiWorkflows[wfID].DAG[father_ofchild.id].FinishTime +  CommunicationTime)              
        return CommunicationTime,maxFatherFinishTimeplusCT
       
    def determineWhetherItsSubtaskReady(self,wfID,taskID):
        childList = []
        for child in self.multiWorkflows[wfID].DAG[taskID].outputs:
            finish_Boolean = True
            for father_ofchild in self.multiWorkflows[wfID].DAG[child.id].inputs:
                if self.multiWorkflows[wfID].DAG[father_ofchild.id].Assigned==None:
                    finish_Boolean = False
                    break
            if finish_Boolean: # Child can be set Ready and add to Event.
                childList.append([wfID,child.id])
        if len(childList)>1:
            self.add_TaskQueue_List(childList)
            self.sortTaskQueue_addEventQueue(self.multiWorkflows[wfID].DAG[taskID].StartTime)   
        elif len(childList)==1:
            # self.subTaskNumberinWorkflow(wfID,childList[0][1])     FinishTime
            self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_READY'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,
                                                        OBJECT=Object(workflowID=childList[0][0],taskID=childList[0][1])))
                # self.taskQueue.append([wfID,child.id])
                # self.add_TaskQueue_1(wfID,child.id)                 

    def subTaskNumberinWorkflow(self,wfID,taskID):
        self.multiWorkflows[wfID].DAGLevel[self.multiWorkflows[wfID].DAG[taskID].Level].remove(taskID)        
        self.multiWorkflows[wfID].unscheduledTaskNumber-=1
        if  self.multiWorkflows[wfID].unscheduledTaskNumber==0:       
            self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['WORKFLOW_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].FinishTime,
                                                        OBJECT=Object(workflowID=wfID)))
        # else:
        #     self.determineWhetherItsSubtaskReady(wfID,taskID)
           
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
            if each.TerminalInstance.ACTUALAVAILABLETIME + each.TerminalInstance.ACTUALEXECUTETIME <= task_deadline:
               meetDL.append(each)
        if meetDL == []:
            time1 = np.inf
            for each in availableServiceInstance:            
                if each.TerminalInstance.ACTUALAVAILABLETIME + each.TerminalInstance.ACTUALEXECUTETIME <time1:
                    time1 = each.TerminalInstance.ACTUALAVAILABLETIME + each.TerminalInstance.ACTUALEXECUTETIME
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
        # cloudProvider,instance = 0, 0
        # self.taskQueue.remove([wfID,taskID])
        # self.multiWorkflows[wfID].DAGLevel[self.multiWorkflows[wfID].DAG[taskID].Level].remove(taskID)
        # self.sub_TaskQueue_1(wfID,taskID)
        if self.multiWorkflows[wfID].DAG[taskID].Category[0]==self.MCSPSystem.Category[0].Category: #['vm']:
            availableServiceInstance = []
            # availableCloud = []
            for eachPlstformID in range(len(self.MCSPSystem.platform)):  
                if self.MCSPSystem.platform[eachPlstformID].CloudProvider in self.MCSPSystem.Category[0].CloudProvider:
                    ''' 1 '''
                    # availableServiceInstance.append([])     
                    avaList = []  
                    ComCost = self.caculateTransmissionCost(wfID,taskID,self.MCSPSystem.platform[eachPlstformID].CloudProvider)               
                    for i in range(len(self.MCSPSystem.platform[eachPlstformID].VMPlatform)):  #  have been created
                        # if self.MCSPSystem.platform[eachPlstformID].VMPlatform[i].InstanceState != InstanceState_Dict['Terminated']:
                        temp_Instance = self.MCSPSystem.platform[eachPlstformID].VMPlatform[i]
                        CommunicationTime,maxFatherFinishTimeplusCT = self.calculateCommunicationTime(wfID,taskID,temp_Instance)
                        temp_Instance.TerminalInstance.ACTUALAVAILABLETIME = max(Time1,temp_Instance.CompleteTime,maxFatherFinishTimeplusCT)
                        temp_Instance.TerminalInstance.EXECUTECOST = self.MCSPSystem.platform[eachPlstformID].VMType.caculateCost(temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID])
                        temp_Instance.TerminalInstance.COMMUNICATIONCOST = ComCost # self.caculateTransmissionCost(wfID,taskID,temp_Instance.CloudProvider)
                        temp_Instance.TerminalInstance.ACTUALEXECUTETIME = self.MCSPSystem.platform[eachPlstformID].VMType.caculateExecuteTime(temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID])# self.multiWorkflows[wfID].DAG[taskID].runtime
                        temp_Instance.TerminalInstance.INSTANCEAVAILABLETIME = temp_Instance.CompleteTime # Time1 
                        temp_Instance.TerminalInstance.SLACKTIME = temp_Instance.TerminalInstance.ACTUALAVAILABLETIME - task_deadline
                        temp_Instance.TerminalInstance.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 
                        # availableServiceInstance.append(temp_Instance)
                        avaList.append(temp_Instance)
                    
                    for i in range(self.MCSPSystem.platform[eachPlstformID].VMType.Numbers): #  test new Creat Instance
                        temp_Instance= deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[eachPlstformID].CloudProvider,
                                                    typeID =i,NewlyCreated=True,TerminalInstance = INSTANCETERMINAL_dict()))
                        CommunicationTime,maxFatherFinishTimeplusCT = self.calculateCommunicationTime(wfID,taskID,temp_Instance)
                        temp_Instance.TerminalInstance.ACTUALAVAILABLETIME = max(Time1 + self.MCSPSystem.vmColdStartup, maxFatherFinishTimeplusCT)
                        temp_Instance.TerminalInstance.EXECUTECOST = (self.MCSPSystem.platform[eachPlstformID].VMType.caculateCost(
                                                                temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID]) + 
                                                                self.MCSPSystem.platform[eachPlstformID].VMType.bootingCost(i))
                        temp_Instance.TerminalInstance.COMMUNICATIONCOST = ComCost
                        temp_Instance.TerminalInstance.ACTUALEXECUTETIME = self.MCSPSystem.platform[eachPlstformID].VMType.caculateExecuteTime(temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID]) # self.multiWorkflows[wfID].DAG[taskID].runtime
                        temp_Instance.TerminalInstance.INSTANCEAVAILABLETIME = Time1 + self.MCSPSystem.vmColdStartup
                        temp_Instance.TerminalInstance.SLACKTIME = temp_Instance.TerminalInstance.ACTUALAVAILABLETIME - task_deadline
                        temp_Instance.TerminalInstance.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 
                        # availableServiceInstance.append(temp_Instance)
                        avaList.append(temp_Instance) 
            
                    availableCloud = {}
                    availableCloud['AVERAGEEXECUTECOST'] = mean([each.TerminalInstance.EXECUTECOST for each in avaList] )
                    availableCloud['AVERAGEEXECUTETIME'] = mean([each.TerminalInstance.ACTUALEXECUTETIME for each in avaList] )
                    availableCloud['AVERAGEACTUALAVAILABLETIME'] = mean([each.TerminalInstance.ACTUALAVAILABLETIME for each in avaList] )
                    availableCloud['AVERAGEINSTANCEAVAILABLETIME'] = mean([each.TerminalInstance.INSTANCEAVAILABLETIME for each in avaList] )
                    availableCloud['AVERAGESLACKTIME'] = mean([each.TerminalInstance.SLACKTIME for each in avaList] )
                    for each in avaList:
                        each.TerminalInstance.AVERAGEEXECUTECOST = availableCloud['AVERAGEEXECUTECOST']
                        each.TerminalInstance.AVERAGEEXECUTETIME = availableCloud['AVERAGEEXECUTETIME']
                        each.TerminalInstance.AVERAGEACTUALAVAILABLETIME = availableCloud['AVERAGEACTUALAVAILABLETIME']
                        each.TerminalInstance.AVERAGEINSTANCEAVAILABLETIME = availableCloud['AVERAGEINSTANCEAVAILABLETIME']
                        each.TerminalInstance.AVERAGESLACKTIME = availableCloud['AVERAGESLACKTIME']
                    availableServiceInstance.extend(avaList)   


            

            #         availableCloud.append(deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[eachPlstformID].CloudProvider,TerminalCloud = CLOUDPLATFORMTERMINAL_dict())))  #  {0:CLOUDPLATFORMTERMINAL_dict(),1:None}
            #         availableCloud[-1].TerminalCloud.COMMUNICATIONCOST = ComCost # mean([each.TerminalInstance.COMMUNICATIONCOST for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEEXECUTECOST = mean([each.TerminalInstance.EXECUTECOST for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEEXECUTETIME = mean([each.TerminalInstance.ACTUALEXECUTETIME for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEACTUALAVAILABLETIME = mean([each.TerminalInstance.ACTUALAVAILABLETIME for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEINSTANCEAVAILABLETIME = mean([each.TerminalInstance.INSTANCEAVAILABLETIME for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 
            #         availableCloud[-1].Priority = treeNode_R(self.cloudRoot, 0, availableCloud[-1].TerminalCloud)
            
            # availableCloud = self.sort_availableServiceInstance(availableCloud)
            # selectedCloud = availableCloud[self.selectOneCloud(availableCloud)].CloudProvider  # priorityIndex 
            # k= 1
            # for availableInstance in availableServiceInstance:
            #     if availableInstance[0].CloudProvider==selectedCloud:
            #         for eachInstance in availableInstance:
            #             eachInstance.Priority = treeNode_R(self.instanceRoot, 0, eachInstance.TerminalInstance )
            #         availableInstance = self.sort_availableServiceInstance(availableInstance)
            #         selectedInstance = self.selectOneInstance(task_deadline,availableInstance) #availableInstance[] availableInstance[priorityIndex]  # self.selectOneCloud(availableInstance)
            #         break
            for eachInstance in availableServiceInstance:
                # treeNode_R.cache = {}
                eachInstance.Priority = treeNode_R(self.instanceRoot, 0, eachInstance.TerminalInstance )   
                # del treeNode_R.cache
                # Priority1 = treeNode_R_NoCache(self.instanceRoot, 0, eachInstance.TerminalInstance ) 
                # if eachInstance.Priority!=Priority1:
                #     print(eachInstance.Priority!=Priority1)                 
            availableServiceInstance = self.sort_availableServiceInstance(availableServiceInstance)         
            selectedInstance = self.selectOneInstance(task_deadline,availableServiceInstance)

            CloudProviderID = self.MCSPSystem.getCloudProviderID(selectedInstance.CloudProvider)
            ''' 1 '''
            if selectedInstance.NewlyCreated:
                selectedInstance.ID = len(self.MCSPSystem.platform[CloudProviderID].VMPlatform)
                Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=selectedInstance.CloudProvider,instance=selectedInstance.ID,InstanceCategory=self.MCSPSystem.Category[0].Category)
                
            else:
                Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=selectedInstance.CloudProvider,instance=selectedInstance.ID,InstanceCategory=self.MCSPSystem.Category[0].Category)

            self.multiWorkflows[wfID].DAG[taskID].Assigned = deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[CloudProviderID].CloudProvider,
                                                                            ID=selectedInstance.ID,typeID= selectedInstance.typeID,))
            self.multiWorkflows[wfID].DAG[taskID].StartTime = selectedInstance.TerminalInstance.ACTUALAVAILABLETIME
            self.multiWorkflows[wfID].DAG[taskID].AET=  selectedInstance.TerminalInstance.ACTUALEXECUTETIME  # self.multiWorkflows[wfID].DAG[taskID].runtime / selectedInstance.
            self.multiWorkflows[wfID].NUMBERTASKINCLOUD[CloudProviderID] += 1
            self.fitness.Cost += selectedInstance.TerminalInstance.COMMUNICATIONCOST + selectedInstance.TerminalInstance.EXECUTECOST
            self.fitness.cost_VM += selectedInstance.TerminalInstance.EXECUTECOST
            # self.fitness.cost_FaaS += 
            self.fitness.cost_Trans +=  selectedInstance.TerminalInstance.COMMUNICATIONCOST            
            self.multiWorkflows[wfID].objectives.cost += selectedInstance.TerminalInstance.COMMUNICATIONCOST + selectedInstance.TerminalInstance.EXECUTECOST
            self.multiWorkflows[wfID].objectives.cost_VM += selectedInstance.TerminalInstance.EXECUTECOST
            # self.multiWorkflows[wfID].objectives.cost_FaaS += 
            self.multiWorkflows[wfID].objectives.cost_Trans +=  selectedInstance.TerminalInstance.COMMUNICATIONCOST

            selectedInstance.taskSequence.append([wfID,taskID])
            selectedInstance.timeTable.append([self.multiWorkflows[wfID].DAG[taskID].StartTime,self.multiWorkflows[wfID].DAG[taskID].FinishTime])
            selectedInstance.CompleteTime = max(selectedInstance.CompleteTime,self.multiWorkflows[wfID].DAG[taskID].FinishTime)
            
            if selectedInstance.NewlyCreated:
                selectedInstance.NewlyCreated = False            
                self.MCSPSystem.platform[CloudProviderID].VMPlatform.append(selectedInstance)
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['BOOTING_INSTANCE_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime-self.MCSPSystem.vmColdStartup,OBJECT=Object_Temp)) 
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['BOOTING_INSTANCE_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 
            else:
                self.MCSPSystem.platform[CloudProviderID].VMPlatform[selectedInstance.ID] = selectedInstance

            CCT,gg = self.calculateCommunicationTime(wfID,taskID,selectedInstance)
            if CCT!=0:
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime-CCT,OBJECT=Object_Temp)) 
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 

            self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 
            self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].FinishTime,OBJECT=Object_Temp)) 

        elif self.multiWorkflows[wfID].DAG[taskID].Category[0]==self.MCSPSystem.Category[1].Category: #['FaaS']:
            availableServiceInstance = []
            # availableCloud = []
            for eachPlstformID in range(len(self.MCSPSystem.platform)):  
                if self.MCSPSystem.platform[eachPlstformID].CloudProvider in self.MCSPSystem.Category[1].CloudProvider:
                    ''' 2 '''
                    # availableServiceInstance.append([])     
                    avaList = []
                    ComCost = self.caculateTransmissionCost(wfID,taskID,self.MCSPSystem.platform[eachPlstformID].CloudProvider)                      
                    for i in range(len(self.MCSPSystem.platform[eachPlstformID].FaaSPlatform)):  #  have been created
                        # if self.MCSPSystem.platform[eachPlstformID].FaaSPlatform[i].InstanceState != InstanceState_Dict['Terminated']:
                        temp_Instance = self.MCSPSystem.platform[eachPlstformID].FaaSPlatform[i]
                        CommunicationTime,maxFatherFinishTimeplusCT = self.calculateCommunicationTime(wfID,taskID,temp_Instance)
                        temp_Instance.TerminalInstance.ACTUALAVAILABLETIME = max(Time1,temp_Instance.CompleteTime,maxFatherFinishTimeplusCT ) # + self.calculateCommunicationTime(wfID,taskID,temp_Instance) 
                        temp_Instance.TerminalInstance.EXECUTECOST = self.MCSPSystem.platform[eachPlstformID].FaaSType.caculateCost(temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID])
                        temp_Instance.TerminalInstance.COMMUNICATIONCOST = ComCost # self.caculateTransmissionCost(wfID,taskID,temp_Instance.CloudProvider)
                        temp_Instance.TerminalInstance.ACTUALEXECUTETIME = self.MCSPSystem.platform[eachPlstformID].FaaSType.caculateExecuteTime(temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID])# self.multiWorkflows[wfID].DAG[taskID].runtime
                        temp_Instance.TerminalInstance.SLACKTIME = temp_Instance.TerminalInstance.ACTUALAVAILABLETIME - task_deadline
                        if temp_Instance.TerminalInstance.ACTUALEXECUTETIME>=900:
                            continue
                        temp_Instance.TerminalInstance.INSTANCEAVAILABLETIME = temp_Instance.CompleteTime # Time1 
                        temp_Instance.TerminalInstance.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 
                        # availableServiceInstance.append(temp_Instance)
                        avaList.append(temp_Instance)
                
                    
                    for i in range(self.MCSPSystem.platform[eachPlstformID].FaaSType.Numbers): #  test new Creat Instance
                        temp_Instance= deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[eachPlstformID].CloudProvider,
                                                    typeID =i,NewlyCreated=True,TerminalInstance = INSTANCETERMINAL_dict()))
                        CommunicationTime,maxFatherFinishTimeplusCT = self.calculateCommunicationTime(wfID,taskID,temp_Instance)
                        temp_Instance.TerminalInstance.ACTUALAVAILABLETIME = max(Time1 + self.MCSPSystem.FaasColdStartup,maxFatherFinishTimeplusCT) #  + self.calculateCommunicationTime(wfID,taskID,temp_Instance) 
                        temp_Instance.TerminalInstance.EXECUTECOST = (self.MCSPSystem.platform[eachPlstformID].FaaSType.caculateCost(
                                                                    temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID]))  
                                                                    # +self.MCSPSystem.platform[eachPlstformID].FaaSType.bootingCost(i) 
                        temp_Instance.TerminalInstance.COMMUNICATIONCOST = ComCost # self.caculateTransmissionCost(wfID,taskID,temp_Instance.CloudProvider)
                        temp_Instance.TerminalInstance.ACTUALEXECUTETIME = self.MCSPSystem.platform[eachPlstformID].FaaSType.caculateExecuteTime(temp_Instance.typeID,self.multiWorkflows[wfID].DAG[taskID]) # self.multiWorkflows[wfID].DAG[taskID].runtime
                        temp_Instance.TerminalInstance.SLACKTIME = temp_Instance.TerminalInstance.ACTUALAVAILABLETIME - task_deadline
                        if temp_Instance.TerminalInstance.ACTUALEXECUTETIME>=900:
                            continue
                        temp_Instance.TerminalInstance.INSTANCEAVAILABLETIME = Time1 + self.MCSPSystem.FaasColdStartup
                        temp_Instance.TerminalInstance.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 
                        # availableServiceInstance.append(temp_Instance) 
                        avaList.append(temp_Instance)

                    availableCloud = {}
                    availableCloud['AVERAGEEXECUTECOST'] = mean([each.TerminalInstance.EXECUTECOST for each in avaList] )
                    availableCloud['AVERAGEEXECUTETIME'] = mean([each.TerminalInstance.ACTUALEXECUTETIME for each in avaList] )
                    availableCloud['AVERAGEACTUALAVAILABLETIME'] = mean([each.TerminalInstance.ACTUALAVAILABLETIME for each in avaList] )
                    availableCloud['AVERAGEINSTANCEAVAILABLETIME'] = mean([each.TerminalInstance.INSTANCEAVAILABLETIME for each in avaList] )
                    availableCloud['AVERAGESLACKTIME'] = mean([each.TerminalInstance.SLACKTIME for each in avaList] )
                    for each in avaList:
                        each.TerminalInstance.AVERAGEEXECUTECOST = availableCloud['AVERAGEEXECUTECOST']
                        each.TerminalInstance.AVERAGEEXECUTETIME = availableCloud['AVERAGEEXECUTETIME']
                        each.TerminalInstance.AVERAGEACTUALAVAILABLETIME = availableCloud['AVERAGEACTUALAVAILABLETIME']
                        each.TerminalInstance.AVERAGEINSTANCEAVAILABLETIME = availableCloud['AVERAGEINSTANCEAVAILABLETIME']
                        each.TerminalInstance.AVERAGESLACKTIME = availableCloud['AVERAGESLACKTIME']
                    availableServiceInstance.extend(avaList)   

            #         availableCloud.append(deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[eachPlstformID].CloudProvider,TerminalCloud = CLOUDPLATFORMTERMINAL_dict())))  #  {0:CLOUDPLATFORMTERMINAL_dict(),1:None}
            #         availableCloud[-1].TerminalCloud.COMMUNICATIONCOST = ComCost  # mean([each.TerminalInstance.COMMUNICATIONCOST for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEEXECUTECOST = mean([each.TerminalInstance.EXECUTECOST for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEEXECUTETIME = mean([each.TerminalInstance.ACTUALEXECUTETIME for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEACTUALAVAILABLETIME = mean([each.TerminalInstance.ACTUALAVAILABLETIME for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.AVERAGEINSTANCEAVAILABLETIME = mean([each.TerminalInstance.INSTANCEAVAILABLETIME for each in availableServiceInstance[-1]] )
            #         availableCloud[-1].TerminalCloud.NUMBERTASKINCLOUD = self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] 
            #         availableCloud[-1].Priority = treeNode_R(self.cloudRoot, 0, availableCloud[-1].TerminalCloud)


            # availableCloud = self.sort_availableServiceInstance(availableCloud)
            # selectedCloud = availableCloud[self.selectOneCloud(availableCloud)].CloudProvider
            # for availableInstance in availableServiceInstance:
            #     if availableInstance[0].CloudProvider==selectedCloud:
            #         for eachInstance in availableInstance:
            #             eachInstance.Priority = treeNode_R(self.instanceRoot, 0, eachInstance.TerminalInstance )
            #         availableInstance = self.sort_availableServiceInstance(availableInstance)
            #         selectedInstance = self.selectOneInstance(task_deadline,availableInstance) # availableInstance[self.selectOneInstance(availableInstance)] #  availableInstance[priorityIndex]  # self.selectOneCloud(availableInstance)
            #         break
            for eachInstance in availableServiceInstance:
                # treeNode_R.cache = {}
                eachInstance.Priority = treeNode_R(self.instanceRoot, 0, eachInstance.TerminalInstance )    
                # del treeNode_R.cache
                # Priority1 = treeNode_R_NoCache(self.instanceRoot, 0, eachInstance.TerminalInstance )   
                # if eachInstance.Priority!=Priority1:
                #     print(eachInstance.Priority!=Priority1)                                           
            availableServiceInstance = self.sort_availableServiceInstance(availableServiceInstance)
            selectedInstance = self.selectOneInstance(task_deadline,availableServiceInstance)

            CloudProviderID = self.MCSPSystem.getCloudProviderID(selectedInstance.CloudProvider)
            ''' 2 '''
            if selectedInstance.NewlyCreated:
                # selectedInstance.NewlyCreated = False
                selectedInstance.ID = len(self.MCSPSystem.platform[CloudProviderID].FaaSPlatform)
                Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=selectedInstance.CloudProvider,instance=selectedInstance.ID,InstanceCategory=self.MCSPSystem.Category[1].Category)
            else:
                Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=selectedInstance.CloudProvider,instance=selectedInstance.ID,InstanceCategory=self.MCSPSystem.Category[1].Category)

            self.multiWorkflows[wfID].DAG[taskID].Assigned = deepcopy(InstanceList(CloudProvider=self.MCSPSystem.platform[CloudProviderID].CloudProvider,
                                                                            ID=selectedInstance.ID,typeID= selectedInstance.typeID,))
            self.multiWorkflows[wfID].DAG[taskID].StartTime = selectedInstance.TerminalInstance.ACTUALAVAILABLETIME
            self.multiWorkflows[wfID].DAG[taskID].AET=  selectedInstance.TerminalInstance.ACTUALEXECUTETIME  # self.multiWorkflows[wfID].DAG[taskID].runtime / selectedInstance.
            self.multiWorkflows[wfID].NUMBERTASKINCLOUD[CloudProviderID] += 1
            self.fitness.Cost += selectedInstance.TerminalInstance.COMMUNICATIONCOST + selectedInstance.TerminalInstance.EXECUTECOST
            # self.fitness.cost_VM += 
            self.fitness.cost_FaaS += selectedInstance.TerminalInstance.EXECUTECOST
            self.fitness.cost_Trans +=  selectedInstance.TerminalInstance.COMMUNICATIONCOST             
            self.multiWorkflows[wfID].objectives.cost += selectedInstance.TerminalInstance.COMMUNICATIONCOST + selectedInstance.TerminalInstance.EXECUTECOST
            # self.multiWorkflows[wfID].objectives.cost_VM += 
            self.multiWorkflows[wfID].objectives.cost_FaaS += selectedInstance.TerminalInstance.EXECUTECOST
            self.multiWorkflows[wfID].objectives.cost_Trans +=  selectedInstance.TerminalInstance.COMMUNICATIONCOST            
            selectedInstance.taskSequence.append([wfID,taskID])
            selectedInstance.timeTable.append([self.multiWorkflows[wfID].DAG[taskID].StartTime,self.multiWorkflows[wfID].DAG[taskID].FinishTime])
            selectedInstance.CompleteTime = max(selectedInstance.CompleteTime,self.multiWorkflows[wfID].DAG[taskID].FinishTime)

            if selectedInstance.NewlyCreated:
                selectedInstance.NewlyCreated = False            
                self.MCSPSystem.platform[CloudProviderID].FaaSPlatform.append(selectedInstance)
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['BOOTING_INSTANCE_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime-self.MCSPSystem.FaasColdStartup,OBJECT=Object_Temp)) 
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['BOOTING_INSTANCE_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 

            else:
                self.MCSPSystem.platform[CloudProviderID].FaaSPlatform[selectedInstance.ID] = selectedInstance

            # self.MCSPSystem.platform[CloudProviderID].FaaSPlatform.append(selectedInstance)
            CCT,gg = self.calculateCommunicationTime(wfID,taskID,selectedInstance)
            if CCT!=0:
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime-CCT,OBJECT=Object_Temp)) 
                self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 

            self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 
            self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].FinishTime,OBJECT=Object_Temp)) 

        elif self.multiWorkflows[wfID].DAG[taskID].Category[0]==self.MCSPSystem.Category[2].Category: #['Office365']:
            '''
                Assume that office365 executes directly. 
                Execution time needs to be modified.
            '''
            for eachPlstformID in range(len(self.MCSPSystem.platform)):
                if self.MCSPSystem.platform[eachPlstformID].CloudProvider in self.MCSPSystem.Category[2].CloudProvider:

                    self.multiWorkflows[wfID].DAG[taskID].Assigned = deepcopy(InstanceList(CloudProvider=self.MCSPSystem.CloudProvider[eachPlstformID],))
                    CommunicationTime,maxFatherFinishTimeplusCT = self.calculateCommunicationTime(wfID,taskID,self.multiWorkflows[wfID].DAG[taskID].Assigned)
                    self.multiWorkflows[wfID].DAG[taskID].StartTime = max(Time1, maxFatherFinishTimeplusCT) # +self.calculateCommunicationTime(wfID,taskID,self.multiWorkflows[wfID].DAG[taskID].Assigned)
                    self.multiWorkflows[wfID].DAG[taskID].AET= self.multiWorkflows[wfID].DAG[taskID].runtime / MULTICLOUDsystem.averageMIPS.Office365 # GlobalResource.maxECU
                    self.multiWorkflows[wfID].NUMBERTASKINCLOUD[eachPlstformID] += 1
                    
                    self.MCSPSystem.platform[eachPlstformID].Office365Platform.taskSequence.append([wfID,taskID])
                    self.MCSPSystem.platform[eachPlstformID].Office365Platform.timeTable.append([self.multiWorkflows[wfID].DAG[taskID].StartTime,self.multiWorkflows[wfID].DAG[taskID].FinishTime])


                    Object_Temp=Object(workflowID=wfID,taskID=taskID,cloudProvider=self.MCSPSystem.CloudProvider[eachPlstformID],
                                        instance=len(self.MCSPSystem.platform[eachPlstformID].Office365Platform.taskSequence),
                                        InstanceCategory = self.MCSPSystem.Category[2].Category    )
                    if CommunicationTime!=0:
                        self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_STARTED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime-CommunicationTime,OBJECT=Object_Temp)) 
                        self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['DATA_TRANSMISSION_COMPLETED'],TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) 

                    self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_STARTED'],
                                                          TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].StartTime,OBJECT=Object_Temp)) #: ['Office365']
                    self.EVENT.addtoEventQueue( EventType(EVENTTYPE=EVENTTYPE_DICT['TASK_COMPLETED'],
                                                          TRIGERTIME=self.multiWorkflows[wfID].DAG[taskID].FinishTime,OBJECT=Object_Temp)) #: ['Office365']
                    break 
# ,InstanceCategory=self.MCSPSystem.Category[1].Category
        # self.determineWhetherItsSubtaskReady(wfID,taskID)
    
            
        #     pass                
        # 




        
        # return cloudProvider,instance


    def EvaluateFitness(self,):
        # print('{:12}'.format('Triger time:'),
        #         '{:30}'.format('Event type:'),
        #         '{:12}'.format('Workflow ID:'),
        #         '{:8}'.format('Task ID:'),
        #         '{:12}'.format('Cloud provider:'),
        #         '{:12}'.format('Instance ID:'))                  
        # eventNumbers = 0

        self.fitness.Cost = 0.0
        self.fitness.cost_VM = 0.0
        self.fitness.cost_FaaS = 0.0
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
                    self.determineWhetherItsSubtaskReady(event.OBJECT.workflowID,event.OBJECT.taskID)
                case 'TASK_STARTED':
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                    self.EVENT.eventHistory.append(event)
                    # if (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category and
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState == InstanceState_Dict['Idle']):
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
                    #     delevent = EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_Terminate'], OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory))
                    #     self.EVENT.delOneTerminateEnventinQueue(delevent)
                    # elif (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category and
                    #       self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState == InstanceState_Dict['Idle']):
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
                    #     delevent = EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_Terminate'], OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory))
                    #     self.EVENT.delOneTerminateEnventinQueue(delevent)

                case 'TASK_COMPLETED':
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                    self.subTaskNumberinWorkflow(event.OBJECT.workflowID,event.OBJECT.taskID)
                    
                    # if (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category and
                    #     event.TRIGERTIME>=self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].CompleteTime):
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Idle']
                    #     self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_WhetherTerminate'], TRIGERTIME=event.TRIGERTIME,
                    #                 OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory)))
                    # elif (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category and
                    #       event.TRIGERTIME>=self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].CompleteTime):
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Idle']
                    #     self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_WhetherTerminate'], TRIGERTIME=event.TRIGERTIME,
                    #                 OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory)))
                    
                case 'BOOTING_INSTANCE_STARTED':
                    # if event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category:
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Booting']
                    # elif event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category:
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Booting']
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                    self.EVENT.eventHistory.append(event)
                case 'BOOTING_INSTANCE_COMPLETED':
                    # if event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category:
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
                    # elif event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category:
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
                    
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                case 'DATA_TRANSMISSION_STARTED':
                    self.MCSPSystem.systemTime = event.TRIGERTIME
                case 'DATA_TRANSMISSION_COMPLETED':
                    self.MCSPSystem.systemTime = event.TRIGERTIME   
                case 'WORKFLOW_COMPLETED':   
                    self.MCSPSystem.systemTime = event.TRIGERTIME 
                    self.multiWorkflows[event.OBJECT.workflowID].objectives.Cmax = event.TRIGERTIME 
                    self.multiWorkflows[event.OBJECT.workflowID].objectives.missDDL = self.multiWorkflows[event.OBJECT.workflowID].systemDeadline-event.TRIGERTIME
                    self.throughput += 1
                case 'INSTANCE_WhetherTerminate':   
                    self.MCSPSystem.systemTime = event.TRIGERTIME 
                    # self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_Terminate'], TRIGERTIME=event.TRIGERTIME+self.MCSPSystem.IdleTimetoTerminate,
                    #                 OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory)))
                case 'INSTANCE_Terminate':   
                    self.MCSPSystem.systemTime = event.TRIGERTIME 
                    # if event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category:
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Terminated']
                    # elif event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category:
                    #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Terminated']
                    
            # '''
            # WORKFLOW_SUBMITTED First;
            # TASK_READY: Assign task to service instace. 
            # '''
            # if event.EVENTTYPE==EVENTTYPE_DICT['WORKFLOW_SUBMITTED']:
            #     self.MCSPSystem.systemTime = event.TRIGERTIME
            #     self.eventTriger_WORKFLOW_SUBMITTED(event)
            # elif event.EVENTTYPE==EVENTTYPE_DICT['TASK_READY']:
            #     self.MCSPSystem.systemTime = event.TRIGERTIME
            #     self.eventProcessReady_1Task(self.MCSPSystem.systemTime,event.OBJECT.workflowID,event.OBJECT.taskID)  
            #     self.determineWhetherItsSubtaskReady(event.OBJECT.workflowID,event.OBJECT.taskID)
            # elif event.EVENTTYPE==EVENTTYPE_DICT['TASK_STARTED']:
            #     self.MCSPSystem.systemTime = event.TRIGERTIME
            #     self.EVENT.eventHistory.append(event)
            #     # if (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category and
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState == InstanceState_Dict['Idle']):
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
            #     #     delevent = EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_Terminate'], OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory))
            #     #     self.EVENT.delOneTerminateEnventinQueue(delevent)
            #     # elif (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category and
            #     #       self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState == InstanceState_Dict['Idle']):
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
            #     #     delevent = EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_Terminate'], OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory))
            #     #     self.EVENT.delOneTerminateEnventinQueue(delevent)

            # elif event.EVENTTYPE==EVENTTYPE_DICT['TASK_COMPLETED']:
            #     self.MCSPSystem.systemTime = event.TRIGERTIME
            #     self.subTaskNumberinWorkflow(event.OBJECT.workflowID,event.OBJECT.taskID)
                
            #     # if (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category and
            #     #     event.TRIGERTIME>=self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].CompleteTime):
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Idle']
            #     #     self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_WhetherTerminate'], TRIGERTIME=event.TRIGERTIME,
            #     #                 OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory)))
            #     # elif (event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category and
            #     #       event.TRIGERTIME>=self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].CompleteTime):
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Idle']
            #     #     self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_WhetherTerminate'], TRIGERTIME=event.TRIGERTIME,
            #     #                 OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory)))
                
            # elif event.EVENTTYPE==EVENTTYPE_DICT['BOOTING_INSTANCE_STARTED']:
            #     # if event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category:
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Booting']
            #     # elif event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category:
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Booting']
            #     self.MCSPSystem.systemTime = event.TRIGERTIME
            #     self.EVENT.eventHistory.append(event)
            # elif event.EVENTTYPE==EVENTTYPE_DICT['BOOTING_INSTANCE_COMPLETED']:
            #     # if event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category:
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
            #     # elif event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category:
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Running']
                
            #     self.MCSPSystem.systemTime = event.TRIGERTIME
            # elif event.EVENTTYPE==EVENTTYPE_DICT['DATA_TRANSMISSION_STARTED']:
            #     self.MCSPSystem.systemTime = event.TRIGERTIME
            # elif event.EVENTTYPE==EVENTTYPE_DICT['DATA_TRANSMISSION_COMPLETED']:
            #     self.MCSPSystem.systemTime = event.TRIGERTIME   
            # elif event.EVENTTYPE==EVENTTYPE_DICT['WORKFLOW_COMPLETED']:   
            #     self.MCSPSystem.systemTime = event.TRIGERTIME 
            #     self.multiWorkflows[event.OBJECT.workflowID].objectives.Cmax = event.TRIGERTIME 
            #     self.multiWorkflows[event.OBJECT.workflowID].objectives.missDDL = max(0,self.multiWorkflows[event.OBJECT.workflowID].systemDeadline-event.TRIGERTIME)
            #     self.throughput += 1
            # elif event.EVENTTYPE==EVENTTYPE_DICT['INSTANCE_WhetherTerminate']:   
            #     self.MCSPSystem.systemTime = event.TRIGERTIME 
            #     # self.EVENT.addtoEventQueue(EventType(EVENTTYPE=EVENTTYPE_DICT['INSTANCE_Terminate'], TRIGERTIME=event.TRIGERTIME+self.MCSPSystem.IdleTimetoTerminate,
            #     #                 OBJECT=Object(cloudProvider=event.OBJECT.cloudProvider, instance=event.OBJECT.instance, InstanceCategory =event.OBJECT.InstanceCategory)))
            # elif event.EVENTTYPE==EVENTTYPE_DICT['INSTANCE_Terminate']:   
            #     self.MCSPSystem.systemTime = event.TRIGERTIME 
            #     # if event.OBJECT.InstanceCategory==self.MCSPSystem.Category[0].Category:
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].VMPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Terminated']
            #     # elif event.OBJECT.InstanceCategory==self.MCSPSystem.Category[1].Category:
            #     #     self.MCSPSystem.platform[self.MCSPSystem.getCloudProviderID(event.OBJECT.cloudProvider)].FaaSPlatform[event.OBJECT.instance].InstanceState = InstanceState_Dict['Terminated']



        
        self.fitness.Cmax = self.MCSPSystem.systemTime 
        
        k,d = 0,0
        for each in self.multiWorkflows:
            d -= (each.objectives.missDDL/each.deadline)
            if each.objectives.missDDL>0:
                k += 1
        self.fitness.successfulrate = k/len(self.multiWorkflows)
        self.fitness.deadlineDeviation = d/len(self.multiWorkflows)
        # k =1 
        # print([each for each in self.EVENT.eventHistory])
        
        return self.fitness # .Cost

