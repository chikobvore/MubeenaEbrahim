import pandas as pd
import numpy as np

data = pd.read_csv("mubeena.csv")


Maths = []
Eng = []
Shona = []
Gp = []
Total = []
Remarks =[]
for x in range( 4 ,len(data)):
    maths = data.iloc[x][25]
    english = data.iloc[x][26]
    shona = data.iloc[x][27]
    gp = data.iloc[x][28]
    total = data.iloc[x][29]
    remarks = data.iloc[x][30]
    
    if remarks == 'Fail' or remarks =='fail':
        remarks = 0
        
        Maths.append(maths)
        Eng.append(english)
        Shona.append(shona)
        Gp.append(gp)
        Total.append(total)
        Remarks.append(remarks)
    elif remarks == 'Pass' or remarks == 'pass':
        remarks = 1
        Maths.append(maths)
        Eng.append(english)
        Shona.append(shona)
        Gp.append(gp)
        Total.append(total)
        Remarks.append(remarks)
    else:
        pass
        
        
    

    
    
Data = {
        "Maths": Maths,
        "English": Eng,
        "Shona": Shona,
        "General Paper": Gp,
        "Total": Total,
        "Remarks": Remarks
    }

Dataset = pd.DataFrame(Data,columns= ['Maths','English','Shona','General Paper','Total','Remarks'])
Export = Dataset.to_csv('mubeena1.csv',index=None,header=True)
print(Dataset.head())