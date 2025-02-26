
EVENTTYPE_DICT = {'WORKFLOW_SUBMITTED':'WORKFLOW_SUBMITTED', 'WORKFLOW_COMPLETED':'WORKFLOW_COMPLETED',
            'TASK_READY':'TASK_READY','TASK_STARTED':'TASK_STARTED', 'TASK_COMPLETED':'TASK_COMPLETED', 
            'BOOTING_INSTANCE_STARTED':'BOOTING_INSTANCE_STARTED', 'BOOTING_INSTANCE_COMPLETED':'BOOTING_INSTANCE_COMPLETED',
            'DATA_TRANSMISSION_STARTED':'DATA_TRANSMISSION_STARTED', 'DATA_TRANSMISSION_COMPLETED':'DATA_TRANSMISSION_COMPLETED',
            'INSTANCE_WhetherTerminate':'INSTANCE_WhetherTerminate','INSTANCE_Terminate':'INSTANCE_Terminate',
            'UPDATE_CONFIG_CONTAINER':'UPDATE_CONFIG_CONTAINER',
             }
# EVENTTYPE_LIST = ['WORKFLOW_SUBMITTED', 'WORKFLOW_COMPLETED',
            
#             'TASK_STARTED', 'TASK_COMPLETED', 
#             'BOOTING_INSTANCE_STARTED', 'BOOTING_INSTANCE_COMPLETED',
#             'DATA_TRANSMISSION_STARTED', 'DATA_TRANSMISSION_COMPLETED']

class Object:
    def __init__(self,workflowID = None,taskID = None,cloudProvider = None,instance = None,InstanceCategory=None,):
        self.workflowID = workflowID
        self.taskID = taskID
        self.cloudProvider = cloudProvider
        self.instance = instance
        self.InstanceCategory = InstanceCategory

class EventType:
    def __init__(self,EVENTTYPE = None, TRIGERTIME = None, OBJECT = None  ):
        self.EVENTTYPE = EVENTTYPE
        self.TRIGERTIME = TRIGERTIME   
        self.OBJECT = OBJECT

    def getEventTrigerTime(self,):
        return self.TRIGERTIME





# class EventQueueClass:
#     def __init__(self,WORKFLOW_SUBMITTED=[], WORKFLOW_COMPLETED=[],
#                  TASK_STARTED=[], TASK_COMPLETED=[],  # TASK_SUBMITTED = None, 
#                  BOOTING_INSTANCE_STARTED=[], BOOTING_INSTANCE_COMPLETED=[],
#                  DATA_TRANSMISSION_STARTED=[], DATA_TRANSMISSION_COMPLETED=[],  ):
        
#         self.WORKFLOW_SUBMITTED = WORKFLOW_SUBMITTED
#         self.WORKFLOW_COMPLETED = WORKFLOW_COMPLETED  

#         # self.TASK_SUBMITTED = TASK_SUBMITTED
#         self.TASK_STARTED = TASK_STARTED
#         self.TASK_COMPLETED = TASK_COMPLETED  

#         self.BOOTING_INSTANCE_STARTED=BOOTING_INSTANCE_STARTED
#         self.BOOTING_INSTANCE_COMPLETED=BOOTING_INSTANCE_COMPLETED

#         self.DATA_TRANSMISSION_STARTED=DATA_TRANSMISSION_STARTED
#         self.DATA_TRANSMISSION_COMPLETED=DATA_TRANSMISSION_COMPLETED
    
class EventClass:
    def __init__(self,):  # ,EVENTLIST_TYPE=EventQueueClass()
        
        self.EVENTQUEUE = []
        self.eventHistory = None
        # self.EVENTLIST_TYPE = EVENTLIST_TYPE  

    def addtoEventQueue(self,newEvent):
        index = -1
        for i in range(len(self.EVENTQUEUE)):
            if newEvent.TRIGERTIME<self.EVENTQUEUE[i].TRIGERTIME:
                index = i
                break
        if index ==-1:  index = len(self.EVENTQUEUE)
        self.EVENTQUEUE.insert(index, newEvent)

    def delOneTerminateEnventinQueue(self,delEvent):
        # for event in self.EVENTQUEU:
        # bool = True
        for i in range(len(self.EVENTQUEUE)):
            event = self.EVENTQUEUE[i]
            if (event.EVENTTYPE==delEvent.EVENTTYPE and 
                event.OBJECT.workflowID==delEvent.OBJECT.workflowID and 
                event.OBJECT.taskID==delEvent.OBJECT.taskID and
                event.OBJECT.cloudProvider==delEvent.OBJECT.cloudProvider # and
                # event.OBJECT.instance==delEvent.OBJECT.instance # and
                # event.OBJECT.InstanceCategory==delEvent.OBJECT.InstanceCategory
                ):
                self.EVENTQUEUE.remove(event) # .pop(i) # event.TRIGERTIME==delEvent.TRIGERTIME and 
                # bool = False
                # print('del event successfully', delEvent.TRIGERTIME,delEvent.OBJECT.workflowID,delEvent.OBJECT.taskID,delEvent.OBJECT.cloudProvider,delEvent.OBJECT.instance)
                break
        # if bool:
        #     print('del event ERROR', delEvent.TRIGERTIME,delEvent.OBJECT.workflowID,delEvent.OBJECT.taskID,delEvent.OBJECT.cloudProvider,delEvent.OBJECT.instance)
        #     # print(self.EVENTQUEUE)
        #     # exit()

        # index = -1
        # for i in range(len(self.EVENTQUEUE)):
        #     if newEvent.TRIGERTIME<self.EVENTQUEUE[i].TRIGERTIME:
        #         index = i
        #         break
        # if index ==-1:  index = len(self.EVENTQUEUE)
        # self.EVENTQUEUE.insert(index, newEvent)

        # if newEvent.EVENTTYPE=='WORKFLOW_SUBMITTED':
        #     self.EVENTLIST_TYPE.WORKFLOW_SUBMITTED.append(newEvent)
        # elif newEvent.EVENTTYPE=='WORKFLOW_COMPLETED':
        #     self.EVENTLIST_TYPE.WORKFLOW_COMPLETED.append(newEvent)

        # elif newEvent.EVENTTYPE=='TASK_STARTED':
        #     self.EVENTLIST_TYPE.TASK_STARTED.append(newEvent)
        # elif newEvent.EVENTTYPE=='TASK_COMPLETED':
        #     self.EVENTLIST_TYPE.TASK_COMPLETED.append(newEvent)

        # elif newEvent.EVENTTYPE=='BOOTING_INSTANCE_STARTED':
        #     self.EVENTLIST_TYPE.BOOTING_INSTANCE_STARTED.append(newEvent)
        # elif newEvent.EVENTTYPE=='BOOTING_INSTANCE_COMPLETED':
        #     self.EVENTLIST_TYPE.BOOTING_INSTANCE_COMPLETED.append(newEvent)

        # elif newEvent.EVENTTYPE=='DATA_TRANSMISSION_STARTED':
        #     self.EVENTLIST_TYPE.DATA_TRANSMISSION_STARTED.append(newEvent) 
        # elif newEvent.EVENTTYPE=='DATA_TRANSMISSION_COMPLETED':
        #     self.EVENTLIST_TYPE.DATA_TRANSMISSION_COMPLETED.append(newEvent)   

    def subfromEventQueue(self,newEvent):
        self.EVENTQUEUE.remove(newEvent)

        # if newEvent.EVENTTYPE=='WORKFLOW_SUBMITTED':
        #     self.EVENTLIST_TYPE.WORKFLOW_SUBMITTED.remove(newEvent)
        # elif newEvent.EVENTTYPE=='WORKFLOW_COMPLETED':
        #     self.EVENTLIST_TYPE.WORKFLOW_COMPLETED.remove(newEvent)

        # elif newEvent.EVENTTYPE=='TASK_STARTED':
        #     self.EVENTLIST_TYPE.TASK_STARTED.remove(newEvent)
        # elif newEvent.EVENTTYPE=='TASK_COMPLETED':
        #     self.EVENTLIST_TYPE.TASK_COMPLETED.remove(newEvent)

        # elif newEvent.EVENTTYPE=='BOOTING_INSTANCE_STARTED':
        #     self.EVENTLIST_TYPE.BOOTING_INSTANCE_STARTED.remove(newEvent)
        # elif newEvent.EVENTTYPE=='BOOTING_INSTANCE_COMPLETED':
        #     self.EVENTLIST_TYPE.BOOTING_INSTANCE_COMPLETED.remove(newEvent)

        # elif newEvent.EVENTTYPE=='DATA_TRANSMISSION_STARTED':
        #     self.EVENTLIST_TYPE.DATA_TRANSMISSION_STARTED.remove(newEvent) 
        # elif newEvent.EVENTTYPE=='DATA_TRANSMISSION_COMPLETED':
        #     self.EVENTLIST_TYPE.DATA_TRANSMISSION_COMPLETED.remove(newEvent)           

    def empty(self):
        if len(self.EVENTQUEUE) == 0:
            return True
        else:
            return False




