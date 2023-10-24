#!/usr/bin/python

"""Notifies myself of IP change. Originally from https://gist.github.com/steven-chau/dec34ceee36321f0db9a139591ffdb19."""
import smtplib, ssl
import requests
import os

# Import the email modules we'll need
from email.mime.text import MIMEText

ADDRESS_FILE = '/tmp/old_ip_address.txt'


def notify_ip_change(newIp):
    msg = MIMEText("Alert! The server's IP has changed to %s" % newIp)

    # updated to use iCloud
    context = ssl.create_default_context()
    sender_email = "johnnyappleseed@mac.com"                    # this is who we actually are
    sender = "admin@my_custom_domain.me"                        # this is who we appear to be (i.e. custom domain email)
    receiver_email = "johnnyappleseeds_brother@mac.com"         # this is to who we have sent the email
    smtp_server = "smtp.mail.me.com"
    password = "app-specific-password-here"                     # https://support.apple.com/en-ca/102654 for more information
    port = 587  # For SSL

    #recipient = 'receiver@example.com'
    msg['Subject'] = 'Alert - IP address has changed'
    msg['From'] = sender
    msg['To'] = receiver_email

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

# [notify_if_change ends]


def detect_ip_change():
    blnDelta = False
    currIp = requests.get('https://api.ipify.org').text

    if not os.path.isfile(ADDRESS_FILE):
        # trigger the script to send email for the first time
        persist_ip('127.0.0.1')

    oldIp = read_old_ip()

    if currIp != oldIp:
        blnDelta = True

    persist_ip(currIp)
    return (blnDelta, currIp)
# [detect_ip_change ends]


def persist_ip(ip):
    f = open(ADDRESS_FILE, 'w')
    f.write(ip)
    f.close()
# [persist_ip ends]


def read_old_ip():
    f = open(ADDRESS_FILE, 'r')
    oldIp = f.read()
    f.close()
    return oldIp
# [read_old_ip ends]


# [START main]
def main():
    deltaTuple = detect_ip_change()
    if deltaTuple[0] is True:
        notify_ip_change(deltaTuple[1])
        print ("IP changed. Email sent!")
    else:
        print ("No news is good news.")
# [END main]


if __name__ == '__main__':
    main()