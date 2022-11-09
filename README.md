# Secret Santa Helper

`secretsanta.py` is a small helper to organize a secret santa.

### Requirements 

 + A gmail address to send emails to the participants. That sending email 
 address must be written in a `sender_address` file in this folder.
 + An OAuth token to allow access to Google API from the script. The
 credentials should be stored in `credentials.json` in this folder.
 If you don't know what that means, see 
 https://www.thepythoncode.com/article/use-gmail-api-in-python
 that helped me quite a lot.
 + A list of participants (names and email addresses).
 + A message to send.

### Usage

This what is returned by `./secretsanta.py -h`:

```
usage: secretsanta.py [-h] [-v] [-d] [-a addr_file] [-m message_file]

Send an email to each participant of a secret santa to tell them who their secret child is.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -d, --dry-run         Do not actually send the emails, but do everything else, including authentication to Google API.
  -a addr_file, --addr-file addr_file
                        Path to a CSV file containing name and email addresses of the participants. Defaults to `addresses.csv`. Each line of the
                        file should be in the format `name,email`. `name` can contain any special character (including spaces) except comma (,).
  -m message_file, --message-file message_file
                        Path to a text file containing the message to send. Defaults to `addresses.csv`. The macros SANTA and CHILD will be replaced
                        with the names of the persons as provided in the addresses file.
``` 