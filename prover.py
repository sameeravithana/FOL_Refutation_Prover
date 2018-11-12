import random
import re

OPS = ["IF", "AND", "OR", "NOT", "IMPLIES"]
QUANTS = ["FORALL", "EXISTS"]


def getElement(xtype, xvalue):
    return (xtype, xvalue)


def remove_conditionals(FOL_Tree):
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()

    _child_nodes = FOL_Tree.get_child_nodes()

    if _symbol_type == "op" and _symbol_value == "IMPLIES":
        _symbol_value = "OR"
        FOL_Tree.set_node(_symbol_type, _symbol_value)

        _child_node = _child_nodes[-1]

        # _child_symbol_type=child_node.get_element_type()
        # _child_symbol_value=child_node.get_element_value()

        new_symbol_type = "op"
        new_symbol_value = "NOT"
        _new_node = Node(new_symbol_type, new_symbol_value)

        _new_node.add_child(_child_node)

        _child_nodes[-1] = _new_node

        FOL_Tree.set_child_nodes(_child_nodes)

    _child_nodes = FOL_Tree.get_child_nodes()
    for i in range(len(_child_nodes)):
        remove_conditionals(_child_nodes[i])

    return FOL_Tree


def deMorgan(FOL_Tree):
    _current_node = FOL_Tree
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()

    _child_nodes = FOL_Tree.get_child_nodes()

    if _symbol_type == "op" and _symbol_value == "NOT":

        _child_node = _child_nodes[0]

        _child_symbol_type = _child_node.get_element_type()
        _child_symbol_value = _child_node.get_element_value()

        # _symbol_value="OR"
        # FOL_Tree.set_node(_symbol_type,_symbol_value)

        new_symbol_type = new_symbol_value = ""
        if _child_symbol_type == "op":
            new_symbol_type = "op"
            if _child_symbol_value == "AND":
                new_symbol_value = "OR"
            elif _child_symbol_value == "OR":
                new_symbol_value = "AND"
        elif _child_symbol_type == "quant":
            new_symbol_type = "quant"
            if _child_symbol_value == "FORALL":
                new_symbol_value = "EXISTS"
            elif _child_symbol_value == "EXISTS":
                new_symbol_value = "FORALL"

        if new_symbol_type != "" and new_symbol_value != "":
            FOL_Tree.set_node(new_symbol_type, new_symbol_value)

            _child_child_nodes = _child_node.get_child_nodes()

            _new_children = []
            for _child_child_node in _child_child_nodes:

                _child_child_symbol_type = _child_child_node.get_element_type()
                _child_child_symbol_value = _child_child_node.get_element_value()

                if _child_child_symbol_type == "variable":

                    _new_children.append(_child_child_node)

                else:

                    _new_node = Node(_symbol_type, _symbol_value)
                    _new_node.add_child(_child_child_node)

                    _new_children.append(_new_node)

            FOL_Tree.set_child_nodes(_new_children)

    _child_nodes = FOL_Tree.get_child_nodes()
    for i in range(len(_child_nodes)):
        deMorgan(_child_nodes[i])

    return FOL_Tree


def standardize(FOL_Tree, variable_names={}):
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()

    _child_nodes = FOL_Tree.get_child_nodes()

    if _symbol_type == "quant":
        _child_node = _child_nodes[-1]

        _child_symbol_type = _child_node.get_element_type()
        _child_symbol_value = _child_node.get_element_value()

        ##print(_child_node.get_text())
        variable_names[_child_symbol_value] = _child_symbol_value + "_" + str(random.randint(0, 10000))

        _child_node.set_node(_child_symbol_type, variable_names[_child_symbol_value])

        _child_nodes[-1] = _child_node

    elif _symbol_type == "function" or _symbol_type == "predicate":
        ##print(variable_names)
        ##_child_node=_child_nodes[-1]

        for i in range(len(_child_nodes)):

            _child_node = _child_nodes[i]
            _child_symbol_type = _child_node.get_element_type()
            _child_symbol_value = _child_node.get_element_value()

            if _child_symbol_value in variable_names:
                _child_node.set_node(_child_symbol_type, variable_names[_child_symbol_value])

            _child_nodes[i] = _child_node

    ##print(variable_names)
    FOL_Tree.set_child_nodes(_child_nodes)

    ##_child_nodes=FOL_Tree.get_child_nodes()
    for i in range(len(_child_nodes)):
        standardize(_child_nodes[i], variable_names)

    return FOL_Tree

def recorrect(FOL_Tree):
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()

    _child_nodes = FOL_Tree.get_child_nodes()

    for i in range(len(_child_nodes)):
        _child_node=_child_nodes[i]

        _child_node_symbol_type = _child_node.get_element_type()
        _child_node_symbol_value = _child_node.get_element_value()

        if (_symbol_type == "function"):
            if (_child_node_symbol_type == "function"):
                _symbol_type = "predicate"
                FOL_Tree.set_node(_symbol_type, _symbol_value)

        if (_symbol_type == "op" or _symbol_type == "quant"):
            if (_child_node_symbol_type == "function"):
                _child_node_symbol_type = "predicate"
                _child_node.set_node(_child_node_symbol_type,_child_node_symbol_value)

                _child_nodes[i]=_child_node

        if (_symbol_type == "predicate"):
            if (_child_node_symbol_type == "symbol"):
                _child_node_symbol_type = "variable"
                _child_node.set_node(_child_node_symbol_type, _child_node_symbol_value)

                _child_nodes[i] = _child_node

        recorrect(_child_node)

    FOL_Tree.set_child_nodes(_child_nodes)

    return FOL_Tree


class Node:
    def __init__(self, element_type, element_value):
        self.set_node(element_type, element_value)

        self.children = []

    def add_child(self, x_node):
        self.children.append(x_node)

    def set_child_nodes(self, children):
        self.children = children

    def get_child_nodes(self):
        return self.children

    def set_node(self, element_type, element_value):
        self.element_type = element_type
        self.element_value = element_value

    def get_element_type(self):
        return self.element_type

    def get_element_value(self):
        return self.element_value

    def get_text(self):
        return "[" + self.get_element_type() + "] " + self.get_element_value()

    def __str__(self, level=0):
        text = "--" * level + self.get_text() + "\n"
        for child_node in self.children:
            text += child_node.__str__(level + 1)
        return text


def printTree(node):
    node.get_child_nodes()


def parse_tree(args):
    _stack = []

    ##(FORALL x (IMPLIES (P x) (Q x)))
    _stack_element = None
    for index in range(len(args)):
        current_index = index

        current_element = args[current_index]
        current_symbol_type = current_element[0]
        current_symbol_value = current_element[1]

        if current_symbol_type == "open_bracket" and current_symbol_value == "(":
            continue
        elif current_symbol_type == "close_bracket" and current_symbol_value == ")":

            _picked_child_nodes = []
            while True:
                _parent_node = _stack.pop()

                _symbol_type = _parent_node.get_element_type()
                _symbol_value = _parent_node.get_element_value()

                if _symbol_type == "op" or _symbol_type == "quant" or _symbol_type == "function" or _symbol_type == "predicate":
                    _child_nodes = _parent_node.get_child_nodes()
                    _no_child_nodes = len(_child_nodes)

                    if _no_child_nodes == 0:
                        break

                _picked_child_nodes.append(_parent_node)

            _parent_node.set_child_nodes(_picked_child_nodes)

            _stack.append(_parent_node)

        else:
            _node = Node(current_symbol_type, current_symbol_value)
            _stack.append(_node)

            ##print(current_element,_stack)

    #print("stack size: %d" % len(_stack))
    assert (len(_stack) == 1)

    return _stack.pop()


def parse(F):
    characters = F

    ## breaking the input to argument types
    ## argument types: open and close bracket, operator and symbol
    args = []

    regex = r'''\(|\)|\[|\]|\-?\d+\.\d+|\-?\d+|[^,(^)\s]+'''

    ## sanitizing the input
    characters = characters.replace("\t", " ")
    characters = characters.replace("\n", " ")
    characters = characters.replace("\r", " ")
    characters = characters.lstrip(" ")
    characters = characters.rstrip(" ")

    ##prev_arg_name = None

    prev_arg = next_arg = None
    lines = []
    arg_list = re.findall(regex, characters)
    for i in range(len(arg_list)):
        arg = arg_list[i]
        if (i - 1 >= 0):
            prev_arg = arg_list[i - 1]
        if (i + 1 < len(arg_list)):
            next_arg = arg_list[i + 1]

        if (arg == "("):
            arg_name = "open_bracket"
        elif (arg == ")"):
            arg_name = "close_bracket"
        elif prev_arg == "(":
            if (arg in OPS):
                arg_name = "op"
            elif (arg in QUANTS):
                arg_name = "quant"
            else:
                arg_name = "function"
        elif (prev_arg in QUANTS):
            arg_name = "variable"
        elif arg.isalnum():
            arg_name = "symbol"

        arg_tuple = (arg_name, arg)
        args.append(arg_tuple)
    ##prev_arg_name = arg_name
    
    return args

    #print(args)

    ## Tree parser for S-expression

    ##FOL_Tree = parse_tree(args)
    #print(FOL_Tree)

    ## recorrecting predicates
    ##FOL_Tree = recorrect(FOL_Tree)

    #FOL_Tree = parse_tree(args)
    #print(FOL_Tree)

    ## recorrecting predicates
    #FOL_Tree = recorrect(FOL_Tree)

    #print(FOL_Tree)

    ## removing conditionals
    ##FOL_Tree = remove_conditionals(FOL_Tree)
    #print(FOL_Tree)


    ## deMorgan
    ##FOL_Tree = deMorgan(FOL_Tree)
    #print(FOL_Tree)

    ## standardization
    #FOL_Tree = standardize(FOL_Tree)

    ##print(FOL_Tree)

##################################################################################
def findIncSet(F):
    result = []
    for i in range(0, len(F)):
        F[i] = algorithm(F[i])
        if F[i] == "Inconsistent":
            result.append(i)
    return result

def algorithm(L):
    for i in range(0, len(L)):
        L[i] = parse(L[i])
        L[i] = parse_tree(L[i])
        L[i] = recorrect(L[i])
        L[i] = remove_conditionals(L[i])
        L[i] = deMorgan(L[i])
    
    standardize(FOL_Tree,variable_names)

    for i in range(0, len(L)):
        L[i] = prenex_form(L[i])
        L[i] = skolemize(L[i])
        L[i] = drop_universal(L[i])
        L[i] = convert_CNF(L[i])

    #clausal form function
    
    #unification & resolution functions

prenex = True
def prenex_form(FOL_Tree): #This function checks if its already in prenex form, if not it passes it to a converter. 
    #Prenex form is pushing all the quantifiers up as far as possible. 
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()

    _child_nodes = FOL_Tree.get_child_nodes()
    _child_symbol_type = _child_node.get_element_type()
    if _symbol_type != "quant" and _child_symbol_type == "quant":
        prenex = False

    for i in range(len(_child_nodes)):
        prenex_form(_child_nodes[i])

    if prenex == True:
        return FOL_Tree
    else: 
        return prenex_convert(FOL_Tree)

def prenex_convert(FOL_Tree):
=======
    #print(FOL_Tree)

    ## prenex 
    #FOL_Tree = prenex_form(FOL_Tree)
    #print(FOL_Tree)

##################################################################################
def findIncSet(F):
    result = []
    for i in range(0, len(F)):
        F[i] = algorithm(F[i])
        if F[i] == "Inconsistent":
            result.append(i)
    return result

def algorithm(L):
    for i in range(0, len(L)):
        L[i] = parse(L[i])
        L[i] = parse_tree(L[i])
        L[i] = recorrect(L[i])
        L[i] = remove_conditionals(L[i])
        L[i] = deMorgan(L[i])
        L[i] = standardize(L[i])
        L[i] = prenex_form(L[i])
        L[i] = skolemize(L[i])
        L[i] = drop_universal(L[i])
        #L[i] = convert_CNF(L[i])
        print(L[i])
        print("Done")

    #clausal form function
    
    #unification & resolution functions

    # Returning L
    return L

############### PRENEX CODE START ###################      
prenex = True
def prenex_form(FOL_Tree): #This function checks if its already in prenex form, if not it passes it to a converter. 
    #Prenex form is pushing all the quantifiers up as far as possible. 
    if_prenex = prenex_check(FOL_Tree)

    if if_prenex == True:
        return FOL_Tree
    else: 
        FOL_Tree = prenex_convert(FOL_Tree)
        return prenex_form(FOL_Tree)

def prenex_check(FOL_Tree):
    global prenex
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()

    currChildren = FOL_Tree.get_child_nodes()

    # Check for lenghth of children here
    if len(currChildren) != 2:
        return True

    leftChild = currChildren[1]
    leftChildType = leftChild.get_element_type()

    rightChild = currChildren[0]
    rightChildType = rightChild.get_element_type()

    if _symbol_type != "quant" and (leftChildType == "quant" or rightChildType == "quant"):
        return False
    
    else:
        return prenex_check(leftChild) and prenex_check(rightChild)

def prenex_convert(FOL_Tree):
    global prenex


    leftChild = currChildren[1]
    leftChildType = leftChild.get_element_type()
    leftChildChildren = leftChild.get_child_nodes()

    leftChildLeft = leftChildChildren[1]
    leftChildLeftType = leftChildLeft.get_element_type()

    leftChildRight = leftChildChildren[0]
    leftChildRightType = leftChildRight.get_element_type()



    rightChild = currChildren[0]
    rightChildType = rightChild.get_element_type()
    rightChildChildren = rightChild.get_child_nodes()

    rightChildLeft = rightChildChildren[1]
    rightChildLeftType = rightChildLeft.get_element_type()

    rightChildRight = rightChildChildren[0]
    rightChildRightType = rightChildRight.get_element_type()


    if leftChildType != "quant" and leftChildLeftType == "quant":
        #left left is the issue
        
    elif leftChildType != "quant" and leftChildRightType == "quant":
        #left right is the issue

    elif rightChildType != "quant" and rightChildLeftType == "quant":
        #right left is the issue

    elif rightChildType != "quant" and rightChildRightType == "quant":
        #right right is the issue
        Temp = rightChild
        TempChildren = Temp.get_child_nodes()
        TempRight = TempChildren[0]

        currChildren[0] = rightChildRight
        set_child_nodes(currentNode, currChildren)

        TempChildren[0] = rightChildRight
        set_child_nodes(Temp, TempChildren)

        rightChildChildren[0] = Temp
        set_child_nodes(rightChild, rightChildChildren)

        currChildren[0] = rightChild
        set_child_nodes(currentNode, currChildren)
        

    else: #not what we're looking for, move on. 
        for i in range(len(_child_nodes)):
            prenex_convert(_child_nodes[i])
    
    prenex = True
    return prenex_form(FOL_Tree) #checks it again since you can miss stuff first time around
       
        
def skolemize(FOL_Tree):
    return FOL_Tree
def drop_universal(FOL_Tree):
    return FOL_Tree
def convert_CNF(FOL_Tree):
    return FOL_Tree
###################################################################################

'''problems = [
    ["(FORALL x (IMPLIES (P x) (Q x)))", "(P (f a))", "(NOT (Q (f a)))"],  # this is inconsistent
    ["(FORALL x (IMPLIES (P x) (Q x)))", "(FORALL x (P x))", "(NOT (FORALL x (Q x)))"],  # this is inconsistent
    ["(EXISTS x (AND (P x) (Q b)))", "(FORALL x (P x))"],  # this should NOT lead to an empty clause
    ["(NOT (NOT (P a)))"],  # this should NOT lead to an empty clause
=======
    if len(currChildren) != 2:
        return FOL_Tree

    leftChild = currChildren[1]
    leftChildType = leftChild.get_element_type()
    leftChildValue = leftChild.get_element_value()
    leftChildChildren = leftChild.get_child_nodes()

    rightChild = currChildren[0]
    rightChildType = rightChild.get_element_type()
    rightChildValue = rightChild.get_element_value()
    rightChildChildren = rightChild.get_child_nodes()

    if _symbol_type == "op" and leftChildType == "quant": #Left subtree is the issue.
        leftChildLeft = leftChildChildren[1]
        leftChildLeftType = leftChildLeft.get_element_type()
        leftChildLeftValue = leftChildLeft.get_element_value()

        leftChildRight = leftChildChildren[0]

        tempType = currentNode.get_element_type()
        tempValue = currentNode.get_element_value()

        currentNode.set_node(leftChildType, leftChildValue)
        leftChild.set_node(tempType, tempValue)

        temp = Node(leftChildLeftType, leftChildLeftValue)
        leftChildLeft = leftChildRight
        leftChildRight = rightChild
        rightChild = leftChild
        leftChild = temp


    elif _symbol_type == "op" and rightChildType == "quant": #Right subtree is the issue.
        rightChildLeft = rightChildChildren[1]
        rightChildLeftType = rightChildLeft.get_element_type()
        rightChildLeftValue = rightChildLeft.get_element_value()

        rightChildRight = rightChildChildren[0]

        tempType = currentNode.get_element_type()
        tempValue = currentNode.get_element_value()

        currentNode.set_node(rightChildType, rightChildValue)
        rightChild.set_node(tempType, tempValue)

        temp = Node(rightChildLeftType, rightChildLeftValue)
        rightChildLeft = leftChild
        leftChild = temp

    prenex_convert(leftChild)
    prenex_convert(rightChild)
    return FOL_Tree

################ PRENEX CODE END ##################

varList = []        
def skolemize(FOL_Tree):
    global varList
    currentNode = FOL_Tree
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()
    
    if _symbol_type != "quant":
        varList = []
        return FOL_Tree
    else:
        currChildren = currentNode.get_child_nodes()

        leftChild = currChildren[1]
        leftChildValue = leftChild.get_element_value()

        rightChild = currChildren[0]
        rightChildType = rightChild.get_element_type()
        rightChildValue = rightChild.get_element_value()

        rightChildChildren = rightChild.get_child_nodes()
        if len(rightChildChildren) == 2:
            rightChildleft = rightChildChildren[1]
        rightChildRight = rightChildChildren[0]
        if _symbol_value == "FORALL":
            varList.append(leftChildValue) 

        else: #EXISTS
            if varList == []:
                new_symbol_type = "symbol"
            else:
                new_symbol_type = "function"
            rename(FOL_Tree, new_symbol_type, leftChildValue)

            currentNode.set_node(rightChildType, rightChildValue)
            if len(rightChildChildren) == 2:
                currChildren[1] = rightChildleft
            currChildren[0] = rightChildRight
            skolemize(currentNode)
            
        skolemize(currChildren[0])    
        return FOL_Tree
    
    
def rename(FOL_Tree, new_symbol_type, var):
    global varList
    currentNode = FOL_Tree
    currChildren = currentNode.get_child_nodes()
    _symbol_type = FOL_Tree.get_element_type()
    _symbol_value = FOL_Tree.get_element_value()
    
    if _symbol_value == var:
        if new_symbol_type == "symbol":
            currentNode.set_node(new_symbol_type, var)
        else: #new_symbol_type == "function"
            currentNode.set_node(new_symbol_type, var)
            for i in range(0, len(varList)):
                temp = Node("variable", varList[i])
                currentNode.add_child(temp)

    else:
        for i in range(len(currChildren)):
            FOL_Tree = rename(currChildren[i], new_symbol_type, var)

    return FOL_Tree

universal_varList = []
def drop_universal(FOL_Tree):
    global universal_varList
    _symbol_type = FOL_Tree.get_element_type()
    currentNode = FOL_Tree
    currChildren = currentNode.get_child_nodes()

    if len(currChildren) != 2:
        return FOL_Tree
    else:
        if _symbol_type == "quant":
            leftChild = currChildren[1]
            leftChildValue = leftChild.get_element_value()
            universal_varList.append(leftChildValue)

            rightChild = currChildren[0]
            rightChildType = rightChild.get_element_type()
            rightChildValue = rightChild.get_element_value()

            rightChildChildren = rightChild.get_child_nodes()
            if len(rightChildChildren) == 2:
                rightChildleft = rightChildChildren[1]
            rightChildRight = rightChildChildren[0]

            FOL_Tree = currChildren[0]
            drop_universal(FOL_Tree)
            currentNode.set_node(rightChildType, rightChildValue)
            if len(rightChildChildren) == 2:
                currChildren[1] = rightChildleft
            currChildren[0] = rightChildRight

            drop_universal(currentNode)
        
        drop_universal(currChildren[0])
        return FOL_Tree
###################################################################################

def convert_CNF(FOL_Tree): ##### STILL NEEDS TO BE DONE.
    return FOL_Tree


problems = [
    ["(FORALL x (IMPLIES (p x) (q x)))", "(p (f a))", "(NOT (q (f a)))"],  # this is inconsistent
    ["(FORALL x (IMPLIES (p x) (q x)))", "(FORALL x (p x))", "(NOT (FORALL x (q x)))"],  # this is inconsistent
    ["(EXISTS x (AND (p x) (q b)))", "(FORALL x (p x))"],  # this should NOT lead to an empty clause
    ["(NOT (NOT (p a)))"],  # this should NOT lead to an empty clause
>>>>>>> 13b9292954c0bb5d2fc2ed004923aa2cdb193b83
    ["(big_f (f a b) (f b c))",
     "(big_f (f b c) (f a c))",
     "(FORALL x (FORALL y (FORALL z (IMPLIES (AND (big_f x y) (big_f y z)) (big_f x z)))))",
     "(NOT (big_f (f a b) (f a c)))"]  # this is inconsistent
]
<<<<<<< HEAD
=======
findIncSet(problems)
>>>>>>> 13b9292954c0bb5d2fc2ed004923aa2cdb193b83

# ## conditional removal
'''parse("(FORALL x (IMPLIES (P x) (Q x)))")

## NNF
parse("(NOT(AND p q))")
parse("(NOT(OR p q))")
parse("(NOT (FORALL x (f x)))")
parse("(NOT (EXISTS y (f y)))")

# standardize variables
parse("(OR (EXISTS x (f x)) (FORALL x (f x)))")
parse("(FORALL y (IMPLIES (FORALL x (FORALL y (P x y))) (EXISTS x (R x y))))")

parse("(P (f x y))")

parse("(FORALL X (FORALL Y (FORALL Z (IMPLIES (AND (big_f X Y) (big_f Y Z)) (big_f X Z)))))")


parse("(FORALL x (P x))")
for problem in problems:
    for p in problem:
        parse(p)
        print("\n==============\n")

'''
parse("(NOT (FORALL x (EXISTS y (IMPLIES (p x y) (AND (FORALL y (EXISTS z (NOT (q x z)))) (FORALL y (NOT (FORALL z (r y z)))))))))")
=======

'''

'''
test = "(FORALL x (EXISTS y (p x y)))"
parsed = parse(test)
full_parse = parse_tree(parsed)
reconnect = recorrect(full_parse)
print(reconnect)
skolemized = skolemize(reconnect)
print(skolemized)
print("Done")

test = "(FORALL y (FORALL x (p x y)))"
parsed = parse(test)
full_parse = parse_tree(parsed)
reconnect = recorrect(full_parse)
print(reconnect)
drop = drop_universal(reconnect)
print(drop)
print("Done")'''

