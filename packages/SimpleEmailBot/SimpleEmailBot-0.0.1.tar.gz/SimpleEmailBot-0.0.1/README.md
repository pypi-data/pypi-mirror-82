# SimpleEmailBot
SimpleEmailBot is a very simple Python package to 
send an email when a script is completed. I use 
this mainly to let me know when deep 
learning models have finished training. 

## Install
SimpleEmailBot is on pip, just run
```
pip install simpleemailbot
```
## Usage

### Bot email
First you need an email for the bot, currently this 
only works with gmail so make a new gmail account [here](https://accounts.google.com/signup).
You also need to go to settings and set allow less secure apps to ON. [Link](https://myaccount.google.com/lesssecureapps). Be careful because this makes the account less secure, that's why we want to 
make a new account. Make sure you are doing this with the new account and not your own gmail also. 

### Secrets
Now you need to put the username and password in a file somewhere
so that they don't end up in your code. This is done with a file at `~/.emailbot`
which is tab separated and contains an identifier, the email address and the password.
e.g.


```bot    mybot@gmail.com password123```

**Make sure you use tabs and not spaces**.
Also you should run `chmod 600 ~/.emailbot`. This 
makes sure only you have read and write permissions.
You can change where the secrets are 
kept with `EmailBot.set_secrets_path()`
### Code
No more setup to do now, here is an example usage.

```python
from simpleemailbot import EmailBot
# bot is the identifier in the secrets file
# don't put anything that identifies the email or password in your code
bot = EmailBot("myemail@gmail.com", "bot")

bot.email_me()
```
This sends an email to myemail@gmail 
with the subject "Task Complete" and the content "Task Complete".

If you want you can change the subject and message:
```python
bot.email_me(subject="Error", message="Oh no something went wrong!")
```