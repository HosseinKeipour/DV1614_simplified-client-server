import string

folder =input()
fld = string.punctuation
for char in fld:
    print("fld", char)
    if char in folder:
        print("folder", char)
        print('\n\rError:The folder does not exist. Try again.')
        

print( "success")
        

