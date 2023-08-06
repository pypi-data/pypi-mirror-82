# pynrds
pynrds will eventually be a complete Python library for the NAR NRDS API Service.

## Installation
```pip install pynrds```

## Usage
The NRDS API has a pretty simple structure, so querying it is straightforward using the `requests` module: 

```python
import requests
import json


# NRDS API spec specifies 'MemberID' for NRDS id #
member_id = '123456789'

# UserRole is provided by NAR for API access
user_role = 'abc-123-defg-4567'

# SenderMemberId is the API user's NRDS id# (??)
sender_member_id = '987654321'

# NRDS Beta API url
base_url = 'https://beta.api.realtor.org/data'

# endpoint
endpoint = '/members/'

# put them together
url = f'{base_url}{endpoint}{member_id}'

# create your payload of credentials
payload = {
    'UserRole'      : user_role,
    'SenderMemberId': sender_member_id
    }

# make the http request and return the result as a json object 'reply'
reply = requests.post(url, payload).json()


# or make the request with a function:
def get_single_member(member_id):

    payload = {
        'UserRole'      : user_role,
        'SenderMemberId': sender_member_id
        }

    url = f'{base_url}/members/{member_id}'

    reply = requests.post(url, payload).json()
    return(reply)
```

Additional endpoints and queries are similar, and I'll build them once I have a system to verify them on, but that's not really the challenge I'm interested in...

The more interesting question, of course, is what can be done with JUST the data the NRDS API provides, using only Open-Source tools? For exploring those questions we're going to need sample data, so we can try new things and make complex mockups without the need to use or affect live NRDS information, or to post member data as part of learning how to use the data the API returns. So, my short-term goal is to create a full test set of simulated NRDS data that anyone can use, scale, and customize to their own needs, then create a dummy API for that test set that exactly mirrors the (typical, documented) behavior of the NRDS API. It should be possible to create a mock Association of any size, populate realistic but fake NRDS data to its "members", and then use it to test any imaginable application based on the NRDS API without the need to use it in early testing. 

### Update 10/12/20: Initial pypi release
Pushed current build to pypi so it can be installed as a module. Added a Designations section to `get_random_member()` to demonstrate the basic method - probabilities and other details still need to be fine-tuned. Examples below updated. Added a modified `get_single_member()` method which should work on the beta NRDS API. 


```python
# NRDS Beta API url
beta_base_url = 'https://beta.api.realtor.org/data'


# get data for a single member, given
# target member ID, user role, and sender member ID
def get_single_member(member_id, user_role, sender_member_id):

    payload = {
        'UserRole'      : user_role,
        'SenderMemberId': sender_member_id
        }

    url = f'{beta_base_url}/members/{member_id}'

    reply = requests.post(url, payload)
    return(reply)
```


### Update 10/10/20: 
Created and uploaded `get_member.py` which returns a `JSON` package of randomized member data in the same format as the NRDS API `/member/` endpoint. Tackled the easy elements first, this script will not generate simulated data for Certifications, Designations, etc (yet!) but the other information looks realistic enough for testing purposes. Ages, DOB, years of membership, NRDS insert dates, and all other info are random, but follow some rules to make the data realistic. The script's dependencies are all in the import section, notably `Delorean` and `Numpy`, as well as two different fake-data libraries: `mimesis` and `faker`, with `mimesis` doing the bulk of the work. The outputted addresses are a bit "European" in flavor, specifically British, but close enough. 

Once I complete simulated data templates for all the NRDS endpoints I can create a stand-in API that will return realistic but fake NRDS-like data and let us quickly mock up queries and build realistic applications that can be expected to work with "real" NRDS data. Eventually, we'll create a whole fake Association's worth of NRDS records and store it so we can interact with it exactly like the NRDS API. There are some clues to the theme in the code...

Example output of `get_random_member()` below:

```json
[
    {
        "Member": {
            "AssociationId": "8128",
            "Designations": [
                {
                    "DesignationCode": "CCIM",
                    "DesignationDate": "05-03-2016",
                    "DesignationDescription": "Certified Commercial Investment Member",
                    "MemberId": "812865015",
                    "Timestamp": 5567039
                },
                {
                    "DesignationCode": "SRS",
                    "DesignationDate": "11-03-2010",
                    "DesignationDescription": "Seller Representative Specialist",
                    "MemberId": "812865015",
                    "Timestamp": 7695568
                }
            ],
            "DirectoryOptOut": "N",
            "DuesWaivedLocalFlag": "N",
            "DuesWaivedNationalFlag": "N",
            "DuesWaivedStateFlag": "N",
            "Email": "coyan1977@live.com",
            "JoinedDate": "07-16-2012",
            "JunkMailFlag": "Y",
            "MLSID": "6142",
            "MemberArbitrationEthicsPending": "Y",
            "MemberBirthDate": "05-29-1950",
            "MemberCellPhone": {
                "PhoneArea": 636,
                "PhoneNumber": 8533602
            },
            "MemberDesignatedRealtor": "N",
            "MemberFirstName": "Cordia",
            "MemberGender": "F",
            "MemberGeneration": "Jr.",
            "MemberHomeAddress": {
                "City": "Springfield",
                "Country": "US",
                "State": "OR",
                "Street1": "880 Kempton Plaza South",
                "Street2": "#168",
                "Zip": "34321",
                "Zip6": "2109"
            },
            "MemberHomePhone": {
                "PhoneArea": 939,
                "PhoneNumber": 8493749
            },
            "MemberId": "812865015",
            "MemberLastName": "Castro",
            "MemberLocalJoinedDate": "07-16-2012",
            "MemberMLSAssociationId": "42774",
            "MemberMailAddress": {
                "City": "Capital City",
                "Country": "US",
                "State": "OR",
                "Street1": "317 Fanning Promenade NW",
                "Street2": "",
                "Zip": "95866",
                "Zip6": "1419"
            },
            "MemberMiddleName": "",
            "MemberNRDSInsertDate": "07-16-2012",
            "MemberNationalDuesPaidDate": "09-23-2019",
            "MemberNickname": "",
            "MemberOccupationName": "Administration Staff",
            "MemberOfficeVoiceExtension": "6787",
            "MemberOnlineStatus": "Y",
            "MemberOnlineStatusDate": "",
            "MemberOrientationDate": "07-23-2012",
            "MemberPager": {
                "PhoneArea": 939,
                "PhoneNumber": 9731711
            },
            "MemberPersonalFax": {
                "PhoneArea": 636,
                "PhoneNumber": 2949099
            },
            "MemberPreferredFax": "O",
            "MemberPreferredMail": "M",
            "MemberPreferredPhone": "H",
            "MemberPreferredPublication": "O",
            "MemberPrimaryStateAssociationId": "0862",
            "MemberRELicense": "SL743006",
            "MemberReinstatementCode": "",
            "MemberReinstatementDate": "",
            "MemberSalutation": "",
            "MemberStateDuesPaidDate": "09-23-2019",
            "MemberStatus": "A",
            "MemberStatusDate": "",
            "MemberSubclass": "R",
            "MemberTitle": "",
            "MemberType": "R",
            "OfficeId": "8128",
            "OnRosterFlag": "Y",
            "PointOfEntry": "070008128",
            "PreviousNonMemberFlag": "N",
            "PrimaryIndicator": "P",
            "StopEMailFlag": "N",
            "StopFaxFlag": "N",
            "StopMailFlag": "N",
            "Timestamp": 9776510,
            "WebPage": "https://agnosia.name"
        }
    },
    {
        "Member": {
            "AssociationId": "8128",
            "Designations": [],
            "DirectoryOptOut": "N",
            "DuesWaivedLocalFlag": "N",
            "DuesWaivedNationalFlag": "N",
            "DuesWaivedStateFlag": "N",
            "Email": "hydromyelocele2040@gmail.com",
            "JoinedDate": "11-01-2012",
            "JunkMailFlag": "Y",
            "MLSID": "5877",
            "MemberArbitrationEthicsPending": "N",
            "MemberBirthDate": "04-27-1959",
            "MemberCellPhone": {
                "PhoneArea": 939,
                "PhoneNumber": 9868824
            },
            "MemberDesignatedRealtor": "N",
            "MemberFirstName": "Talisha",
            "MemberGender": "F",
            "MemberGeneration": "",
            "MemberHomeAddress": {
                "City": "Springfield",
                "Country": "US",
                "State": "OR",
                "Street1": "984 Arleta Esplanade SW",
                "Street2": "",
                "Zip": "55571",
                "Zip6": "2928"
            },
            "MemberHomePhone": {
                "PhoneArea": 636,
                "PhoneNumber": 1802199
            },
            "MemberId": "812888551",
            "MemberLastName": "Kidd",
            "MemberLocalJoinedDate": "11-01-2012",
            "MemberMLSAssociationId": "96006",
            "MemberMailAddress": {
                "City": "Shelbyville",
                "Country": "US",
                "State": "OR",
                "Street1": "865 Portal St NW",
                "Street2": "",
                "Zip": "24041",
                "Zip6": "8198"
            },
            "MemberMiddleName": "",
            "MemberNRDSInsertDate": "11-01-2012",
            "MemberNationalDuesPaidDate": "12-06-2019",
            "MemberNickname": "",
            "MemberOccupationName": "Prison Chaplain",
            "MemberOfficeVoiceExtension": "5902",
            "MemberOnlineStatus": "Y",
            "MemberOnlineStatusDate": "",
            "MemberOrientationDate": "02-21-2012",
            "MemberPager": {
                "PhoneArea": 636,
                "PhoneNumber": 1426625
            },
            "MemberPersonalFax": {
                "PhoneArea": 636,
                "PhoneNumber": 8463141
            },
            "MemberPreferredFax": "O",
            "MemberPreferredMail": "F",
            "MemberPreferredPhone": "O",
            "MemberPreferredPublication": "H",
            "MemberPrimaryStateAssociationId": "0862",
            "MemberRELicense": "SL397031",
            "MemberReinstatementCode": "",
            "MemberReinstatementDate": "",
            "MemberSalutation": "",
            "MemberStateDuesPaidDate": "12-06-2019",
            "MemberStatus": "A",
            "MemberStatusDate": "",
            "MemberSubclass": "R",
            "MemberTitle": "",
            "MemberType": "R",
            "OfficeId": "8128",
            "OnRosterFlag": "Y",
            "PointOfEntry": "070008128",
            "PreviousNonMemberFlag": "N",
            "PrimaryIndicator": "P",
            "StopEMailFlag": "N",
            "StopFaxFlag": "N",
            "StopMailFlag": "N",
            "Timestamp": 5770472,
            "WebPage": "https://exogen.com"
        }
    }
]
```
