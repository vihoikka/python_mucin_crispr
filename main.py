import random
import sys, os
import pandas as pd
import copy

from time import sleep

timesteps = 100
reps = 10
n = 100
maxPopulation = 1000
bacs = []
deadBacs = []

#global variables
globalEnergyReserve = float(100)

initialEnergy = 1000
globalEnergyConsumption = 2 #how much energy each cell consumes per time step
globalEnergyReplenish = 100

globalProbabilityOfReplication = 0.3

globalInfectionThreshold = 0.01 #the probability of becoming infected per time step
globalDeathThreshold = 0.5 #the probability of dying when infected

globalSpacerOdds = 0.5 #probability of obtaining spacer
globalCRISPREffect = 0.1 #multiplier to the probability of dying when cell has spacer

globalRoughTransform = 0.1 #probability of becoming rough

globalMucinModeProbability = 0.1 #probability of entering mucin mode per timestep (roughs can't enter mucin mode)
globalMucinMultiplier = 1.1 #multiplier to replication probability when in mucin mode
agelimit = 4 #what age the bacterium dies

# Disable printing function
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Restore printing function
def enablePrint():
    sys.stdout = sys.__stdout__


class Bacterium:
    """A single bacterium"""

    def __init__(self):
        self.hasSpacer = False
        self.morphotype = "Rhizoid"
        self.virulent = True
        self.crisprEffect = 1 #initially, no spacers
        self.resistant = False
        self.age = 0
        self.probabilityOfReplication = globalProbabilityOfReplication #probability of creating daughter cells per time step
        self.mucinMode = False
        self.mucinMultiplier = 1
        self.energy = initialEnergy

#why don't the young replicate

def getsInfected(bac, threshold):
    if not b.resistant:
        infOdd = random.uniform(0,1)
        if infOdd < globalInfectionThreshold:
            print("Bacterium infected")
            return True
        else:
            print("Bacterium survives")
            return False
    else:
        return False

def deathTest(b, globaldeathOdd):
    randomNumber = random.uniform(0,1)
    deathOdds = globaldeathOdd * bac.crisprEffect #a spacer lowers the odds of dying
    if randomNumber < deathOdds:
        print("Bacterium died")
        return True
    else:
        print("Bacterium survived")
        return False

def probTest(odds, type): #a common probability tester for anything 0-1
    randomNumber = random.uniform(0,1)
    if randomNumber < odds:
        print(str(type) + " positive")
        return True
    else:
        print(str(type) + " negative")
        return False

def morphotypeChangeTest(b, roughProb):
    randomNumber = random.uniform(0,1)
    if randomNumber < roughProb:
        print("Becoming rough")
        return True
    else:
        return False

def spacerTest(b, odds):
    randomNumber = random.uniform(0,1)
    if randomNumber < odds:
        print("New spacer acquired")
        return True
    else:
        return False

def mucinModeTest(b, mucinProb):
    randomNumber = random.uniform(0,1)
    if randomNumber < mucinProb:
        print("Entering mucin mode")
        return True
    else:
        return False

def duplicateCell(bac):
    newbac = copy.copy(bac)
    newbac.age = 0
    #print("New morphotype: " + str(newbac.morphotype))
    #print("Old morphotype: " + str(bac.morphotype))
    #print(newbac)
    #print(bac)
    # newBac.resistant = bac.resistant
    # newBac.morphotype = bac.resistant
    # newBac.crisprEffect = bac.crisprEffect
    # newBac.hasSpacer = bac.hasSpacer
    # newBac.virulent = bac.virulent
    return newbac
def getRoughs(livingbacs):
    roughs = 0
    for i in livingbacs:
        if i.morphotype == "Rough":
            roughs += 1
    if len(livingbacs) > 0:
        fraction = roughs / len(livingbacs)
        return fraction
    else:
        return 0
def getSpacered(livingbacs):
    spacered = 0
    for i in livingbacs:
        if i.hasSpacer == True:
            spacered += 1
    if len(livingbacs) > 0:
        fraction = spacered / len(livingbacs)
        return fraction
    else:
        return 0
def getVirulents(livingbacs):
    virulents = 0
    for i in livingbacs:
        if i.virulent == True:
            virulents += 1
    if len(livingbacs) > 0:
        fraction = virulents / len(livingbacs)
        return fraction
    else:
        return 0
def getResistants(livingbacs):
    resistants = 0
    for i in livingbacs:
        if i.resistant == True:
            resistants += 1
    if len(livingbacs) > 0:
        fraction = resistants / len(livingbacs)
        return fraction
    else:
        return 0
def getMucinModed(livingbacs):
    mucin = 0
    for i in livingbacs:
        if i.mucinMode == True:
            mucin += 1
    if len(livingbacs) > 0:
        fraction = mucin / len(livingbacs)
        return fraction
    else:
        return 0

filename = "crispr_sim.csv"

#create bacteria and store them in list
for i in range(n):
    bac = Bacterium()
    bacs.append(bac)
print("Created " + str(n) + " bacteria")

events = []
eventsDf = pd.DataFrame(events, columns = ['replicate', 'time', 'living', 'dead', "rough", "spacer", "resistants", "virulent", "mucin_mode", "global_energy_reserves"])
repcounter = 0

for r in range(reps):
    counter = 0
    bacs = []
    deadBacs = []
    nextTimestepBacs = []
    for i in range(n): #Create new set of bacteria
        bac = Bacterium()
        bacs.append(bac)
    print("Starting pop size " + str(len(bacs)))
    for i in range(timesteps):
        blockPrint()
        print("Timestep " + str(i) + " pop size: " + str(len(bacs)))
        nextTimestepBacs = []
        for b in bacs:
            b.energy -= globalEnergyConsumption #living consumes energy
            if (b.age < agelimit) & (globalEnergyReserve > 0): #if bacterium is not too old and there is energy left
                print("Age " + str(b.age) + ", spacer: " + str(b.hasSpacer) + ", morphotype: " + str(b.morphotype))
                infected = getsInfected(b, globalInfectionThreshold) #does the bacterium become infected?
                print("Infection status: " + str(infected))
                if infected: #if so...
                    dead = deathTest(b, globalDeathThreshold) #... does it die?
                    print("Death status: " + str(dead))
                    if not dead & b.hasSpacer: #... if not, does it get a spacer (if does not already have one)?
                        newSpacer = spacerTest(b, globalSpacerOdds)
                        print("Spacer status: " + str(newSpacer))
                        if newSpacer: #if new spacer was acquired
                            b.hasSpacer = True #make it true
                            b.crisprEffect = globalCRISPREffect #modify the crispr effector
                    if dead: #if the bacterium died
                        deadBacs.append(b) #... add it to dead list
                        break #terminate this bacterium loop (bacterium is not added to nextTimestepBacs list)
                if probTest(globalRoughTransform, "Morphotype change"): #test for morphotype change
                    b.resistant = True #.. make it permanently resistant
                    b.virulent = False #and nonvirulent
                    b.morphotype = "Rough" #and rough
                    b.mucinMode = False #and non-mucinmode

                if probTest(globalMucinModeProbability, "Mucin-mode") & (b.morphotype != "Rough") & (b.mucinMode == False): #becometh mucin-moded
                    #enablePrint()
                    print("Somebody got mucined")
                    blockPrint()
                    #sleep(1)
                    b.mucinMode = True
                    b.mucinMultiplier = globalMucinMultiplier

                if probTest(b.probabilityOfReplication*b.mucinMultiplier, "Replication"): #if cell is infectious and crosses threshold. Mucin-moded get higher probability
                   # enablePrint()
                    newBac = duplicateCell(b) #duplicate cell
                    print(newBac.morphotype)
                    print(newBac.age)
                    print(b.age)
                    nextTimestepBacs.append(newBac) #and add daughter cell to living cells list
                globalEnergyReserve -= 1
                b.energy += 1
                b.age += 1
                nextTimestepBacs.append(b)
            else:
                deadBacs.append(b)
                #sleep(0.05)
       # eventsDf.loc[i] = str(i) + str(len(bacs)) + str(len(deadBacs)) + str(getRoughs(bacs)) + str(getSpacered(bacs)) + str(getResistants(bacs)) + str(getVirulents(bacs))
        enablePrint()
        counter += 1
        globalEnergyReserve += globalEnergyReplenish
        bacs = []
        bacs = copy.copy(nextTimestepBacs)
        newRow = {"replicate": str(r),
                  "time": str(i),
                  "living": str(len(bacs)),
                  "dead": str(len(deadBacs)),
                  "rough": str(getRoughs(bacs)),
                  "spacer": str(getSpacered(bacs)),
                  "resistants": str(getResistants(bacs)),
                  "virulent": str(getVirulents(bacs)),
                  "mucin_mode": str(getMucinModed(bacs)),
                  "global_energy_reserves": str(globalEnergyReserve)}
        eventsDf = eventsDf.append(newRow, ignore_index=True)
    repcounter += 1
    enablePrint()

    print("Finished round " + str(repcounter))
    print("Population size " + str(len(bacs)))

print("Size of live cells: " + str(len(bacs)))
print("Size of dead cells " + str(len(deadBacs)))

eventsDf.to_csv(filename, index=True, sep = ',', header = True)