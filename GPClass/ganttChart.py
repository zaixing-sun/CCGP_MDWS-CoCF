
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from GPClass.EventClass import *
import copy,random
import numpy as np
import matplotlib as mpl

categoryList = ['vm','FaaS','Office365']
providerList = ['AmazonWS','Azure','GoogleCloud']
WIDTH_SIZE,HEIGHT_SIZE = 20,15



def drawChart(individual):
    random.seed(10000)
    np.random.seed(10000)
    workflowColor = []
    for wfID in range(len(individual.multiWorkflows)):
        r = np.round(np.random.rand(),1)
        g = np.round(np.random.rand(),1)
        b = np.round(np.random.rand(),1)
        workflowColor.append([r,g,b])

        for level in range(len(individual.multiWorkflows[wfID]._DAGLevel)):
            for taskID in individual.multiWorkflows[wfID]._DAGLevel[level]: # range(len(individual.multiWorkflows[wfID].DAG)):
                task = individual.multiWorkflows[wfID].DAG[taskID]
                # print(wfID,taskID,task.StartTime,task.FinishTime)
    
    # individual.multiWorkflows[wfID].DAG[taskID]


    #figure 
    fig = plt.figure(figsize=(WIDTH_SIZE,HEIGHT_SIZE))

    plt.suptitle(x=0.5,y=0.925,t='Numbers of Workflow: %d'%(len(individual.multiWorkflows))+'; Total Cost: %f'%(individual.fitness.Cost)+'; Makespan: %f'%(individual.fitness.Cmax) )

    edgecolor = "w" # silver"
    edgelinewidth=0.15
    # plt.grid(ls='--')
    # Makespan = individual.fitness.Cmax
    
    AWS_VM = fig.add_subplot(331)
    AWS_VM.set_ylabel('AmazonWS')
    AWS_FaaS = fig.add_subplot(332)
    Azure_VM = fig.add_subplot(334)
    Azure_VM.set_ylabel('Azure')
    Azure_365 = fig.add_subplot(336)
    Azure_365.set_xlabel('Office365')
    Google_VM = fig.add_subplot(337)
    Google_VM.set_xlabel('vm')
    Google_VM.set_ylabel('GoogleCloud')
    Google_FaaS = fig.add_subplot(338)
    Google_FaaS.set_xlabel('FaaS')
    # fig.add_subplot(339).set_xlabel('Office365')
    AWS_VM_event = []
    AWS_FaaS_event = []
    Azure_VM_event = []
    Azure_365_event = []
    Google_VM_event = []
    Google_FaaS_event = []
    eventList = copy.deepcopy(individual.EVENT.eventHistory)
    while eventList!=[]:
        event = eventList.pop(0)
        starttime = event.TRIGERTIME
        wfID = event.OBJECT.workflowID
        taskID = event.OBJECT.taskID
        instanceID = event.OBJECT.instance   
        
        if event.EVENTTYPE==EVENTTYPE_DICT['TASK_STARTED']:
            # starttime = event.TRIGERTIME
            # wfID = event.OBJECT.workflowID
            # taskID = event.OBJECT.taskID
            # instanceID = event.OBJECT.instance
            str1 = '$' +str(taskID)+'^{'+str(wfID)+'}$'
            taskCategory = individual.multiWorkflows[wfID].DAG[taskID].Category[0]
            width = individual.multiWorkflows[wfID].DAG[taskID].AET
            if (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'AmazonWS'):
                ''' AWS_VM = fig.add_subplot(331) '''
                AWS_VM_event.append(event)
                instanceTypeID =  individual.MCSPSystem.platform[0].VMPlatform[instanceID].typeID
                str1 += '$^{,'+str(instanceTypeID)+'}$'
                AWS_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                AWS_VM.text(x=starttime+ width/3, y=instanceID+0.25,s=str1,size='small') # ,color="k",family='serif', style='italic' 

            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'AmazonWS'): 
                ''' AWS_FaaS = fig.add_subplot(332) '''            
                AWS_FaaS_event.append(event)
                instanceTypeID =  individual.MCSPSystem.platform[0].FaaSPlatform[instanceID].typeID
                str1 += '$^{,'+str(instanceTypeID)+'}$'
                AWS_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                AWS_FaaS.text(x=starttime+ width/3, y=instanceID+0.25,s=str1,size='small')  
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'Azure'): 
                ''' Azure_VM = fig.add_subplot(334) '''
                Azure_VM_event.append(event)
                instanceTypeID =  individual.MCSPSystem.platform[1].VMPlatform[instanceID].typeID
                str1 += '$^{,'+str(instanceTypeID)+'}$'  # '$^{,'+str(instanceTypeID)+'}$'
                Azure_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Azure_VM.text(x=starttime+ width/3, y=instanceID+0.25,s=str1,size='small') 

            elif (taskCategory == 'Office365') and (event.OBJECT.cloudProvider == 'Azure'):
                ''' Azure_365 = fig.add_subplot(336) '''                
                Azure_365_event.append(event)
                Azure_365.barh(y=len(Azure_365_event),left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Azure_365.text(x=starttime+ width/3, y=len(Azure_365_event)+0.25,s=str1,size='small') 
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                ''' Google_VM = fig.add_subplot(337) '''  
                Google_VM_event.append(event)
                instanceTypeID =  individual.MCSPSystem.platform[2].VMPlatform[instanceID].typeID
                str1 += '$^{,'+str(instanceTypeID)+'}$'
                Google_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Google_VM.text(x=starttime+ width/3, y=instanceID+0.25,s=str1,size='small') 
                
            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                '''  Google_FaaS = fig.add_subplot(338) '''                
                Google_FaaS_event.append(event)
                instanceTypeID =  individual.MCSPSystem.platform[2].VMPlatform[instanceID].typeID
                str1 += '$^{,'+str(instanceTypeID)+'}$'
                Google_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Google_FaaS.text(x=starttime+ width/3, y=instanceID+0.25,s=str1,size='small') 
                
            # print(event.OBJECT.cloudProvider,taskCategory, instanceID,starttime,event.EVENTTYPE)

        elif event.EVENTTYPE==EVENTTYPE_DICT['BOOTING_INSTANCE_STARTED']:
            # starttime = event.TRIGERTIME
            # wfID = event.OBJECT.workflowID
            # taskID = event.OBJECT.taskID
            # instanceID = event.OBJECT.instance
            
            taskCategory = individual.multiWorkflows[wfID].DAG[taskID].Category[0]
            widthVM = individual.MCSPSystem.vmColdStartup
            widthFaaS = individual.MCSPSystem.FaasColdStartup
            if (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'AmazonWS'):
                ''' AWS_VM = fig.add_subplot(331) '''
                AWS_VM_event.append(event)
                AWS_VM.barh(y=instanceID,left=starttime, width=widthVM,height=0.5,color= 'k')

            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'AmazonWS'): 
                ''' AWS_FaaS = fig.add_subplot(332) '''            
                AWS_FaaS_event.append(event)
                AWS_FaaS.barh(y=instanceID,left=starttime, width=widthFaaS,height=0.5,color= 'k')
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'Azure'): 
                ''' Azure_VM = fig.add_subplot(334) '''
                Azure_VM_event.append(event)
                Azure_VM.barh(y=instanceID,left=starttime, width=widthVM,height=0.5,color= 'k')

            # elif (taskCategory == 'Office365') and (event.OBJECT.cloudProvider == 'Azure'):
            #     ''' Azure_365 = fig.add_subplot(336) '''                
            #     Azure_365_event.append(event)
            #     Azure_365.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                ''' Google_VM = fig.add_subplot(337) '''  
                Google_VM_event.append(event)
                Google_VM.barh(y=instanceID,left=starttime, width=widthVM,height=0.5,color= 'k')
                
            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                '''  Google_FaaS = fig.add_subplot(338) '''                
                Google_FaaS_event.append(event)
                Google_FaaS.barh(y=instanceID,left=starttime, width=widthFaaS,height=0.5,color= 'k')   
            # print(event.OBJECT.cloudProvider,taskCategory, instanceID,starttime,event.EVENTTYPE)
        elif event.EVENTTYPE==EVENTTYPE_DICT['INSTANCE_Terminate']:  

            str1 = 'Terminate'
            taskCategory = event.OBJECT.InstanceCategory# individual.multiWorkflows[wfID].DAG[taskID].Category[0]
            width = individual.MCSPSystem.IdleTimetoTerminate   # individual.multiWorkflows[wfID].DAG[taskID].AET
            if (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'AmazonWS'):
                ''' AWS_VM = fig.add_subplot(331) '''
                AWS_VM_event.append(event)
                AWS_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                AWS_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small') #+ width/3 ,color="k",family='serif', style='italic' 

            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'AmazonWS'): 
                ''' AWS_FaaS = fig.add_subplot(332) '''            
                AWS_FaaS_event.append(event)
                AWS_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                AWS_FaaS.text(x=starttime, y=instanceID+0.25,s=str1,size='small')  
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'Azure'): 
                ''' Azure_VM = fig.add_subplot(334) '''
                Azure_VM_event.append(event)
                Azure_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                Azure_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small') 

            elif (taskCategory == 'Office365') and (event.OBJECT.cloudProvider == 'Azure'):
                ''' Azure_365 = fig.add_subplot(336) '''                
                Azure_365_event.append(event)
                Azure_365.barh(y=len(Azure_365_event),left=starttime, width=width,height=0.5,color= 'k')
                Azure_365.text(x=starttime, y=len(Azure_365_event)+0.25,s=str1,size='small') 
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                ''' Google_VM = fig.add_subplot(337) '''  
                Google_VM_event.append(event)
                Google_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                Google_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small') 
                
            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                '''  Google_FaaS = fig.add_subplot(338) '''                
                Google_FaaS_event.append(event)
                Google_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                Google_FaaS.text(x=starttime, y=instanceID+0.25,s=str1,size='small') 

    # plt.savefig('GPClass/GanttChart/Total Cost %f.pdf'%(individual.fitness.Cost), dpi=150)
    # # plt.savefig("test_rasterization.eps", dpi=150)
    fig.show()
    k =2




def drawDynamicChart(individual):
    def update(event_index):
        global AWS_VM,AWS_FaaS,Azure_VM,Azure_365,Google_VM,Google_FaaS
        global text,AWS_VM_event,AWS_FaaS_event, Azure_VM_event, Azure_365_event, Google_VM_event, Google_FaaS_event
        if event_index==0:
            fig.clear()
            plt.suptitle(x=0.5,y=0.925,t='Numbers of Workflow: %d'%(len(individual.multiWorkflows))+'; Total Cost: %f'%(individual.fitness.Cost)+'; Makespan: %f'%(individual.fitness.Cmax) )
            AWS_VM = fig.add_subplot(331)
            AWS_VM.set_ylabel('AmazonWS')
            AWS_FaaS = fig.add_subplot(332)
            Azure_VM = fig.add_subplot(334)
            Azure_VM.set_ylabel('Azure')
            Azure_365 = fig.add_subplot(336)
            Azure_365.set_xlabel('Office365')
            Google_VM = fig.add_subplot(337)
            Google_VM.set_xlabel('vm')
            Google_VM.set_ylabel('GoogleCloud')
            Google_FaaS = fig.add_subplot(338)
            Google_FaaS.set_xlabel('FaaS')
            # fig.add_subplot(339).set_xlabel('Office365')
            AWS_VM_event = []
            AWS_FaaS_event = []
            Azure_VM_event = []
            Azure_365_event = []
            Google_VM_event = []
            Google_FaaS_event = [] 
            text = fig.text(3, 0.9, '', transform=AWS_VM.transAxes, color='#777777', size=0, ha='right', weight=800)        
        # for event in eventList[:event_index+1]:
        event = eventList[event_index]

        starttime = event.TRIGERTIME
        wfID = event.OBJECT.workflowID
        taskID = event.OBJECT.taskID
        instanceID = event.OBJECT.instance        
        taskCategory = individual.multiWorkflows[wfID].DAG[taskID].Category[0] 
        AWS_VM.set_xlim(0,starttime)
        AWS_FaaS.set_xlim(0,starttime)
        Azure_VM.set_xlim(0,starttime)
        Azure_365.set_xlim(0,starttime)
        Google_VM.set_xlim(0,starttime)
        Google_FaaS.set_xlim(0,starttime)

        text.remove()
        text = fig.text(3, 0.9, 'Current Time: %f'%(starttime), transform=AWS_VM.transAxes, color='#777777', size=12, ha='right', weight=800)    

        if event.EVENTTYPE==EVENTTYPE_DICT['TASK_STARTED']:
            # starttime = event.TRIGERTIME
            # wfID = event.OBJECT.workflowID
            # taskID = event.OBJECT.taskID
            # instanceID = event.OBJECT.instance
            str1 = '$' +str(taskID)+'^'+str(wfID)+'$'
            # taskCategory = individual.multiWorkflows[wfID].DAG[taskID].Category[0]
            width = individual.multiWorkflows[wfID].DAG[taskID].AET
            if (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'AmazonWS'):
                ''' AWS_VM = fig.add_subplot(331) '''
                AWS_VM_event.append(event)
                AWS_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                AWS_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') # ,color="k",family='serif', style='italic' 

            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'AmazonWS'): 
                ''' AWS_FaaS = fig.add_subplot(332) '''            
                AWS_FaaS_event.append(event)
                AWS_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                AWS_FaaS.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic')  
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'Azure'): 
                ''' Azure_VM = fig.add_subplot(334) '''
                Azure_VM_event.append(event)
                Azure_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Azure_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') 

            elif (taskCategory == 'Office365') and (event.OBJECT.cloudProvider == 'Azure'):
                ''' Azure_365 = fig.add_subplot(336) '''                
                Azure_365_event.append(event)
                Azure_365.barh(y=len(Azure_365_event),left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Azure_365.text(x=starttime, y=len(Azure_365_event)+0.25,s=str1,size='small' ,family='serif', style='italic') 
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                ''' Google_VM = fig.add_subplot(337) '''  
                Google_VM_event.append(event)
                Google_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Google_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') 
                
            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                '''  Google_FaaS = fig.add_subplot(338) '''                
                Google_FaaS_event.append(event)
                Google_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= workflowColor[wfID],data= str(taskID),edgecolor=edgecolor,linewidth=edgelinewidth)
                Google_FaaS.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') 
                
            # print(event.OBJECT.cloudProvider,taskCategory, instanceID,starttime,event.EVENTTYPE)

        elif event.EVENTTYPE==EVENTTYPE_DICT['BOOTING_INSTANCE_STARTED']:
            # starttime = event.TRIGERTIME
            # wfID = event.OBJECT.workflowID
            # taskID = event.OBJECT.taskID
            # instanceID = event.OBJECT.instance
            
            # taskCategory = individual.multiWorkflows[wfID].DAG[taskID].Category[0]
            widthVM = individual.MCSPSystem.vmColdStartup
            widthFaaS = individual.MCSPSystem.FaasColdStartup
            if (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'AmazonWS'):
                ''' AWS_VM = fig.add_subplot(331) '''
                AWS_VM_event.append(event)
                AWS_VM.barh(y=instanceID,left=starttime, width=widthVM,height=0.5,color= 'k')

            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'AmazonWS'): 
                ''' AWS_FaaS = fig.add_subplot(332) '''            
                AWS_FaaS_event.append(event)
                AWS_FaaS.barh(y=instanceID,left=starttime, width=widthFaaS,height=0.5,color= 'k')
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'Azure'): 
                ''' Azure_VM = fig.add_subplot(334) '''
                Azure_VM_event.append(event)
                Azure_VM.barh(y=instanceID,left=starttime, width=widthVM,height=0.5,color= 'k')

            # elif (taskCategory == 'Office365') and (event.OBJECT.cloudProvider == 'Azure'):
            #     ''' Azure_365 = fig.add_subplot(336) '''                
            #     Azure_365_event.append(event)
            #     Azure_365.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                ''' Google_VM = fig.add_subplot(337) '''  
                Google_VM_event.append(event)
                Google_VM.barh(y=instanceID,left=starttime, width=widthVM,height=0.5,color= 'k')
                
            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                '''  Google_FaaS = fig.add_subplot(338) '''                
                Google_FaaS_event.append(event)
                Google_FaaS.barh(y=instanceID,left=starttime, width=widthFaaS,height=0.5,color= 'k')   
            # print(event.OBJECT.cloudProvider,taskCategory, instanceID,starttime,event.EVENTTYPE)
        elif event.EVENTTYPE==EVENTTYPE_DICT['INSTANCE_Terminate']:  
            # starttime = event.TRIGERTIME
            # wfID = event.OBJECT.workflowID
            # taskID = event.OBJECT.taskID
            # instanceID = event.OBJECT.instance
            str1 = 'Terminate'
            # taskCategory = event.OBJECT.InstanceCategory# individual.multiWorkflows[wfID].DAG[taskID].Category[0]
            width = individual.MCSPSystem.IdleTimetoTerminate   # individual.multiWorkflows[wfID].DAG[taskID].AET
            if (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'AmazonWS'):
                ''' AWS_VM = fig.add_subplot(331) '''
                AWS_VM_event.append(event)
                AWS_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                AWS_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') #+ width/3 ,color="k",family='serif', style='italic' 

            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'AmazonWS'): 
                ''' AWS_FaaS = fig.add_subplot(332) '''            
                AWS_FaaS_event.append(event)
                AWS_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                AWS_FaaS.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic')  
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'Azure'): 
                ''' Azure_VM = fig.add_subplot(334) '''
                Azure_VM_event.append(event)
                Azure_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                Azure_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') 

            elif (taskCategory == 'Office365') and (event.OBJECT.cloudProvider == 'Azure'):
                ''' Azure_365 = fig.add_subplot(336) '''                
                Azure_365_event.append(event)
                Azure_365.barh(y=len(Azure_365_event),left=starttime, width=width,height=0.5,color= 'k')
                Azure_365.text(x=starttime, y=len(Azure_365_event)+0.25,s=str1,size='small' ,family='serif', style='italic') 
                
            elif (taskCategory == 'vm') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                ''' Google_VM = fig.add_subplot(337) '''  
                Google_VM_event.append(event)
                Google_VM.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                Google_VM.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') 
                
            elif (taskCategory == 'FaaS') and (event.OBJECT.cloudProvider == 'GoogleCloud'):
                '''  Google_FaaS = fig.add_subplot(338) '''                
                Google_FaaS_event.append(event)
                Google_FaaS.barh(y=instanceID,left=starttime, width=width,height=0.5,color= 'k')
                Google_FaaS.text(x=starttime, y=instanceID+0.25,s=str1,size='small' ,family='serif', style='italic') 


    random.seed(10000)
    np.random.seed(10000)
    workflowColor = []
    for wfID in range(len(individual.multiWorkflows)):
        r = np.round(np.random.rand(),1)
        g = np.round(np.random.rand(),1)
        b = np.round(np.random.rand(),1)
        workflowColor.append([r,g,b])

        for level in range(len(individual.multiWorkflows[wfID]._DAGLevel)):
            for taskID in individual.multiWorkflows[wfID]._DAGLevel[level]: # range(len(individual.multiWorkflows[wfID].DAG)):
                task = individual.multiWorkflows[wfID].DAG[taskID]
                # print(wfID,taskID,task.StartTime,task.FinishTime)
    
    # individual.multiWorkflows[wfID].DAG[taskID]

    
    #figure 
    fig = plt.figure(figsize=(WIDTH_SIZE,HEIGHT_SIZE))
    plt.suptitle(x=0.5,y=0.925,t='Numbers of Workflow: %d'%(len(individual.multiWorkflows))+'; Total Cost: %f'%(individual.fitness.Cost)+'; Makespan: %f'%(individual.fitness.Cmax) )
    edgecolor = "w" # silver"
    edgelinewidth=0.15

    eventList = copy.deepcopy(individual.EVENT.eventHistory)

    ani = animation.FuncAnimation(fig, update, frames=len(eventList), interval=0.001) 
    fig.show() # init_func=init,, blit=False, repeat=False

    # To save the animation using Pillow as a gif
    writer = animation.PillowWriter() # fps=15,metadata=dict(artist='Me'),bitrate=1800
    ani.save('GPClass/GanttChart/Total Cost %f.gif'%(individual.fitness.Cost), writer=writer)
    # FFwriter = animation.FFMpegWriter()
    # ani.save('GPClass/GanttChart/animation.mp4')  # , writer = FFwriter, fps=10 

    # ani.save()
    k =2       


# if True:
#     drawChart(individual)