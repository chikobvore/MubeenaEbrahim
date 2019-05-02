import pandas as pd
import numpy as np

data = pd.read_csv("mubeena1.csv")
data.dropna()


Reading = []
Spelling = []
Comp = []
Math = []
Total = []
Remarks =[]
for x in range( 4 ,len(data)):
    data.dropna()
    read = data.iloc[x][0]
    spellings = data.iloc[x][1]
    comp = data.iloc[x][2]
    math = data.iloc[x][3]

    remedials = []

    if read is None:
        print("asi aunyare here")

    print(read)
    if int(read) < 50:
        remarks = "Practice, the more  you read the better reader you become, do feed your mind"
        print(remarks)
        remedials.append(remarks)
    
    
    if int(spellings) <50:
        remarks = "Practice wide and wild reading to improve vocabulary"
        print(remarks)
        remedials.append(remarks)

    if int(comp) < 50:
        remarks = "Practice, the more  you read the better reader you become, do feed your mind"
        print(remarks)
        remedials.append(remarks)
    
    if int(math) < 50:
        remarks = "Play mathematical games so that you can have fun and learn at the same time"
        print(remarks)
        remedials.append(remarks)
    
    if int(read) > 50 and int(spellings) > 50 and int(comp) > 50 and int(math) > 50:
        remarks = "Child is very Inteligent"
        print(remarks)
        remedials.append(remarks)

    if int(read) == 50 or int(spellings) == 50 or int(comp) == 50 or int(math) == 50:
        remarks = "Child is inteligent but needs help from guidane also"
        print(remarks)
        remedials.append(remarks)
    
        
    Reading.append(read)
    Spelling.append(spellings)
    Comp.append(comp)
    Math.append(math)
    Remarks.append(remedials)
# #         Remarks.append(remarks)
# #     elif remarks == 'Pass' or remarks == 'pass':
# #         remarks = 1
# #         Maths.append(maths)
# #         Eng.append(english)
# #         Shona.append(shona)
# #         Gp.append(gp)
# #         Total.append(total)
# #         Remarks.append(remarks)
# #     else:
# #         pass
        
        
    

    
    
Data = {
        "Reading": Reading,
        "Spelling": Spelling,
        "Comprehension": Comp,
        "Mathematics": Math,
        "Remarks": Remarks
    }

Dataset = pd.DataFrame(Data,columns= ['Reading','Spelling','Comprehension','Mathematics','Remarks'])
Export = Dataset.to_csv('mubeena2.csv',index=None,header=True)
print(Dataset.head())