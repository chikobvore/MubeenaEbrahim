import pandas as pd 

data = pd.read_csv('mubeena.csv')
print(data.head())

Writing_list = []
Addition_list = []
Subtraction_list = []
Multiplication_list = []
Division_list = []
Reading_list = []
Spelling_list = []
Comments = []
for i in range(4,len(data)):


    
    comprehen = data.iloc[i][4]
    maths = data.iloc[i][6]
    Subtraction = data.iloc[i][8]
    Multiplication = data.iloc[i][10]
    Division = data.iloc[i][12]
    Reading = data.iloc[i][15]
    Spelling = data.iloc[i][17]

    if comprehen is not None:
        print(comprehen)
        mycomment = []
        if int(comprehen) < 50 :
            comment = "Practice, the more  you read the better reader you become, do feed your mind"
            mycomment.append(comment)

        if  int(Reading) < 50:
            comment = "Provide the student  with recommended books as an alternative to self reading"
            mycomment.append(comment)
        
        if int(Spelling) < 50:
            comment = "Practice wide and wild reading to improve vocabulary"
            mycomment.append(comment)
        if int(maths) < 50:
            comment = "Play mathematical games so that you can have fun and learn at the same time"
            mycomment.append(comment)
            
            
        Writing_list.append(comprehen)
        Addition_list.append(maths)
        Comments.append(mycomment)
        Division_list.append(Division)
        Reading_list.append(Reading)
        Spelling_list.append(Spelling)
        Comments.append(mycomment)
        Data = {
            "Comprehension": Writing_list,
            "Reading": Reading_list,
            "Spellings": Spelling_list,
            "Mathematics": Addition_list,
            "Comments": Comments
            }
        
        print(len(Writing_list))
        print(len(Comments))
        # Dataset = pd.DataFrame(Data,columns= ['Comprehension','Reading','Spellings','Mathematics','Comments'])
        # Export = Dataset.to_csv('newdata.csv',index=None,header=True)
        # print(Dataset.head())