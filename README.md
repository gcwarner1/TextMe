This module sends you an SMS message when your script finishes and lets you know whether it ran successfully or crashed.

Usage:

       textme = textMe(number=yournumber, carrier=yourcarrier)
       textme.run()
       
If you do not have a SMTP server on your network (if you are at the Martinos Center you do) you can use your gmail account
by using:

       textme = textMe(number=yournumber, carrier=yourcarrier, gmail=you@gmail.com, password=yourgmailpassword)
       textme.run()
