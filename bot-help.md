### All User commands:
- `$Help` - Provides a link to this page.
- `$Roll` - rolls a D6.
- `$Roll {n}d{s}` - rolls a `n` dice with `s` sides. For example `$roll 2d6` or `$roll 1d3`.
- `$Flip` - Flips a coin.
- `$Timezones` - Lists timezones available for the timezone converion commands.
- `${timezone}` - Converts a time to designated Timezone. For example `$CEST 09:00 PDT` will convert the 09:00 CEST to Pacific Daylight Time, `$NZST 12:00 ACDT` will conver 12:00 NZST to ACDT. Times must be in the format `hh:mm`. 
- `$GitHub` - Provides a link to Thom's [GitHub](https://github.com/LarnuUK).
- `$Timer` - Sets a timer for the requested time period. Time must in the format `hh:mm`. For example - `$Timer 03:00` will set a timer for 3 hours. Can optionally be followed by a message. On expiry the user who created it will receive a ping.
- `$Events` - Give a list of ongoing and upcoming events on the server.
- `$EventDetails` - Gives full information on a specific event on the server. Must be followed by the event's unique ID. For example `$EventDetails 101`.
- `$GermanPairing` - Initiates a three player team pairing process against a mentioned user using the German Pairing Method. For example `$GermanPairing @Ryan`. You will first be asked if won the roll off, so please ensure you roll off for who picks the table first. Can only be used in table channels.

*With the exception of `$heret`, the following commands must be used in a bot channel.*

### Head Judge Commands:
- `$heret` - Sets a timer for the requested time period. Time must in the format `hh:mm`. Must be followed by a message. For example `$heret 01:30 Dice down!`. On expiry the @here role will be pinged.
- `$AddEvent` - Create an event on the server. Needs to be followed by a name for said event. For example `$AddEvent 50pt Steamroller`
- `$AddEventDetail` - Add a detail to an existing event. Must be followed by the event's unique ID. For example `$AddEventDetail 101`.
- `$EditEvent` - Edit the property of an event (not a detail). Must be followed by the event's unique ID. For example `$EditEvent 101`.
- `$DeleteEvent` - Delete an event. ust be followed by the event's unique ID: For example `$DeleteEvent 101`.
- `$DeleteDetail` - Delete an event's detail. ust be followed by the detail's unique ID: For example `$DeleteEvent 234`.
- `$AddCaptain` - Grants a user the Team Captain Role related to that server. Must be followed by a mentioned user. For example `$AddCaptain @Barry`.

### Server Administrator Commands:
- `$AddRoleAccess` - Gives a role an access level on the bot. Must be followed by a valid role/mentioned role: for example `$AddRoleAccess Team Captain`.
- `$RemoveRoleAccess` - Removes access levels on the bot for a role. Must be followed by a valid role/mentioned role. For example `$RemoveRoleAccess Team Captain`.
- `$CheckRoleAccess` - Confirms the access level on the bot for a role. Must be followed by a valid role/mentioned role. For example `$CheckRoleAccess Team Captain`.

### VTC Server Only Commands *(Can only be used by the Server Owner on the VTC Server)*: 
- `$LimitVCs` - Limits the maximum users who can connect to a game VC to 4.
- `$UnlimitVCs` - Removes to limit to the maximum users who can connect to a game VC.
- `$OpenServer` - Allows everyone to access the table text and voice channels
- `$CloseServer` - Removes everyone to access the table text and voice channels