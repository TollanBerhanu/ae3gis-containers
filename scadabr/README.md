# Building ScadaBR image
1. Create a container using ScadaBR dockerfile
2. Open a shell into the container and run the installation script.
3. Exit the container and create a new image from the modified container.

# Starting ScadaBR
*Note: These instructions assume you kept the defaults during the installation*
1. Open a console and run `./ScadaBR_Installer/scadabr.sh start`
2. Open a browser and go to `http://[ScadaBR IP Address]:8080/ScadaBR`
3. Login with username `admin` and password `admin`

# TODO
* Figure out how ScadaBR configures items from the install script so a new dockerfile can be created for ScadaBR.