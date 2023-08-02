import sys
import requests
import getopt
import json
import urllib.parse
from veracode_api_signing.plugin_requests import RequestsAuthPluginVeracodeHMAC
import time

from veracode_api_signing.credentials import get_credentials


json_headers = {
    "User-Agent": "List all application GUIDs - python script",
    "Content-Type": "application/json"
}

def get_api_base():
    api_key_id, api_key_secret = get_credentials()
    api_base = "https://api.veracode.{instance}/"
    if api_key_id.startswith("vera01"):
        return api_base.replace("{instance}", "eu", 1)
    else:
        return api_base.replace("{instance}", "com", 1)

foundGuidsAsText = ""
foundGuids = 0
maxGuids = 0
applicationsUrl = f"{get_api_base()}appsec/v1/applications"

def print_help():
    """Prints command line options and exits"""
    print("""list-application-guids.py [-d]"
        Reads all applications and lists all their guids
""")
    sys.exit()

def read_all_application_guids_from_page(currentPage, lastPage, verbose):
    global foundGuids
    global maxGuids
    global foundGuidsAsText
    path = f"{applicationsUrl}?page={currentPage}"
    currentPage += 1
    if verbose:
        print(f"Calling: {path}")

    response = requests.get(path, auth=RequestsAuthPluginVeracodeHMAC(), headers=json_headers)
    data = response.json()

    if response.status_code == 200:
        if verbose:
            print("API returned:")
            print(data)
        
        lastPage = data["page"]["total_pages"]
        maxGuids = data["page"]["total_elements"]

        applicationList = data["_embedded"]["applications"]
        for index in range(len(applicationList)):
            element = applicationList[index]
            foundGuidsAsText += f"\n{element['profile']['name']} | {element['guid']}"
            foundGuids+=1

        return currentPage < lastPage, currentPage, lastPage
    else:
        print(f"ERROR: failed call to applications API")
        print(f"ERROR: code: {response.status_code}")
        print(f"ERROR: value: {data}")
        return 0, 0, False

def read_all_application_guids(verbose):
    global applicationsUrl
    currentPage = 0
    lastPage = 0
    shouldContinue = True

    while shouldContinue:
        shouldContinue, currentPage, lastPage = read_all_application_guids_from_page(currentPage, lastPage, verbose)

def main(argv):
    global foundGuids
    global maxGuids
    global foundGuidsAsText
    try:
        verbose = False
        opts, args = getopt.getopt(argv, "hd", [])
        for opt, arg in opts:
            if opt == '-h':
                print_help()
            if opt == '-d':
                verbose = True
        read_all_application_guids(verbose)
    except requests.RequestException as e:
        print("An error occurred!")
        print(e)
    finally:
        if foundGuidsAsText:
            print(f"Found {foundGuids}/{maxGuids} guids:")
            print(foundGuidsAsText)


if __name__ == "__main__":
    main(sys.argv[1:])
