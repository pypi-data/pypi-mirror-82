# Alectio Key Management package
This package is used to manage alectio authorization token, that is needed to run AlectioSDK and AlectioCLI
 
#### Installation
```console
pip install alectio-kms
```
make sure that the pip binary is also accessible for sudo/root user. That is use pip outside any of your virtual environment.
 
One the package is installed run:
```console
sudo alectio-kms
```
Upon running the package it will walk you through to get you keys setup
If you have not already created your Client ID and Client Secret then do so by visiting:
1. open https://auth.alectio.com
2. Login there and click 'Create Client' Link, only change Name in the form and leave everything as is
3. Click submit
4. Now you should have you Client ID and Client Secret
You will use them in the terminal where you are running alectio-kms
After you have entered your Client ID and Client Secret, it will open a web browser where you will authenticate yourself.
Upon successful authentication your Client ID, Client Secret and Auth Token will be save at /opt/alectio and will
also be outputted in your terminal.
 

