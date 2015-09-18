'''
Created on Aug 12, 2015

@author: Pavel Mamaev

This script will look attempt to do the following

1.  It will look in the specific folder for a CSV file named "Fan...." and will load only 3 fieldsinto an internal list.
    A.  Combined filed Third and Fourth Column from the CSV (First Name + Last Name)
    B.  Fanduel points this player scored so far, fifth column of the CSV
    C.  Fanduel prices for that player for this week
  
    
2.  It will then look for specific CVS file named "DKS...", the program will then pick specific columns from this file and the internal list from #1 and write it to a new file
    A.  First and Last Name of the player - will only write it if it's find a corresponding name from FanDuel Data
    B.  dddggg

'''
from _ssl import err_codes_to_names
from collections import defaultdict

if __name__ == '__main__':
    import csv
    import os
    import copy
    import shutil
    
    # Change this Varible to the Number you'd like to Control for
    varNumber = '8'
    Bands = ["Micro 0-13K","HV1 120K-500K","HV2 500K-1M","HV3 1M-MAX","Large 52K-120K", "Medium 26K-52K", "Small 13K-26K" ]
    #Defenses = ['Miami','Baltimore','St Louis','Seattle','Carolina','Arizona','Houston','Tennessee','Cleveland','Cincinnati','New Orleans','Green Bay','Indianapolis','Buffalo','Minnesota','Kansas City','Philadelphia','New York','San Francisco','San Diego','New England','Detroit','Pittsburgh','Oakland','Denver','Dallas','Washington','Jacksonville','Atlanta','New York','Tampa Bay','Chicago']
    NotPlaying = ['Dez Bryant','Geno Smith','Charlie Whitehurst','Landry Jones','Stephen Morris','Trevor Siemian','Taylor Heinicke','Tyler Clutts','Jerome Felton','Marcus Thigpen','Marlon Moore','Will Johnson']
    FanDuelData = []

    
    # Going through the main file the first time to get the unique value bands
    path= r"C:\Users\MamaevP\Desktop\Fantasy\Daily Salaries\CSVs"
    
    dirs = os.listdir(path)
    os.chdir(path)
    
    #First, lets make a copy of the original file and save it as .TXT 
    #for file in dirs:
    #    #if file[len(file)-3:len(file)]=='csv':
    #    if file[0:3]=='DKS': 
    #        shutil.copyfile(file, file[0:len(file)-4]+ "_Original.txt")

    # go through the FanDuel file and capture the data into a twodimentionalarray    
    for file in dirs:
        if file[len(file)-3:len(file)]=='csv':
            if file[0:3] == 'Fan':
                with open(file) as first_file:
                    DataCaptured = csv.reader(first_file)
                    #Skipping the header for Bands
                    next(DataCaptured,None)
                    for row in DataCaptured:
                        if row[1] =='D':
                            s = row[3]
                            # Don thing for Defenses now
                        else:
                            name = row[2]+' '+row[3]
                            points = row[4]
                            price = row[6]
                            name.strip()
                            points.strip()
                            price.strip()
                            FanDuelData.append((name,points,price))
                    first_file.close()
    #Bands.sort()
    
    #outFileName = copy.copy(Bands)
    #out_control = copy.copy(Bands)
    
      
    # Change the directory where your CVS are located
    dirs = os.listdir(path)
    os.chdir(path)

    #print path
    
    # first separate all the disabled users into a separate file
    for file in dirs:
        if file[len(file)-3:len(file)]=='csv':
            if file[0:3]=='DKS': 
                outPut = "Result.csv"
                outTemp = "Temp.csv"
                with open(file) as inp, open(outPut, "wb") as out_main, open(outTemp, "wb") as out_temp:
                    writerMain = csv.writer(out_main)
                    writerTemp = csv.writer(out_temp)
                    reader = csv.reader(inp)
                    headers = next(reader,None)
                    if headers:
                        #writerTemp.writerow(headers)
                        # headers.insert(0,'Name ID')
                        writerMain.writerow(('Name','POS','DK Pts','DK Price','FD Points', 'FD Price', 'DK/FD Pts%', 'DK/FD Price %'))
                    for row in reader:
                        # Skip DEFENSES for Now and change some of the player's names since they are different in FanDule and DK
                        if row[0]<>'DST' and row[1] not in NotPlaying:
                            s = row[1]
                            if s=='Stevie Johnson':
                                s='Steve Johnson'
                            elif s=='Steve Smith Sr.':
                                s='Steve Smith'
                            elif s =='Chris Ivory':
                                s='Christopher Ivory'
                            elif s =='Duke Johnson Jr.':
                                s='Duke Johnson'
                            elif s=='Cecil Shorts III':
                                s='Cecil Shorts'
                            elif s=='EJ Manuel':
                                s='E.J. Manuel'
                            s.strip()
                            #Now lest find FanDuelData in the FanDuelData list of lists
                            for t in range(len(FanDuelData)):
                                if FanDuelData[t][0]==s:
                                    row.insert(0,s)
                                    writerMain.writerow((row[0],row[1],row[5],row[3],FanDuelData[t][1],FanDuelData[t][2]))
                                    break
                    try:
                        inp.close()
                        os.remove(file)
                    except IOError, e:
                        print "Problems deleting main file"
                        #print e
                        
                    try:
                        out_main.close()
                        out_temp.close()
                        os.rename(outTemp, file)
                        #change the extension of the disabled file
                        base = os.path.splitext(outPut)[0]
                        os.rename(outPut, base+ ".txt")
                    except:
                        print "Problems renaming file"

                
    dirs = os.listdir(path)
    os.chdir(path)
    
    # rename TXT to CVS
    for file in dirs:
        if file[len(file)-3:len(file)]=='txt':
            base = os.path.splitext(file)[0]
            os.rename(file, base+ ".csv")
            
    dirs = os.listdir(path)
    os.chdir(path)
            
    for file in dirs:
        with open(file) as inp:
            reader = csv.reader(inp)
            rows = list(reader)
            print len(rows), inp.name
            if len(rows)==1 or len(rows)==0:
                inp.close()
                os.remove(file)
                

            


    


                        
    

    

    
