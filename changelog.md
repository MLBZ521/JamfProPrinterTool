v1.1.0 = Improved Expected GUI Functionality
+ Updated to Python 3.9.2 and required packages (see requirements.txt)
  * Outside of PySide2, previous requirements should continue to work without changes
  * Notes on PySide2 versions:
    * v5.14.2.3 requires `import _tkinter` on macOS 11 Big Sur (used in v1.0.1 and earlier)
    * v5.15.2 works without issues on macOS 10.14+
    * PySide6 works with five total edits to the script
+ After creating a printer, look it up and add to local list of JPS Printers
+ After deleting a printer, remove from from local list of JPS Printers
+ Sometimes in my original testing, an API call would fail while getting printer details, added some logic to attempt to retry getting the printer one more time -- haven't really been able to test this yet though
+ Improved logic for when buttons should be enabled/disabled
+ Add API error catch for code 409 when attempting to create a printer and the name already exists in Jamf Pro 
+ Updated the QPushButton value name for for the create printers button to match other button name values
* Notated requirements for Big Sur compatibility

v1.0.1 = Numerous fixes
+ Corrected incorrect status code checks on create and update actions (failed to update these after testing for errors)
+ Fixed an encoding issue with xml payloads
+ Corrected the method used on the delete action (failed to revert after testing other logic)
+ Added/updated verbosity that will print to the Jamf Pro Policy Logs

v1.0.0
+ Initial Release