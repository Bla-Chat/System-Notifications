# System-Notifications
System Notifications for Bla Chat.

This provides system notifications for bla.

## Setup on Linux (Ubuntu + Gnome)

Clone the repo and run the preInstall.sh.
```bash
git clone https://github.com/Bla-Chat/System-Notifications.git
cd System-Notifications
./preInstall.sh
```

Now add the python script to the startup applications.
For that you need to open gnome 'startup applications' and add a new entry.

TODO Image how to open startup applications

The entry you add must be specified as following
```
name: 'Bla Chat'
command: 'python /home/michael/chechout/Bla/System-Notifications/bla-gnome-notify.py'
comment: 'Bla chat notification daemon.'
```

TODO Image how to fill out the dialog.
