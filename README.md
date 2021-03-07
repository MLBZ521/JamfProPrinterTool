JamfProPrinterTool
======

An App that allows Site Admins to manage printers "assigned" to their Site(s) in Jamf Pro.

<center><img src="https://github.com/mlbz521/JamfProPrinterTool/blob/master/Jamf Pro Printer Tool.png" /></center>


## About

This application utilizes Python and the Qt for Python Library to create a GUI that allows Site Admins to provide full life-cycle management of their printers without needing assistance from Full Jamf Pro Admins.  They are able to Create, Update, and Delete printers within Site(s) they have permissions too.  In addition, they can review the printer configurations, both local and how they are currently configured in Jamf Pro.

Obviously this functionality is not built into Jamf Pro, so to "assign" printers to Sites, I am "tagging" printers to the Site that they "belong" too.  To accomplish this, I am nesting a JSON object within the Notes field.  It's slightly hacky, but it works!

So, for existing printers, Site Admins would need to request printers to be assigned to the Sites that they should be assigned too.


## Details

I took this approach so that I could pass an authorized set of credentials that would be able to utilize the Jamf Pro Classic API to be able manage Printers within Jamf Pro.

This is my first project of this type and scale with Python as well as my first use of Qt for Python (PySide2).  I believe I've tried to follow all best practices with PySide2 and have added proper flow control and threading.  I have also included multi-threading when querying for each printer from Jamf Pro.  In my environment with slightly over 400 printers at the current time, this reduced the lookup period from over 3.5 minutes to under thirty seconds (on a Mac with twelve cores).

All that said, it's not perfect and I'm sure there are improvements to be had.


## Planned Features / Contributing

Feature Requests and Pull Requests are welcome.  Feel free to contribute!

These are the current items I plan to add based on functionality I did not implement before releasing and feedback from my Site Admins:
  * ~After creating a printer, add to local list~
    * Added!
  * ~After deleting a printer, remove from local list~
    * Added!
  * ~Retry getting a printers' details if the API call fails~
    * Added!  (I think?  Hard to test this.)
  * Editable Device Details (update without having local printer of same name)
  * ? Client side verbosity/debugging (GUI Enabled) ?

##  Requirements

The latest version of the script was tested using Python 3.9.2, but I believe most Python 3 versions should be supported.

This tool requires the following packages and their dependencies:
  * cryptography
  * PySide2
    * v5.14.2.3 requires `import _tkinter` on macOS 11 Big Sur
    * v5.15.2 works without issues on macOS 10.14+
    * PySide6 works with five total edits to the script
  * requests

Please see the requirements.txt file for additional information.


## How to setup

Obviously, Python 3 and the above required Libraries will be required on any system that runs this script.  You can deploy a relocatable Python framework to support this.  See Greg Neagle's [Relocatable Python Framework](https://github.com/gregneagle/relocatable-python) and the [MacAdmins Python](https://github.com/macadmins/python) for details.

Then you'll need a Jamf Pro Account with CRUD to the Printer Object type.

I encrypt the credentials using the cryptography.fernet module.  To encrypt your credentials:

```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

encoded_username = "<username>".encode()
encoded_password = "<password>".encode()

encrypted_username = f.encrypt(encoded_username)
encrypted_password = f.encrypt(encoded_password)

print("key:  {}".format(key))
print("encrypted_username:  {}".format(encrypted_username))
print("encrypted_password:  {}".format(encrypted_password))
```

Simply pass these strings as Script Parameters in a Policy, and you're good to go.

Parameters:
  * `[ --api-username | -u ] API_USERNAME`
  * `[ --api-password | -p ] API_PASSWORD`
  * `[ --secret | -s ] SECRET`

Test locally by:

  * `sudo ./PrinterTool.py -s 'encryption_key' -u 'encrypted_username' -p 'encrypted_password'`


## Licensing Information

The code that generates the "Jamf Pro Printer Tool" is licensed under the MIT License.

This application utilizes the Qt Framework (specifically PySide2) to generate the GUI portion of the application.  Qt and Qt for Python (PySide2) are licensed under the GNU (L)GPLv3.  Please see [qt.io/licensing](https://qt.io/licensing) for an overview of Qt licensing.

The current image used in this project is property of Jamf.
