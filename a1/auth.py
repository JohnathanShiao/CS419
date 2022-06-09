import json
import sys
from os.path import exists

users={}
domains={}
types={}
access={}

def addUser(username, password):
    if len(username) == 0:
        print("Error: username missing")
        return
    if users.get(username):
        print("Error: user exists")
        return
    #users are unique, can use dict
    users[username] = password
    print("Success")

    
def authenticate(username, password):
    if len(username) == 0:
        print("Error: username missing")
        return
    if users.get(username) is None:
        print("Error: no such user")
        return
    if users.get(username) == password:
        print("Success")
    else:
        print("Error: bad password")

def setDomain(username, domain):
    if len(domain) == 0:
        print("Error: missing domain")
        return
    if users.get(username) is None:
        print("Error: no such user")
        return
    #check for existence, if not create new, else append 
    temp = domains.get(domain)
    if temp is None:
        domains[domain] = [username]
    else:
        if username not in temp:
            temp.append(username)
    print("Success")

def domainInfo(domain):
    if len(domain)==0:
        print("Error: missing domain")
        return
    temp = domains.get(domain)
    #check for existence, only print if it exists
    if temp is None:
        return
    for item in temp:
        print("{}".format(item))

def setType(object, type):
    if len(object) == 0:
        print("Error: missing object")
        return
    if len(type) == 0:
        print("Error: missing type")
        return
    temp = types.get(type)
    #check for existence, only add if exists and is the first time it exists
    if temp is None:
        types[type] = [object]
    else:
        if object not in temp:
            temp.append(object)
    print("Success")

def typeInfo(type):
    if len(type)==0:
        print("Error: missing type")
        return
    temp = types.get(type)
    #check for existence, only print if exists
    if temp is None:
        return
    for item in temp:
        print("{}".format(item))

def addAccess(operation,domain,type):
    if len(operation) == 0:
        print("Error: missing operation")
        return
    if len(domain) == 0:
        print("Error: missing domain")
        return
    if len(type) == 0:
        print("Error: missing type")
        return
    oper = access.get(operation)
    exists = 0
    if oper is not None:
        for item in oper:
            if item.get(domain) == type:
                exists = 1
    #create new if not exists, append if it does
    if not exists:
        if oper is None:
            access[operation] = [{domain: type}]
        else:
            oper.append({domain: type})
    print("Success")

def canAccess(operation,username,object):
    if len(operation) == 0:
        print("Error: missing operation")
        return
    if len(username) == 0:
        print("Error: missing username")
        return
    if len(object) == 0:
        print("Error: missing object")
        return
    user_domains = []
    #create list of domains user is in
    for key in domains.keys():
        for name in domains.get(key):
            if name == username:
                user_domains.append(key)
    temp = access.get(operation)
    #check if the operation contains that user_domain
    for pair in temp:
        for domain in user_domains:
            #if domain matches, check if object is the same
            if pair.get(domain) is not None:
                for item in types.get(pair.get(domain)):
                    if item == object:
                        print("Success")
                        return
    print("Error: access denied")


def main():
    global users, domains, types, access
    if exists("./auth.json"):
        fd = open("auth.json")
        try:
            data = json.load(fd)
        except:
            print("Error: auth.json is empty, please delete the file")
            return
        users = data.get("users")
        domains = data.get("domains")
        types = data.get("types")
        access = data.get("access")
        fd.close()
        fd = open("auth.json","w")
    else:
        fd = open("auth.json","w")
    commands=["adduser","authenticate","setdomain","domaininfo","settype","typeinfo","addaccess","canaccess"]
    if sys.argv[1].lower() not in commands:
        print("Error: invalid command {}".format(sys.argv[1]))
    else:
        i = commands.index(sys.argv[1].lower())
        if i == 0:
            if len(sys.argv) < 4:
                print("Error: not enough arguments for AddUser")
            elif len(sys.argv) > 4:
                print("Error: too many arguments for AddUser")
            else:
                addUser(sys.argv[2].lower(),sys.argv[3].lower())
        elif i == 1:
            if len(sys.argv) < 4:
                print("Error: not enough arguments for Authenticate")
            elif len(sys.argv) > 4:
                print("Error: too many arguments for Authenticate")
            else:
                authenticate(sys.argv[2].lower(),sys.argv[3].lower())
        elif i == 2:
            if len(sys.argv) < 4:
                print("Error: not enough arguments for SetDomain")
            elif len(sys.argv) > 4:
                print("Error: too many arguments for SetDomain")
            else:
                setDomain(sys.argv[2].lower(),sys.argv[3].lower())
        elif i == 3:
            if len(sys.argv) < 3:
                print("Error: not enough arguments for DomainInfo")
            elif len(sys.argv) > 3:
                print("Error: too many arguments for DomainInfo")
            else:
                domainInfo(sys.argv[2].lower())
        elif i == 4:
            if len(sys.argv) < 4:
                print("Error: not enough arguments for SetType")
            elif len(sys.argv) > 4:
                print("Error: too many arguments for SetType")
            else:
                setType(sys.argv[2].lower(),sys.argv[3].lower())
        elif i == 5:
            if len(sys.argv) < 3:
                print("Error: not enough arguments for TypeInfo")
            elif len(sys.argv) > 3:
                print("Error: too many arguments for TypeInfo")
            else:
                typeInfo(sys.argv[2].lower())
        elif i == 6:
            if len(sys.argv) < 5:
                print("Error: not enough arguments for AddAccess")
            elif len(sys.argv) > 5:
                print("Error: too many arguments for AddAccess")
            else:
                addAccess(sys.argv[2].lower(),sys.argv[3].lower(),sys.argv[4].lower())
        else:
            if len(sys.argv) < 5:
                print("Error: not enough arguments for CanAccess")
            elif len(sys.argv) > 5:
                print("Error: too many arguments for CanAccess")
            else:
                canAccess(sys.argv[2].lower(),sys.argv[3].lower(),sys.argv[4].lower())
    data = {
        "users": users,
        "domains": domains,
        "types": types,
        "access": access
    }
    json_string = json.dumps(data, indent=4)
    fd.write(json_string)
    fd.close
if __name__ == "__main__":
    main()