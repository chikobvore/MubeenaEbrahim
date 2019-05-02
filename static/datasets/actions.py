import pandas as pd
import numpy as np

data = pd.read_csv("mubeena.csv")


Reading = []
Spelling = []
Comp = []
Math = []
Total = []
Remarks =[]
for x in range( 4 ,20):
    read = data.iloc[x][25]
    spellings = data.iloc[x][26]
    comp = data.iloc[x][27]
    math = data.iloc[x][28]

    remedials = []
    if int(read) < 50:
        remarks = "Practice, the more  you read the better reader you become, do feed your mind"
        print(remarks)
        remedials.append(remarks)
    
    
    if int(spellings) <50:
        remarks = "Practice wide and wild reading to improve vocabulary"
        remedials.append(remarks)

    if int(comp) < 50:
        remarks = "Practice, the more  you read the better reader you become, do feed your mind"
        remedials.append(remarks)
    
    if int(math) < 50:
        remarks = "Play mathematical games so that you can have fun and learn at the same time"
        remedials.append(remarks)
    
    if int(read) > 50 and int(spellings) > 50 and int(comp) > 50 and int(math) > 50:
        remarks = "Child is very Inteligent"
    
        
    Reading.append(read)
    Spelling.append(spellings)
    Comp.append(comp)
    Math.append(math)
    Remarks.append(remedials)
#         Remarks.append(remarks)
#     elif remarks == 'Pass' or remarks == 'pass':
#         remarks = 1
#         Maths.append(maths)
#         Eng.append(english)
#         Shona.append(shona)
#         Gp.append(gp)
#         Total.append(total)
#         Remarks.append(remarks)
#     else:
#         pass
        
        
    

    
    
Data = {
        "Reading": Reading,
        "Spelling": Spelling,
        "Comprehension": Comp,
        "Mathematics": Math,
        "Remarks": Remarks
    }

Dataset = pd.DataFrame(Data,columns= ['Reading','Spellings','Comprehension','Mathematics','Remarks'])
Export = Dataset.to_csv('mubeena2.csv',index=None,header=True)
print(Dataset.head())