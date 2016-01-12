# System-Notifications
System Notifications for Bla Chat.

This provides system notifications for bla.

## Setup on Linux (Ubuntu + Gnome)

Clone the repo and run the preInstall.sh.
```bash
cd ~/checkout/Bla
git clone https://github.com/Bla-Chat/System-Notifications.git
cd System-Notifications
./preInstall.sh
```

Now add the python script to the startup applications.
For that you need to open gnome 'startup applications' and add a new entry.

![Press start and search for startup applications](https://raw.githubusercontent.com/Bla-Chat/System-Notifications/master/images/StartupApplications.png)

The entry you add must be specified as following
```
name: 'Bla Chat'
command: 'python /home/<youruser>/checkout/Bla/System-Notifications/bla-gnome-notify.py'
comment: 'Bla chat notification daemon.'
```

![Add an entry to the startup applications](https://raw.githubusercontent.com/Bla-Chat/System-Notifications/master/images/EditStartupApplications.png)

Now relog insert your bla chat credentials and enjoy notifications.

![Enjoy the notifications](https://raw.githubusercontent.com/Bla-Chat/System-Notifications/master/images/Notification.png)
