'''
Final Project (Python)
Gregory White - J00527454
Due Date: 7/31/20
'''

# import the sqlite3 database
import sqlite3

# global variables
num_males = 0
num_females = 0
female_total_height = 0.0
male_total_height = 0.0
female_total_weight = 0.0
male_total_weight = 0.0
female_total_BMI = 0.0
male_total_BMI = 0.0
female_total_CPA = 0.0
male_total_CPA = 0.0

# function to convert metric kilograms to english pounds
def kgToPounds(kg):
    pounds = kg * 2.20462
    return pounds


# function to convert centimeters to inches
def cmToInches(cm):
    inches = cm * 0.393701
    return inches


# function to calculate and return the BMI (Body Mass Index)
def getBMI(heightCm, weightKg):
    bmi = weightKg / (heightCm * heightCm / 10000)
    return bmi


# function to calculate and return the CPA
def getCPA(ChestDiam, ChestDepth, BitroDiam, wristGirth, AnkleGirth, heightInCm):
    cpa = -110 + (1.34 * ChestDiam) + (1.54 * ChestDepth) + (1.2 * BitroDiam) + \
          (1.11 * wristGirth) + (1.15 * AnkleGirth) + (0.177 * heightInCm)

    return cpa


def updateTotals(wt, ht, gnd, chDia, chDept, bitDia, wriGirt, ankGirt):
    global num_males
    global num_females
    global female_total_height
    global male_total_height
    global female_total_weight
    global male_total_weight
    global female_total_BMI
    global male_total_BMI
    global female_total_CPA
    global male_total_CPA

    if gnd == 0:  # female
        num_females += 1
        female_total_height += ht
        female_total_weight += wt
        female_total_BMI += getBMI(ht, wt)
        female_total_CPA += getCPA(chDia, chDept, bitDia, wriGirt, ankGirt, ht)
    else:
        num_males += 1
        male_total_height += ht
        male_total_weight += wt
        male_total_BMI += getBMI(ht, wt)
        male_total_CPA += getCPA(chDia, chDept, bitDia, wriGirt, ankGirt, ht)

    return


def printOne(num, wt, ht, gend, chDiam, chDep, bitDia, wristGirt, ankGirt):
    # Respondent info
    print("Respondent #:", end="")
    print(num)
    print("Weight: {:.2f}".format(kgToPounds(wt)))
    print("Height: {:.2f}".format(cmToInches(ht)))
    print("Sex: ", end="")
    if gend == 0:
        print("Female")
    else:
        print("Male")
    print("BMI: {:.2f}".format(getBMI(ht, wt)))
    print("CPA: {:.2f}".format(getCPA(chDiam, chDep, bitDia, wristGirt, ankGirt, ht)))
    print("----------")


def printAverages():
    # Averages
    print('\033[1m' + 'Averages')  # the following two line of cold will Bold the word "Averages"
    print('\033[0m', end="")
    print("_________")

    print("Sex-->Females: {0} | Males: {1} | Total: {2}".format(num_females, num_males, num_females + num_males))
    if num_females == 0:
        newFVal = 0
    else:
        newFVal = cmToInches(female_total_height) / num_females
    if num_males == 0:
        newMVal = 0
    else:
        newMVal = cmToInches(male_total_height) / num_males

    totalTotal = cmToInches(female_total_height + male_total_height) / (num_females + num_males)

    print("Height-->Females: {:.2f} | Males: {:.2f} | Overall: {:.2f} (inches)".format(newFVal, newMVal, totalTotal))
    if num_females == 0:
        newFVal = 0
    else:
        newFVal = kgToPounds(female_total_weight) / num_females
    if num_males == 0:
        newMVal = 0
    else:
        newMVal = kgToPounds(male_total_weight) / num_males
    totalTotal = kgToPounds(female_total_weight + male_total_weight) / (num_females + num_males)
    print("Weight-->Females: {:.2f} | Males: {:.2f} | Overall: {:.2f} (lbs.)".format(newFVal, newMVal, totalTotal))
    if num_females == 0:
        newFVal = 0
    else:
        newFVal = female_total_BMI / num_females
    if num_males == 0:
        newMVal = 0
    else:
        newMVal = male_total_BMI / num_males
    totalTotal = (female_total_BMI + male_total_BMI) / (num_females + num_males)
    print('BMI-->Females: {:.2f} | Males: {:.2f} | Overall: {:.2f}'.format(newFVal, newMVal, totalTotal))
    if num_females == 0:
        newFVal = 0
    else:
        newFVal = female_total_CPA / num_females
    if num_males == 0:
        newMVal = 0
    else:
        newMVal = male_total_CPA / num_males
    totalTotal = (female_total_CPA + male_total_CPA) / (num_females + num_males)
    print("CPA-->Females: {:.2f} | Males: {:.2f} | Overall: {:.2f}".format(newFVal, newMVal, totalTotal))
    return




# main
sqliteConnection = ''
cursor = ''


try:
    sqliteConnection = sqlite3.connect('datafile.db')
    cursor = sqliteConnection.cursor()

    sqlite_select_Query = "SELECT * FROM dimensions;"
    cursor.execute(sqlite_select_Query)
    rows = cursor.fetchall()
    i = 1
    for row in rows:
        weightInKg = row[22]
        heightInCm = row[23]
        gender = row[24]
        ChestDiam = row[4]
        ChestDepth = row[3]
        BitroDiam = row[2]
        wristGirth = row[6]
        AnkleGirth = row[8]
        # print info for this person
        printOne(i, weightInKg, heightInCm, gender, ChestDiam, ChestDepth, BitroDiam, wristGirth, AnkleGirth)

        # add their info to the totals
        updateTotals(weightInKg, heightInCm, gender, ChestDiam, ChestDepth, BitroDiam, wristGirth, AnkleGirth)

        i += 1

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        cursor.close()
        sqliteConnection.close()
        #  print("The SQLite connection is closed")


printAverages()
