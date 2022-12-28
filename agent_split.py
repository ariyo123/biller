import csv
import os
import shutil
from shutil import copytree, rmtree
from time import time, ctime
import calendar
import time
import datetime 
import pandas as pd
import glob

#get the unique variable to defferentiate date
#date=input("enter date: yyyy-mm-dd: ")    
CurrentDate=datetime.date.today()  
days = datetime.timedelta(0)

new_date = CurrentDate - days
final_date= new_date.strftime('%Y-%m-%d')
#%d is for date  dd
#%m is for month  mm
#Y is for Year  yyyy
date=final_date
print(final_date)

#path1 is the path to the downloaded file
path1='C:/python_work/agent_billing/source/enrollmentReports.csv'
#path2 is the config/list of all agent in the billing week
path2='C:/python_work/agent_billing/App/agents.txt'
#open the agent list and convert to a python list
with open(path2, 'r') as file_object:
    linesq=file_object.read()
    #convert the content of the agent file into list using split('\n')
    contents2=linesq.split('\n')
    print(contents2)
    #loop though the list of Agents and then create directory for each Agent
    for agent in contents2[:]:
        # Directory
        directory = agent

        # Parent Directory path
        parent_dir = "C:/python_work/agent_billing/AGENT_SPLIT/"
        # Path
        path = os.path.join(parent_dir, directory)

        # Create the directory for each agent
        os.mkdir(path)
        print(f"Directory {agent} created")
        continue
#create a function that will split the downloaded source file into files per Agent
def agents(path1, agent_name):
    try:
        with open(path1, 'r') as file_object:
            lines=file_object.read()
        #print(lines)
    except:
        print(f"The source file does not exist in the location")

    else:
        contents1=lines.split('\n')
        #Open the a file per Agent
        textfile = open(f"{parent_dir}{agent_name}/{agent_name}_week_ending_{final_date}.txt", "a")
        #write the column header for the Agent file per Agent
        textfile.write('TICKET NUMBER,BVN,AGT MGT INST NAME,AGT MGT INST CODE,AGENT NAME,AGENT CODE,ENROLLER CODE,LATITUDE,LONGITUDE,FINGER PRINT SCANNER,BMS TICKET ID,VALIDATION STATUS,VALIDATION MESSAGE,AMOUNT,CAPTURE DATE,SYNC DATE,VALIDATION DATE\n')
        #loop through the source file and search for each agent and write their details in the source file to
        #their individual text file in their respective folders
        for line in contents1[:]:
    
            search=agent_name
            if search in line:
                
                textfile.write(line + "\n")
                continue
            #textfile.close()


#loop through the Agents in in the config and call the funtion that will do the spliting
for agent in contents2[:]:
    agents(path1, agent)
    print(f"Main file splited to {agent}'s  Directory")
        
# Loop through the Agents config again to read each slpited files per agent and determining what to pay each
import os
with open(path2, 'r') as file_object:
    linesq=file_object.read()

    contents2=linesq.split('\n')

    for agent in contents2[:]:
    # Get the directory path
        path_split = f"C:/python_work/agent_billing/AGENT_SPLIT/{agent}/"

        # Use the listdir() function to get a list of the files and directories in the directory
        files_and_directories = os.listdir(path_split)

        # Create a list of the full paths for each Agent file and directory
        full_paths = [os.path.join(path_split, f) for f in files_and_directories]
        final_full_paths=full_paths.pop()
        # Print the list of full paths
        print(final_full_paths)
        
        
        # Read the each agent splitted file into a dataframe
        df = pd.read_csv(f'{final_full_paths}',encoding='utf-8')
        #group each file by Agent code and count the enrolment per Agent
        group_agent=df.groupby('AGENT CODE').count()
        #determine the columns i want to return from the each agent's billing fine
        df = df.loc[:, ['AGT MGT INST NAME','AGENT CODE']]
        #count the enrolment per agent and add the count to a column in the dataframe
        counts = df.groupby('AGENT CODE').size().reset_index(name='count')
        #actuall 
        df = df.merge(counts, on='AGENT CODE')
        
        #df.to_csv(f'{path}/{agent}.csv',index=False)
        df = df.drop_duplicates()
        #an empty list to store the actual ammount to be paid to each agent
        pay=[]
        #loop through the newly created count column and use it to determinine what is due each Agent
        for value in df['count']:
            #print(value)
            #Determine pay if enrolment count<=30
            if value<=30:
                final_amount=value*100
                pay.append(final_amount)
            #Determine pay if enrolment count<=60    
            elif value<=60:
                final_amount=value-30
                final_amount1=final_amount*125
                final_amount2=30*100
                final_amount=final_amount1+final_amount2
                pay.append(final_amount)
                
            #Determine pay if enrolment count<=90    
            elif value<=90:
                cumulative_pay=[]
                final_amount_origin=30*100
                cumulative_pay.append(final_amount_origin) 
                final_amount1=30*125
                cumulative_pay.append(final_amount1) 
                final_amount=value-60
                #cumulative_pay=[]
                if final_amount<=30:
                    final_amount4=final_amount*150
                    cumulative_pay.append(final_amount4)
                    
                final_amounts=sum(cumulative_pay)
                pay.append(final_amounts)
                #df['Actual_Pay']=pay
            elif value<=120:
                cumulative_pay=[]
                final_amount_origin=30*100
                cumulative_pay.append(final_amount_origin) 
                final_amount1=30*125
                cumulative_pay.append(final_amount1) 
                final_amount2=30*150
                cumulative_pay.append(final_amount2) 
                final_amount=value-90
                #cumulative_pay=[]
                if final_amount<=30:
                    
                    final_amount4=final_amount*175
                    cumulative_pay.append(final_amount4)
                    
                final_amounts=sum(cumulative_pay)
                pay.append(final_amounts)
                #df['Actual_Pay']=pay 
            elif value>=121:
                cumulative_pay=[]
                final_amount_origin=30*100
                cumulative_pay.append(final_amount_origin) 
                final_amount1=30*125
                cumulative_pay.append(final_amount1) 
                final_amount2=30*150
                cumulative_pay.append(final_amount2) 
                final_amount3=30*175
                cumulative_pay.append(final_amount3)
                final_amount=value-120
                #cumulative_pay=[]
                if final_amount>=1:
                    
                    final_amount4=final_amount*200
                    cumulative_pay.append(final_amount4)
                    
                final_amounts=sum(cumulative_pay)
                pay.append(final_amounts)
                #df['Actual_Pay']=pay
                #print(pay)
        #Add another column to the Agent billing report to the Actual Pay per Agent
        df['Actual_Pay']=pay
        print(df)
                
        #generate a csv file per agent with the payment summary by looping throuth the each Agent's   file     
        full_paths = [os.path.join(path_split, f) for f in files_and_directories] 
        for pato in full_paths:
            #convert the dataframe per agent to CSV       
            df.to_csv(f'{pato}.csv',index=False)
            #make a copy of the csv to the Agent billing folder
            pat=f"C:/python_work/agent_billing/"
            shutil.copy2(f"{pato}.csv",pat)
            #df.to_csv(f'{pat}.csv',index=False)

#make a list of all csv files and store in filenames using glob() method
filenames = glob.glob('*.csv')
df_list = []
#loop through all the csv file and append them to a list
for filename in filenames:
    df = pd.read_csv(filename)
    df_list.append(df)
#merge all the content of te csv into one single csv for admin use by using the concat() fuction and store output in combined_bill_{final_date}.csv
df = pd.concat(df_list)
df.to_csv(f'combined_bill_{final_date}.csv', index=False)
