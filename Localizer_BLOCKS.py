#python3
#coding:utf8
# Title: Localizer Task
# Author: Lindsay S. Shaffer


import csv
import random # for randomizing data structures
import time
import numpy as np
from psychopy import core, visual, event, gui, os, parallel, monitors  

#============================================================
#                            GUI                            #
#============================================================

# Prompt to get subject info
def getInfo():
    modeType = ["block", "full"]
    blockType = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

    # Create GUI elements to get subject arguments
    dlg = gui.Dlg(title= "Localizer Task")
    dlg.addField("Subject Number: ") # dlg 0
    dlg.addField("Mode: ", choices = modeType) # dlg 1
    dlg.addField("Block number: ", choices = blockType) # dlg 2
    dlg.show()
    return dlg

#============================================================
#                       GLOBAL CONSTANTS                    #
#============================================================


# define your monitor without PsychoPy's Monitor Center
my_monitor = monitors.Monitor(name='my_monitor_name')
my_monitor.setSizePix((1280, 800))
my_monitor.setWidth(20)
my_monitor.setDistance(100)
my_monitor.saveMon()
dlg = getInfo()
win = visual.Window(monitor = my_monitor, fullscr=True, color = 'grey')
win.mouseVisible = False
useTriggers = False
if useTriggers is True:
    port = parallel.ParallelPort(address='0x0378')
    print("EEG trigger active.")

#Designate the Window Information

# current wd
dir_path = os.path.dirname(os.path.realpath('__file__'))

# create dict of strings converted into bytes
# NOTE: if bytes doesn't work, try int(254) etc
triggerDict = {
           "eegStart": int(254),
           "eegEnd": int(255),
           "animal": int(10), 
           "automobile": int(11),
           "body_part" : int(12),
           "building": int(13),
           "furniture": int(14),
           "handheld_object": int(15),
           "plant": int(16),
           "category_choice": int(30),
           "resp_up": int(31),
           "resp_down": int(32),
           "resp_slow": int(33),
           "fix_ISI": int(50),
           "fix_ITI": int(51),
           "restStart": int(250),
           "restEnd": int(251)
           }

#============================================================
#                       SUBJECT CLASS                       #
#============================================================

class Subject:

    global dir_path

    # subject constructor with arguments 
    def __init__(self, subjID, modeType, blockType):
        self.id = subjID
        self.modeType = modeType
        self.subjectFileName = ""
        self.blockType = blockType

    # For debugging purposes
    def printSubject(self):
        print("Subject ID: " + self.id)
        print("Mode Type: " + self.modeType)
        if self.modetype == "block":
            print("Block number: " + self.blockType)


    def saveSubjectInfo(self):
        ''' Writing subject info to disk as a CSV file'''
       
        directory = os.path.join(dir_path, "Subject Data/")

        # Create an empty folder for subject if it doesn't exist.
        if (not os.path.exists(directory)):
            # create new foldr with said id
            os.mkdir(directory)

        # Create a file with the labels for the columns
       
        if self.modeType == "full":
            fileSubject = "LOC" + str(self.id) + "_" + str(self.modeType) + ".csv" # replaced Pre Post (sessionType) with modeTpe
        else:
            fileSubject = "LOC" + str(self.id) + "_" + str(self.modeType) + "_" + str(self.blockType) + ".csv"
            
        fileSubject = os.path.join(directory, fileSubject)
        self.subjectFileName = fileSubject # save file name for appending data later


        with open(fileSubject, 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter = ',', quotechar='|',
                    quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["blockNumber", "trialNumber",
                             "itiJitter", "stimulusPic", "isiJitter",
                             "responseUpChoice", "responseDownChoice",
                            "choiceKey", "choiceResponseTime"])

#============================================================
#                       TRIAL CLASS                         #
#============================================================
class Trial:
    """ Create the trial class. Constructs all components for a given trial. """

    def __init__(self, stimulus, blockNumber, responseChoice):
        """ Construct trial based on args"""
        self.stimulus = stimulus # stimPic
        self.blockNumber = blockNumber
        self.dataRow = [self.blockNumber]
        self.responseChoice = responseChoice
        self.trialNumber = -1  #self.trialNumber is used after in makeTrials()

    def eegTrigger(self, triggerType):
        """ Send trigger for EEG """
        if useTriggers is True:
            parallel.setPortAddress(port)
            port.setData(triggerType)
            print(triggerType)
            core.wait(0.1) #changed from 0.001 to 0.1 ms--nuShawn can't handle 0.001 ms
            port.setData(0)

    def doTrial(self):
        """ Sequence of functions to present and record a single trial"""
        self.dataRow.append(self.trialNumber)
        self.fixation_ITI() # cue the ITI bro
        self.stimuliPresent() # cue the pictures bro
        self.fixation_ISI() # cue the ISI bro
        self.selectCategory() # cue the response choices bro
        if (self.trialNumber != 0 and self.trialNumber % 21 == 0): # if trialNum is divisible by 21 and is not the first trial, cue break
                self.restSession()
                    
            
    def fixation_ITI(self):

        jitterITI = random.uniform(0.7, 1.5)
        cross = visual.TextStim(win = win, 
                                text = "+",
                                height = 0.25)
        cross.draw()
        win.flip()
        self.eegTrigger(triggerDict.get("fix_ITI")) 
        core.wait(jitterITI)
        self.dataRow.append(jitterITI) # record to itiJitter col  
                    
                    
    def stimuliPresent(self):
        """ Present different objects and record data """

        stimPic = visual.ImageStim(win = win, 
                                   image=dir_path + '/' + self.stimulus + '.png',
                                   name = 'stimulus',
                                   pos = (0, 0),
                                   units='deg',
                                   size = (2,2))
        
        #win.flip()
        self.eegTrigger(triggerDict[self.stimulus])
        stimPic.draw()
        win.flip()
        core.wait(1.0)
        self.dataRow.append(self.stimulus)

     
    def fixation_ISI(self):

        jitterISI = random.uniform(0.2, 0.4) # min: 200 ms, max: 400 ms
        cross = visual.TextStim(win = win, 
                                text = "+",
                                height = 0.25)

        self.eegTrigger(triggerDict.get("fix_ISI"))
        cross.draw()
        win.flip()
        core.wait(jitterISI)
        self.dataRow.append(jitterISI) #record to isitJitter col

        
    def selectCategory(self):
        responseKeysChoice = ['up', 'down']
        categories = ["animal", "automobile", "body part", "building", "furniture", "handheld object", "plant"]
        
        stimPicName = str(self.responseChoice)
        otherPicList = [x for x in categories if x != stimPicName]
        otherPicName = random.choice(otherPicList)

        responseChoiceList = [stimPicName, otherPicName]        
        responseChoiceList = np.random.permutation(responseChoiceList)

        responseUpChoice = responseChoiceList[0]
        responseDownChoice = responseChoiceList[1]

        self.dataRow.append(responseUpChoice)
        self.dataRow.append(responseDownChoice)

        response_Up = visual.TextStim(win=win, name='resp_up',
                                       text=responseUpChoice,
                                       font=u'Arial',
                                       pos=(0, 0.2), height=0.09, wrapWidth=None, ori=0, 
                                       color=u'white', colorSpace='rgb', opacity=1,
                                       depth=0.0)
                                        
        response_Down = visual.TextStim(win=win, name='resp_down',
                                        text=responseDownChoice,
                                        font=u'Arial',
                                        pos=(0, -0.2), height=0.09, wrapWidth=None, ori=0, 
                                        color=u'white', colorSpace='rgb', opacity=1,
                                        depth=0.0)
        
        # Dunno if we're adding this in? I forgot.
        #response_slow = visual.TextStim(win=win, name='resp_slow',
        #                                text=u'Too slow!',
        #                                font=u'Arial',
        #                                pos=(0, -0.2), height=0.09, wrapWidth=None, ori=0, 
        #                                color=u'white', colorSpace='rgb', opacity=1,
        #                                depth=0.0)
        
        cross = visual.TextStim(win = win, 
                                text = "+",
                                height = 0.25,
                                pos=(0,0))


        response_Up.draw()
        cross.draw()
        response_Down.draw()
        self.eegTrigger(triggerDict.get("category_choice")) # options are presented
        win.flip()
            
        # start timer
        startChoice = time.time()

        choiceKey = event.waitKeys(keyList=responseKeysChoice)

        if (choiceKey != None): # if a response HAS been made by the subject
            if (choiceKey[0] == "up"):
                    self.eegTrigger(triggerDict.get("resp_up"))
            elif (choiceKey[0] == "down"):
                    self.eegTrigger(triggerDict.get("resp_down"))
            else: # for debugging
                print("Error: This shouldn't happen.")

        
        choiceResponseTime = time.time() - startChoice 
        self.dataRow.append(choiceKey[0]) #report only item from responseKeyChoice because it's a list
        self.dataRow.append(choiceResponseTime)
        win.flip()

    def clickNext(self):
        
        responseKeyNext = ['space']
        clickPrompt = visual.TextStim(win = win,
                                      text = 'You may now continue the task by pressing the space bar.',
                                      font = 'Arial',
                                      pos = (0, 0),
                                      height = 0.1,
                                      color = 'white')
        clickPrompt.draw()
        win.flip()

        #startClick = time.time()
        clickKey = event.waitKeys(keyList=responseKeyNext)

        if(clickKey != None): # if a response HAS been made by the subject
            #win.callOnFlip(sendTrigger(triggerDict[trigName])) # then send trigger & get ready to win.flip
            # get response time for doors
            self.eegTrigger(triggerDict.get("restEnd"))
            win.flip()

    def restSession(self):        
        
        breakPrompt = visual.TextStim(win = win,
                                      text = 'Please take a 30 second break.\n\nThe space bar will appear when 30 seconds are up. You may press it to begin.\n\n Remember to relax your jaw, stay still, and not blink when you are completing the task.',
                                      font = 'Arial',
                                      pos = (0, 0),
                                      height = 0.1,
                                      color = 'white')
        breakPrompt.draw()
        win.flip()
        self.eegTrigger(triggerDict.get("restStart"))
        core.wait(30.0) # on 10 for debug
        self.clickNext()



#============================================================
#                       EXPERIMENT CLASS                    #
#============================================================

class Experiment:

    def __init__(self, subject, numberOfTrials, numberOfBlocks):

        """ Make the experiment """

        #build dictionary and create block groups for subject
        global triggerDict

        self.subject = subject
        self.numberOfTrials = numberOfTrials
        self.numberOfBlocks = numberOfBlocks
        #self.trialType = trialType
        self.trialBlocks = self.makeTrials()

    def introduction(self):
        #self.eegTrigger(triggerDict["eegStart"])
        intro = "Welcome. In this task, you will complete a task in which you should identify the category of the picture as accurately as possible. \n\n"
        intro = "For this task, you will first briefly see a cross and then see a series of images. Each image belongs to a category: animals, automobiles, body parts, buildings, furniture, handheld objects, or plants. \n\n"
        intro += "\n\nAfter you see each image, you will briefly see a cross sign and then you will either use the up arrow key or the down arrow key to select which category the image belongs to." 
        intro += "Ocassionally, you might be prompted to take a break. Please make sure to use your breaks well since its really important to stay still for each trial. \n\n"
        intro += "Remember to not blink during each trial, stay as still yet relaxed as possible, and keep your eyes on the center of the screen where the cross is located. When you see the screen that prompts you to take a break, use this opportunity to move around, stretch, and blink your eyes."    
        intro += "As soon as the experimenter closes the door shut, please press the space bar to begin."
        
        showText(intro, keys = ["space"], height=0.05)

    def makeTrials(self):

        trialBlocks = []
        numCategories = 7

        trialsPerBlock = int(self.numberOfTrials/self.numberOfBlocks) # 210/10 = 21
        numberOfAnimalTrials = trialsPerBlock/int(numCategories) # self.trialType[0] = 1st entry in trialType
        numberOfAutomobileTrials = trialsPerBlock/int(numCategories) + numberOfAnimalTrials
        numberOfBodyPartTrials = trialsPerBlock/int(numCategories) + numberOfAutomobileTrials - 1 # lol janky fix
        numberOfBuildingTrials = trialsPerBlock/int(numCategories) + numberOfBodyPartTrials
        numberOfFurnitureTrials = trialsPerBlock/int(numCategories) + numberOfBuildingTrials
        numberOfHandheldTrials = trialsPerBlock/int(numCategories) + numberOfFurnitureTrials
        numberOfPlantTrials = trialsPerBlock/int(numCategories) + numberOfHandheldTrials
        
        #print("plant trials: " + str(numberOfPlantTrials))
        #print(numberOfAutomobileTrials)

        # Make blocks
        trialNum = 0 # counter

        for blockNumber in range(self.numberOfBlocks): 
            # Make trials
            block = [] # a block has a list of trials
            for trialNumber in range(trialsPerBlock):
                if trialNumber < numberOfAnimalTrials: 
                    trial = Trial("animal", blockNumber, "animal") #having blockNumber pass through here records it in dataRow
                elif trialNumber < numberOfAutomobileTrials:
                    trial = Trial("automobile", blockNumber, "automobile")
                elif trialNumber <= numberOfBodyPartTrials:
                    trial = Trial("body_part", blockNumber, "body part")
                elif trialNumber <= numberOfBuildingTrials:
                    trial = Trial("building", blockNumber, "building")
                elif trialNumber <= numberOfFurnitureTrials:
                    trial = Trial("furniture", blockNumber, "furniture")
                elif trialNumber <= numberOfHandheldTrials:
                    trial = Trial("handheld_object", blockNumber, "handheld object")
                elif trialNumber <= numberOfPlantTrials:
                    trial = Trial("plant", blockNumber, "plant")
                block.append(trial)
            random.shuffle(block)
            trialBlocks.append(block)
            for trial in block: # iterate over trials in a given block
                trial.trialNumber = trialNum # create a new member variable called trialNumber
                trialNum += 1 # add 1 to trialNumber so that trials are ordered

        return trialBlocks


    def doTrials(self):
        #function for trials
        for block in self.trialBlocks:
            for trial in block:
                trial.doTrial()
                self.saveData(trial.dataRow)

    def saveData(self, dataRow):
        """ Write data to disk as a row"""

        fileName = self.subject.subjectFileName
        with open(fileName, 'a', newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(dataRow)

    def getData(self, blockNumber, trialNum):
        ''' Get the data that the subject has put in'''

        self.blockNumber = blockNumber
        self.trialNumber = trialNum

        dataRow = [blockNumber]
        dataRow.append(trialNum)

        return dataRow

    def thankYou(self):
        thanks = "You have reached the end of the experiment. Please notify the researcher."
        thanks += "\n\n Thank you so much for volunteering for our study."
        showText(thanks, keys = ["space"], height=0.05)

#===========================================================#
#                     HELPER FUNCTION                       #
#===========================================================#

def showText(text, t_color = 'White', keys = [], 
    height = 0.1, maxWait=float('inf'), clock=None):
    message = visual.TextStim(win, text=text, height=height, color=t_color)
    message.size = (0.2, 0.5)
    message.draw()          # draw the message offscreen
    win.flip()              # flip the Scrseen

    if (len(keys) == 0):
        keyPressed = event.waitKeys()	    # Wait for keypress to continue
    else:
        # find keypressed during trial here
        if clock == None:
            keyPressed = event.waitKeys(maxWait=maxWait, keyList=keys)
        else:
            keyPressed = event.waitKeys(maxWait=maxWait, keyList=keys, timeStamped=clock)

    return keyPressed 


#============================================================
#                     EXECUTE EXPERIMENT                    #
#============================================================

def main():    
    # Put data from fields at the beginning of the experiment
    # and construct a Subject object.
    subject = Subject(dlg.data[0], dlg.data[1], dlg.data[2])
    subject.saveSubjectInfo()

    # full modeType = 240 trials and 10 blocks
    # debug modeType = 24 trials and 1 block

    if dlg.data[1] == "full":
        trials = int(42)
        blocks = int(2)
    else:
        trials = int(21)  
        blocks = int(1)

    # make experiment
    experiment = Experiment(subject, trials, blocks) #subjID, trials, blocks, trialType
    experiment.introduction()
    experiment.doTrials()
    experiment.thankYou()

    print("Normal exit")

    if dlg.OK == False:
        win.close()
        core.quit()  # cancelled
    else:
        subject.printSubject()

main()
