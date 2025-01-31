# Motivation

You might wonder what's the USP for this package. Messages (event) queues are usually async and use a broker, etc.

The main goal is to provide a way to separate your domains in Django and reduce coupling between domains or Django apps.

So why should you use "django-queuebie"?

* Thinking in commands and events splits up your business logic from one big chunk to manageable sizes
* Handlers are function-based with a defined input (the context), they are predictable and easy to test
* Decoupling different parts of your application by listening to events instead of imperative programming
* Avoid putting business logic in your view layer since it has to live inside a handler function
* Creates an explicit pattern for connecting services (places of different business logic) instead of chaining them
  individually

# Why not Django signals?

The reader might think "Hey, sync queues in Django? I already have this!" — and that's true, somehow.

The key differences are mostly on a semantic level.

First, commands and events are a concept that doesn't exist for Django signals. They provide a proven way of separating
your business logic, and in addition, provide a basis for discussion with non-technical folks.

Furthermore, queuebie messages (commands and events) don't belong to a model. Models represent the way you store your
data. That's not necessarily the best way to structure your custom logic. So by using signals, you're strongly primed to
think in models, meaning database structure, and not in domain concerns.

Messages provide an explicit context via a dataclass which can be interpreted as an explicit internal API to communicate
between your domains. That's a huge plus since explicit is better than implicit.
