solution = {}
with open('solution.txt') as f:
    next(f)
    for line in f:
        x = line.split(",")
        solution[x[0]] = x[1].strip().split(" ")


submission = {}
with open('submission.txt') as f:
    next(f)
    for line in f:
        x = line.split(",")
        submission[x[0]] = x[1].strip().split(" ")





average_precision = 0

# loop querys
for key in solution.keys():
    # calc percision
    precision = 0
    index = 0
    found = 0
    #loop documents
    for doc in submission[key]:
        index +=1
        #check if relevant
        if doc in solution[key]:
            found +=1
            precision += found/index
    average_precision += precision/len(solution[key])
MAP= average_precision/len(solution.keys())
print(MAP)

