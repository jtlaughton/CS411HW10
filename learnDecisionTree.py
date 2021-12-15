import csv
import math
import random

from os import name

# holds data for a specific attribute
class Attribute:
    def __init__(self, name, index):
        self.name = name    # name of attribute
        self.index = index  # index in the attributes array
        self.values = []    # values associated with attribute
    
    # equality overload. Need to properly check equality as well as operators such as in and .index()
    def __eq__(self, other):
        return self.name == other.name

# holds data for a specific value
class Value:
    def __init__(self, name, attribute):
        self.name = name            # name of the value
        self.attribute = attribute  # values associated attribute

    # equality overload. Need to properly check equality as well as operators such as in and .index
    def __eq__(self, other):
        return (self.name == other.name) and (self.attribute == other.attribute)

# holds data for a specific example
class Example:
    def __init__(self, index, output):
        self.index = index          # index in the examples array
        self.output = output        # output associated with that example
        self.attributeValues = []   # the values associated with every attribute in the example, parallel to attributes array

# node of the three
class Node:
    def __init__(self, label):
        self.label = label # label of the node
        self.children = [] # if empty that means its a action yes or no
    
    # recursive string builder for calling print(node). Keep track of level for determining spaces
    def __str__(self, level=0):
        ret = ""
        # if we are at the beginning no spaces
        if(level == 0):
            ret = repr(self.label)+"\n"
        # if our child is a leaf don't print a new line
        elif (len(self.children) == 1) and (len(self.children[0].children) == 0):
            ret = "|"+"---"*(level)+repr(self.label)
        # if we have a leaf print an arrow to denote that
        elif len(self.children) == 0:
            ret = " => " + repr(self.label) + "\n"
        # otherwise calculate necessary hyphens for this level of the tree
        else:
            ret = "|"+"---"*(level)+repr(self.label)+"\n"
        # for every child call this function again but with updated level
        for child in self.children:
            ret += child.__str__(level+1)
        # return the built string and remove the single quotes
        return ret.replace("'", "")

# does plurality value calculation
def plurality_value(examples):
    num_yes = 0
    num_no = 0

    # determine how many of each output there are
    for ex in examples:
        if ex.output == "Yes":
            num_yes += 1
        else:
            num_no += 1
    
    # if we have more yeses pick yes
    if num_yes > num_no:
        return Node("Yes")
    # if we have equal yeses and nos randomly pick between yes and no
    elif num_no == num_yes:
        r = random.randint(1, 2)
        if r == 1:
            return Node("No")
        else:
            return Node("Yes")
    # otherwise more nos so pick no
    else:
        return Node("No")

# calculates B() from texbook
def b_val(q):
    # no uncertaintiy if probability is 1 or 0 because that means it always happens or never happends
    # so return 0
    if (q == 1) or (q == 0):
        return 0

    # first expression in the B() function
    first_term = q * math.log(q, 2)

    # second expression in the B() function
    second_term = (1 - q) * math.log(1-q, 2)

    # return B()
    return (first_term + second_term) * -1

# does information gain function
def Gain(attrib, examples):
    # positives and negatives
    p = 0
    n = 0

    # calculate how many positves and negatives in each example
    for ex in examples:
        output = ex.output

        if output == "Yes":
            p += 1
        else:
            n += 1
    
    # calculate B for all examples
    q = p / (p + n)
    B = b_val(q)

    # calculate remainder
    size = len(attrib.values)
    remainder = 0

    for i in range(size):
        # positves and negatives associated with each value of attribute
        p_k = 0
        n_k = 0

        # calculate p_k and n_k for value
        for ex in examples:
            output = ex.output

            # if the output of the example is yes and the attribute value is the same as our current value then add to p_k
            if (output == "Yes") and (attrib.values[i] == ex.attributeValues[attrib.index]):
                p_k += 1
            # same but just if output is no
            elif (output == "No") and (attrib.values[i] == ex.attributeValues[attrib.index]):
                n_k += 1

        # first expression of remainder
        first_term = (p_k + n_k) / (p + n)

        # if first term is zero it doesnt affect remainder so skip
        if first_term == 0:
            continue
        
        # calculate iteration of remainder
        q_k = p_k / (p_k + n_k)

        remainder += first_term * b_val(q_k)
    
    # return information gain
    return B - remainder

# builds the learn decision tree
def learn_decision_tree(examples, attributes, parent_examples):
    # base case of algorithm
    if len(examples) == 0:
        return plurality_value(parent_examples)
    
    # determine if output for all examples is the same
    the_output = examples[0].output
    same_class = True

    for exs in examples:
        if(exs.output != the_output):
            same_class = False
            break
    
    # if so base case
    if same_class:
        return Node(the_output)
    
    # base case of algorithm
    if len(attributes) == 0:
        return plurality_value(examples)

    # values for tracking max attribute
    max_attrib = attributes[0]
    max_importance = Gain(max_attrib, examples)

    # for all attributes find the one with max info gain
    for attrib in attributes:
        new_importance = Gain(attrib, examples)

        if(new_importance > max_importance):
            max_importance = new_importance
            max_attrib = attrib

    # make a tree with head of attribute, add | to make it stand out
    tree = Node("| " + max_attrib.name + " |")
    vals = max_attrib.values

    # find index in remaining attributes
    index = attributes.index(max_attrib)

    # make a new list based on attributes and pop at the index
    new_attribs = attributes
    new_attribs.pop(index)

    # for each val in the max attribute do this
    for val in vals:
        exs = []

        # find all examples that have val in them
        for ex in examples:
            if ex.attributeValues[max_attrib.index] == val:
                exs.append(ex)

        # build a subtree on the value
        subtree = Node(val.name)

        # add output of learn_decision_tree to subtrees children
        subtree.children.append(learn_decision_tree(exs, new_attribs, examples))

        # add subtree as child of tree
        tree.children.append(subtree)
    
    return tree

# attributes = [Attribute("Alt", 0),
#               Attribute("Bar", 1),
#               Attribute("Fri", 2),
#               Attribute("Hun", 3),
#               Attribute("Pat", 4),
#               Attribute("Price", 5),
#               Attribute("Rain", 6),
#               Attribute("Res", 7),
#               Attribute("Type", 8),
#               Attribute("Est", 9),]

attributes = []
examples = []

filename = input("Enter Filename: ")
print()

rows = []

# get each row from the csv file
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    for row in csvreader:
        rows.append(list(map(str.strip, row)))

header = rows.pop(0)

for i in range(len(header) - 1):
    attributes.append(Attribute(header[i], i))

# make an example object for each row and add all the values to their corresponing attribute
for i in range(len(rows)):
    row = rows[i]
    output = row[len(row) - 1]

    # add example to examples
    examples.append(Example(i, output))

    for j in range(len(row) - 1):
         # create a new value
        newVal = Value(str(row[j]), attributes[j].name)

        # if that value is not in attributes then add it
        if(newVal not in attributes[j].values):
            attributes[j].values.append(newVal)

        # find index of the value that we are looking for
        index = attributes[j].values.index(newVal)

        # add the value we are looking for tp examples list of attribute values
        examples[i].attributeValues.append(attributes[j].values[index])

# make decision tree and output it
head = learn_decision_tree(examples, attributes, [])

print("Output Tree:")
print()
print(head)