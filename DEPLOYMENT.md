#Deployment

Deployment is done using [fabric](http://www.fabfile.org/) and is fully automated.

However, it does require some variables and users to be set.

Assuming default locations you need to only add a new user, and set the username/password combination in config.py along with the server IP you're deploying to.
If you do not add this in the config file you will be prompted to do so upon running the `create` command.


You should also set new secret key and password hash to whatever you want it to be.

Once you've done that simply run:

    $ fab create

# Username

After creating a new user on your server, or if you're using the default root one (not recommended) you need to specify the username in two places.

1. In `config/flask_cbr.conf` change the `newuser` to your username.

Hint:

To add new user and add it to the sudo group run:

    $ adduser newuser
    $ adduser newuser sudo
    
*Note:* On Debian and other distros that do not come with `sudo` installed by default you first need to run `$ apt install sudo`

2. In the config.py file in the variable `server_user` enter the user username.


#New password hash and app secret

To generate new password hash and app secret simply run:

    $ python config.py --create_password
    
or

    $ python config.py --create_secret
   
And add the values to the config.py file.

# Different location for cbr-db

By default the cbr-db will be cloned to `/home/flask_cbr/flask_cbr/cbr-db`

If you want to change this you will have to change the location of the project in few places. If not you can skip this section.

1. Change the clone location in the fabfile.py in `install_flask` function to your desired folder.

2. In `flask_cbr.py` in `execute_command` function you will need to change `bankfrom` variable to point to `bankform.py` file.

3. In `gitpull.sh` you will need to `cd` into the `cbr-db` directory for the pull command to work.

4. In `config/flask_cbr` file you will need to specify where the `/downloads` alias leads to for the downloads section to work. 
    
    
#DigitalOcean step by step

1. Create a new droplet, use Debian 8.1 x64 or Ubuntu

2. Login to your droplet `ssh root@your_ip` and enter password or use the ssh key if you provided one.

3. Run the `adduser` commands from the "Username" section above, replace `newuser` in the command with whatever you like

4. Logout.

5. Run `python config.py --create_secret` and enter the new app secret in the `flask_cbr.py file`. Save the file.

6. Run `python configr.py --create_password` and follow the instructions, enter the password in the `flask_cbr.py` file and save it.

7. Open `config/flask_cbr.config` file and change `newuser` to whatever username you picked in step 3.

8. Open `config.py` file and enter the server IP, username, and password you use to access the server.

9. Install `fabric` by running `$ pip install fabric` and run `$ pip install -U paramiko` to ensure you're using latest paramiko.

9a. Run `fab create` in the project root directory (where this file is located). Your flask frontend will be deployed to the server.

10. The `cbr-db` script will be cloned to `/home/flask_cbr/flask_cbr/cbr-db`, however it will **not be configured** read the instructions of that project
in order to configure it properly.

11. Visit the IP/domain of your server and make sure everything is running OK.