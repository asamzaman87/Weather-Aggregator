# Weather Aggregator
Weather Aggregator is an application which displays weather information and news for a particular region

## Setup
### Download Code
Open up your IDE and open the terminal. Copy and paste the command below

`git clone https://github.com/asamzaman87/Weather-Aggregator.git`

Follow the prompts and save the resulting folder in the directory that you want.

Open the folder in your IDE to create a new project

### Download the Requirements and Database
Run the following command to download all requirements into your virtual environment

`pip install -r requirements.txt`

This will download the framework and all other APIs needed to run the webapp

#### Database
Will add database information here once discussed!

### How to Commit New Code

    1. git add .
    2. git commit -m "[enter your message here]"
    3. git pull
    4. git push

#### Step 1

The first step is to add your changes. To check all the files you changed/added/deleted, run the following command:

`git status`

This will list all of you changed files. If you want to only add changes from a specific file use the following command:

`git add filename.txt`

If you want to add all of your changes, use the following command:

`git add .`

You can use `git status` again to check that the files you have added are under the _Changes to be committed_ group

#### Step 2
 
The next thing you want to do is package your changes to be sent to the repository. Use the command below:

`git commit -m "[enter your message here]"`

This will start your commit. the `-m` flag means you are attaching a message, _which is required for all commits_. 
Replace the `[enter your message here]` with a short message on the content of your changes

#### Step 3

Once your changes are committed, you can pull changes from the repository online. This can be done with the command below:

`git pull`

Once changes are pulled in, you will be able to see the most recent version of the repository in your IDE

#### Step 4

The final step is to push your changes to the repository. This can be done with the command below:

`git push`

If it is asking you for a username and password, enter your github username and a personal access token. 

_Note: If you want to skip the credential check, you can log into github on your IDE or set up an SSH token. 
Then you won't be prompted to enter credentials during every push_

#### Example

    1. git add homepage.html
    2. git commit -m "added new homepage"
    3. git pull
    4. git push

