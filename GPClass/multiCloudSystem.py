
# # from GPClass.function_terminal_3D import INSTANCETERMINAL_dict
# from copy import deepcopy
# import math


# FaasColdStartup = 6.0 
# vmColdStartup = 55.9



# InstanceState_Dict = {'Booting':'Booting','Running':'Running','Idle':'Idle','Terminated':'Terminated'}

# # FaasColdStartup = 0 
# # vmColdStartup = 0


# class  CategoryProvider:
#     def __init__(self,Category = None,CloudProvider=None):  
#         self.Category = Category
#         self.CloudProvider=CloudProvider
    

# # class GoogleCloudPlatfom:
# #     def __init__(self,):    
# #         self.CloudProvider='GoogleCloud'
# #         self.VMPlatform = []
# #         self.FaaSPlatform=[]
# #         self.VMType=Google_VMType()
# #         self.FaaSType= Google_FaaS()
# #         self.Office365Type= None
# # class AmazonWSPlatfom:
# #     def __init__(self,):    
# #         self.CloudProvider='AmazonWS'
# #         self.VMPlatform = []
# #         self.FaaSPlatform=[]
# #         self.VMType=AWS_VMType()
# #         self.FaaSType= AWS_FaaS()
# #         self.Office365Type= None
# # class AzurePlatfom:
# #     def __init__(self,):    
# #         self.CloudProvider='Azure'
# #         self.VMPlatform = []
# #         self.VMType=Azure_VMType()
# #         self.FaaSType= None
# #         self.Office365Platform=deepcopy(InstanceList())
# #         self.Office365Type= Azure_Office365()

# #         # self.AmazonWS = {'CloudProvider':'AmazonWS', 'VMPlatform':[],'FaaSPlatform':[],'VMType':AWS_VMType(),'FaaSType':AWS_FaaS()}
# #         # self.Azure = {'CloudProvider':'Azure', 'VMPlatform':[],'Office365Platform':deepcopy(InstanceList(TerminalInstance = INSTANCETERMINAL_dict())),'VMType':Azure_VMType(),'Office365Type':Azure_Office365()}




# class InstanceList:
#     def __init__(self,CloudProvider= None,ID = None,typeID = None,taskSequence=[],timeTable=[],CompleteTime=0,
#                  NewlyCreated = False,TerminalInstance = None, TerminalCloud = None, Priority = None,InstanceState= None,InstanceCategory= None):
#         self.CloudProvider= CloudProvider 
#         self.ID = ID
#         self.typeID = typeID 
#         self.taskSequence = taskSequence
#         self.timeTable = timeTable
#         self.CompleteTime = CompleteTime

#         self.NewlyCreated = NewlyCreated     
#         self.TerminalInstance = TerminalInstance   
#         self.Priority = Priority 
#         self.TerminalCloud = TerminalCloud
#         self.InstanceState = InstanceState
#         self.InstanceCategory = InstanceCategory
#         # self.SLR = None
#         # self.Energy = None
#         # self.missDDL = None
#         # self.TotalTardiness = None 

# class Configurations():
#     def __init__(self, vCPU=None,Bandwith = None, ECU= None, unitPrice= None,
#                 unitTime = None, Memory =None, perOneMillionRequests = None,
#                 PkgWattIdle=None,PkgWattFull=None,RAMWattIdle=None,RAMWattFull=None,DeltaFullMachine=None): # BillingInterval = None  TotalMIPS = None,
#         self.vCPU = vCPU
#         self.Bandwith = Bandwith
#         self.ECU = ECU
#         self.unitPrice = unitPrice # 
#         self.unitTime = unitTime
#         self.Memory = Memory
#         # self.TotalMIPS = TotalMIPS
#         # self.BillingInterval = BillingInterval
#         self.perOneMillionRequests = perOneMillionRequests
#         self.GHz = None
#         # vCPU=1,Bandwith =1,ECU=1,Memory= 1.3,unitPrice=0.047/3600,unitTime=1,
#         self.PkgWattIdle=PkgWattIdle
#         self.PkgWattFull=PkgWattFull
#         self.RAMWattIdle=RAMWattIdle
#         self.RAMWattFull=RAMWattFull
#         self.DeltaFullMachine=DeltaFullMachine


#         # self.ProcessingCapacity = [4.4*i for i in self.ECU ]  #[3*4.4,  6.5*4.4,  114*4.4,  28*4.4,  55*4.4,  104*4.4]    #计算能力，用来计算实际的运行时间
#         # self.price_ProCap = [self.M[i]/self.ProcessingCapacity[i] for i in range(self.m)]
#         # self.price_trans_data = {'IN':0.09,'OUT':0.02}#[0.09, 0.02]  数据传输   定价基于“传入”和“传出”Amazon EC2 的数据计算。
#         # self.price_store_data = 0.1056  ##   通用型 SSD (gp3) – 存储   每月每 GB 的价格：0.1056 USD  
#     # @property
#     # def ProcessingCapacity(self):
#     #     return 4.4*self.ECU
#     @property
#     def TotalMIPS(self):
#         return 1000*self.ECU    
#     # @property
#     # def price_ProCap(self):
#     #     return self.unitPrice/self.ProcessingCapacity    


# class CloudSeverType(object):

#     """
#     @article{Barika2022,
#         abstract = {Big data processing applications are becoming more and more complex. They are no more monolithic in nature but instead they are composed of decoupled analytical processes in the form of a workflow. One type of such workflow applications is stream workflow application, which integrates multiple streaming big data applications to support decision making. Each analytical component of these applications runs continuously and processes data streams whose velocity will depend on several factors such as network bandwidth and processing rate of parent analytical component. As a consequence, the execution of these applications on cloud environments requires advanced scheduling techniques that adhere to end user's requirements in terms of data processing and deadline for decision making. In this article, we propose two multicloud scheduling and resource allocation techniques for efficient execution of stream workflow applications on multicloud environments while adhering to workflow application and user performance requirements and reducing execution cost. Results showed that the proposed genetic algorithm is an adequate and effective for all experiments.},
#         annote = {三种供应商 虚拟机 VM 的配置},
#         archivePrefix = {arXiv},
#         arxivId = {1912.08392},
#         author = {Barika, Mutaz and Garg, Saurabh and Chan, Andrew and Calheiros, Rodrigo N.},
#         doi = {10.1109/TSC.2019.2963382},
#         eprint = {1912.08392},
#         file = {:home/zaixing/.local/share/data/Mendeley Ltd./Mendeley Desktop/Downloaded/Barika et al. - 2022 - Scheduling Algorithms for Efficient Execution of Stream Workflow Applications in Multicloud Environments.pdf:pdf;:home/zaixing/Ph.D/Paper/Jordan pap396s3-file1-final.pdf:pdf;:home/zaixing/Ph.D/Paper/Scheduling{\_}Algorithms{\_}for{\_}Efficient{\_}Execution{\_}of{\_}Stream{\_}Workflow{\_}Applications{\_}in{\_}Multicloud{\_}Environments.pdf:pdf},
#         issn = {19391374},
#         journal = {IEEE Transactions on Services Computing},
#         keywords = {Big data,genetic algorithm,greedy algorithm,scheduling,stream workflow},
#         mendeley-groups = {multiple clouds},
#         number = {2},
#         pages = {860--875},
#         publisher = {IEEE},
#         title = {{Scheduling Algorithms for Efficient Execution of Stream Workflow Applications in Multicloud Environments}},
#         volume = {15},
#         year = {2022}
#         }
#     """

#     def __init__(self,numofType=[3,3,4,4,5], Bandwidth= 2): # BandwidthofWAN
#         self.Category = 'vm'  #  'FaaS'  'Office365'
#         self.ColdStartup = vmColdStartup          
#         self.Type = [Configurations(vCPU=2,Bandwith =1,ECU=7,Memory= 3.75,unitPrice=0.128/3600,unitTime=1,),
#                      Configurations(vCPU=4,Bandwith =1.5,ECU=14,Memory= 7.5,unitPrice=0.255/3600,unitTime=1,),
#                      Configurations(vCPU=8,Bandwith =2,ECU=28,Memory= 15,unitPrice=0.511/3600,unitTime=1,),
#                      Configurations(vCPU=16,Bandwith =3,ECU=55,Memory= 30,unitPrice=1.021/3600,unitTime=1,),
#                      Configurations(vCPU=32,Bandwith =3,ECU=108,Memory= 60,unitPrice=2.043/3600,unitTime=1,)]
#         self.delay = 0.03  # Delay of WAN is 30 ms
#         self.Bandwidth = Bandwidth
    
#         self.Provider='CloudSever'
#         self.VMPlatform = []
#         self.eachTypeNumbers = numofType
#         # self.VMType=Azure_VMType()
#         # self.FaaSType= None
#         # self.Office365Platform=deepcopy(InstanceList())
#         # self.Office365Type= Azure_Office365()

#     @property
#     def Numbers(self):
#         return len(self.Type)
#     def caculateCost(self,TypeID,task):
#         return math.trunc(task.runtime/self.Type[TypeID].TotalMIPS/self.Type[TypeID].unitTime) *self.Type[TypeID].unitTime *self.Type[TypeID].unitPrice
#     def bootingCost(self,TypeID):
#         return  self.ColdStartup * self.Type[TypeID].unitPrice
#     def caculateExecuteTime(self,TypeID,task):
#         return task.runtime/self.Type[TypeID].TotalMIPS

# class FogNodeType(object):
#     def __init__(self,numofType=[math.inf,math.inf,math.inf,math.inf,math.inf],Bandwidth= 0.5):  # BandwidthofLAN #, m,P, N, U,B,M

#         """
#                 On-Demand Plans for Amazon EC2 Previous Generation  
#                 Select a location type and region       Location Type: AWS Region           Region:  US West (N. California)
#                 Select an operating system              Operating system :  Linux
#                 Select an instance type to view rates   Instance type:  General Purpose        
#                     power: https://engineering.teads.com/sustainability/carbon-footprint-estimator-for-aws-instances/
#                         https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=504755275
#             Instance name    On-Demand hourly rate    vCPU    ECU    Memory    Storage  PkgWattIdle  PkgWattFull   RAMWattIdle  RAMWattFull    DeltaFullMachine
#             m1.small	$0.047	1	1	1.7 GiB	    1 x 160 SSD 0.72    5.76    0.34    1.02    1.2
#             m3.medium	$0.077	1	3	3.75 GiB	1 x 4 SSD   0.87    6.97    0.75    2.25    1.4
#             m3.large	$0.154	2	6.5	7.5 GiB	    1 x 32 SSD  1.73    13.94   1.5     4.5     2.9
#             m3.xlarge	$0.308	4	13	15 GiB	    2 x 40 SSD  3.47    27.87   3.00    9.00    5.8
#             m3.2xlarge	$0.616	8	26	30 GiB	    2 x 80 SSD  6.94    55.74   6.00    18.00   11.5
            
#             m1.medium	$0.095	1	2	3.75 GiB	1 x 410 SSD
#             m1.large	$0.19	2	4	7.5 GiB	2 x 420 SSD
#             m1.xlarge	$0.379	4	8	15 GiB	4 x 420 SSD
        
#         """

#         self.Category = 'vm'  #  'FaaS'  'Office365'
#         self.ColdStartup = vmColdStartup          
#         self.Type = [Configurations(vCPU=1,Bandwith =1,ECU=1,Memory= 1.3,unitPrice=0.047/3600,unitTime=1,PkgWattIdle=0.72,PkgWattFull=5.76,RAMWattIdle=0.34,RAMWattFull=1.02,DeltaFullMachine=1.2,),
#                      Configurations(vCPU=1,Bandwith =1.5,ECU=3,Memory= 3.75,unitPrice=0.077/3600,unitTime=1,PkgWattIdle=0.87,PkgWattFull=6.97,RAMWattIdle=0.75,RAMWattFull=2.25,DeltaFullMachine=1.4,),
#                      Configurations(vCPU=2,Bandwith =2,ECU=6.5,Memory= 7.5,unitPrice=0.154/3600,unitTime=1,PkgWattIdle=1.73,PkgWattFull=13.94,RAMWattIdle=1.5,RAMWattFull=4.5,DeltaFullMachine=2.9,),
#                      Configurations(vCPU=4,Bandwith =3,ECU=13,Memory= 15,unitPrice=0.308/3600,unitTime=1,PkgWattIdle=3.47,PkgWattFull=27.87,RAMWattIdle=3,RAMWattFull=9,DeltaFullMachine=5.8,),
#                      Configurations(vCPU=8,Bandwith =3,ECU=26,Memory= 30,unitPrice=0.616/3600,unitTime=1,PkgWattIdle=6.94,PkgWattFull=55.74,RAMWattIdle=6,RAMWattFull=18,DeltaFullMachine=11.5,)]
#         self.delay = 0.0005 # Delay of LAN is 0.5 ms
#         self.Bandwidth = Bandwidth

#         self.Provider='FogSever'
#         self.VMPlatform = []
#         self.eachTypeNumbers = numofType # [math.inf,math.inf,math.inf,math.inf,math.inf]

#     @property
#     def Numbers(self):
#         return len(self.Type)
#     def caculateCost(self,TypeID,task):
#         return math.trunc(task.runtime/self.Type[TypeID].TotalMIPS/self.Type[TypeID].unitTime) *self.Type[TypeID].unitTime *self.Type[TypeID].unitPrice
#     def bootingCost(self,TypeID):
#         return  self.ColdStartup * self.Type[TypeID].unitPrice
#     def caculateExecuteTime(self,TypeID,task):
#         return task.runtime/self.Type[TypeID].TotalMIPS



# class CloudFogSystem(object):
#     def __init__(self):
#         self.systemTime = 0

#         # self.AmazonWS = {'VMPlatform':[],'FaaSPlatform':[],'VMType':AWS_VMType(),'FaaSType':AWS_FaaS()}
#         # self.Azure = {'VMPlatform':[],'Office365Platform':deepcopy(InstanceList(TerminalInstance = INSTANCETERMINAL_dict())),'VMType':Azure_VMType(),'Office365Type':Azure_Office365()}
#         # self.GoogleCloud = {'VMPlatform':[],'FaaSPlatform':[],'VMType':Google_VMType(),'FaaSType':Google_FaaS()}
#         # self.Category = {'vm':'vm','FaaS':'FaaS','Office365':'Office365',} # {'vm':[AWS_VMType(),Azure_VMType(),Google_VMType()],'FaaS':[AWS_FaaS(),Google_FaaS()],'Office365':[Azure_Office365()],}
#         # self.cloudProvider= {'AmazonWS':'AmazonWS','Azure':'Azure','GoogleCloud':'GoogleCloud',}
#         ''' Must NOT CHANGE THE SORT'''
#         self.platform = [CloudSeverType(),FogNodeType(),]
#         self.vmColdStartup = vmColdStartup  # 
#         self.FaasColdStartup = FaasColdStartup  #  The cold start time of FaaS needs to be confirmed again
#         self.TransmissionUnitGBPrice = 0.2
#         self.bandwidth_in1Cloud = 0.1*1024       # The bandwidth in one cloud is 0.1 GB/s, and the bandwidth between clouds is 0.05 GB/s. Moreover,
#         self.bandwidth_Clouds = 0.05*1024
#         self.IdleTimetoTerminate=600










# # class multiCloudSystem(object):
# #     def __init__(self):
# #         self.systemTime = 0
# #         # self.AmazonWS = {'VMPlatform':[],'FaaSPlatform':[],'VMType':AWS_VMType(),'FaaSType':AWS_FaaS()}
# #         # self.Azure = {'VMPlatform':[],'Office365Platform':deepcopy(InstanceList(TerminalInstance = INSTANCETERMINAL_dict())),'VMType':Azure_VMType(),'Office365Type':Azure_Office365()}
# #         # self.GoogleCloud = {'VMPlatform':[],'FaaSPlatform':[],'VMType':Google_VMType(),'FaaSType':Google_FaaS()}
# #         # self.Category = {'vm':'vm','FaaS':'FaaS','Office365':'Office365',} # {'vm':[AWS_VMType(),Azure_VMType(),Google_VMType()],'FaaS':[AWS_FaaS(),Google_FaaS()],'Office365':[Azure_Office365()],}
# #         # self.cloudProvider= {'AmazonWS':'AmazonWS','Azure':'Azure','GoogleCloud':'GoogleCloud',}
# #         ''' Must NOT CHANGE THE SORT'''
# #         self.platform = [AmazonWSPlatfom(),AzurePlatfom(),GoogleCloudPlatfom(),]
# #         self.vmColdStartup = vmColdStartup  # 
# #         self.FaasColdStartup = FaasColdStartup  #  The cold start time of FaaS needs to be confirmed again
# #         self.TransmissionUnitGBPrice = 0.2
# #         self.bandwidth_in1Cloud = 0.1*1024       # The bandwidth in one cloud is 0.1 GB/s, and the bandwidth between clouds is 0.05 GB/s. Moreover,
# #         self.bandwidth_Clouds = 0.05*1024
# #         self.IdleTimetoTerminate=600




# #     def addPlatform(self,platform):
# #         return self.platform.append(platform)
# #     @property
# #     def CloudProvider(self,):
# #         return [each.CloudProvider for each in self.platform ]
    
# #     def getCloudProviderID(self,CloudProvider):
# #         for each in self.platform:
# #             if each.CloudProvider==CloudProvider:
# #                 break
# #         return self.platform.index(each)

# #     @property
# #     def averageMIPS(self,):
# #         class cc:
# #             def __init__(self,vm = None,FaaS=None,Office365 =1):   # 
# #                 self.vm = vm
# #                 self.FaaS=FaaS     
# #                 self.Office365 = Office365
# #         # list0 = cc(vm = 0,FaaS=0) # ,Office365 =0
# #         vmList = []
# #         FaaSList = []
# #         # Office365List = []
# #         for each in self.platform:
# #             if each.VMType!=None:
# #                 vmList.extend([eachMIPS.TotalMIPS for eachMIPS in each.VMType.Type])
# #             if each.FaaSType!=None:
# #                 FaaSList.extend([eachMIPS.TotalMIPS for eachMIPS in each.FaaSType.Type])
# #             # if each.Office365Type!=None:
# #             #     Office365List.extend([eachMIPS.TotalMIPS for eachMIPS in each.Office365Type.Type])
        

# #         return cc(vm = sum(vmList)/len(vmList),FaaS=sum(FaaSList)/len(FaaSList))
    
# #     @property
# #     def maxMIPS(self,):
# #         class cc:
# #             def __init__(self,vm = None,FaaS=None,Office365 =1):   # 
# #                 self.vm = vm
# #                 self.FaaS=FaaS     
# #                 self.Office365 = Office365
# #         # list0 = cc(vm = 0,FaaS=0) # ,Office365 =0
# #         vmList = []
# #         FaaSList = []
# #         # Office365List = []
# #         for each in self.platform:
# #             if each.VMType!=None:
# #                 vmList.extend([eachMIPS.TotalMIPS for eachMIPS in each.VMType.Type])
# #             if each.FaaSType!=None:
# #                 FaaSList.extend([eachMIPS.TotalMIPS for eachMIPS in each.FaaSType.Type])
# #             # if each.Office365Type!=None:
# #             #     Office365List.extend([eachMIPS.TotalMIPS for eachMIPS in each.Office365Type.Type])
        

# #         return cc(vm = max(vmList),FaaS=max(FaaSList))    

# #     @property
# #     def Category(self,):
# #         ''' Must NOT CHANGE THE SORT'''
# #         list1 = [CategoryProvider(Category='vm',CloudProvider=[]),
# #                  CategoryProvider(Category='FaaS',CloudProvider=[]),
# #                  CategoryProvider(Category='Office365',CloudProvider=[])]
        
# #         for each in self.platform:
# #             if each.VMType!=None:
# #                 list1[0].CloudProvider.append(each.CloudProvider)
# #             if each.FaaSType!=None:
# #                 list1[1].CloudProvider.append(each.CloudProvider)
# #             if each.Office365Type!=None:
# #                 list1[2].CloudProvider.append(each.CloudProvider)
        
# #         return list1


# # MULTICLOUDsystem = multiCloudSystem()
# CLOUDFOGsystem = CloudFogSystem()





# '''
# \begin{table*}[!htbp]
#     \centering
#     \setlength{\abovecaptionskip}{0cm} 
#     \setlength{\belowcaptionskip}{-0.2cm}    
#     \caption{Configurations and powers of Fog Nodes.}
#         \label{Table: Configurations and powers of Fog Nodes}
#         \setlength{\tabcolsep}{1mm}
#         \begin{tabular}{cccccccc}
#         \toprule       
    
#             Type       &  ECU   & Memory(GB)   &  CPU-based idle power &  CPU-based full power &  memory-based idle power &  memory-based full power &   base power \\
#             \midrule
#             m1.smal    & 	1	& 	1.7     & 	0.72    & 	5.76    & 	0.34    & 	1.02    & 	1.2     \\
#             m3.medium  & 	3	& 	3.75	 & 	0.87    & 	6.97    & 	0.75    & 	2.25    & 	1.4     \\
#             m3.large   & 	6.5	& 	7.5     & 	1.73    & 	13.94   & 	1.5     & 	4.5     & 	2.9     \\  
#             m3.xlarge  & 	13	& 	15 	     & 	3.47    & 	27.87   & 	3.00    & 	9.00    & 	5.8     \\
#             m3.2xlarge & 	26	& 	30	    & 	 6.94    & 	55.74   & 	6.00    & 	18.00   & 	11.5    \\

#     \bottomrule
#     \end{tabular}
# \end{table*}
# '''