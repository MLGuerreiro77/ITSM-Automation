# ITSM Automation

### ⚠️**DISCLAIMER**⚠️
I´d like to inform that this script was created for studying purposes only! Please take care before use this on your **production environment!** This script may not work on your environment since we may be working in different situations or even other ITSM tools. My intention is to learn and improve my Python and Cisco automation skills.
For security and ethical reasons, the line of code where we would set the URL is fake


This automation is built mainly with Python´s Selenium library and is far for being perfect. I used it to close some events and once it worked, it became very helpful. A folder with the "*Firefox/geckodriver*" is provided and must be on same folder of the main script. Again, the script is very simple to use and also is not complex in terms of coding since I´m not a programming guy.

### **INSTRUCTIONS**
Paste some event number on file *"eventos.txt"* following the examples on the same file.
The script has 2 modes of operation: one showing the Firefox web browser and the other hiding it. This can be setting by hiding/unhiding the following code:

```python
# Bloco headless
'''
options = Options()
options.add_argument("--headless")
firefox_driver = "C:\Python\Webdrivers\geckodriver.exe"
driver = webdriver.Firefox(options=options)
'''
#Bloco normal head
firefox_options = Options()
firefox_driver = "C:\Python\Webdrivers\geckodriver.exe"
driver = webdriver.Firefox()
# Maximizar janela
driver.maximize_window()
```
Note the headless block is comented. So, the web browser will be shown.

At this point, 2 templates are used for ticket closure. So a simple menu will be presented for you to choose:

1. *Event was closed during troubleshooting*
2. *Event is being treated on other event*

The only valid point here is the second option that in case you choose it, the user will prompted to inform the secondary event and this will be printed with the event closure info.

Finally, when the script is running, the terminal will present the events succesfully closed or not.

Thank´s for visiting my page!
🙂