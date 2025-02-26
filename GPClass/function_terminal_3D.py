import ctypes
expression_evaluator  = ctypes.CDLL('./expression_evaluator.so')
# g++ -shared -o expression_evaluator.so -fPIC expression_evaluator.cpp

expression_evaluator.evaluate_expression_from_python.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int
]
expression_evaluator.evaluate_expression_from_python.restype = ctypes.c_double


'''工作流终止符'''
class WORKFLOWTERMINAL_dict:    
    def __init__(self, NUMBERTASKSQUEUE=0, TOTALEXECUTETIMEQUEUE=0,NUMBERREMAININGTASKS=0, 
                    TOTALEXECUTETIMEREMAININGTASKS=0, ):  # SLACKTIME=0,
        self.NUMBERTASKSQUEUE = NUMBERTASKSQUEUE
        self.TOTALEXECUTETIMEQUEUE = TOTALEXECUTETIMEQUEUE
        self.NUMBERREMAININGTASKS = NUMBERREMAININGTASKS
        self.TOTALEXECUTETIMEREMAININGTASKS = TOTALEXECUTETIMEREMAININGTASKS
        # self.SLACKTIME = SLACKTIME
        
    def __repr__(self):
        return 'terminal_workflow'

# WORKFLOWTERMINAL_dict = {'NUMBERTASKSQUEUE':0, 'TOTALEXECUTETIMEQUEUE':0,'NUMBERREMAININGTASKS':0, 
#                     'TOTALEXECUTETIMEREMAININGTASKS':0, 'SLACKTIME':0, }
#         # # self.numberTasksQueue = 0  # 在队列中的任务数 the number of tasks in the queue
#         # # self.TOTALEXECUTETIMEQUEUE = 0 # 在队列中任务的执行时间之和  total weight of the operations in the queue. 
#         # # self.numberRemainingTasks = 0  # 剩余任务的数量 the number of remaining tasks
#         # # self.TOTALEXECUTETIMEREMAININGTASKS = 0 #剩余任务的的执行时间之和  total 执行时间 of the remaining tasks. totalWeightRemainingTasks
#         # # self.slackTime = 0 # 松弛时间 deadline减去 当前伪关键路径（剩余任务执行时间之和）的大小
#         # # self.waitingTime = 0 # 等待时间 'WAITINGTIME':0,

'''任务终止符'''
class TASKTERMINAL_dict:    
    def __init__(self, SUBDEADLINE=0, NUMBERSCHILDREN=0,UPWARDRANK=0, 
                    EXECUTETIME=0, AVERAGECOMMUNICATIONTIME=0,
                    NUMBERTASKSQUEUE=0, TOTALEXECUTETIMEQUEUE=0,NUMBERREMAININGTASKS=0, 
                    TOTALEXECUTETIMEREMAININGTASKS=0, NUMBERSFATHER =0,
                    MINCPU=0,MINMEMORY=0,TASKCATEGORY=0,):
        self.SUBDEADLINE = SUBDEADLINE                      # @initialization    SLACKTIME=0,parents=[], storage=0 ,core=None,deepcopy(TASKTERMINAL_dict)
        self.NUMBERSCHILDREN = NUMBERSCHILDREN              # @initialization
        self.NUMBERSFATHER = NUMBERSFATHER                  # @initialization
        self.UPWARDRANK = UPWARDRANK                        # @initialization
        self.EXECUTETIME = EXECUTETIME                      # @initialization
        self.AVERAGECOMMUNICATIONTIME = AVERAGECOMMUNICATIONTIME    # @initialization
        self.NUMBERTASKSQUEUE = NUMBERTASKSQUEUE            #                   parents=[], storage=0 ,core=None,deepcopy(TASKTERMINAL_dict)
        self.TOTALEXECUTETIMEQUEUE = TOTALEXECUTETIMEQUEUE  # 
        self.NUMBERREMAININGTASKS = NUMBERREMAININGTASKS    #
        self.TOTALEXECUTETIMEREMAININGTASKS = TOTALEXECUTETIMEREMAININGTASKS # 
        self.MINCPU = MINCPU                                # @initialization
        self.MINMEMORY = MINMEMORY                          # @initialization
        self.TASKCATEGORY = TASKCATEGORY                    # @initialization
        # self.SLACKTIME = SLACKTIME
    def __repr__(self):
        return 'terminal_task'
    
    @property
    def names_values(self):
        names = [b"SUBDEADLINE",b"NUMBERSCHILDREN",b"UPWARDRANK",b"EXECUTETIME",b"AVERAGECOMMUNICATIONTIME",
                b"NUMBERTASKSQUEUE",b"TOTALEXECUTETIMEQUEUE",b"NUMBERREMAININGTASKS",b"TOTALEXECUTETIMEREMAININGTASKS",
                b"NUMBERSFATHER",b"MINCPU",b"MINMEMORY",b"TASKCATEGORY"]
        values = [self.SUBDEADLINE,self.NUMBERSCHILDREN,self.UPWARDRANK,self.EXECUTETIME,self.AVERAGECOMMUNICATIONTIME,
                self.NUMBERTASKSQUEUE,self.TOTALEXECUTETIMEQUEUE,self.NUMBERREMAININGTASKS,self.TOTALEXECUTETIMEREMAININGTASKS,
                self.NUMBERSFATHER,self.MINCPU,self.MINMEMORY,self.TASKCATEGORY]
        return names,values

# TASKTERMINAL_dict = {'SUBDEADLINE':0, 'NUMBERSCHILDREN':0, 'UPWARDRANK':0,
#                 'EXECUTETIME':0, 'AVERAGECOMMUNICATIONTIME':0,
#                 'NUMBERTASKSQUEUE':0, 'TOTALEXECUTETIMEQUEUE':0,'NUMBERREMAININGTASKS':0, 
#                     'TOTALEXECUTETIMEREMAININGTASKS':0, 'SLACKTIME':0,} #, 'WAITINGTIME':0
#         # # SUBDEADLINE                 #  子截止时间
#         # # NUMBERSCHILDREN             #  子任务的个数
#         # # UPWARDRANK                  #  HEFT rank值
#         # # EXECUTETIME                 #  执行时间
#         # # AVERAGECOMMUNICATIONTIME    #  平均通讯时间
#         # # # WAITINGTIME                 #  等待时间  # 任务的等待时间 暂时不加入，未找到可解释性
# # 对于任务，其执行时间正比于执行花费，故不在考虑其花费。考虑了与父任务的平均通信时间

'''实例终止符'''
class INSTANCETERMINAL_dict:    
    def __init__(self, ACTUALAVAILABLETIME=0,COMMUNICATIONCOST=0, SLACKTIME=0,
                    #  EXECUTECOST=0, ACTUALEXECUTETIME=0, INSTANCEAVAILABLETIME=0,
                    CURRENTLYCPU_INSTANCE=0,CURRENTLYMEMORY_INSTANCE=0,
                    # MINCPU_INSTANCE=0,MINMEMORY_INSTANCE=0,
                    # MAXCPU_INSTANCE=0,MAXMEMORY_INSTANCE=0,
                    # MINCOST_INSTANCE=0,MAXCOST_INSTANCE=0,
                    # MINENERGY_INSTANCE=0,MAXENERGY_INSTANCE=0,
                    # MINUTILISATION_INSTANCE=0,MAXUTILISATION_INSTANCE=0,
                    NUMBERTASKINCLOUD = 0, WEIGHT_TASK_CATEGORY = 0,
                    CPU_CONFIGURATION = 0, MEMORY_CONFIGURATION = 0,
                    PRICE_CONFIGURATION = 0, STATICPOWER_CONFIGURATION = 0,
                    MINEXECUTETIME = 0, COMMUNICATIONTIME = 0,
                    ):   # 
        self.ACTUALAVAILABLETIME = ACTUALAVAILABLETIME
        # self.EXECUTECOST = EXECUTECOST
        self.COMMUNICATIONCOST = COMMUNICATIONCOST
        # self.ACTUALEXECUTETIME = ACTUALEXECUTETIME
        # self.INSTANCEAVAILABLETIME = INSTANCEAVAILABLETIME
        self.NUMBERTASKINCLOUD = NUMBERTASKINCLOUD
        self.SLACKTIME = SLACKTIME
        self.CURRENTLYCPU_INSTANCE = CURRENTLYCPU_INSTANCE
        self.CURRENTLYMEMORY_INSTANCE = CURRENTLYMEMORY_INSTANCE
        self.CPU_CONFIGURATION = CPU_CONFIGURATION
        self.MEMORY_CONFIGURATION = MEMORY_CONFIGURATION
        self.PRICE_CONFIGURATION = PRICE_CONFIGURATION
        self.STATICPOWER_CONFIGURATION = STATICPOWER_CONFIGURATION
        # self.MINCPU_INSTANCE = MINCPU_INSTANCE
        # self.MINMEMORY_INSTANCE = MINMEMORY_INSTANCE
        # self.MAXCPU_INSTANCE = MAXCPU_INSTANCE
        # self.MAXMEMORY_INSTANCE = MAXMEMORY_INSTANCE
        # self.MINCOST_INSTANCE = MINCOST_INSTANCE
        # self.MAXCOST_INSTANCE = MAXCOST_INSTANCE
        # self.MINENERGY_INSTANCE = MINENERGY_INSTANCE
        # self.MAXENERGY_INSTANCE = MAXENERGY_INSTANCE
        # self.MINUTILISATION_INSTANCE = MINUTILISATION_INSTANCE
        # self.MAXUTILISATION_INSTANCE = MAXUTILISATION_INSTANCE
        self.WEIGHT_TASK_CATEGORY = WEIGHT_TASK_CATEGORY
        self.MINEXECUTETIME = MINEXECUTETIME
        self.COMMUNICATIONTIME = COMMUNICATIONTIME

        
    def __repr__(self):
        return 'terminal_instance'

    @property
    def names_values(self):
        names = [b"ACTUALAVAILABLETIME",b"COMMUNICATIONCOST",b"SLACKTIME",
                # b"EXECUTECOST",b"ACTUALEXECUTETIME",b"INSTANCEAVAILABLETIME",
                b"CURRENTLYCPU_INSTANCE",b"CURRENTLYMEMORY_INSTANCE",
                # b"MINCPU_INSTANCE",b"MINMEMORY_INSTANCE",
                # b"MAXCPU_INSTANCE",b"MAXMEMORY_INSTANCE",
                # b"MINCOST_INSTANCE",b"MAXCOST_INSTANCE",
                # b"MINENERGY_INSTANCE",b"MAXENERGY_INSTANCE",
                # b"MINUTILISATION_INSTANCE",b"MAXUTILISATION_INSTANCE",
                b"NUMBERTASKINCLOUD",b"WEIGHT_TASK_CATEGORY",
                b"CPU_CONFIGURATION",b"MEMORY_CONFIGURATION",
                b"PRICE_CONFIGURATION",b"STATICPOWER_CONFIGURATION",
                b"MINEXECUTETIME",b"COMMUNICATIONTIME",]
        values = [self.ACTUALAVAILABLETIME,self.COMMUNICATIONCOST,self.SLACKTIME,
                # self.EXECUTECOST,self.ACTUALEXECUTETIME,self.INSTANCEAVAILABLETIME,
                self.CURRENTLYCPU_INSTANCE,self.CURRENTLYMEMORY_INSTANCE,
                # self.MINCPU_INSTANCE,self.MINMEMORY_INSTANCE,
                # self.MAXCPU_INSTANCE,self.MAXMEMORY_INSTANCE,
                # self.MINCOST_INSTANCE,self.MAXCOST_INSTANCE,
                # self.MINENERGY_INSTANCE,self.MAXENERGY_INSTANCE,
                # self.MINUTILISATION_INSTANCE,self.MAXUTILISATION_INSTANCE,
                self.NUMBERTASKINCLOUD,self.WEIGHT_TASK_CATEGORY,
                self.CPU_CONFIGURATION,self.MEMORY_CONFIGURATION,
                self.PRICE_CONFIGURATION,self.STATICPOWER_CONFIGURATION,
                self.MINEXECUTETIME,self.COMMUNICATIONTIME,]
        return names,values

class CONTAINERTERMINAL_dict:
    def __init__(self,  MIN_CPU_MEMORY_TASK=0,
                    SLACKTIME=0,REMAININGWEIGHT=0,
                    NUMBERSCHILDREN=0,ASSIGNED_CPU_MEMORY=0,
                    ): # 
        self.ASSIGNED_CPU_MEMORY = ASSIGNED_CPU_MEMORY
        self.MIN_CPU_MEMORY_TASK = MIN_CPU_MEMORY_TASK
        self.SLACKTIME = SLACKTIME
        self.REMAININGWEIGHT = REMAININGWEIGHT
        self.NUMBERSCHILDREN = NUMBERSCHILDREN

    def __repr__(self):
        return 'terminal_container'

    @property
    def names_values(self):        
        names = [b"ASSIGNED_CPU_MEMORY",b"MIN_CPU_MEMORY_TASK",b"SLACKTIME",b"REMAININGWEIGHT",b"NUMBERSCHILDREN"]
        values = [self.ASSIGNED_CPU_MEMORY,self.MIN_CPU_MEMORY_TASK,self.SLACKTIME,self.REMAININGWEIGHT,self.NUMBERSCHILDREN]
        return names,values



# class CLOUDPLATFORMTERMINAL_dict:    
#     def __init__(self, COMMUNICATIONCOST=0, AVERAGEEXECUTECOST=0,AVERAGEEXECUTETIME=0, AVERAGEACTUALAVAILABLETIME = 0,
#                     AVERAGEINSTANCEAVAILABLETIME=0,NUMBERTASKINCLOUD = 0,AVERAGESLACKTIME=0):
#         self.COMMUNICATIONCOST = COMMUNICATIONCOST
#         self.AVERAGEEXECUTECOST = AVERAGEEXECUTECOST
#         self.AVERAGEEXECUTETIME = AVERAGEEXECUTETIME
#         self.AVERAGEACTUALAVAILABLETIME = AVERAGEACTUALAVAILABLETIME
#         self.AVERAGEINSTANCEAVAILABLETIME = AVERAGEINSTANCEAVAILABLETIME
#         self.NUMBERTASKINCLOUD = NUMBERTASKINCLOUD
#         self.AVERAGESLACKTIME = AVERAGESLACKTIME

# INSTANCETERMINAL_dict = {'ACTUALAVAILABLETIME':0, 'EXECUTECOST':0, 'COMMUNICATIONCOST':0, 
#                 'ACTUALEXECUTETIME':0, 'INSTANCEAVAILABLETIME':0,}
#         # # ActualAvailableTime     # 在实例上的实际可用时间        
#         # # EXECUTECost              # 执行花费
#         # # COMMUNICATIONcost       # 通信花费
#         # # ActualEXECUTETime        # 在实例上的执行时间
#         # # InstanceAvailableTime   # 实例的可用时间
#         # # NUMBERTASKINCLOUD       # The number of tasks belonging to the same workflow in a cloud

WORKFLOWTERMINAL_SET = ['NUMBERTASKSQUEUE', 'TOTALEXECUTETIMEQUEUE','NUMBERREMAININGTASKS',
                        'TOTALEXECUTETIMEREMAININGTASKS']  # , 'SLACKTIME', 'WAITINGTIME'
TASKTERMINAL_SET = WORKFLOWTERMINAL_SET + ['SUBDEADLINE', 'NUMBERSCHILDREN','NUMBERSFATHER', 'UPWARDRANK',
                    'EXECUTETIME', 'AVERAGECOMMUNICATIONTIME','MINCPU','MINMEMORY','TASKCATEGORY'  ]    #, 'WAITINGTIME'
INSTANCETERMINAL_SET = ['ACTUALAVAILABLETIME', 'COMMUNICATIONCOST','SLACKTIME',
                        # 'EXECUTECOST', 'ACTUALEXECUTETIME', 'INSTANCEAVAILABLETIME', 
                        'CURRENTLYCPU_INSTANCE','CURRENTLYMEMORY_INSTANCE',
                        # 'MINCPU_INSTANCE','MINMEMORY_INSTANCE',
                        # 'MAXCPU_INSTANCE','MAXMEMORY_INSTANCE',
                        # 'MINCOST_INSTANCE','MAXCOST_INSTANCE',
                        # 'MINENERGY_INSTANCE','MAXENERGY_INSTANCE',
                        # 'MINUTILISATION_INSTANCE','MAXUTILISATION_INSTANCE',
                        'NUMBERTASKINCLOUD','WEIGHT_TASK_CATEGORY',
                        'CPU_CONFIGURATION','MEMORY_CONFIGURATION',
                        'PRICE_CONFIGURATION','STATICPOWER_CONFIGURATION', 
                        'MINEXECUTETIME','COMMUNICATIONTIME',                   
                        ]  # ,

CONTAINERTERMINAL_SET = ['MIN_CPU_MEMORY_TASK','SLACKTIME','ASSIGNED_CPU_MEMORY',
                         'REMAININGWEIGHT','NUMBERSCHILDREN']  # 

# CLOUDPLATFORMTERMINAL_SET = ['COMMUNICATIONCOST', 'AVERAGEEXECUTECOST', 'AVERAGEACTUALAVAILABLETIME',
#                         'AVERAGEEXECUTETIME', 'AVERAGEINSTANCEAVAILABLETIME','NUMBERTASKINCLOUD','AVERAGESLACKTIME']


FUNCTION_SET = ['ADD','SUB','MUL','PRODIV','MIN','MAX']

# FUNCTION_TERMINAL_WORKFLOW = WORKFLOWTERMINAL_SET + FUNCTION_SET
# FUNCTION_TERMINAL_TASK = TASKTERMINAL_SET + FUNCTION_SET
# FUNCTION_TERMINAL_INSTANCE = INSTANCETERMINAL_SET + FUNCTION_SET
# ALLTERMINAL = TASKTERMINAL_SET + INSTANCETERMINAL_SET  # WORKFLOWTERMINAL_SET + 
# # ALLTERMINAL_DICT = dict(WORKFLOWTERMINAL.items() + TASKTERMINAL.items() + INSTANCETERMINAL.items()) 
# # ALLTERMINAL_dict = {'NUMBERTASKSQUEUE':0, 'TOTALEXECUTETIMEQUEUE':0,'NUMBERREMAININGTASKS':0, 
# #                     'TOTALEXECUTETIMEREMAININGTASKS':0, 'SLACKTIME':0, 
# #                     'SUBDEADLINE':0, 'NUMBERSCHILDREN':0, 'UPWARDRANK':0,
# #                     'EXECUTETIME':0, 'AVERAGECOMMUNICATIONTIME':0,
# #                     'ACTUALAVAILABLETIME':[], 'EXECUTECOST':[], 'COMMUNICATIONCOST':[], 
# #                     'ACTUALEXECUTETIME':[], 'INSTANCEAVAILABLETIME':[],}


# K =1 
# class OPERATE_ADD:
#     def __init__(self, name = None, numbers= 2,parameter1= None,parameter2= None,):
#         name = name
#         numbers = numbers
#         parameter1 = parameter1
#         parameter2 = parameter2
#     # @property
#     # def result(self):
#     #     return self.parameter1 + self.parameter2

# # FUNCTIONSET1 = {'ADD':OPERATE_ADD(name ='ADD',parameter1= 1,parameter2= 2), 'EXECUTECOST':0, 'COMMUNICATIONCOST':0, 
# #                 'ACTUALEXECUTETIME':0, 'INSTANCEAVAILABLETIME':0,}

# # FUNCTIONSET1['ADD']
# # K =1 

# class FUNCTIONSET:
#     def __init__(self,):
#         ADD = None
#         SUB = None
#         MUL = None
#         PRODIV = None
#         MIN = None
#         MAX = None





# 'CURRENTTIME':0CURRENTTIME # 为系统当前时间 或者 已调度任务的最大完成时间

# 'TASKQUEUE'
# 'NUMBERTASKSQUEUE'
# 'TOTALEXECUTETIMEQUEUE'
# 'NUMBERREMAININGTASKS'
# 'TOTALEXECUTETIMEREMAININGTASKS'
# 'SLACKTIME'
# 'WAITINGTIME'
    # taskQueue
    # numberTasksQueue
    # TOTALEXECUTETIMEQUEUE
    # numberRemainingTasks
    # TOTALEXECUTETIMEREMAININGTASKS
    # slackTime
    # waitingTime

# WORKFLOWTERMINAL = {'TASKQUEUE':[], 'NUMBERTASKSQUEUE':None, 'TOTALEXECUTETIMEQUEUE':None, 
#                     'NUMBERREMAININGTASKS':None, 'TOTALEXECUTETIMEREMAININGTASKS':None, 
#                     'SLACKTIME':None, 'WAITINGTIME':None,'CURRENTTIME':None}



# workflowTerminal = {'TASKQUEUE':[], 'NUMBERTASKSQUEUE':None, 'TOTALEXECUTETIMEQUEUE':None, 
#                     'NUMBERREMAININGTASKS':None, 'TOTALEXECUTETIMEREMAININGTASKS':None, 
#                     'SLACKTIME':None, 'WAITINGTIME':None,}
