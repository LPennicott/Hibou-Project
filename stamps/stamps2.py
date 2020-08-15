import os
import zeep
import xmltodict
import requests

os.chdir("stamps")

apiKey = os.getenv("Hibou_Key")
username = os.getenv("Stamps_User")
password = os.getenv("Stamps_Pass")

Credentials = {
    "Credentials": {
        "IntegrationID": apiKey,
        "Username": username,
        "Password": password,
    }
}

# Stamps.com specification
url = "https://swsim.testing.stamps.com/swsim/swsimv69.asmx?wsdl"
client = zeep.Client(wsdl=url)

# Used Stamps.com example call to expedited the process and minimize typing.
with open("test_label_2.xml") as f:
    data = f.read()

# Convert xml string to dictionary, add credentials and ensure credentials
# in front for CreateIndicium format
data = xmltodict.parse(data)
data = data["CreateIndicium"]
data.update(Credentials)
data.move_to_end("Credentials", last=False)

r = client.service.CreateIndicium(**data)

# Get label/form and print to PDF
response = requests.get(r["URL"])

with open("International_Label.pdf", "wb") as f:
    f.write(response.content)
