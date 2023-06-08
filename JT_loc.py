#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from psychopy import locale_setup, gui, visual, core, data, event, logging, clock, constants
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os  # handy system and path functions
import sys  # to get file system encoding
import random
from numpy.random import random, randint, normal, shuffle
import numpy as np

path = os.getcwd()

triggerDict = {
           "eegStart": int(254),
           "eegEnd": int(255),
           "building": int(10),
           "animal": int(11),
           "furniture" : int(12),
           "fullbody": int(13),
           "body_part":int(14),
           "automobile":int(15),
           "plant":int(16),
           "resp_up": int(31),
           "resp_down": int(32),
           "fixation": int(50),
           #"fix_ITI": int(51),
           "restStart": int(250),
           "restEnd": int(251)
           }
useTriggers = False #for debugging at home
if useTriggers is True:
    port = parallel.ParallelPort(address='0x0378')
    print("EEG trigger active.")
    
def eegTrigger(self, triggerType):
        """ Send trigger for EEG """
        if useTriggers is True:
            parallel.setPortAddress(port)
            port.setData(triggerType)
            print(triggerType)
            core.wait(0.1) #changed from 0.001 to 0.1 ms
            port.setData(0)



# Store info about the experiment session
expName = u'eeg-localizer'  # from the Builder filename that created this script
expInfo = {'a. session': '01', 'b. participant': '', 'c. run': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = path + '/' + expInfo['b. participant'] + '/' + expInfo['b. participant'] + '_' + expName + '_' + expInfo['c. run'] + '_' + expInfo['date']
# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=path + u'/eeg_localizer.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# clocks
globalClock = core.Clock()
trialClock = core.Clock()
taskClock = core.Clock()

# Setup the Window
win = visual.Window(
    size=(1920, 1080), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=u'grey', colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 25.0  # could not measure, so guess

### image stimuli
images = [path + '/task_images/building',
                    path + '/task_images/animal',
                    path + '/task_images/furniture',
                    path + '/task_images/tree',
                    path + '/task_images/body_part2',
                    path + '/task_images/automobile',
                    path + '/task_images/handheldobj'];
                    #path + '/stim/chair/chair_08s.jpg',
                    #path + '/stim/chair/chair_09s.jpg',
                    #path + '/stim/chair/chair_10sjpg'];
                    
image_names = ['building',
                                'animal',
                                'furniture',
                                'plant',
                                'body part',
                                'automobile',
                                'handheld object',];
                                #'chair_08',
                                #'chair_09',
                                #'chair_10'];

image_idx = [0,1,2,3,4,5,6];
###some task things
Instructions = visual.TextStim(win=win, name='Start',
    text=u'In this task you will see a series of images. Keep your eyes on the cross in the center of the screen. Each image will belong to a cateogry: animals, plants, buildings, body parts, handheld objects, furniture, or automobiles. Using the up and down arrow keys, indicate what category the image belongs to. \n\n When you are ready, press space to continue',
    font=u'Arial',
    pos=(0, 0), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

fixation = visual.TextStim(win=win, name='fixation',
    text=u'+',
    font=u'Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
pathImage = visual.ImageStim(
    win=win, image= path + '/task_images/building',
    units='deg', pos=(0, 0), flipHoriz=False, 
    flipVert=False, name='outcome_low', autoLog=None)
    
response_one = visual.TextStim(win=win, name='response_up',
    text=u'response_one',
    font=u'Arial',
    pos=(0, 0.2), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
response_two = visual.TextStim(win=win, name='response_dn',
    text=u'response_two',
    font=u'Arial',
    pos=(0, -0.2), height=0.09, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
#routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 
# set up handler to look after randomisation of conditions etc
nTrials = 10

conditions=[]
for Idx in range (10):
    conditions.append("chair")

trials = data.TrialHandler(nReps=nTrials, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=conditions,
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
#if thisTrial != None:
 #   for paramName in thisTrial:
  #      exec('{} = thisTrial[paramName]'.format(paramName))

Instructions.draw()
eegTrigger(triggerDict.get("eegStart"))
win.flip()
paused = True # stop right here
while paused:
    if event.getKeys(keyList=['space']):
        paused = False
        taskClock.reset()
        T=0
        k = 0
    else:
        core.wait(0.05)
        
for frame in range (120):
    fixation.draw()
    eegTrigger(triggerDict.get("fixation"))
    win.flip()
   
g = 0
for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    #if thisTrial != None:
    #    for paramName in thisTrial:
    #        exec('{} = thisTrial[paramName]'.format(paramName))
    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    #routineTimer.add(12.00000)
    # update component parameters for each repeat
    key_resp_2 = event.BuilderKeyResponse()
    # keep track of which components have finished
    trialComponents = [key_resp_2, pathImage, fixation, response_one, response_two]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    pathImage.tStart = -1
    v = -1
    a = np.arange(7)
    shuffle(a)
    image_idx=a[0]
    other_idx=a[1]
    # -------Start Routine "trial"-------
    #while continueRoutine and routineTimer.getTime() > 0:
    while continueRoutine:
        # get current time
        t = trialClock.getTime()

        timeLeft = 0
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

        if t >= 0.0 and (pathImage.status == NOT_STARTED):
            if pathImage.status == NOT_STARTED: # at least one key was pressed
                pathImage.image = images[image_idx]
                pathImage.tStart = taskClock.getTime() 
                win.flip()
                
                for frame in np.random.randint(120,180,24): #this is the ITI
                    fixation.draw()
                    eegTrigger(triggerDict.get("fixation"))
                    win.flip()               
                pathImage.frameNStart = frameN  # exact frame index
                for frame in range(48):
                    pathImage.draw()
                    if frame < 1 : #if frame is 0
                        #if port.status == NOT_STARTED and pathImage.status == STARTED:
                        if pathImage.status == STARTED:
                            if (pathImage.status == 'building'):
                                self.eegTrigger(triggerDict.get('building'))
                            elif (pathImage.status == 'furniture'):
                                self.eegTrigger(triggerDict.get('furniture'))
                            elif (pathImage.status == 'fullbody'):
                                self.eegTrigger(triggerDict.get('fullbody'))
                            elif (pathImage.status == 'body_part'):
                                self.eegTrigger(triggerDict.get('body_part'))
                            elif (pathImage.status == 'automobile'):
                                self.eegTrigger(triggerDict.get('automobile'))
                            elif (pathImage.status == 'plant'):
                                self.eegTrigger(triggerDict.get('plant'))
                    win.flip()

                pathImage.status == STOPPED
                g +=1
                
        for frame in range (np.random.randint(24,48)): #minimum of 200 ms max 400ms// creates a random ISI between 20-50 frames (aforementionped ms)
                    fixation.draw()
                    eegTrigger(triggerDict.get("fixation"))
                    win.flip() 
        response_one.text = image_names[other_idx]
        response_one.tStart = taskClock.getTime()
        response_two.text = image_names[image_idx]
        response_two.tStart = taskClock.getTime()
        position_choice = [-0.2,0.2]
        shuffle(position_choice)
        response_one.pos=(0,position_choice[0])
        response_two.pos=(0,position_choice[1])
        
        responseDr = ['up','down']
        #respKey = event.waitKeys(keyList=responseDr)

        response_paused = True # stop right here
        while response_paused:
            theseKeys = event.getKeys(responseDr)
            #if event.getKeys(keyList=['up', 'down']):
            if theseKeys: 
                key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                if (theseKeys[-1] == 'up'):
                  eegTrigger(triggerDict.get("resp_up"))
                elif (theseKeys[-1] == 'down'):
                  eegTrigger(triggerDict.get("resp_down"))
                key_resp_2.rt = key_resp_2.clock.getTime()
                k = taskClock.getTime()
                response_paused = False
                taskClock.reset()
                T=0
                k = 0
            else:
                response_one.draw()
                fixation.draw()
                response_two.draw()
                win.flip()
                core.wait(0.05)
        
                
                
        #theseKeys = event.getKeys(responseDr)
        #if len(theseKeys) > 0 :  # at least one key was pressed
         #   key_resp_2.keys = theseKeys[-1]  # just the last key pressed
          #  key_resp_2.rt = key_resp_2.clock.getTime()
           # k = taskClock.getTime()
                    
                #if key_resp_2.keys == 'm' and outcomeImage.status == NOT_STARTED and (pathImage.status == STOPPED) :  # at least one key was pressed
                #    outcomeImage.tStart = trialClock.getTime() 
                #    outcomeImage.image = outcomeH
                #    outcomeImage.frameNStart = frameN  # exact frame index
                #    for frame in range(90):
                #        outcomeImage.draw()
                #        win.flip()
            
            # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
            
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
            
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
                
                
        win.flip()
        for frame in range (5):
                win.flip()
            
        event.clearEvents(eventType='keyboard')

        win.flip()
        core.wait(0.2)
        fixation.draw()
        eegTrigger(triggerDict.get("fixation"))
        win.flip()      
        if event.getKeys('p'):
            paused = True # stop right here
            paused_trial.append(trials.thisN) 
            while paused:
                if event.getKeys('space'):
                    paused = False
                else:
                    core.wait(0.01)
            else:
                break

            # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys=None
    thisExp.addData('key_resp_2.keys',key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        thisExp.addData('key_resp_2.rt', key_resp_2.rt)
        thisExp.addData('button_press', k)
    thisExp.addData('path_time', pathImage.tStart)
    thisExp.addData('path_Image', pathImage.image)
    #thisExp.addData('outcomeImage', outcomeImage.image)
    #thisExp.addData('condition', condition) 
    #thisExp.addData('paused_trial', paused_trial)
    thisExp.nextEntry()
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
fin.draw()
eegTrigger(triggerDict.get("eegEnd"))
win.flip()
paused = True # stop right here
while paused:
    if event.getKeys(keyList=['space']):
        paused = False
        taskClock.reset()
        T=0
        k = 0
    else:
        core.wait(0.05)

for frame in range (10):
    print( taskClock.getTime())
core.wait(1.0)

logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
