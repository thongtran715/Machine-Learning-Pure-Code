#Given the set of the data
training_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]

#Caculate the impurity (Gini)

def total_set_counts (rows):
    dic = {}
    for row in rows:
        d = row[-1]
        if d not in dic:
            dic[d] = 1
        else:
            dic[d] += 1
    return dic

#Check total
#dic = total_set_counts(training_data)
#print (dic)

#this function will calculate how much succeed to pick up the right product
def summation_right_pick (rows):
    total_denominator = float(len(rows))
    sets = total_set_counts(rows)
    sum = 0 
    for lbl in sets:
        sum += (sets[lbl] / total_denominator) ** 2
    return sum

def gini(rows):
    # 1 - summation of p succeed in one category 
    return 1 - summation_right_pick(rows)

headers = ["Color", "Diameter", "label"]

#Get the isNumeric
def isNumeric(data):
    return isinstance(data,int) or isinstance(data,float)

class Question:
    def __init__(self, column,value):
        self.column = column
        self.value = value
    def match(self, data):
        compare = data[self.column]
        if isNumeric(compare):
            return self.value >= compare
        else:
            return self.value == compare
    def __str__(self):
        condition = "=="
        if isNumeric(self.value):
            condition = ">="
        return "Is %s %s %s ?" %(headers[self.column], condition, self.value)

def partition (question, training_data):
    true_rows = []
    false_rows = []
    for data in training_data:
        if question.match(data):
            true_rows.append(data)
        else:
            false_rows.append(data)
    return true_rows, false_rows

#true_rows, false_rows = partition(Question(0,"Red"), training_data)
#print (true_rows)
#print(false_rows)

def information_gain (left_rows, right_rows, top_rows):
    impurity_left = gini(left_rows)
    impurity_right = gini(right_rows)
    impurity_top = gini(top_rows)
    p = float(len(left_rows))/float(len(top_rows))
    return impurity_top - (p*impurity_left + (1 - p) * impurity_right)

#true_rows, false_rows = partition(Question(0, 'Red'), training_data)
#m = information_gain(false_rows,true_rows, training_data)
def find_best_split (rows):
    best_gain = 0 
    best_question = "None"
    num_features = len(rows[0]) - 1
    for col in range(num_features):
        unique_values = set([row[col] for row in rows] )
        for val in unique_values:
            question = Question(col,val)
            true_rows , false_rows = partition(question,rows)
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue
            gain = information_gain(false_rows,true_rows,training_data)
            if gain >= best_gain:
                best_gain,best_question = gain, question
    return best_gain,best_question
class Leaf:
    def __init__(self, rows):
        self.predictions = total_set_counts(rows)
class Decision_Node:
    def __init__(self,question,true_branch,false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch
def build_tree(rows):
    best_gain, best_question = find_best_split(rows)
    if best_gain == 0: return Leaf(rows)
    true_rows, false_rows = partition(best_question,rows)
    true_branch = build_tree(true_rows)
    false_branch = build_tree(false_rows)
    return Decision_Node(best_question,true_branch,false_branch)
def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return
    print (spacing + str(node.question))
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")
def classify(row, node):
    """See the 'rules of recursion' above."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)
def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs
my_tree = build_tree(training_data)
c = print_leaf(classify(training_data[1], my_tree))


# Evaluate# Evalua 
testing_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 4, 'Apple'],
    ['Red', 2, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]
for row in testing_data:
    print ("Actual: %s. Predicted: %s" %
           (row[-1], print_leaf(classify(row, my_tree))))
