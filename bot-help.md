## [Commands](#commands) {#commands}
Below are a the currently available commands Corgi has.

### [All User commands](#user) {#user}
- `$Help` - Provides a link to this page.
- `$Roll` - rolls a D6.
- `$Roll {n}d{s}` - rolls `n` dice with `s` sides. For example `$roll 2d6` or `$roll 1d3`.
- `$QuantumRoll` - rolls a D6. *Uses Quantum numbers. For the non-beleivers.*
- `$QuantumRoll {n}d{s}` - rolls `n` dice with `s` sides. For example `$roll 2d6` or `$roll 1d3`. *Uses Quantum numbers. For the non-beleivers.*
- `$Flip` - Flips a coin.
- `$Timezones` - Lists timezones available for the timezone converion commands.
- `${timezone}` - Converts a time to designated Timezone. For example `$CEST 09:00 PDT` will convert the 09:00 CEST to Pacific Daylight Time, `$NZST 12:00 ACDT` will conver 12:00 NZST to ACDT. Times must be in the format `hh:mm`. 
- `$GitHub` - Provides a link to Thom's [GitHub](https://github.com/LarnuUK).
- `$Timer` - Sets a timer for the requested time period. Time must in the format `hh:mm`. For example - `$Timer 03:00` will set a timer for 3 hours. Can optionally be followed by a message. On expiry the user who created it will receive a ping.
- `$Events` - Give a list of ongoing and upcoming events on the server.
- `$EventDetails` - Gives full information on a specific event on the server. Must be followed by the event's unique ID. For example `$EventDetails 101`.
- `$GermanPairing` - Initiates a three player team pairing process against a mentioned user using the German Pairing Method. For example `$GermanPairing @Ryan`. You will first be asked if won the roll off, so please ensure you roll off for who picks the table first. Can only be used in table channels.
- `$loscheck` - Initiates a volumetric LOS check. The bot will prompt you with questions and then provide an image to demonstrate the LOS. Can only be used in table channels.

*With the exception of `$heret`, the following commands must be used in a bot channel.*

- `$LeaveTeam` - Leave a team you are a member of. If you are a Captain of the team, you will need to assign another player as the Captain first.
- `$FetchScores` - Get the leader board for the Fetch easter egg minigame.

### [Team Captain Commands](#captain) {#captain}
- `$CreateTeam` - Create a Team with the provided name. For example `$CreateTeam The Speedy Turtles`
- `$TeamColour` - Changed the colour of your Team! Use `$Colours` for supported colours.
- `$AddPlayer` - Adds a player to a team. Must be followed by a mentioned user. For example `$AddPlayer @Dean`.
- `$RemovePlayer` - Removes a player from a team. Must be followed by a mentioned user. For example `$RemovePlayer @Dean`.
- `$RegisterTeam` - Register a team for a Team Event. Must be followed by an event ID. For example `$RegisterTeam 101`. If the event permits it, channels for the team will be created.
- `$DeregisterTeam` - Deregister a team for a Team Event. Must be followed by an event ID. For example `$DeregisterTeam 101`.
- `$RenameTeam` - Renames one of the teams you are a Captain of. Must be followed by a new Team name. For example `$RenameTeam The slow Cheetahs`.
- `$AssignCaptain` - Change the acting Captain of a Team from yourself to another. Must be followed by a mentioned user. For example `$AssignCaptain @Thom`. If the Player is not a part of your team, they will be added to it.
- `$DeleteTeam` - Delete a team you are a captain of. Options will be presented to you. This action **cannot** be undone if committed.


### [Head Judge Commands](#headjudge) {#headjudge}
- `$heret` - Sets a timer for the requested time period. Time must in the format `hh:mm`. Must be followed by a message. For example `$heret 01:30 Dice down!`. On expiry the @here role will be pinged.
- `$AddEvent` - Create an event on the server. Needs to be followed by a name for said event. For example `$AddEvent 50pt Steamroller`
- `$AddEventDetail` - Add a detail to an existing event. Must be followed by the event's unique ID. For example `$AddEventDetail 101`.
- `$EditEvent` - Edit the property of an event (not a detail). Must be followed by the event's unique ID. For example `$EditEvent 101`.
- `$DeleteEvent` - Delete an event. Must be followed by the event's unique ID: For example `$DeleteEvent 101`.
- `$DeleteDetail` - Delete an event's detail. ust be followed by the detail's unique ID: For example `$DeleteEvent 234`.
- `$AddCaptain` - Grants a user the Team Captain Role related to that server. Must be followed by a mentioned user. For example `$AddCaptain @Barry`.
- `$RemoveCaptain` - Removes the Team Captain Role related to the server from the User. Must be followed by a mentioned user. For example `$RemoveCaptain @Barry`. If the Captain has made any teams, a new Team Captain will be assigned. If they have any teams that only they are part of, they will be deleted.

### [Server Administrator Commands](#admin) {#admin}
- `$AddRoleAccess` - Gives a role an access level on the bot. Must be followed by a valid role/mentioned role: for example `$AddRoleAccess Team Captain`.
- `$RemoveRoleAccess` - Removes access levels on the bot for a role. Must be followed by a valid role/mentioned role. For example `$RemoveRoleAccess Team Captain`.
- `$CheckRoleAccess` - Confirms the access level on the bot for a role. Must be followed by a valid role/mentioned role. For example `$CheckRoleAccess Team Captain`.

## [Inviting Corgi](#inviting) {#inviting}
If you want Corgi on your own server, you can invite him [here](https://discord.com/api/oauth2/authorize?client_id=721707690124115991&permissions=2650275409&scope=bot). Note, however, that as the bot is set up primarily for Fishcord and the VTC it has certain expectations of the server that are currently hard coded. For the time being, a text channel called "corgi-logs" must exist, for the bot to place its logs, and commands noted as only working in a "bot" or "table" channel will only work in channels where the channel's name begin with "bot" and "table" respectively.