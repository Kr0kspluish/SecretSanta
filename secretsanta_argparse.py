from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(
        description="Send an email to each participant of a secret santa \
to tell them who their secret child is."
    )
    
    parser.add_argument("-v", "--verbose", action='count', default=0)
    parser.add_argument(
        "-d", "--dry-run", 
        action='store_true',
        dest='dry_run',
        help="Do not actually send the emails, but do everything else, \
including authentication to Google API."
        )
    parser.add_argument(
        "-a", "--addr-file", 
        action='store', 
        dest='addr_file',
        metavar="addr_file",
        default="addresses.csv",
        help="\
Path to a CSV file containing name and email addresses of the participants. \
Defaults to `addresses.csv`. \
Each line of the file should be in the format `name,email`. \
`name` can contain any special character (including spaces) except comma (,)."
        )
    parser.add_argument(
        "-m", "--message-file", 
        action='store', 
        dest='message_file',
        metavar='message_file',
        default="message.txt", 
        help="Path to a text file containing the message to send. \
Defaults to `addresses.csv`. \
The macros SANTA and CHILD will be replaced with the names of the persons as \
provided in the addresses file."
        )

    return parser.parse_args()