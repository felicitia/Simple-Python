import csv
import os
import glob

rootdir='E:\\XTEAM\\HW2_XTEAM_package\\distribution_package\\XTEAM_scaffold_code\\XTEAM_scaffold-size50\\XTEAM_scaffold\\XTEAM_Simulation'

def csvFinder(dir):
    csvlist = glob.glob(os.path.join(dir, '*.csv'))
    return csvlist

def calEnergy(filename):
    total = 0
    count = 0
    flag = False
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if flag == True:    
                total = total + float(row[1])
                count = count + 1
                lastrow = row
                if count == 1:
                    firstrow = row
            else:
                flag = True
        f.close()
    avg = total/(float(lastrow[0]) - float(firstrow[0]))
    return total,avg

def calMemory(filename):
    total = 0
    count = 0
    flag = False
    max = 0
    lasttime = 0
    mem = 0
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if flag == True:
                cell = float(row[1])
                total = total + cell
                count = count + 1
                lastrow = row
                if count == 1:
                    firstrow = row
                    lasttime = row[0]
                    mem = float(row[1])
                else:
                    if row[0] == lasttime:
                        #print 'aaa',row
                        count = count - 1
                        mem = mem + cell
                    else:
                        if max < mem:
                            max = mem
                        mem = float(row[1])
                    lasttime = row[0]
            else:
                flag = True
        f.close()
    avg = total/count
#    print 'total',total
#    print 'count',count
    return max,avg

def calLatency(filename):
    total = 0
    count = 0
    flag = False
    max = 0
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if flag == True:
                if row[2] == '-':
                    break
                cell = float(row[2])    
                total = total + cell
                count = count + 1
                lastrow = row
                if max < cell:
                    max = cell
                if count == 1:
                    firstrow = row
            else:
                flag = True
        f.close()
    avg = total/count
    return max,avg

    
filelist = csvFinder(rootdir)
with open('output.csv', 'wb') as writerfile:
    writer = csv.writer(writerfile)

    for file in filelist :
        filename = rootdir + '\\' + os.path.basename(file)
        if str(filename).endswith('Energy_Log.csv'):
            print '#energy#', filename
            total,avg = calEnergy(filename)
            print 'total=', total
            print 'avg=', avg
            writer.writerow((total,))
            #writer.writerow((avg,))
     
        elif str(filename).endswith('Memory_Log.csv'):
            print '#memory#', filename
            max,avg = calMemory(filename)
            print 'max=', max
            print 'avg=', avg
            writer.writerow((max,))
            writer.writerow((avg,))
            
        else:
            print '#latency#', filename
            max,avg = calLatency(filename)
            print 'max=', max
            print 'avg=', avg
            writer.writerow((max,))
            writer.writerow((avg,))
    writerfile.close()
     