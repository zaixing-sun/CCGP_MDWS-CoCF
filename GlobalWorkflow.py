from sys import maxsize
import matplotlib
import matplotlib.pyplot as plt
from math import trunc
import os

from matplotlib.pyplot import close  

from Class.SyntheticGenerator import SyntheticGenerator
import numpy as np
from Class.VMType import PrivateCloudVMType
# import GlobalResource
from Class.File import File
from Class.Task import Task
import math,random
import copy

import xlwings as xw

from multiprocessing import  Process
from GPClass.multiCloudSystem import MULTICLOUDsystem




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

    DAG = copy.deepcopy(workflow)
    DAG[len(DAG)] = Task(len(DAG),name = 'entry')
    list1 = [taskId for taskId,task in DAG.items()]
    for taskid in list1: #range(len(DAG)-1):
        if DAG[taskid].inputs == []:   #原源节点 size = 0  JITCAWorkflow[len(JITCAWorkflow)-1]
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

def getEST_SubDeadline(workflow,MET):
    scheduleOrder = breadth_first_search_SubDeadline(workflow)
    EST = [-1 for each in range(len(workflow))] # {} #
    EFT = [-1 for each in range(len(workflow))]  #{} #
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
                listPEST = [ EST[each.id] + MET[each.id] + each.size/MULTICLOUDsystem.bandwidth_in1Cloud for each in parents  ] #
                EST[taskid] = max(listPEST)
            else:
                EST[taskid] = 0
            EFT[taskid] = EST[taskid] + MET[taskid]
            scheduleOrder.remove(taskid)
            break
    return EST,EFT

def getLFT(workflow,MET,Deadline):
    scheduleOrder = breadth_first_search_SubDeadline(workflow)
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
                listCLFT = [ (LFT[each.id] - MET[each.id] - each.size/MULTICLOUDsystem.bandwidth_in1Cloud) for each in child_1  ]
                LFT[taskid] = min(listCLFT)
            else:
                LFT[taskid] = Deadline
            LST[taskid] = LFT[taskid] - MET[taskid]
            scheduleOrder.remove(taskid)
            break
    return LFT,LST

def ResetDeadline(workflow,DeadlineFactor):
    MET = getMET_SubDeadline(workflow)          #  /GlobalResource.maxECU
    EST,EFT = getEST_SubDeadline(workflow,MET)  #  /GlobalResource.maxB
    Deadline = max(EFT)*DeadlineFactor
    return Deadline


class SalpClass:   #  szx
    def __init__(self):
        self.ContiSalp=None
        self.DiscrSalp=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.LevelTask=None
class ChromClass:  #   IS
    def __init__(self):
        self.X=None
        self.Y=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.pm = None
        self.pc = None

class ChromClass:   #  ASC
    def __init__(self):
        """ .TasksOrder 任务序列"""
        self.VMOrder=None
        self.TasksOrder=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
        self.scheduleMatrix=None
        self.cloneVector=None
        self.PBVMIndexlist = None
        self.VMList = None

class ChromClass:  #  IJPR
    def __init__(self):
        """ .TasksOrder 任务序列"""
        self.VMOrder=None
        self.TasksOrder=None
        self.objectives=None
        self.multiworflow=None
        self.VMSchedule=None
# ####################  读取非劣解集 .npy文件    ####################################

# app = xw.App(visible=True, add_book=False)
# app.display_alerts = False    # 关闭一些提示信息，可以加快运行速度。 默认为 True。
# app.screen_updating = True    # 更新显示工作表的内容。默认为 True。关闭它也可以提升运行速度。
# book = app.books.add()
# sheet = book.sheets.active
# listfileName=os.listdir(os.getcwd()+'\\ParetoFront') 
# PF = []
# # for fileName in listfileName:
# for n1 in range(len(listfileName)):
#     fileName = listfileName[n1]
#     tempPF = np.load(os.getcwd()+'\\ParetoFront\\'+fileName,allow_pickle=True)
#     PF.append(np.load(os.getcwd()+'\\ParetoFront\\'+fileName,allow_pickle=True)) # ,allow_pickle=True).item()) # 

#     for i in range(len(tempPF)):
#         sheet[i,n1*3+1].value = str(tempPF[i].objectives.Cost)
#         sheet[i,n1*3+2].value = str(tempPF[i].objectives.Energy)
#         sheet[i,n1*3+3].value = str(tempPF[i].objectives.TotalTardiness)

# k = 1
# ###############################################################################################


# # ####################### 读取  GlobalResource.WorkFlowTestName  数据 存到 .npy文件 ############################################
# # syntheticGenerator = SyntheticGenerator('%s.xml'%GlobalResource.WorkFlowTestName) #     

# # workflow = syntheticGenerator.generateSyntheticWorkFlow()

# # MET = getMET(workflow)
# # EST,EFT = getEST(workflow,MET)
# # Deadline = max(EFT)

# # workflow['Deadline'] = trunc(Deadline*1.1)

# # currentpath = os.getcwd()

# # np.save(currentpath+'\\data_npy\\'+GlobalResource.WorkFlowTestName+'.npy', workflow)                  #保存字典 注意带上后缀名

# # # workflow2 =  np.load(WorkFlowTestName+'.npy',allow_pickle=True).item()   #读取字典

# # print('GlobalWorkflow')
# # ################################################################################################


####################  读取所有数据 并将字典格式的workflow存到 .npy文件    ####################################
# def readWorkflow(fileName,DeadlineFactor):
#     PrivateFactor = 4
#     listDeadlineFactor = [0.8,1.1,1.5,1.8] 
#     for DeadlineFactor in listDeadlineFactor:
#         for factor in range(PrivateFactor):
#             print('****************\t\t\t' + fileName + ' is running. \t\t\t****************')
#             syntheticGenerator = SyntheticGenerator(fileName) #'%s.xml'% 
#             workflow = syntheticGenerator.generateSyntheticWorkFlow()
#             for taskid,task in workflow.items():
#                 task.runtime = abs(task.runtime*GlobalResource.ReferenceProcessingCapacity)
#                 task.MI = 1 if random.random()<0.2 else 0  # random.randint(0,1)  
#             Deadline = ResetDeadline(workflow,DeadlineFactor) 
#             # DeadlineFactor = 1.1
#             workflow['Deadline'] = trunc(Deadline*DeadlineFactor)
#             workflow['DeadlineFactor'] = DeadlineFactor
#             currentpath = os.getcwd()
#             workflowName = fileName[0:5]+'_'+"".join(list(filter(str.isdigit, fileName))).rjust(4,'0')
#             np.save(currentpath+'\\data_npy\\'+workflowName+'_'+str(DeadlineFactor)+'_'+str(factor)+'.npy', workflow)     

if __name__ == '__main__':
    listfileName=os.listdir('data_SyntheticWorkflows') 
    listDeadlineFactor = [0.8,1.1,1.5,1.8] 
    PrivateFactor = 4
    # temp_MCSPSystem = MULTICLOUDsystem # multiCloudSystem()
    # k = temp_MCSPSystem.averageMIPS.vm
    # Pro = []
    # for each1,each in temp_MCSPSystem.Category.items():
    #     Pro.append(len(temp_MCSPSystem.Category[each1]))
    # Sum1 = sum(Pro)
    # Pro = [each/Sum1 for each in Pro]
    # # for each in Pro:
    categoryList = ['vm','FaaS','Office365']
    weight = [6,3.5,0.5]
    # for each1,each in temp_MCSPSystem.Category.items():
    #     categoryList.append(each1)  
    #     weight.append(len(temp_MCSPSystem.Category[each1]))


    for fileName in listfileName:    #os.getcwd() 
        if fileName.endswith('.xml') :
            # p = Process(target=readWorkflow,args=(fileName,))
            # p.start()
            for DeadlineFactor in listDeadlineFactor:
                for factor in range(PrivateFactor):
                    print('****************\t\t\t' + fileName + ' is running. \t\t\t****************')
                    syntheticGenerator = SyntheticGenerator(fileName) #'%s.xml'% 
                    workflow = syntheticGenerator.generateSyntheticWorkFlow()
                    for taskid,task in workflow.items():
                        # task.runtime = abs(task.runtime*GlobalResource.ReferenceProcessingCapacity)
                        # task.MI = 1 if random.random()<0.2 else 0  # random.randint(0,1)  
                        random.seed(task.runtime)
                        r1 = random.random()
                        task.Category = random.choices(categoryList,weights =tuple(weight),k=1)      
                        if task.Category[0] =='FaaS': 
                            task.Invocations = int(10**6*(0.0001+0.9999*r1))           # [100,10^6]                  
                            task.runtime = 900*(1-r1)/(1+r1)*MULTICLOUDsystem.averageMIPS.FaaS
                        elif task.Category[0] =='vm': 
                            task.runtime = abs(task.runtime*MULTICLOUDsystem.averageMIPS.vm) # GlobalResource.ReferenceProcessingCapacity

                    # if workflow[taskid].Category[0]== 'vm':
                    #     # MULTICLOUDsystem.bandwidth_in1Cloud
                    #     workflow[taskid].terminal_task.EXECUTETIME = workflow[taskid].runtime /MULTICLOUDsystem.averageMIPS.vm  #GlobalResource.maxECU MULTICLOUDsystem.bandwidth_in1Cloud
                    # elif workflow[taskid].Category[0]== 'FaaS':
                    #     workflow[taskid].terminal_task.EXECUTETIME = workflow[taskid].runtime /MULTICLOUDsystem.averageMIPS.FaaS  #GlobalResource.maxECU MULTICLOUDsystem.bandwidth_in1Cloud
                    # elif workflow[taskid].Category[0]== 'Office365':
                    #     workflow[taskid].terminal_task.EXECUTETIME = workflow[taskid].runtime /MULTICLOUDsystem.averageMIPS.Office365 

                    Deadline = ResetDeadline(workflow,DeadlineFactor) 
                    workflow['Deadline'] = trunc(Deadline*DeadlineFactor)
                    workflow['DeadlineFactor'] = DeadlineFactor
                    # currentpath = os.getcwd() # currentpath+
                    workflowName = fileName[0:5]+'_'+"".join(list(filter(str.isdigit, fileName))).rjust(4,'0')
                    np.save('data_npy/'+workflowName+'_'+str(DeadlineFactor)+'_'+str(factor)+'.npy', workflow)                  #保存字典 注意带上后缀名
    k = 1
###############################################################################################


# ##################  Excel 表归一化  #############################################################
# app = xw.App(visible=True,add_book=False)
# book = app.books.open('.\\ResultExcel\\test2_Normalized.xlsx')
# sheet = book.sheets[0]  #引用工作表
# sheet2 = book.sheets.add("Normalized")
# AlgNum = GlobalResource.AlgorithmNumbers #len(GlobalResource.ObjectiveNumbers)
# ObjNum = len(GlobalResource.ObjectiveNumbers)
# ObjNum2 = 3 # 要归一化的目标的个数
# start1= 2 # 开始的行
# end1 = 114 #162 # 82 结束的行
# maxid = None #  2 最大化的目标
# for i in range(start1,end1):
#     for y in range(3):  # 前三列
#         sheet2[i,y].value = sheet[i,y].value
#     for NumAlgorithm in range(AlgNum):
#         for NumObj in range(ObjNum2):
#             y = 3+NumObj+NumAlgorithm*ObjNum
#             sheet2[i,y].value = sheet[i,y].value  # len(GlobalResource.ObjectiveNumbers)*NumAlgorithm + 5

#     for NumObj in range(ObjNum2):
#         list1 = []
#         lable1 = []
#         for NumAlgorithm in range(AlgNum):
#             y = 3+NumObj+NumAlgorithm*ObjNum
#             if not(sheet2[i,y].value == '--'):
#                 list1.append(sheet2[i,y].value)
#                 lable1.append(y)

#         if len(list1)==0:
#             continue
#         elif len(list1)==1:
#             y = lable1[0]
#             if NumObj==maxid:
#                 sheet2[i,y].value = 1
#             else:
#                 sheet2[i,y].value = 0
#             sheet2[i,y].api.Font.Color = 0x0000ff #red
#         else:
#             if (max(list1)!= min(list1)):
#                 for y in lable1:
#                     if (sheet2[i,y].value == min(list1))and(NumObj!=maxid):
#                         sheet2[i,y].api.Font.Color = 0x0000ff #red
#                     elif (sheet2[i,y].value == max(list1))and(NumObj==maxid):
#                         sheet2[i,y].api.Font.Color = 0x0000ff #red

#                 for k in range(len(lable1)):
#                     y = lable1[k]
#                     sheet2[i,y].value = round((list1[k]-min(list1))/(max(list1)-min(list1)),2)                
#             else:
#                 for k in range(len(lable1)):
#                     y = lable1[k]
#                     sheet2[i,y].value = 0

# book.save()#('.\\ResultExcel\\test2.xlsx')
# book.close()
# app.quit()
# ##################  Excel 表归一化  #############################################################

# ##################  Excel 表归一化后调整  #############################################################
# app = xw.App(visible=True,add_book=False)
# book = app.books.open('.\\ResultExcel\\test2_Normalized.xlsx')
# sheet = book.sheets[0]  #引用工作表
# sheet2 = book.sheets.add("CostRU")
# AlgNum = GlobalResource.AlgorithmNumbers #len(GlobalResource.ObjectiveNumbers)
# ObjNum = len(GlobalResource.ObjectiveNumbers)
# ObjNum2 = 3 # 要处理的目标
# start1= 2 # 开始的行
# end1 = 114 #162 # 82 结束的行
# maxid = None #  2 最大化的目标
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


# for i in range(7): # 7种dag结构
#     List1 = None
#     Obj = Objectives()
#     List1 = [Objectives() for i in range(AlgNum*16)  ] 
#     k = 0
#     y1 = 3      
#     for j in range(AlgNum):#range(ObjNum2):
#         x = 2 + i*16
#         y = 3 + j * ObjNum
#         for j1 in range(16):
#             # x = x1 + j* ObjNum
#             List1[k].Cost = sheet[x,y].value
#             List1[k].ResourceUtilization = sheet[x,y+1].value
#             x += 1
#             k += 1    
#     for j in range(AlgNum*16):
#         sheet2[j+2,2+i*2].value = List1[j].Cost
#         sheet2[j+2,2+i*2+1].value = List1[j].ResourceUtilization

# book.save()#('.\\ResultExcel\\test2.xlsx')
# book.close()
# app.quit()
# ##################  Excel 表归一化调整  #############################################################


# ##################  Excel 运行时间处理  #############################################################
# app = xw.App(visible=True,add_book=False)
# book = app.books.open('.\\ResultExcel\\test2_Normalized.xlsx')
# sheet = book.sheets[0]  #引用工作表
# sheet6 = book.sheets.add("RunTime")
# # sheet2 = book.sheets[1]
# ObjNum = GlobalResource.ObjectiveNumbers
# ObjNum2 = 2 
# sheet6[1,1].value = 'IC_PCP'
# sheet6[1,2].value = 'PSO'
# sheet6[1,3].value = 'JIT-C'
# sheet6[1,4].value = 'QL-HEFT'
# sheet6[1,5].value = 'T2FA'
# for i in range(28):    
#     listy = [6,10,14,18,22]  #  没有PSO
#     sheet6[2+i,0].value = sheet[2+i*4,1].value
#     for y in listy:
#         list1 = []    
#         for x in range(2+i*4,6+i*4):
#             if not(sheet[x,y].value == '--' or sheet[x,y].value == None):        
#                 if sheet[x,y-3].value<=sheet[x,2].value:
#                     list1.append(sheet[x,y].value)
#         if list1 != []:
#             sheet6[i+2,listy.index(y)+1].value = sum(list1)/len(list1)         
# book.save()#('.\\ResultExcel\\test2.xlsx')
# book.close()
# app.quit()

# ##################  Excel 运行时间处理  #############################################################


# ##################  Excel 表最值标注  #############################################################
# app = xw.App(visible=True,add_book=False)
# book = app.books.open('.\\ResultExcel\\test2_10.xlsx')
# sheet = book.sheets[0]  #引用工作表
# ObjNum = GlobalResource.ObjectiveNumbers
# for i in range(2,82):
#     for j in range(ObjNum):
#         if j != 2:  # 取小
#             listObjective = 99999999999
#         else:       # 取大
#             listObjective = 0
#         x = None
#         for k in range(4):
#             y = 3+j+k*ObjNum
#             if not(sheet[i,y].value == '--' or sheet[i,y].value == None):
#                 if listObjective >sheet[i,y].value and j != 2:
#                     listObjective = sheet[i,y].value
#                     x = y
#                 elif listObjective < sheet[i,y].value and (j == 2):
#                     listObjective = sheet[i,y].value
#                     x = y

#                 if (sheet[i,2].value < sheet[i,y].value) and (j == 0):
#                     sheet[i,y].api.Font.Color = 0xff0000 #Italic = True
#                     sheet[i,y].api.Font.Bold = True
        
#         sheet[i,x].api.Font.Color = 0x0000ff #Italic = True
#         if sheet[i,2].value < sheet[i,x].value and (j == 0):
#             sheet[i,3+4*ObjNum].value = 'False'        
# book.save()#('.\\ResultExcel\\test2.xlsx')
# book.close()
# app.quit()

# ##################  Excel 表最值标注  #############################################################


# ##################  绘图 (按顺序排好，不满足deadline赋值为空)  #############################################################
# # text = matplotlib.get_backend()  #查看后端
# from matplotlib.font_manager import FontProperties
# app = xw.App(visible=False,add_book=False)
# app.display_alerts=False
# app.screen_updating=False
# book = app.books.open('.\\ResultExcel\\test2_Normalized0.xlsx')
# # book = xw.Book('.\\ResultExcel\\test2_Normalized0.xlsx')
# sheet = book.sheets[1]  #引用工作表

# AlgNum = GlobalResource.AlgorithmNumbers #len(GlobalResource.ObjectiveNumbers)
# ObjNum = len(GlobalResource.ObjectiveNumbers)
# start1= 2 # 开始的行
# end1 = 114 #162 # 82 结束的行
# maxid = None #  2 最大化的目标
# DAGNum = 7   # DAG类型的个数
# ProEveryDAGNum = 4 # 每种DAG问题的个数
# ListMarker = ['o','p','*','1','2','^']  # 
# colors = ['orange', 'gold', 'lawngreen', 'lightseagreen', 'red', 'royalblue','blueviolet'] # 
# linestyles = ['solid']
# listDeadlineFactor = ['0.8','1.1','1.5','1.8'] 
# listY0 = [0,0.25,0.5,0.75,1]
# ObjNum2 = 2 
# font_Times = FontProperties(fname=r"C:\Windows\Fonts\times.ttf")
# font_dict = {'family':'Times New Roman', 'size':9}
# # plt.figure(dpi=300)
# for j in range(ObjNum2): # 每个目标绘制一张图 1,
#     # ## 以下为 7*4
#     # fig,ax = plt.subplots(DAGNum,ProEveryDAGNum, sharex=True, sharey=True)  
#     # for h in range(DAGNum*ProEveryDAGNum): # 子图的个数
#     #     ax_x = math.trunc(h/ProEveryDAGNum)
#     #     ax_y = h%ProEveryDAGNum     
#     # ## 以下为 4*7
#     fig,ax = plt.subplots(ProEveryDAGNum, DAGNum,sharex=True, sharey=True)  
#     for h in range(DAGNum*ProEveryDAGNum): # 子图的个数
#         ax_x = h%ProEveryDAGNum
#         ax_y = math.trunc(h/ProEveryDAGNum)

#         for y1 in range(AlgNum): # 每个子图中的每个算法
#             y = 3 + j + y1*ObjNum
#             listy = []
#             for x1 in range(ProEveryDAGNum):
#                 x = 2 + h*ProEveryDAGNum + x1 
#                 listy.append(sheet[x,y].value)

#             ax[ax_x,ax_y].plot(listDeadlineFactor,listy,marker =ListMarker[y1%AlgNum],color =colors[y1%AlgNum],linewidth=1,linestyle=linestyles[0],fillstyle='none') #markersize=8,

#         ax[ax_x,ax_y].set_title(sheet[1+h*ProEveryDAGNum+1,1].value,FontProperties=font_Times,fontsize=10)
#         ax[ax_x,ax_y].set_xticks(range(len(listDeadlineFactor)))
#         ax[ax_x,ax_y].set_xticklabels(listDeadlineFactor,fontdict=font_dict)
#         ax[ax_x,ax_y].set_yticks(listY0)
#         ax[ax_x,ax_y].set_yticklabels(listY0,fontdict=font_dict)
#     fig.text(0.5, 0.06, 'Deadline factors', ha='center',FontProperties='Times New Roman', size=11)
#     if j == 0: #Makespan
#         fig.text(0.07, 0.45, 'Normalized Total Cost', ha='center', rotation='vertical',FontProperties='Times New Roman', size=11)
#     elif j == 1: #Cost
#         fig.text(0.06, 0.45, 'Normalized Total resource Idle Rate', va='center', rotation='vertical',FontProperties='Times New Roman', size=11)

#     # legend=fig.legend([sheet[1,3].value,sheet[1,4].value,sheet[1,5].value,sheet[1,6].value],
#     #           loc ='lower center',frameon=False,ncol=4,bbox_to_anchor=(0.5,0.9),fontsize=10,handlelength=2.5)  #, title_fontproperties='Times New Roman'
#     legend=fig.legend([sheet[0,3].value,sheet[0,3+4].value,sheet[0,3+8].value,sheet[0,3+12].value,sheet[0,3+16].value],
#             loc ='lower center',frameon=False,ncol=5,bbox_to_anchor=(0.5,0.9),prop='Times New Roman', fontsize=9,handlelength=2.5)

#     figure = plt.gcf() # get current figure   
#     # figure.set_size_inches(19,9.5)
#     if j == 0: #Makespan
#         plt.savefig('ResultExcel/TC.pdf',format="pdf",dpi=300) #bbox_inches='tight',
#     elif j == 1: #Cost    
#         plt.savefig('ResultExcel/TIR.pdf',format="pdf",dpi=300) #bbox_inches='tight',
#     plt.show()
# # book.save()
# book.close()
# app.quit()

# ##################  绘图  #############################################################