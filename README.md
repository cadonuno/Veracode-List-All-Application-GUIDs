# Veracode List All Application GUIDs

## Overview
This script will read all available applications and print their names and GUIDs

## Installation

Clone this repository:

    git clone https://github.com/cadonuno/Veracode-List-All-Application-GUIDs.git

Install dependencies:

    cd Veracode-List-All-Application-GUIDs
    pip install -r requirements.txt

### Getting Started

It is highly recommended that you store veracode API credentials on disk, in a secure file that has 
appropriate file protections in place.

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

### Running the script
    py list-application-guids.py [-d]
        -d will add debug information to the console output, making it easier to troubleshoot

The plugin will print all applications in the following format:
&ltApplication 1 name&gt | &ltApplication 1 GUID&gt
&ltApplication 2 name&gt | &ltApplication 2 GUID&gt
...
&ltApplication x name&gt | &ltApplication x GUID&gt