import csv
import math

from os import name

class Attribute:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.values = []
    
    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        # temp = ""
        # temp += "[Name: " + self.name + ", "
        # temp += "Index: " + str(self.index) + ", "
        # temp += "Values: ["

        # for val in self.values:
        #     temp += repr(val) + ","
        
        # temp += "]"

        # return temp
        return self.name
    
    def __repr__(self):
        # temp = ""
        # temp += "[Name: " + self.name + ", "
        # temp += "Index: " + str(self.index) + ", "
        # temp += "Values: ["

        # for val in self.values:
        #     temp += repr(val) + ","
        
        # temp += "]"

        # return temp
        return self.name



class Value:
    def __init__(self, name, attribute, index):
        self.index = index
        self.name = name
        self.attribute = attribute
        self.positives = 0
        self.negatives = 0

    def __eq__(self, other):
        return (self.name == other.name) and (self.attribute == other.attribute)
    
    def __str__(self):
        # temp = ""
        # temp += "[Name: " + self.name + ", "
        # temp += "Index: " + str(self.index) + ", "
        # temp += "Positives: " + str(self.positives) + ", "
        # temp += "Negatives: " + str(self.negatives) + "]"
        # return temp
        return  "[Attrib: " + self.attribute + ", Name: " + self.name +"]"

    def __repr__(self):
        # temp = ""
        # temp += "[Name: " + self.name + ", "
        # temp += "Index: " + str(self.index) + ", "
        # temp += "Positives: " + str(self.positives) + ", "
        # temp += "Negatives: " + str(self.negatives) + "]"
        # return temp
        return  "[Attrib: " + self.attribute + ", Name: " + self.name +"]"

class Example:
    def __init__(self, index, output):
        self.index = index
        self.output = output
        self.attributeValues = []

    def __str__(self):
        temp = ""
        # temp += "[Index: " + str(self.index) + ", "
        # temp += "Atrib Vals: "

        for val in self.attributeValues:
            temp += repr(val) + ", "
        return temp
    
    def __repr__(self):
        temp = ""
        # temp += "[Index: " + str(self.index) + ", "
        # temp += "Atrib Vals: "

        for val in self.attributeValues:
            temp += repr(val) + ", "
        return temp

class Node:
    def __init__(self, label):
        self.label = label
        self.children = [] # if empty that means its a action yes or no
    
    def __str__(self, level=0):
        ret = ""
        if(level == 0):
            ret = repr(self.label)+"\n"
        elif (len(self.children) == 1) and (len(self.children[0].children) == 0):
            ret = "|"+"---"*(level)+repr(self.label)
        elif len(self.children) == 0:
            ret = " => " + repr(self.label) + "\n"
        else:
            ret = "|"+"---"*(level)+repr(self.label)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret.replace("'", "")

def plurality_value(examples):
    num_yes = 0
    num_no = 0

    for ex in examples:
        if ex.output == "Yes":
            num_yes += 1
        else:
            num_no += 1
    
    if num_yes > num_no:
        return Node("Yes")
    
    else:
        return Node("No")

def b_val(q):
    if (q == 1) or (q == 0):
        return 0

    first_term = q * math.log(q, 2)

    second_term = (1 - q) * math.log(1-q, 2)

    return (first_term + second_term) * -1

def Gain(p, n, attrib, examples):
    # print("new call")
    # print()
    p = 0
    n = 0

    for ex in examples:
        output = ex.output

        if output == "Yes":
            p += 1
        else:
            n += 1
    
    q = p / (p + n)
    B = b_val(q)

    size = len(attrib.values)
    remainder = 0

    for i in range(size):
        p_k = 0
        n_k = 0

        for ex in examples:
            output = ex.output

            if (output == "Yes") and (attrib.values[i] == ex.attributeValues[attrib.index]):
                p_k += 1
            elif (output == "No") and (attrib.values[i] == ex.attributeValues[attrib.index]):
                n_k += 1

        first_term = (p_k + n_k) / (p + n)

        if first_term == 0:
            continue
        
        q_k = p_k / (p_k + n_k)

        remainder += first_term * b_val(q_k)
    
    return B - remainder

def learn_decision_tree(examples, attributes, parent_examples):
    if len(examples) == 0:
        return plurality_value(parent_examples)
    
    the_output = examples[0].output
    same_class = True

    for exs in examples:
        if(exs.output != the_output):
            same_class = False
            break
    
    if same_class:
        return Node(the_output)
    
    if len(attributes) == 0:
        return plurality_value(examples)

    max_attrib = attributes[0]
    max_importance = Gain(p, n, max_attrib, examples)
    importances = ""

    for attrib in attributes:
        new_importance = Gain(p, n, attrib, examples)
        importances += str(new_importance) + ","

        if(new_importance > max_importance):
            max_importance = new_importance
            max_attrib = attrib

    tree = Node("| " + max_attrib.name + " |")
    vals = max_attrib.values

    index = attributes.index(max_attrib)

    new_attribs = attributes
    new_attribs.pop(index)

    for val in vals:
        exs = []

        for ex in examples:
            if ex.attributeValues[max_attrib.index] == val:
                exs.append(ex)

        subtree = Node(val.name)

        subtree.children.append(learn_decision_tree(exs, new_attribs, examples))

        tree.children.append(subtree)
    
    return tree

def print_tree(head, spaces):
    if len(head.children) == 0:
        print("|" + spaces + ">" + head.label)
        return
    else:
        print("|" + spaces + head.label)

    for child in head.children:
        temp_spaces = spaces + "___"
        
        print_tree(child, temp_spaces)

attributes = [Attribute("Alt", 0),
              Attribute("Bar", 1),
              Attribute("Fri", 2),
              Attribute("Hun", 3),
              Attribute("Pat", 4),
              Attribute("Price", 5),
              Attribute("Rain", 6),
              Attribute("Res", 7),
              Attribute("Type", 8),
              Attribute("Est", 9),]

examples = []

filename = "restaurants.csv"

rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:
        rows.append(list(map(str.strip, row)))

for i in range(len(rows)):
    row = rows[i]
    output = row[len(row) - 1]

    for j in range(len(row)-1):
        newVal = Value(str(row[j]), attributes[j].name, len(attributes[j].values))

        if(newVal not in attributes[j].values):
            attributes[j].values.append(newVal)
        
        index = attributes[j].values.index(newVal)

        if(output == "Yes"):
            attributes[j].values[index].positives += 1
        else:
            attributes[j].values[index].negatives += 1

p = 0
n = 0

for i in range(len(rows)):
    row = rows[i]
    output = row[len(row) - 1]

    if output == "Yes":
        p += 1
    else:
        n += 1

    examples.append(Example(i, output))

    for j in range(len(row) - 1):
        newVal = Value(str(row[j]), attributes[j].name, len(attributes[j].values))

        index = attributes[j].values.index(newVal)

        examples[i].attributeValues.append(attributes[j].values[index])

head = learn_decision_tree(examples, attributes, [])

print(head)