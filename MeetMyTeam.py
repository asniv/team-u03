"""
4. My Team

Let's get to know our team a bit better and Create a text file (team.txt) in a project team repository that all team members have access to. Each team member should add four lines to the text file in the following format.

Jane Groot {jgroot@address.edu}
Jane Groot {senior}
Jane Groot My interests include {this, that, the_other_thing}
Jane Groot I am committed to me and my team members learning Python

Where Jane is the student’s first name and Groot is the student’s last name. If there are three team members, for example, there should be 12 lines. After the first member creates, populates, and adds the text file, other members should add their lines to the file and push the newer version into the project repository. Don't shortcut this step and have one student enter in all the information. Our goal is to start to learn how to work together on a file. Note that the curly brackets ‘{‘ and ‘}’ are included in the text file.

When this is done, each team member should pull the text file and fill in the function MeetMyTeam() that imports the text file and prints the following report on the file:

Number of team members: <#>
Number of team members committed to helping the team learn python: <#>
Their collective list of interests in alphabetical order include: <robotics, that, the_other_thing, this>
Team members in alphabetical order: <first name>, <first name>, <first name>

Note that we will use a fictitious but valid team file to check that each student's function is working correctly. Our file will be syntactically correct, but may contain any number of team members and those members may have any number of interests greater than zero. The interests should all be one word. The word 'and' should not be listed among the interests. The triangular brackets < > should not be included in your answer. <#> should be replaced by the correct answers with no brackets in the output. The collective list of interests should be a unique list, so if two team members have the same interest it should only be listed once.

The alphabetical lists should be CASE SENSITIVE so in a list containing apple and Axle, when sorted Axle would come before apple.
"""


def MeetMyTeam():
    # read file and store in list for adjustment
    f = open('team.txt', 'r') # open text file
    t = list(f) # store contents of team file as a list before we finalize formatting

MeetMyTeam()
