#
# Setting up the service on Ubuntu to start automatically using systemd
#
# 1. Create file in /lib/systemd/system named <myservice>.service, with the
#    contents listed below
#
#   $ vi <myservice>.service
#
# 2. Set user and group to root:
#
#   $ sudo chown root:root <myservice>.service
#
# 3. Create a link to the new file in the /etc/systemd/system directory
#
#   $ sudo ln -s /lib/systemd/system/<myservice>.service <myservice.service>
#
# 4. Reload the systemd configurations (always run this step when you update a service
#    configuration file.
#
#   $ sudo systemctl daemon-reload
#
# 5. Test out the new service configuration
#
#   In a separate terminal window, tail the /var/log/syslog file:
#
#       $ sudo tail -f /var/log/syslog
#
#   Start the service:
#
#       $ sudo systemctl start <myservice>
#
#   Check the output of syslog for the status of the service start. Correct any errors.
#
# 6. Enable the service to start automatically on reboot
#
#   $ sudo systemctl enable <myservice>
#
# Available commands to manage service:
#
#   $ sudo systemctl status <myservice>     - report current status of the service
#   $ sudo systemctl start <myservice>      - start the specified service
#   $ sudo systemctl stop <myservice>       - stop/cancel the specified service
#   $ sudo systemctl restart <myservice>    - restart the specified service
#


# ############################################################################# #
# ############################################################################# #
#
# <mservice>.service
#
[Unit]
Description=FRC 1073 Vision Service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=pi

# set the working directory where the main python module resides
WorkingDirectory=/home/pi/GitHub/vision19

# specify the command that used to start the application
ExecStart=python3 visionmanager.py <cmd options>

[Install]
WantedBy=multi-user.target

# ############################################################################# #
# ############################################################################# #
