import os
import requests, json
import requests.packages.urllib3

if 'DRACUSR' and 'DRACPWD' in os.environ:
    usr = os.environ['DRACUSR']
    pwd = os.environ['DRACPWD']
else:
    usr = "root"
    pwd = "password"

requests.packages.urllib3.disable_warnings()

IP = "192.168.1.1"
root = "https://"+ IP + "/redfish/v1/"

def get(uri):
    response = requests.get(uri, auth=(usr, pwd), verify=False)
    jresponse = json.loads(response.content)
    return jresponse

print ("------------------------------------------------")
print ("\n - First let's examine the root of the REDFISH tree")
raw_input("\n --- Press Enter to start ---\n\n")
uri = root
print (json.dumps(get(uri), indent=4))

print ("\n")
print (" - Each of the @odata.id can be explored further")
print (" - REDFISH offers two distinct branches for chassis and systems")
print (" - This way it can work with traditional, blades and even FX servers")
print ("------------------------------------------------")
print ("\n - Let's explore the Processors branch")
raw_input("\n --- Press Enter to continue ---\n\n")
folder = "Systems/System.Embedded.1/Processors"
uri = root + folder
print (json.dumps(get(uri), indent=4))

print ("")
print (" - There are 4 sockets in this server. Let's dig into the first one")
print ("------------------------------------------------")
raw_input("\n --- Press Enter to continue ---\n\n")
folder = "Systems/System.Embedded.1/Processors/CPU.Socket.1"
uri = root + folder
print (json.dumps(get(uri), indent=4))

print ("\n")
print (" - The Model key has a description of the processor")
print (" - Let's use also the Socket and the TotalCores keys")
print (" - Let's iterate over all processors to do a little report")
print ("------------------------------------------------")
raw_input("\n --- Press Enter to continue ---\n\n")
folder = "Systems/System.Embedded.1/Processors"
uri = root + folder
Procs = get(uri)
for each_proc in Procs['Members']:
    data = get("https://"+ IP + each_proc[u'@odata.id'])
    print (data['Socket'] + "  =  " + data['Model'] + ", contains " + str(data['TotalCores']) + " cores")

print ("\n")
print (" - Let's explore the Managers branch off the root")
print ("------------------------------------------------")
raw_input("\n --- Press Enter to continue ---\n\n")
folder = "Managers"
uri = root + folder
print (json.dumps(get(uri), indent=4))

print ("\n")
print (" - The only manager is the iDRAC")
print (" - We use iDRAC branch for things like viewing the logs")
print ("------------------------------------------------")
raw_input("\n --- Press Enter to continue ---\n\n")
folder = "Managers/iDRAC.Embedded.1/Logs/Sel"
uri = root + folder
Logs = get(uri)
for each_log in Logs['Members']:
    print (each_log['Description'] + " : " + each_log['Created'] + " : Sev = " + each_log['Severity'])
    print (each_log['Message'])
    print ("")

print ("\n")
print (" - So far we have used only HTTP GET methods")
print (" - The REDFISH API supports also:")
print ("    + POST   : Create resource or perform actions")
print ("    + PATCH  : Modify an existing resource ")
print ("    + DELETE : Delete a resource")
print ("")
print (" - For example Restarting the system requires POST")
print (" - The API also provides info on how to do the actions ")
print ("------------------------------------------------")
raw_input("\n --- Press Enter to continue ---\n\n")
folder = "Systems/System.Embedded.1"
uri = root + folder
output = get(uri)
print (json.dumps(output['Actions'], indent=4))

print ("")
print (" - Let's perform a Graceful Restart")
print ("------------------------------------------------")
raw_input("\n --- Press Enter to continue ---\n\n")
folder = "Systems/System.Embedded.1/Actions/ComputerSystem.Reset"
uri = root + folder
payload = {'ResetType':'GracefulRestart'}
headers = {'content-type':'application/json'}
response = requests.post(uri, data=json.dumps(payload), headers=headers, auth=(usr, pwd), verify=False)
print response

    
