This module sends you an SMS message when your script finishes and lets you know whether it ran successfully or crashed. I built this when I was debugging analyses with multihour runtimes so I didn't have to sit at my desk waiting for my script to crash all day. It let me go grab lunch or take a walk while it was running and I would get a text if it crashed and I needed to go back and check what happened. Very handy in a "work smarter, not harder" kind of way.

Usage:

       textme = textMe(number=yournumber, carrier=yourcarrier)
       textme.run()
       
If you do not have a SMTP server on your network you can use your gmail account
by using:

       textme = textMe(number=yournumber, carrier=yourcarrier, gmail=you@gmail.com, password=yourgmailpassword)
       textme.run()
