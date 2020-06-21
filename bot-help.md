**All User commands:**
$Roll - rolls a D6.
$Flip - Flips a coin.
$GitHub - Provides a link to Thom's github.
$Timer - Sets a timer for the requested time period. Time must in the format `hh:mm`. For example `$Timer 03:00` will set a timer for 3 hours. Can optionally be followed by a message. On expiry the user who created it will receive a ping.

The following commands can only be used in #bot-commands (except `$heret`):

$Colours: Returns a list of predefined colours for teams.

**VTC Committee only commands:**
$AddCaptain - Gives a user the Team Captain Role. Must be followed by a mentioned user: for example `$AddCaptain @Larnu#1860` (You cannot make a user who already has a role a Team Captain).
$AddJudge - Gives a user the Judge Role. Must be followed by a mentioned user (You cannot make a user who already has a role a Judge).
$AddHeadJudge - Gives a user the Head Judge and Judge Roles. Must be followed by a mentioned user (You cannot make a user who already had a role a Judge). Please note this will also error if you try to give a Judge the Head Judge Role *(This might be fixed. Work around it to remove the Judge Role and give the Head Judge.)*
$RemoveJudge - Removes a user from the (Head) Judge Role(s).
$AddStreamer - Gives a user the Streamer Roler. Must be followed by a mentioned user (You cannot make a user who already have a role a Judge).
$RemoveStreamer - Removes a user from the Stream Role.
$heret - Sets a timer for the requested time period. Time must in the format `hh:mm`. Must be followed by a message. For example `$heret 01:30 Dice down!`. On expiry the @here role will be pinged.

-----

**Team Captain only commands:**
$TeamName - Creates, or renames your Team's role in the server, along with it's channel category. If it does, it will rename the role and category. For example `$TeamName The Speedy Turtles`
*The following commands can only be used once you have created your team using `$TeamName`*
$TeamColour - Sets the colour for team's role. Must be 6 digit hex or a predefined colour. Use `$colours` for the list. For example `$TeamColour c29949` or `$teamcolour blue`. You can use a site like <https://htmlcolorcodes.com/color-picker/> to find a colour you like.
$AddPlayer - Adds a user to your Team Role. Must be followed by a mentioned user: for example `$AddPlayer @ryanwillmott923#0436`. You cannot add a User who is a member of another team to your team.
$RemovePlayer  - Removes a user to your Team Role. Must be followed by a mentioned user: for example `$RemovePlayer @ryanwillmott923#0436`

Adding/Removing a user from your team's role will grant/remove their access rights to your team's channel and category, as well as the tables while the server closed is to everyone during an event.