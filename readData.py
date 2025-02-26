import os
import numpy as np
import csv ,json
from GPClass.workflowClass import workflowClass
from Class.Task import Task
from Class.File import File
# from Class.commonFunctionClass import Objectives # ,workflowClass,Task,File


Address = 'Testdata/0.90'
listfileName=os.listdir(Address) 
listfileName.sort()

# multiWorkflow = []
for each in listfileName:            
    WFName = os.path.join(Address,each)

    workflow = np.load(WFName,allow_pickle=True).item()
    print(workflow)
    print(workflow.DAG)
# np.save('multiWorkflow_OriginalData.npy', multiWorkflow) 
