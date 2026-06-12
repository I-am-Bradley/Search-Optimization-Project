# 3-SAT problem generator
import numpy as np
n = 4 # number of variables
m = 6 # number of clauses

with open("3SAT_"+str(n)+"_"+str(m)+".txt", "w") as f:
    created = set()
    created.add("")
    for i in range(m):
        clause = ""
        while clause in created:
            clause = ""
            indices = np.random.choice(n, 3, replace=False)
            polarity = np.random.choice(["pos", "neg"], 3)
            order = np.argsort(indices)
            clause = clause + "x" + str(indices[order[0]]) + "_" + polarity[order[0]] + " "
            clause = clause + "x" + str(indices[order[1]]) + "_" + polarity[order[1]] + " "
            clause = clause + "x" + str(indices[order[2]]) + "_" + polarity[order[2]]
        created.add(clause)
        print(clause)
        f.write(clause+"\n")



        
