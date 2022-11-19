#!/usr/bin/python3

import csv
from random import shuffle

from secretsanta_argparse import parse_args
from secretsanta_email import send_email, gmail_authenticate

# Command-line arguments parsing
args = parse_args()

def vprint(v, *print_args, **print_kwargs):
    """Calls print if the required level of verbosity is met."""
    if(args.verbose >= v):
        print(*print_args, **print_kwargs)


# Read the sender's email address
vprint(1, "Reading the sender email address...", flush=True)
with open('sender_email', 'r') as f:
    sender_email = f.readline()
vprint(1, "Emails will be sent from %s.\n"%sender_email)

# Read participants' email and name
people = []
vprint(1, "Reading addresses from %s..."%args.addr_file, flush=True)
with open(args.addr_file, 'r', newline='') as csv_in:
    reader = csv.reader(csv_in)
    for p in reader:
        people.append({"name":p[0], "email":p[1].strip()})
        vprint(2, "\tFound new person: name=%s, email=%s"%(p[0],p[1].strip()))
vprint(1, "Finished reading addresses.\n")

# Do the random draw. 
vprint(1, "Shuffling the list of participants...", flush=True)
vprint(2, "\tList of participants before shuffle:\n\t",
    '\n\t '.join([str(p) for p in people])
    )
shuffle(people)
vprint(1, "Shuffling done.")
vprint(2, "\tList of participants after shuffle:\n\t",
    '\n\t '.join([str(p) for p in people])
    )
vprint(1)

if args.save_draw:
    with open("draw.txt", "w") as out_f:
        out_f.write("\n".join([p['name'] for p in people]))

# Read the generic message to send to participants.
vprint(1, "Reading the generic message from %s..."%args.message_file, flush=True)
with open(args.message_file, 'r') as message_in:
    message = message_in.read()
vprint(1, "Message successfuly read.")
vprint(2, "The file contains:\n{sep}\n%s\n{sep}".format(sep='-'*40)%message)
vprint(1)

# Authenticate to Google API
vprint(1, "Authenticating to Google services API...", flush=True)
google_session = gmail_authenticate()
vprint(1, "Authentication complete.\n")

# Send the messages
n = len(people)
vprint(1, "Starting to loop on %d participants to send emails..."%n, flush=True)
for i in range(n):
    santa = people[i]
    child = people[(i+1) % n]
    vprint(2, "\tCouple n°%d: santa is \"%s\" and child is \"%s\""%(i, santa['name'], child['name']), flush=True)
    # Customize the message for the given (santa, child) pair
    custom_message = message.replace("SANTA", santa['name']).replace("CHILD", child['name'])
    # Send the email to santa. 
    send_email(
        sender_email,
        santa['email'], 
        args.email_object, 
        custom_message, 
        service=google_session,
        verbose=(args.verbose >= 3),
        dry_run=args.dry_run
    )
    vprint(2, "\tEmail successfuly sent.")
vprint(1, "All emails sent.")