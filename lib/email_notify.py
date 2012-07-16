def send_email(to_address, from_address, file_names, host):
    """Sends an Email Notification"""
    import smtplib
    from socket import error
    from config import get_config

    header = ("From: %s\r\nTo: %s\r\n" % (from_address, to_address, 'Torrent Tracker'))

    body = str()
    for f in filenames:
        body = body + '%s downloaded\n' % f
    msg = header + body

    try:
        server = smtplib.SMTP(host)
    except Exception, error:
        print "Unable to connect to SMTP server"

    else:
        server.sendmail(from_address, to_address, msg)
        server.quit()
