# XMedius Mail Relay Server 

**This module enables a Windows service (XMedius Mail Relay Server) that can 
forward emails to different SMTP servers according to destination patterns.**

For example, this service can be used to dispatch some of the emails sent from
a multifunction printer (MFP) in order to send them as faxes through XMediusFAX
(SMTP Gateway) when the destination is a fax number instead of an email address.

# Table of Contents

* [Installation](#installation)
* [Quick Start](#quick-start)
* [Configuration Options](#configuration-options)
* [License](#license)
* [Credits](#credits)

# Installation

## Prerequisites

- Python version 3.6 (minimum)
- [pywin32](https://sourceforge.net/projects/pywin32/files/pywin32/) for
  installed Python version
- Pip updated to its latest version:
  ```
  python.exe -m pip install --upgrade pip
  ```

## Install Package

Run the following command as an administrator:

```
pip install -v https://github.com/xmedius/xmedius-mailrelayserver/tarball/master
```

# Quick Start (Example: Faxing from MFP)

**Note:** This explains how to use the XMedius Relay Server in order to allow
users to scan & send faxes from a Multifunction Printer (MFP) through XMediusFAX
when the destination entered on the MFP consists of digits (i.e. is intended to
be a fax number). It is assumed that:
 * The MFP has the functionality to send scanned documents by email
 * One or more XMediusFAX SMTP Gateway modules are installed

To enable this scenario:

1. Edit the file "$PYTHON_HOME\Lib\site-packages\xmediusmailrelayserver\config.yml"
   * Change the following values:
       * ```DefaultRelayServer```: the address of your organization SMTP server
       * ```FromAddress```: The SMTP address that will be used to send error
         notifications
   * Under the "Patterns" section, associate one or multiple regular expression
     destination patterns with SMTP servers using this format:
     ```
     Patterns:
       "[0-9]+": [ "xmediusfax-smtpgateway1.your-domain.com", "xmediusfax-smtpgateway2.your-domain.com" ]
       ".*": [ "your-organization-smtp-server.your-domain.com" ]
     ```

2. Start the **XMedius Mail Relay Server** service.
3. Configure the MFP to send all emails through the XMedius Mail Relay Server.

# Configuration options

All configuration options are found in the file 
"$PYTHON_HOME\Lib\site-packages\xmediusmailrelayserver\config.yml".
Editing this file requires restarting the **XMedius Mail Relay Server** service
for changes to be taken into account.

Option                   | Description
-------------------------|----------------------------
```Hostname```           | The local host name or ip address the relay server will listen on.
```Port```               | The local port the relay server will listen on.
```DefaultRelayServer``` | The SMTP relay server that will be used to send bounce e-mails.
```FromAddress```        | The SMTP address that will be used to send bounce e-mails.
```Debug```              | Can be set to the value '1' to enable additional logging.
```MailRetryInterval```  | The number of seconds before retrying when failing to relay a message.
```MailRetryTimeout```   | The number of seconds before giving up relaying a message.
```Patterns```           | The list of all destination patterns and their associated SMTP relay server.
 
**Advanced Configurations:**
 * If you have more than one XMediusFAX SMTP Gateway installed, you can use
   pattern definitions for:
   * High-availability (specify several SMTP Gateways separated by commas for
     a single pattern), and
   * Load-balancing (split patterns into several ranges assigned to different
     SMTP Gateways).
 * If any of the destination SMTP servers (company server or SMTP Gateway) is
   listening on non-standard smtp port
(default: 25), use the syntax "```server.domain.com:port```".

# License

xmedius-mailrelayserver is distributed under [MIT License](https://github.com/xmedius/xmedius-mailrelayserver/blob/master/LICENSE).

# Credits

xmedius-mailrelayserver is developed, maintained and supported by 
[XMedius Solutions Inc.](https://www.xmedius.com?source=xmedius-mailrelayserver)

The names and logos for xmedius-mailrelayserver are trademarks of XMedius Solutions Inc.

![XMedius Logo](https://s3.amazonaws.com/xmc-public/images/xmedius-site-logo.png)
