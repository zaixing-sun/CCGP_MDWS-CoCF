import os,shutil
import numpy as np
import csv ,random
from GPClass.workflowClass import workflowClass
from Class.Task import Task
from Class.File import File
# from GPClass.multiCloudSystem import MULTICLOUDsystem
from GPClass.generalDef_3D import getDeadline
from Environments.CLOUDFOGsystem import CLOUDFOGsystem

from math import trunc,ceil
from Class.SyntheticGenerator import SyntheticGenerator
from Class.commonFunctionClass import Objectives # ,workflowClass,Task,File

# categoryList = ['vm','FaaS','Office365']
# weight = [6,3.5,0.5]

categoryList = ["00","01","10","11"]        # ['vm','FaaS','Office365']
weight = [1.0, 3.0, 3.0, 3.0]               # [6,3.5,0.5]
minTransData = 500
maxTransData = 5000
times_ET_ORIGINAL = 10          # from 100 to 10
listDeadlineFactor = [0.8,1.1,1.5,1.8]



given_ECU  = CLOUDFOGsystem.representativeType().ECU 
given_Mem  = CLOUDFOGsystem.representativeType().Memory
given_ECU_Mem = given_ECU * given_Mem

minCPU = 0.05       # actually 0.5
maxCPU = 4          # < given_ECU 
minMemory = 0.05    # actually 0.5
maxMemory = 4       # < given_Mem

# deadlineFactor = 1.2
def setupCategoryandExcuteTimeforTaskinWorkflow(dag):
    k = 1
    jobID=int(dag[1].jobsetname[2:])    
    for id,task in dag.items():
        givenRunTime = task._given_end_time - task._given_start_time
        task.MI = givenRunTime
        givenRunTime += 1 
        task.runtime = givenRunTime*times_ET_ORIGINAL
        # np.random.seed(task.runtime)
        np.random.seed(jobID+k)
        k+=1
        task.Category = random.choices(categoryList,weights =tuple(weight),k=1)  

        task.minCPU = random.uniform(minCPU,maxCPU)
        task.minMEM = random.uniform(minMemory,maxMemory)
        task.minCPU = ceil(task.minCPU*2)/2
        task.minMEM = ceil(task.minMEM*2)/2


        # ww = CLOUDFOGsystem.representativeType()
        task.runtimePerCPU_Memory = task.runtime * given_ECU_Mem
        task._given_runtime = task.runtime
        task.runtime = task.getRuntime(given_ECU,given_Mem)        

        # if task.Category[0] =='FaaS': 
        #     r1 = givenRunTime/(30+givenRunTime)   # np.random.random()
        #     task.Invocations = task._given_instance_num # int(10**3*(0.001+0.999*np.random.random()))   # 1   int(10**6*(1.001+0.999*r1))   #              
        #     task.runtime = 900*r1*MULTICLOUDsystem.averageMIPS.FaaS  #  (1-r1)/(1+r1)
        # elif task.Category[0] =='vm': 
        #     task.runtime = abs(task.runtime*MULTICLOUDsystem.averageMIPS.vm) 
        # # else:
        # #     task.runtime = task.runtime

def setupInputorOutputDataforTaskinWorkflow(dag):
    k = 1
    jobID=int(dag[1].jobsetname[2:])
    for id,task in dag.items():
        for each in task.inputs:
            np.random.seed(jobID+k)
            k+=1
            each.size = np.random.randint(minTransData,maxTransData)            
            for i in dag[each.id].outputs:
                if i.id ==id:
                    i.size = each.size
                    break

def checkCircle(workflow):
    find = False
    for taskid,each in workflow.DAG.items(): #  in workflow
        inputID = [ kk.id for kk in each.inputs]
        outputID = [ kk.id for kk in each.outputs]
        set2 = [item for item in inputID if  item  in outputID]
        if list(set2)!=[]:
            find = True
            break
    return find







if __name__ == '__main__':
    
    # data = 'SyntheticWorkflows'
    data = 'AliData' 

    if data == 'SyntheticWorkflows':
        random.seed(199999)
        np.random.seed(199999)
        listfileName=os.listdir('SyntheticWorkflows') 
        listfileName.sort()
        num_List = ['50','100','200','300']
        one_num = 20
        if not os.path.exists('Testdata/200.0/'):
            os.makedirs('Testdata/200.0/')
        if not os.path.exists('Testdata/200.1/'):
            os.makedirs('Testdata/200.1/')
        for eachSynthetic in listfileName:
            for num in num_List:
                for i in range(one_num):                
                    fileName = eachSynthetic+'/'+eachSynthetic+'.n.'+num+'.'+str(i)+'.dax'
                    syntheticGenerator = SyntheticGenerator(fileName) #'%s.xml'% 
                    workflow = workflowClass()
                    workflow.objectives = Objectives()
                    workflow.name = fileName.split('/')[1]
                    workflow.DAG = syntheticGenerator.generateSyntheticWorkFlow()
                    for id,task in workflow.DAG.items():
                        task.Category = random.choices(categoryList,weights =tuple(weight),k=1)
                        task.minCPU = random.uniform(minCPU,maxCPU)
                        task.minMEM = random.uniform(minMemory,maxMemory)
                        task.minCPU = ceil(task.minCPU*2)/2
                        task.minMEM = ceil(task.minMEM*2)/2


                        # ww = CLOUDFOGsystem.representativeType()
                        task.runtimePerCPU_Memory = task.runtime * given_ECU_Mem
                        task._given_runtime = task.runtime
                        task.runtime = task.getRuntime(given_ECU,given_Mem)                        


                    #     if task.Category[0] =='FaaS': 
                    #         r1 = task.runtime /(30+task.runtime)
                    #         task.Invocations = 1 # int(10**6*(0.001+0.999*np.random.random()))   # 1 task._given_instance_num #   int(10**6*(1.001+0.999*r1))   #              
                    #         task.runtime = 900*r1*MULTICLOUDsystem.averageMIPS.FaaS  #  (1-r1)/(1+r1)
                    #     elif task.Category[0] =='vm': 
                    #         task.runtime = abs(task.runtime*MULTICLOUDsystem.averageMIPS.vm) 
                    # # workflow.DAG = DAG

                    workflow.deadlineFactor = random.choice(listDeadlineFactor)
                    workflow.deadline = getDeadline(workflow.DAG,workflow.deadlineFactor) 
                    if i<10:
                        np.save('Testdata/200.0/'+workflow.name+'.npy', workflow)   
                    else:
                        np.save('Testdata/200.1/'+workflow.name+'.npy', workflow)   

        
        # PrivateFactor = 4


   

    # data = 'AliData' 
    if data == 'AliData':
        # listDeadlineFactor = [0.8,1.1,1.5,1.8]
        # # update parameters
        readMultiWorkflow = np.load('multiWorkflow_OriginalData.npy',allow_pickle=True)
        # k = 0
        for each in readMultiWorkflow:
            if checkCircle(each):
                continue
            setupInputorOutputDataforTaskinWorkflow(each.DAG)
            setupCategoryandExcuteTimeforTaskinWorkflow(each.DAG)
            random.seed(each.id)
            each.deadlineFactor = random.choice(listDeadlineFactor)
            each.deadline = getDeadline(each.DAG,each.deadlineFactor) # (each._givenMaxFinishTime-each._givenMinStartTime)*times_ET_ORIGINAL*deadlineFactor
            np.save('TrainingData/'+each.name+'.npy', each)
        # np.save('multiWorkflow_SetupData.npy', readMultiWorkflow) 
   
        numList = [[0,500],[1,300],[1,500],[1,1000]]
        Address = 'TrainingData'
        listfileName=os.listdir(Address)
        random.seed(len(listfileName))
        random.shuffle(listfileName)
        for i,num in numList:
            poplist = [listfileName.pop(0) for _ in range(num)]        
            dst_dir = 'Testdata/'+str(i)  + '.' + str(num)+ '/' 
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for each in poplist:
                shutil.copy(os.path.join('TrainingData',each), dst_dir) 



        # # # copy file
        # totalNum = 300
        # trainNum,testNum = 210,90
        # numList = [400,500,600,1000,2000,4500] # [300,500,800,1000]
        # k = 0 
        # Address = 'TrainingData'
        # listfileName=os.listdir(Address)
        # random.seed(len(listfileName))
        # random.shuffle(listfileName)
        # # k = 46
        # # numList = [4*k,5*k,6*k,10*k,20*k,50*k]
        # for i in range(1):
        #     for num in numList:
        #         poplist = [listfileName.pop(0) for _ in range(num)]        
        #         dst_dir = 'Testdata/'+str(num)  + '.' + str(i)+ '/' 
        #         if not os.path.exists(dst_dir):
        #             os.makedirs(dst_dir)
        #         for each in poplist:
        #             shutil.copy(os.path.join('TrainingData',each), dst_dir) 
                    
        # # for num in numList:
        # #     for i in range(2):
        # #         poplist = [listfileName.pop(0) for _ in range(num)]        
        # #         dst_dir = 'Testdata/'+str(num)  + '.' + str(i)+ '/' 
        # #         if not os.path.exists(dst_dir):
        # #             os.makedirs(dst_dir)
        # #         for each in poplist:
        # #             shutil.copy(os.path.join('TrainingData',each), dst_dir) 

        # # dst_dir = 'Testdata/Excess/' 
        # # poplist = [listfileName.pop(0) for _ in range(len(listfileName))]  
        # # if not os.path.exists(dst_dir):
        # #     os.makedirs(dst_dir)
        # # for each in poplist:
        # #     shutil.copy(os.path.join('TrainingData',each), dst_dir)             



        # # # # copy file
        # # totalNum = 300
        # # trainNum,testNum = 210,90
        # # numList = [90,210,300,500,800,1000]
        # # k = 0 
        # # Address = 'TrainingData'
        # # listfileName=os.listdir(Address)
        # # while len(listfileName)!=0 and len(listfileName)>=totalNum:
        # #     if k <3:
        # #         poplist = [listfileName.pop(0) for _ in range(trainNum)]        
        # #         dst_dir = 'dataset/'+str(k)  + '/train/' # + '.' + str(len(poplist))
        # #         if not os.path.exists(dst_dir):
        # #             os.makedirs(dst_dir)
        # #         for each in poplist:
        # #             shutil.copy(os.path.join('TrainingData',each), dst_dir) 

        # #         poplist = [listfileName.pop(0) for _ in range(testNum)]        
        # #         dst_dir = 'dataset/'+str(k)  + '/test/' # + '.' + str(len(poplist))
        # #         if not os.path.exists(dst_dir):
        # #             os.makedirs(dst_dir)

        # #         for each in poplist:
        # #             shutil.copy(os.path.join('TrainingData',each), dst_dir) 
        # #     else:
        # #         for num in numList:
        # #             for i in range(3):
        # #                 poplist = [listfileName.pop(0) for _ in range(num)]        
        # #                 dst_dir = 'dataset/'+str(num)  + '.' + str(i)+ '/' 
        # #                 if not os.path.exists(dst_dir):
        # #                     os.makedirs(dst_dir)
        # #                 for each in poplist:
        # #                     shutil.copy(os.path.join('TrainingData',each), dst_dir) 

        # #         dst_dir = 'dataset/Excess/' 
        # #         poplist = [listfileName.pop(0) for _ in range(len(listfileName))]  
        # #         if not os.path.exists(dst_dir):
        # #             os.makedirs(dst_dir)
        # #         for each in poplist:
        # #             shutil.copy(os.path.join('TrainingData',each), dst_dir)             







        #     k += 1       
            

    k = 1
