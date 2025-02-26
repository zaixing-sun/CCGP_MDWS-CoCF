
class PrivateCloudVMType(object):
    def __init__(self):#, m,P, N, U,B,M
        """
        m:总的类型数；          P:类型编号
        N:vCPU个数；            B:带宽大小
        M:租赁价格；            ProcessingCapacity:执行能力=ECU*4.4，单位：GFLOPS；
        ECU:ECU
        """
        self.m      = 3  # int(m) # 
        self.P      = [i for i in range(self.m)]
        # self.N      = [1,       2,      4,      8,      16,     32]   #核数 阿里云
        self.N      = [1,       1,      1]
        self.B      = [1.25,    1.75,   2.5]          #内网带宽 阿里云  单位Gbps
        self.ECU    = [10,      15,     22] 
        self.M      = [0,       0,      0]      #单价 FGCS2019
        self.ProcessingCapacity = [4.4*i for i in self.ECU ]        #计算能力，用来计算实际的运行时间
        self.price_ProCap = [self.M[i]/self.ProcessingCapacity[i] for i in self.P]
        self.dynamic_power = [110,    190,  300] # 一下三种随机设置
        self.idle_power = [10,    20,   35]
        self.trans_power = 5

class VMType(object):

    """
    休眠先决条件 https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/Hibernate.html
        要使按需实例 或 Reserved Instance 休眠，必须满足以下先决条件：

        支持的实例系列   C3、C4、C5、、                   I3
                        M3、M4、M5、M5a、M5ad、、        R3、R4、R5、R5a、R5ad、、、、
                        T2、T3、T3a
        实例 RAM 大小 - 必须小于 150 GB。
        根卷类型 - 必须是 EBS 卷，而不能是实例存储卷。
        支持的 EBS 卷类型 – 通用型 SSD (gp2 和 gp3）或预置 IOPS SSD（io1 和 io2）

    弹性IP价格 0.005$/h
    考虑有足够大的存储空间.
    EC2 计算单位 (ECU) – 一个 EC2 计算单位 (ECU) 相当于一个 1.0-1.2 GHz 2007 Opteron 或 2007 Xeon CPU 的计算能力。

    	        vCPU	ECU	    内存 (GiB)	    实例存储 (GB)	Linux/UNIX 使用量
    m3.medium	1	    3	    3.75 GiB	    1 个 4 SSD	    每小时 0.096 USD
    m3.large	2	    6.5	    7.5 GiB	        1 个 32 SSD	    每小时 0.193 USD
    c3.xlarge	4	    14	    7.5 GiB	        2 个 40 SSD	    每小时 0.255 USD
    c3.2xlarge	8	    28	    15 GiB	        2 个 80 SSD	    每小时 0.511 USD
    c3.4xlarge	16	    55	    30 GiB	        2 个 160 SSD	每小时 1.021 USD
    r3.8xlarge	32	    104	    244 GiB	        2 个 320 SSD	每小时 3.192 USD

    考虑 每G的单价 修改为C3类型的实例
                vCPU	ECU	    内存 (GiB)	实例存储 (GB)	Linux/UNIX 使用量	M	     P    		 每G的价格
    c3.large	2	    7	    3.75 GiB	2 个 16 SSD	    每小时 0.128 USD	0.128	30.8		0.004155844
    c3.xlarge	4	    14	    7.5 GiB	    2 个 40 SSD	    每小时 0.255 USD	0.255	61.6		0.00413961
    c3.2xlarge	8	    28	    15 GiB	    2 个 80 SSD	    每小时 0.511 USD	0.511	123.2		0.004147727
    c3.4xlarge	16	    55	    30 GiB	    2 个 160 SSD	每小时 1.021 USD	1.021	242		    0.004219008
    c3.8xlarge	32	    108	    60 GiB	    2 个 320 SSD	每小时 2.043 USD	2.043	475.2		0.004299242


    """

    def __init__(self):#, m,P, N, U,B,M
        """
        m:总的类型数；          P:类型编号；
        N:vCPU个数；            B:带宽大小；
        M:租赁价格；            ProcessingCapacity:执行能力=ECU*4.4，单位：GFLOPS；
        ECU:ECU；
        """
        # C3类型
        self.m      = 5  # int(m) # 
        self.P      = [i for i in range(self.m)]
        # self.N      = [1,       2,      4,      8,      16,     32]  #  [1,2,4,8,16]              #核数 阿里云
        self.N      = [1,       1,      1,      1,      1]
        self.B      = [1,       1.5,    2,      3,      3]                  #内网带宽 阿里云  单位Gbps
        self.ECU    = [7,       14,     28,     55,     108] 
        self.M      = [0.128,   0.255,  0.511,  1.021,  2.043]  #单价 FGCS2019
        self.ProcessingCapacity = [4.4*i for i in self.ECU ]  #[3*4.4,  6.5*4.4,  114*4.4,  28*4.4,  55*4.4,  104*4.4]    #计算能力，用来计算实际的运行时间
        self.price_ProCap = [self.M[i]/self.ProcessingCapacity[i] for i in range(self.m)]
        self.price_trans_data = {'IN':0.09,'OUT':0.02}#[0.09, 0.02]  数据传输   定价基于“传入”和“传出”Amazon EC2 的数据计算。
        self.price_store_data = 0.1056  ##   通用型 SSD (gp3) – 存储   每月每 GB 的价格：0.1056 USD





        """ #   m3.medium	    m3.large 
                c3.xlarge       c3.2xlarge   
                c3.4xlarge      r3.8xlarge
        self.m      = 6  # int(m) # 
        self.P      = [i for i in range(self.m)]
        # self.N      = [1,       2,      4,      8,      16,     32]  #  [1,2,4,8,16]              #核数 阿里云
        self.N      = [1,       1,      1,      1,      1,      1]
        self.B      = [1,       1.5,    1.5,    2,      3,      3]                  #内网带宽 阿里云  单位Gbps
        self.ECU    = [3,       6.5,    14,    28,     55,     104] 
        self.M      = [0.096,   0.193,  0.255,  0.511,  1.021,  3.192]  #单价 FGCS2019
        self.ProcessingCapacity = [4.4*i for i in self.ECU ]  #[3*4.4,  6.5*4.4,  114*4.4,  28*4.4,  55*4.4,  104*4.4]    #计算能力，用来计算实际的运行时间
        self.price_ProCap = [self.M[i]/self.ProcessingCapacity[i] for i in range(self.m)]
        """
        # 只有一种类型
        # self.m      = 1  # int(m) # 
        # self.P      = [i for i in range(self.m)]
        # # self.N      = [1,       2,      4,      8,      16,     32]  #  [1,2,4,8,16]              #核数 阿里云
        # self.N      = [1]
        # self.B      = [1.5]                  #内网带宽 阿里云  单位Gbps
        # self.ECU    = [14] 
        # self.M      = [0.255]  #单价 FGCS2019
        # self.ProcessingCapacity = [4.4*i for i in self.ECU ]  #[3*4.4,  6.5*4.4,  114*4.4,  28*4.4,  55*4.4,  104*4.4]    #计算能力，用来计算实际的运行时间
        # self.price_ProCap = [self.M[i]/self.ProcessingCapacity[i] for i in range(self.m)]
        

    # def value(self):

    #     for i in self.P:
    #         self.ProcessingCapacity.append(self.ECU*4.4)    
    #         self.price_ProCap.append(self.M[i]/self.ProcessingCapacity[i])





################################
##  以下一起全注释
#     provider_name_list = ["amazon", "google", "microsoft"]
#     lambda_list_default = [0.001, 0.003, 0.002]
#     # N = [2,4,8,16,36]
#     # U = [3.75,7.5,15,30,60]
#     # M = [0.1,0.199,0.398,0.796,1.591]

#     def __init__(self):#, m,P, N, U,B,M
#         # self = [i for i in range(1,5+1)]
#         # for i in range(self.m):
#         #     self[i].N = N[i]

#         self.m = 5  # int(m) # 
#         self.P = [i for i in range(self.m)]
#         # self.N = [2,4,8,16,36]  #  [1,2,4,8,16]              #核数 阿里云
#         # self.Memory = [3.75,7.5,15,30,60]       # FGCS2019
#         # self.B = [1,1.5,2,3,3]                  #内网带宽 阿里云  单位Gbps
#         # self.M = [0.108,0.216,0.432,0.864,1.944]  #单价 FGCS2019
#         # self.ProcessingCapacity = [10,20,39,73,139]  #计算能力，用来计算实际的运行时间        
        
#         # self.Memory = [3.75,7.5,15,30,60]       # FGCS2019
#         self.N = [2,4,8,16,32]  #  [1,2,4,8,16]              #核数 阿里云
#         self.B = [1,1.5,2,3,3]                  #内网带宽 阿里云  单位Gbps
#         self.M = [0.1,0.199,0.398,0.796,1.591]  #单价 FGCS2019
#         self.ProcessingCapacity = [1.8,2.2,2.7,3.15,3.5]  #计算能力，用来计算实际的运行时间

#         # self.N = [2,4,8,16,32]  #  [1,2,4,8,16]   [1,1,1,1,1] #           #核数 AWS M5
#         # self.B = [1,1.5,2,3,3]                  #内网带宽 阿里云  单位Gbps
#         # self.M = [0.132,0.264,0.528,1.056,2.112]  #单价 FGCS2019
#         # self.ProcessingCapacity = [10,16,37,70,128]  #计算能力，用来计算实际的运行时间
   
#     # def __P__():
    
# # class VMTask(object):
# #     def __init__(self):
# #         """
# #         分层后，每层的TaskSchedule: case3，case2，RuleLNS,RuleLTTF, RuleLEF,RuleSET

# #         任务在VM的状态表，包含：
# #         任务分配的VM、所在VM的核、任务的开始处理时间、任务结束处理时间
# #         """
# #         pass  



