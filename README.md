# Anonylections

Anonylections is a simply Flask web app that allows you to organise an online election that provides the following properties:
* Voters are assigned unique tokens to vote which aren't stored (who voted what is not visible)
* Voters are provided with a token after voting that allows them to verify their vote has actually been counted

It was originally written for worker council elections in an international organisation where employees from various countries were allowed to vote. This made a paper ballot box impractical to use and hence this tool was born. 


# How does it work?

* The election organiser sets up a new election and adds the valid voting choices
* The election organiser sends out e-mail invitations to those who are eligable to vote with a unique token per voter. Which voter receives which token is not stored
* The election organiser opens the elections
* The voter clicks on the link in the mail and casts their vote 
* The voter receives a unique number that allows them to check their vote
* The election organiser closes the votes when the time is up and shares the results
* The voter can check if their unique code is indeed represented in the election results.

The election organiser can choose to show the results to the voter directly after voting or wait until the elections are over.

# Is this truly anonymous?

Considering the code is not modified from the above described behaviour it would still be possible for a network administrator to keep track of which machine in the network cast which vote. If this is a concern, consider using the Tor browser to hide your network identity.

# Caveats

People could potentially game the system by saying they never received their token (since the system doesn't store this). Should problems with tokens arise it is best to discard the election with problems and organise a new election and verify everyone who needs to vote received their token.

# Requirements

See requirements.txt

# Config

Make sure to enter valid mail server credentials in the config.py file otherwise you cannot send mail :)

# Default login

The default credentials are admin/admin

# Docker easy run 

Download and run:

```docker-compose up --build```

Note that this uses the flask built-in webserver so not suitable for production environments.
The application will run on port 5000 by default.
