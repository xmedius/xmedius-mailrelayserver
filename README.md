# XMedius Mail Relay Server 

**This module enables a Windows service (XMedius Mail Relay Server) that can forward emails to different 
SMTP servers according to destination patterns.**

This service can be used to dispatch some of the emails sent by a multifunction device to an XMediusFAX SMTP 
gateway so it is sent as a fax.

# Table of Contents

* [Installation](#installation)
* [Quick Start](#quick-start)
* [Usage](#usage)
* [Configuration Options](#configuration-options)
* [License](#license)
* [Credits](#credits)

# Installation

## Prerequisites

- Python version 3.6
- [pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/) for installed Python version
- One or more XMediusFax SMTP Gateway modules
- Pip updated to its latest version:
  ```
  python.exe -m pip install --upgrade pip
  ```

## Install Package

Run the following command as an administrator:

```
pip install -v https://github.com/xmedius/xmedius-mailrelayserver/tarball/master
```

# Quick Start

To enable the XMedius Relay Server service:

1. Edit the file "$PYTHON_HOME\Lib\site-packages\xmediusmailrelayserver\config.yml" 
   * Change the following values:
       * ```DefaultRelayServer```: the address of your organization SMTP server
       * ```FromAddress```: The SMTP address that will be used to send error notifications
   * Under the Patterns section, associate one or multiple regular expression destination patterns with SMTP 
     servers using this format:
     ```
     Patterns:
       "[0-9]+": [ "xmedius-smtpgateway1.your-domain.com", "xmedius-smtpgateway2.your-domain.com" ]
       ".*": [ "your-organization-smtp-server.your-domain.com" ]
     ```

2. Start the **XMedius Mail Relay Server** service.

# Usage

To use the service to relay mails from a multifunction device, configure the multifunction device to relay all 
emails through the XMedius Mail Relay Server.

# Configuration options

All configuration options are found in the file "$PYTHON_HOME\Lib\site-packages\xmediusmailrelayserver\config.yml".
Editing this file requires restarting the **XMedius Mail Relay Server** service for changes to be taken into 
account.

  * ```Hostname```: the local host name or ip address the relay server will listen on
  * ```Port```: the local port the relay server will listen on
  * ```DefaultRelayServer```: The SMTP relay server that will be used to send bounce e-mails
  * ```FromAddress```: The SMTP address that will be used to send bounce e-mails
  * ```Debug```: Can be set to the value '1' to enable additional logging
  * ```MailRetryInterval```: The number of seconds before retrying when failing to relay a message
  * ```MailRetryTimeout```: The number of seconds before giving up relaying a message
  * ```Patterns```: The list of all destination patterns and their associated SMTP relay server
  

# License

xmedius-mailrelayserver is distributed under [MIT License](https://github.com/xmedius/xmedius-relayserver/blob/master/LICENSE).

# Credits

xmedius-relayserver is developed, maintained and supported by 
[XMedius Solutions Inc.](https://www.xmedius.com?source=xmedius-mailrelayserver)

The names and logos for xmedius-mailrelayserver are trademarks of 
[XMedius Solutions Inc.](https://www.xmedius.com?source=xmedius-mailrelayserver)

![XMedius Logo](https://s3.amazonaws.com/xmc-public/images/xmedius-site-logo.png)
