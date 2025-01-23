a = int(input("Enter a number: "))
b = int(input("Enter another number: "))
c = int(input("Enter another number: "))

maxnum = a
minnum = b
if maxnum < b:
    maxnum = b
if maxnum < c:
    maxnum = c
if minnum > a:
    minnum = a
if minnum > c:
    minnum = c

print("Max number is: ", maxnum, " Min number is: ", minnum)