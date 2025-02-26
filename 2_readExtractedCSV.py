
import os
import numpy as np
import csv ,json
from GPClass.workflowClass import workflowClass
from Class.Task import Task
from Class.File import File
from Class.commonFunctionClass import Objectives # ,workflowClass,Task,File

def fromCSVtoWorkflow(one_batchTask): # task,
    # in batch_task
    task_name_Index = 0 
    instance_num_Index = 1 
    job_name_Index = 2 
    task_type_Index = 3 
    status_Index = 4 
    start_time_Index = 5
    end_time_Index = 6 
    plan_cpu_Index = 7 
    plan_mem_Index = 8  

    workflow = workflowClass()
    workflow.name = one_batchTask[0][job_name_Index]
    workflow.id = int(workflow.name[2:])
    workflow._givenMinStartTime = min([float(each[start_time_Index]) for each in one_batchTask ])
    workflow._givenMaxFinishTime= max([float(each[end_time_Index]) for each in one_batchTask ])
    workflow.objectives = Objectives()
    originalIndex= []
    
    for each in one_batchTask:
        task_name = each[task_name_Index]
        splits = task_name.split("_")
        task_ID = splits[0][1:]
        originalIndex.append(int(task_ID))
    originalIndex.sort()
    newIndex = [i for i in range(len(one_batchTask))]
    newName = []
    for each in one_batchTask:
        task_name = each[task_name_Index]
        splits = task_name.split("_")
        str1 = splits[0][0]
        str1 = str1+ str(newIndex[originalIndex.index(int(splits[0][1:]))])

        for i in range(1,len(splits)):
            try:
                str1 = str1 + '_' + str(newIndex[originalIndex.index(int(splits[i]))])
            except:
                pass
        newName.append(str1) 
    k = 0
    DAG = {}
    for each in one_batchTask:
        task_name = newName[k] # each[task_name_Index]
        k += 1
        splits = task_name.split("_")
        task_ID = splits[0][1:]
        task = Task(int(task_ID),name=task_name,namespace = each[task_name_Index] , jobsetname=workflow.name,)
        task._given_start_time = float(each[start_time_Index])
        task._given_end_time = float(each[end_time_Index]) 
        task._given_plan_cpu = float(each[plan_cpu_Index]) if  each[plan_cpu_Index]!='' else 0 
        task._given_plan_mem = float(each[plan_mem_Index]) if  each[plan_cpu_Index]!='' else 0 
        task._given_instance_num = int(each[instance_num_Index]) 
        inputs = [File(x,id=int(x)) for x in splits[1:] if x.isdigit()]      
        l1 = []
        for fa in inputs:
            if fa.id not in l1:
                l1.append(fa.id)
                task.addInput(fa)
            else:
                pass
        DAG.update({ task.id:task })
    DAG = dict(sorted(DAG.items()))
    for id,task in DAG.items():
        if task.inputs!=[]:
            for fa in task.inputs:
                fa.booleaninput, fa.booleanoutput= True, False
                file1 = File(str(id),id=id,size= fa.size,booleaninput= False, booleanoutput= True)
                DAG[fa.id].addOutput(file1)

                # pass
    workflow.DAG = DAG
    return workflow

def to_json(obj):
    return json.dumps(obj, default=lambda obj: obj.__dict__,indent=4,sort_keys=True,ensure_ascii=False)
# def to_json(obj,f):
#     return json.dumps(obj,f, default=lambda obj: obj.__dict__,indent=4,sort_keys=True,ensure_ascii=False)

def readDataFromExtracted_sorted_task_ToNPY():
    Address = 'task_csv_V1_UpdataSTFT'
    listfileName=os.listdir(Address) 
    multiWorkflow = []
    for each in listfileName:            
        with open(os.path.join(Address,each), 'r') as csvfile:
            task = list(csv.reader(csvfile)  )
        workflow = fromCSVtoWorkflow(task)
        multiWorkflow.append(workflow)
    np.save('multiWorkflow_OriginalData.npy', multiWorkflow) 

    # Address = 'WorkflowTrace/extracted_sorted_task'
    # # jsonFileAddress = 'WorkflowTrace/json'
    # listfileName=os.listdir(Address)
    # with open('WorkflowTrace/sorted_MinStartTime_Task_Instance.csv', 'r') as csvfile:
    #     sortedTaskList = list(csv.reader(csvfile))  # minST = 86954

    # multiWorkflow = []
    # for task in sortedTaskList:
    #     if task[0]+'.csv' in listfileName:            
    #         with open(os.path.join(Address,task[0]+'.csv'), 'r') as csvfile:
    #             job = list(csv.reader(csvfile)  )
    #         workflow = fromCSVtoWorkflow(task,job)
            
    #         # with open(os.path.join(jsonFileAddress,workflow.name+'.json'),'w',encoding='utf-8') as jsonFile:
    #         #     jsonFile.write(workflow.toJson())
    #         # np.save(os.path.join(jsonFileAddress,workflow.name+'.npy'), workflow)

    #         # with open(os.path.join(jsonFileAddress,workflow.name+'.json'), 'r') as f:
    #         #     json_string = f.read()

    #         # # Deserialize the JSON string back to a dictionary
    #         # json_dict = json.loads(json_string)
    #         # Workflow = np.load(os.path.join(jsonFileAddress,workflow.name+'.npy'),allow_pickle=True).item()

    #         multiWorkflow.append(workflow)

    # np.save('multiWorkflow_OriginalData.npy', multiWorkflow) 
   
readDataFromExtracted_sorted_task_ToNPY()
# readMultiWorkflow = np.load('multiWorkflow_OriginalData.npy',allow_pickle=True)
k =1 