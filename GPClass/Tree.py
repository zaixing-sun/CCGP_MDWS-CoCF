from random import choice, randint, shuffle
from statistics import mean
from copy import deepcopy
from GPClass.function_terminal import * 
# from Class.Task import Task
# from Class.File import File
# from GPClass.workflowClass import workflowClass
import numpy as np

class Node:
    def __init__(self, left=None, right=None, val=0, op=None):
        self.left = left
        self.right = right
        self.val = val
        self.op = op

    def size(self):
        return (self.left.size() if self.left != None else 0) + 1 + (self.right.size() if self.right != None else 0)

    # def uses_nonstatic(self):
    #     if self.left == None and self.right == None:
    #         return self.op in NONSTATIC
    #     elif self.left == None and self.right != None or self.right == None and self.left != None:
    #         print('!!!!!!!malformed tree!!!!!!!!!')
    #     else:
    #         return True if self.op in NONSTATIC else self.left.uses_nonstatic() or self.right.uses_nonstatic()

    # def growWorkflow(self, depthLimit):
    #     '''
    #     generate tree with max depth depthLimit
    #     '''
    #     if depthLimit == 0:
    #         self.op = choice(WORKFLOWTERMINAL_SET)
    #     else:
    #         self.op = choice(FUNCTION_TERMINAL_WORKFLOW)
    #     if self.op in FUNCTION_SET:
    #         self.left = Node()
    #         self.left.growWorkflow(depthLimit - 1)
    #         self.right = Node()
    #         self.right.growWorkflow(depthLimit - 1)

    # def fullWorkflow(self, depthLimit):
    #     '''
    #     generate tree full to passed depth_limt
    #     '''
    #     if depthLimit == 0:
    #         self.op = choice(WORKFLOWTERMINAL_SET)
    #     else:
    #         self.op = choice(FUNCTION_TERMINAL_WORKFLOW)
    #         self.left = Node()
    #         self.left.fullWorkflow(depthLimit - 1)
    #         self.right = Node()
    #         self.right.fullWorkflow(depthLimit - 1)
    #     # if self.op == CONST:
    #     #     self.val = randint(0, 255)

    def growTask(self, depthLimit):
        '''
        generate tree with max depth depthLimit
        '''
        if depthLimit == 0:
            self.op = choice(TASKTERMINAL_SET)
        else:
            self.op = choice(FUNCTION_TERMINAL_TASK)
        if self.op in FUNCTION_SET:
            self.left = Node()
            self.left.growTask(depthLimit - 1)
            self.right = Node()
            self.right.growTask(depthLimit - 1)

    def fullTask(self, depthLimit):
        '''
        generate tree full to passed depth_limt
        '''
        if depthLimit == 0:
            self.op = choice(TASKTERMINAL_SET)
        else:
            self.op = choice(FUNCTION_TERMINAL_TASK)
            self.left = Node()
            self.left.fullTask(depthLimit - 1)
            self.right = Node()
            self.right.fullTask(depthLimit - 1)
        # if self.op == CONST:
        #     self.val = randint(0, 255)

    def growInatance(self, depthLimit):
        '''
        generate tree with max depth depthLimit
        '''
        if depthLimit == 0:
            self.op = choice(INSTANCETERMINAL_SET)
        else:
            self.op = choice(FUNCTION_TERMINAL_INSTANCE)
        if self.op in FUNCTION_SET:
            self.left = Node()
            self.left.growInatance(depthLimit - 1)
            self.right = Node()
            self.right.growInatance(depthLimit - 1)

    def fullInatance(self, depthLimit):
        '''
        generate tree full to passed depth_limt
        '''
        if depthLimit == 0:
            self.op = choice(INSTANCETERMINAL_SET)
        else:
            self.op = choice(FUNCTION_TERMINAL_INSTANCE)
            self.left = Node()
            self.left.fullInatance(depthLimit - 1)
            self.right = Node()
            self.right.fullInatance(depthLimit - 1)
        # if self.op == CONST:
        #     self.val = randint(0, 255)

    def choose_node(self, graft=False, node=None):
        '''
        Copyright Kool Kids Klub
        '''

        def choose_r(tree_array, node, i):
            if node.left != None and node.op not in ALLTERMINAL:
                next_idx = 2 * i
                tree_array.append(next_idx)
                tree_array = choose_r(tree_array, node.left, next_idx)
            if node.right != None and node.op not in ALLTERMINAL:
                next_idx = (2 * i) + 1
                tree_array.append(next_idx)
                tree_array = choose_r(tree_array, node.right, next_idx)
            return tree_array

        tree_array = [1]
        tree_array = choose_r(tree_array, self, 1)
        random_node = 1 if tree_array == [] else choice(tree_array)
        parent_list = []  # Was parent_list = [random_node], but I changed this so the selected node is never moved to
        while random_node != 1:  # generate lineage
            random_node = random_node // 2
            parent_list.append(random_node)  # += [random_node // 2]
        #print(parent_list)
        if parent_list != []: parent_list.pop()  # remove root, last element is parent
        #print(parent_list)
        parent_list.reverse()
        current_node = self
        for node_idx in parent_list:
            # follow tree back to chosen node
            current_node = current_node.left if node_idx % 2 == 0 else current_node.right
        if graft:
            #print('NODE:{}'.format(node))
            spam = False
            if random_node == 1:
                self = deepcopy(node)
            else:
                if current_node.op in ALLTERMINAL:
                    print('PANIC!!!!!')
                    print('OP:{}'.format(current_node.op))
                    spam = True
                if random_node % 2 == 0:  # graft on randomly selected node
                    if spam:
                        print('CURRENT:{}'.format(current_node))
                        print('LEFT:{}'.format(current_node.left))
                    current_node.left = deepcopy(node)  # changed to deepcopy
                else:
                    if spam:
                        print('CURRENT:{}'.format(current_node))
                        print('RIGHT:{}'.format(current_node.right))
                    current_node.right = deepcopy(node)  # changed to deepcopy
        return current_node

    def recombine(self, other):
        self.choose_node(True, other.choose_node)

    def evaluateTree(self,terminal): # ,instanceID=0
        '''
            WORKFLOWTERMINAL_SET = ['NUMBERTASKSQUEUE', 'TOTALEXECUTETIMEQUEUE','NUMBERREMAININGTASKS',
                                    'TOTALEXECUTETIMEREMAININGTASKS', 'SLACKTIME'] #, 'WAITINGTIME'
            TASKTERMINAL_SET = ['SUBDEADLINE', 'NUMBERSCHILDREN', 'UPWARDRANK',
                                'EXECUTETIME', 'AVERAGECOMMUNICATIONTIME'] 
            INSTANCETERMINAL_SET = ['ACTUALAVAILABLETIME', 'EXECUTECOST', 'COMMUNICATIONCOST',
                                    'ACTUALEXECUTETIME', 'INSTANCEAVAILABLETIME']
            FUNCTION_SET = ['ADD','SUB','MUL','PRODIV','MIN','MAX']        
        '''
        # # workflow
        if self.op == 'NUMBERTASKSQUEUE':
            return terminal.NUMBERTASKSQUEUE
        elif self.op == 'TOTALEXECUTETIMEQUEUE':
            return terminal.TOTALEXECUTETIMEQUEUE
        elif self.op == 'NUMBERREMAININGTASKS':
            return terminal.NUMBERREMAININGTASKS
        elif self.op == 'TOTALEXECUTETIMEREMAININGTASKS':
            return terminal.TOTALEXECUTETIMEREMAININGTASKS
        elif self.op == 'SLACKTIME':
            return terminal.SLACKTIME
        # elif self.op == 'WAITINGTIME':
        #     return terminal.WAITINGTIME
        # # task  
        elif self.op == 'SUBDEADLINE':
            return terminal.SUBDEADLINE
        elif self.op == 'NUMBERSCHILDREN':
            return terminal.NUMBERSCHILDREN
        elif self.op == 'UPWARDRANK':
            return terminal.UPWARDRANK    
        elif self.op == 'EXECUTETIME':
            return terminal.EXECUTETIME
        elif self.op == 'AVERAGECOMMUNICATIONTIME':
            return terminal.AVERAGECOMMUNICATIONTIME
        # # instance
        elif self.op == 'ACTUALAVAILABLETIME':
            return terminal.ACTUALAVAILABLETIME
        elif self.op == 'EXECUTECOST':
            return terminal.EXECUTECOST
        elif self.op == 'COMMUNICATIONCOST':
            return terminal.COMMUNICATIONCOST
        elif self.op == 'ACTUALEXECUTETIME':
            return terminal.ACTUALEXECUTETIME
        elif self.op == 'INSTANCEAVAILABLETIME':
            return terminal.INSTANCEAVAILABLETIME
        # # function
        elif self.op == 'ADD': # 'ADD','SUB','MUL','PRODIV','MIN','MAX'
            return self.left.evaluateTree(terminal) + self.right.evaluateTree(terminal) # ,instanceID,instanceID
        elif self.op == 'SUB':
            return self.left.evaluateTree(terminal) - self.right.evaluateTree(terminal) # ,instanceID,instanceID
        elif self.op == 'MUL':
            return self.left.evaluateTree(terminal) * self.right.evaluateTree(terminal) #  ,instanceID,instanceID
        elif self.op == 'PRODIV':
            right = self.right.evaluateTree(terminal)  # ,instanceID
            return 1 if right == 0 else self.left.evaluateTree(terminal)  / right # ,instanceID
        elif self.op == 'MIN':
            return min(self.left.evaluateTree(terminal), self.right.evaluateTree(terminal)) #  ,instanceID,instanceID
        elif self.op == 'MAX':
            return max(self.left.evaluateTree(terminal), self.right.evaluateTree(terminal)) #  ,instanceID,instanceID
        else:
            print('HELP in Tree evaluate')





