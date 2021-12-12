from __future__ import division
from django.shortcuts import render

###############################################
###############################################
# main arrays
array = []

###############################################
###############################################
# read raw date from a file


def read(file):
    Instances = []
    fp = open(file, 'r')
    for line in fp:
        line = line.strip('\n')
        if line != '':
            Instances.append(line.split(','))
    fp.close()
    return(Instances)

###############################################
###############################################
#  Split the 7 attributes into [key, attr]


def split(content, i):
    abalone_data = []
    for r in content:
        abalone_data.append([r[i+1], r[0]])
    return(abalone_data)

###############################################
###############################################
# Count the number of the same record


def count(abalone_data):
    counted_data = []
    abalone_data.sort(key=lambda abalone_data: abalone_data[0])
    i = 0
    while(i < len(abalone_data)):
        # count the number of the same record
        times = abalone_data.count(abalone_data[i])
        record = abalone_data[i][:]
        # append the number of the same record to the record
        record.append(times)
        counted_data.append(record)
        i += times  # count the next different item
    return(counted_data)

###############################################
###############################################
# Build a structure that ChiMerge algorithm works properly on it


def build(counted_data):
    length_dic = {}
    for record in counted_data:
        if record[0] not in length_dic.keys():
            length_dic[record[0]] = [0, 0, 0]
        if record[1] == 'F':
            length_dic[record[0]][0] = record[2]
        elif record[1] == 'M':
            length_dic[record[0]][1] = record[2]
        elif record[1] == 'I':
            length_dic[record[0]][2] = record[2]
        else:
            raise TypeError("Data Exception")
    length_dic = sorted(length_dic.items())
    return(length_dic)

###############################################
###############################################
#  Order data and make every value is in a separate interval


def Initialize(content, i):
    abalone_data = split(content, i)
    counted_data = count(abalone_data)
    length_dic = build(counted_data)
    return(length_dic)

###############################################
###############################################
# Compute the Chi-Square value


def chi2(intervals):
    m = len(intervals)
    num_class = len(intervals[0])
    # sum of each row
    Rows = []
    for i in range(m):
        sum = 0
        for j in range(num_class):
            sum += intervals[i][j]
        Rows.append(sum)
    # sum of each column
    Cols = []
    for j in range(num_class):
        sum = 0
        for i in range(m):
            sum += intervals[i][j]
        Cols.append(sum)
    # total number in the intervals
    N = 0
    for i in Cols:
        N += i

    chi_value = 0
    for i in range(m):
        for j in range(num_class):
            Estimate = Rows[i]*Cols[j]/N
            if Estimate != 0:
                chi_value = chi_value+(intervals[i][j]-Estimate)**2/Estimate
    return chi_value

###############################################
###############################################
#  ChiMerge algorithm


def ChiMerge(length_dic, max_interval):

    num_interval = len(length_dic)
    ceil = max(record[0] for record in length_dic)
    while(num_interval > max_interval):
        num_pair = num_interval-1
        chi_values = []
        # calculate the chi value of each neighbor interval
        for i in range(num_pair):
            intervals = [length_dic[i][1], length_dic[i+1][1]]
            chi_values.append(chi2(intervals))
        # get the minimum chi value
        min_chi = min(chi_values)
        # treat from the last one, because I change the bigger interval as 'Merged'
        for i in range(num_pair-1, -1, -1):
            if chi_values[i] == min_chi:
                # combine the two adjacent intervals
                temp = length_dic[i][:]
                for j in range(len(length_dic[i+1])):
                    temp[1][j] += length_dic[i+1][1][j]

                length_dic[i] = temp
                length_dic[i+1] = 'Merged'
        while('Merged' in length_dic):  # remove the merged record
            length_dic.remove('Merged')
        num_interval = len(length_dic)

    split_points = []
    for record in length_dic:
        split_points.append(record[0])

    return(split_points)


###############################################
###############################################
# ChiMerge discrimination of the abalone plants database


def discrete(path):
    content = read(path)

    max_interval = 6
    num_attr = 7
    attrlist = ['Length',
                'Diameter',
                'Height',
                'Whole_weight',
                'Shucked_weight',
                'Viscera_weight',
                'Shell_weight']
    for i in range(num_attr):
        # print('\n'+attrlist[i])
        length_dic = Initialize(content, i)  # Order and Initialize
        # discretion data using ChiMerge algorithm
        split_points = ChiMerge(length_dic, max_interval)
        array.append([attrlist[i], split_points])


discrete('/home/user/Desktop/mobina/uni/tu-01/machine learning/hw/hw3/chiMerge/chiMerge/static/abalone.data')


# Attribute Information:

#    Given is the attribute name, attribute type, the measurement unit and a
#    brief description.  The number of rings is the value to predict: either
#    as a continuous value or as a classification problem.

# 	Name		    Data Type	Meas.	Description
# 	----		    ---------	-----	-----------
# 	Sex		        nominal			    M, F, and I (infant)
# 	Length		    continuous	mm	    Longest shell measurement
# 	Diameter	    continuous	mm	    perpendicular to length
# 	Height		    continuous	mm	    with meat in shell
# 	Whole weight	continuous	grams	whole abalone
# 	Shucked weight	continuous	grams	weight of meat
# 	Viscera weight	continuous	grams	gut weight (after bleeding)
# 	Shell weight	continuous	grams	after being dried
# 	Rings		    integer			    +1.5 gives the age in years

#    Statistics for numeric domains:

# 		    Length	Diam	Height	Whole	Shucked	Viscera	Shell	Rings
# 	Min	    0.075	0.055	0.000	0.002	0.001	0.001	0.002	    1
# 	Max	    0.815	0.650	1.130	2.826	1.488	0.760	1.005	   29
# 	Mean	0.524	0.408	0.140	0.829	0.359	0.181	0.239	9.934
# 	SD	    0.120	0.099	0.042	0.490	0.222	0.110	0.139	3.224
# 	Correl	0.557	0.575	0.557	0.540	0.421	0.504	0.628	  1.0


############################################################################################

# view on http://127.0.0.1:8000/


def home(request):
    return render(request, 'home.html', {"array": array})
