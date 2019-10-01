FLOORHUB = 4
ROOMHUB = 4
LIGHTBULB = 3

testcase = []
temp = []
count = []
for x in range(1, FLOORHUB+1):
    temp.append(x)
    for y in range(1, ROOMHUB+1):
        temp.append(y)
        for z in range(1, LIGHTBULB+1):
            temp.append(z)
            testcase.append(temp)
            temp = [x,y]
        # testcase.append(temp)
        temp = [x]
    temp = []

for n, i in enumerate(testcase):
    print(str(i)+" = "+str(n+1))

print(tempcount)
print(count)

# for eq in testcase:
#     x = eq[0]
#     y = eq[1]
#     z = eq[2]
#     print(6*(x-1)+3*(y-1)+z)
        
