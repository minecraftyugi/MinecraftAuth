import requests

#disable URLLib warnings
requests.packages.urllib3.disable_warnings()

NAME_URL = "https://api.mojang.com/users/profiles/minecraft/"
UUID_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"
AUTH_URL = "https://authserver.mojang.com/authenticate"

def nameToID(name):
    """ (str) -> str

    Return the UUID for the given minecraft username name. Returns the empty
    string if name is not associated with a minecraft account.

    >>> nameToID("CaptainSparklez")
    '5f820c3958834392b1743125ac05e38c'
    """
    
    try:
        response = requests.get(NAME_URL + name, timeout=3)
        if response.status_code == 200:      
            response = response.json()
            return str(response["id"])
        else:
            response.raise_for_status()
            return ""
        
    except Exception as e:
        print e
        return ""

def IDToName(ID):
    """ (str) -> str

    Return the username for the given minecraft UUID ID. Returns the empty
    string if ID is not associated with a minecraft account.

    >>> IDToName("5f820c3958834392b1743125ac05e38c")
    'CaptainSparklez'
    """
    
    try:
        response = requests.get(UUID_URL + ID, timeout=3)
        if response.status_code == 200:      
            response = response.json()
            return str(response["name"])
        else:
            response.raise_for_status()
            return ""
        
    except Exception as e:
        print e
        return ""

def authenticateCreds(username, password):
    """ (str, str) -> boolean

    Returns true iff the given username and password are valiid credentials
    for a minecraft account.
    """
    
    payload = {
    "agent": {
        "name": "Minecraft",
        "version": 1
    },
    "username": username,
    "password": password
    }
    header = {"Content-Type": "application/json"}
    try:
        response = requests.post(AUTH_URL, json=payload, headers=header)
        if response.status_code == 200:
            return True
        else:
            response = response.json()
            print response["errorMessage"]
            return False

    except Exception as e:
        print e
        return False

def isUnmigrated(username, password):
    """ (str, str) -> bool

    Returns true iff the given username and password are valiid credentials
    for an unmigrated minecraft account.
    """

    payload = {
    "agent": {
        "name": "Minecraft",
        "version": 1
    },
    "username": username,
    "password": password,
    }
    header = {"Content-Type": "application/json"}
    try:
        response = requests.post(AUTH_URL, json=payload, headers=header)
        if response.status_code == 200:
            response = response.json()
            return response["selectedProfile"].get("legacy", False)
        else:
            response = response.json()
            print response["errorMessage"]
            return False

    except Exception as e:
        print e
        return False
