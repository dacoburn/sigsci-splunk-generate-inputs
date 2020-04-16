import requests
import json

config_file = "settings.json"
conf_handle = open(config_file, "r")
confJson = json.load(conf_handle)

# Settings loaded from the Confiuration file - Do not Modify

if "corp" not in confJson or "api_user" not in confJson or \
        "api_token" not in confJson or "inputs_file" not in confJson:
    print("Critical error! All of the following settings must be defined:")
    print("corp\napi_user\napi_token\ninputs_file")
    exit(1)
else:
    corp = confJson["corp"]
    api_user = confJson["api_user"]
    api_token = confJson["api_token"]
    inputs_file = confJson["inputs_file"]

if "input_delta" in confJson:
    input_delta = confJson["input_delta"]
else:
    input_delta = 5

if "input_index" in confJson:
    input_index = confJson["input_index"]
else:
    input_index = "default"

if "input_interval" in confJson:
    input_interval = confJson["input_interval"]
else:
    input_interval = 300

if "input_disabled" in confJson:
    input_disabled = confJson["input_disabled"]
else:
    input_disabled = 0

if "requestEnabled" in confJson:
    requestEnabled = confJson["requestEnabled"]
else:
    requestEnabled = True

if "eventEnabled" in confJson:
    eventEnabled = confJson["eventEnabled"]
else:
    eventEnabled = True

if "activityEnabled" in confJson:
    activityEnabled = confJson["activityEnabled"]
else:
    activityEnabled = True

# Generic Global Settings - Do not Modify
base_url = "https://dashboard.signalsciences.net/api/v0/corps"
reqType = "SigsciRequests"
eventType = "SigsciEvent"
corpType = "SigsciActivity"

# Handy function for pretty printing JSON
def prettyJson(data):
    return(json.dumps(data, indent=4, separators=(',', ': ')))

def loadInputFile(file):
    tmpData = { reqType: {}, eventType: {}, corpType: {}}
    fh = open(file, "r")
    lines = fh.readlines() 
    firstLine = False
    curInputName = ""
    curInputType = ""
    for line in lines:
        line = line.strip()
        if line.startswith("[") and line.endswith("]") and \
                "://" in line:
            firstLine = True
            inputType, inputName = line.split("://")
            curInputType = inputType[1:]
            curInputName = inputName[:-1]
            tmpData[curInputType][curInputName] = {
                "delta": "",
                "index": "",
                "site": "",
                "interval": "",
                "disabled": ""
            }
        else:
            if line != "" and line is not None:
                inputKey, inputValue = line.split(" = ")
                tmpData[curInputType][curInputName][inputKey] = inputValue

    fh.close()
    return(tmpData)

def doRequest(url, user, token):
    payload = {}
    headers = {
      'x-api-user': user,
      'x-api-token': token,
      'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    return(response)


def getSites(curURL):
    response = doRequest(curURL, api_user, api_token)
    response_code = response.status_code
    response_text = response.text
    tmpData = []

    if response_code == 200:
        jsonData = json.loads(response_text)
        siteData = jsonData["data"]
        numSites = jsonData["totalCount"]
        for curSite in siteData:
            api_site_name = curSite["name"]
            tmpData.append(api_site_name)
        return(True, response_code, tmpData)
        #print(prettyJson(siteData))
    else:
        jsonData = json.loads(response_text)
        errorMessage = jsonData["message"]
        return(False, response_code, errorMessage)
        #print(response.text.encode('utf8'))

def checkForNewInputs(iData, sData):
    newInputNames = {
        reqType: [],
        eventType: [],
        corpType: []
    }
    for curSite in sData:
        # Check for new Request Inputs
        requestInput = iData[reqType]
        newReqInput = True
        for curReqInput in requestInput:
            reqSite = requestInput[curReqInput]["site"]
            if curSite == reqSite:
                newReqInput = False
        if newReqInput:
            newInputNames[reqType].append(curSite)
        
        # Check for new Event Inputs
        eventInput = iData[eventType]
        newEventInput = True
        for curEventInput in eventInput:
            eventSite = eventInput[curEventInput]["site"]
            if curSite == eventSite:
                newEventInput = False
        if newReqInput:
            newInputNames[eventType].append(curSite)

    # Check for new Corp Inputs
    corpInput = iData[corpType]
    newCorpInput = True
    totalCorp = len(corpInput)
    print(totalCorp)
    if totalCorp > 0:
        newCorpInput = False
    else:
        newInputNames[corpType].append(corp)
    return(newInputNames)

def writeInputFile(file, data):
    log = open(file, 'a')
    reqEntries = data[reqType]
    eventEntries = data[eventType]
    corpEntries = data[corpType]
    if requestEnabled:
        for newRequestInput in reqEntries:
            reqName = "[%s://%s]\n" % (reqType, newRequestInput)
            reqName = reqName.replace("-", "_")
            reqName = reqName.replace(" ", "_")
            reqDelta = "delta = %s\n" % input_delta
            reqIndex = "index = %s\n" % input_index
            reqSite = "site = %s\n" % newRequestInput
            reqInterval = "interval = %s\n" % input_interval
            reqDisabled = "disabled = %s\n" % input_disabled

            log.write("\n")
            log.write(reqName)
            log.write(reqDelta)
            log.write(reqIndex)
            log.write(reqSite)
            log.write(reqInterval)
            log.write(reqDisabled)
            # exit()
    if eventEnabled:
        for newEventInput in eventEntries:
            eventName = "[%s://%s]\n" % (eventType, newEventInput)
            eventName = eventName.replace("-", "_")
            eventName = eventName.replace(" ", "_")
            eventDelta = "delta = %s\n" % input_delta
            eventIndex = "index = %s\n" % input_index
            eventSite = "site = %s\n" % newEventInput
            eventInterval = "interval = %s\n" % input_interval
            eventDisabled = "disabled = %s\n" % input_disabled

            log.write("\n")
            log.write(eventName)
            log.write(eventDelta)
            log.write(eventIndex)
            log.write(eventSite)
            log.write(eventInterval)
            log.write(eventDisabled)
    if activityEnabled:
        for newCorpInput in corpEntries:
            corpName = "[%s://%s]\n" % (corpType, newCorpInput)
            corpName = corpName.replace("-", "_")
            corpName = corpName.replace(" ", "_")
            corpDelta = "delta = %s\n" % input_delta
            corpIndex = "index = %s\n" % input_index
            corpInterval = "interval = %s\n" % input_interval
            corpDisabled = "disabled = %s\n" % input_disabled

            log.write("\n")
            log.write(corpName)
            log.write(corpDelta)
            log.write(corpIndex)
            log.write(corpInterval)
            log.write(corpDisabled)
    log.close

sitesURL = "%s/%s/sites" % (base_url, corp)
sites_success, response_code, siteData = getSites(sitesURL)

if not sites_success:
    print("Unable to pull Site Data")
    print("Url: %s" % sitesURL)
    print("ResponseCode: %s" % response_code)
    print("Error Message: %s" % siteData)
    exit()
else:
    totalSites = len(siteData)
    print("Total Sites Found: %s" % totalSites)
    print("Site API Names:")
    for curSite in siteData:
        print("\t%s" % curSite)

inputData = loadInputFile(inputs_file)
numInputs = len(inputData)

if numInputs > 0:
    newInputs = checkForNewInputs(inputData, siteData)
    print(prettyJson(newInputs))
    writeInputFile(inputs_file, newInputs)