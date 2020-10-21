**All User commands:**
`$Roll` - rolls a D6.
`$Roll {n}d{s}` - rolls a `n` dice with `s` sides. For example `$roll 2d6` or `$roll 1d3`.
`$Flip` - Flips a coin.
`$Timezones` - Lists timezones available for the timezone converion commands.
`${timezone}` - Converts a time to designated Timezone. For example `$CEST 09:00 PDT` will convert the 09:00 CEST to Pacific Daylight Time, `$NZST 12:00 ACDT` will conver 12:00 NZST to ACDT. Times must be in the format `hh:mm`. 
`$GitHub` - Provides a link to Thom's github.
`$Timer` - Sets a timer for the requested time period. Time must in the format `hh:mm`. For example `$Timer 03:00` will set a timer for 3 hours. Can optionally be followed by a message. On expiry the user who created it will receive a ping.

The following commands can only be used in #bot-commands (except `$heret`):

$Colours: Returns a list of predefined colours for teams.

-----

**Team Captain only commands:**
`$TeamName` - Creates, or renames your Team's role in the server, along with it's channel category. If it does, it will rename the role and category. For example `$TeamName The Speedy Turtles`
*The following commands can only be used once you have created your team using `$TeamName`*
`$TeamColour` - Sets the colour for team's role. Must be 6 digit hex or a predefined colour. Use `$colours` for the list. For example `$TeamColour c29949` or `$teamcolour blue`. You can use a site like <https://htmlcolorcodes.com/color-picker/> to find a colour you like.
`$AddPlayer` - Adds a user to your Team Role. Must be followed by a mentioned user: for example `$AddPlayer @ryanwillmott923#0436`. You cannot add a User who is a member of another team to your team.
`$RemovePlayer`  - Removes a user to your Team Role. Must be followed by a mentioned user: for example `$RemovePlayer @ryanwillmott923#0436`

Adding/Removing a user from your team's role will grant/remove their access rights to your team's channel and category, as well as the tables while the server closed is to everyone during an event.

-----

**Server Administrator:**
`$AddRoleAccess` - Gives a role an access level on the bot. Must be followed by a valid role/mentioned role: for example `$AddRoleAccess Team Captain`.
`$RemoveRoleAccess` - Removes access levels on the bot for a role. Must be followed by a valid role/mentioned role: for example `$RemoveRoleAccess Team Captain`.
`$CheckRoleAccess` - Confirms the access level on the bot for a role. Must be followed by a valid role/mentioned role: for example `$CheckRoleAccess Team Captain`.
`$heret` - Sets a timer for the requested time period. Time must in the format `hh:mm`. Must be followed by a message. For example `$heret 01:30 Dice down!`. On expiry the @here role will be pinged.

-----

**Server Owner Only Commands** *(Can only be used by the Server Owner)* **:** 
`$ResetTeams` - Purges all current teams, along with their Categories and Channels, removes all users from the Team Captain Role and then Opens the Server. *This action cannot be undone. It will ask you to confirm the action before it is completed.*

**VTC Server Only Commands** *(Can only be used by the Server Owner on the VTC Server)* **:** 
`$LimitVCs` - Limits the maximum user who can connect to a game VC to 4.
`$UnlimitVCs` - Removes to limit to the maximum user who can connect to a game VC.
`$OpenServer` - Allows everyone to access the table text and voice channels
`$CloseServer` - Removes everyone to access the table text and voice channels