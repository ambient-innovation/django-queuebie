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
