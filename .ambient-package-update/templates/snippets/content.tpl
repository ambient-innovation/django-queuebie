## Features

* Split up your business logic in commands and events
* Commands are imperatives telling your system what to do, events reflect that something has happened
* Register light-weight functions via a decorator to listen to your commands and events
* Message handlers receive the context of the message (command or event), providing an explicit API
* No magic, no side-effects since the queue works synchronously
