Githubly
===================


A simple CLI to get github issues of a repo

----------


How to run?
-------------

Follow below steps to run

> **Note:**

> - git clone project.
> - Create and activate virtualenv.
> - Do 'pip install -r requirements.txt'.
> - Run by 'python githubly.py'.
> - Follow on screen instructions.

Example
-------------

A sample 

> **Note:**

> (venv) Kumarans-MacBook-Air:githubly kumaran$ python githubly.py
>Githublyyyyyyyyyyyyyyyyyyyyy
>Please enter your github username, password below. This is needed to avoid >github's rate limitation.
>Don't worry I am not saving your credentials ;)
>Username: kumaranvpl
>Password:
>Menu
>1. List issues
>2. Issue in detail
>3. Open new issue
>4. Close issue
>5. Add comment to an issue
>Exit or Ctrl + C to quit
>Please enter your choice: 1
>Please enter username of another user to list issues, else enter no: rails
>Do you want to see all repos?(y/n) n
>Please enter a repo name: rails
>26884-ActiveRecord: unable to update records with a `has_one, through:` relationship
>26882-Add types to ActiveRecord::Store accessors
>26881-[SanitizeHelper] sanitize does not work in title
>26877-Exception when attribute is `Infinity` in `Hash`
>26875-In Rails 5 params.merge raises exception
>26874-`Broadcast#silence` breaks custom loggers that do not include `Logg…
>26869-Fix brittle tests which were relying on the error message text from mysql2 gem
>26865-fix the uniqueness validation scope with a polymorphic association
>26852-Spike which adds logging of unhandled exceptions to AsyncAdapter.
>26851-update kindlerb gem
>26849-Is it really necessary to override the `*_type=` method for ActiveRecord Polymorphic Association with Single Table Inheritance?
>26848-ActiveJob AsyncAdapter swallows exceptions, doesn't log by default
>26847-Rails5, concurrency in action method, deadlock, docs needed including for executor/reloader
>26841-Be able to use String#blank? with invalid encoding
>26838-allow ActiveRecord::Core#slice to use array arg
>26836-Add npm support in new apps using --npm option
>26835-Testing fails if scaffolded model is named "App"
>26834-Non null constraint exception when creating model with a has many through association
>26817-parent.children.build.parent is nil if has_many has scope
>26815-Log the original call site for an ActiveRecord query
>26813-XmlMini_REXML throws potentially undefined errors.
>26812-Appending format to path in routes can break tests
>26811-Adds proc support for :allow_blank and :allow_nil
>26808-Avoid unneccessarily converting nil to string
>26805-`eager_load` returns incorrectly populated object with belongs_to and has_many relation
>26804-Inflector issues
>26803-Actioncable closes automatically Process (pid=19895, group=the_grid_api_websocket) no longer exists! Detaching it from the pool.
>26799-Support i18n key at translation of value in submit tag
>26798-Shouldn't stop the user due to bcrypts limitation
>26796-Support stop listening to individual broadcasts
>Next - https://api.github.com/repositories/8514/issues?page=2
>Last - https://api.github.com/repositories/8514/issues?page=42
>Please enter next/last to navigate to next/last page. Enter exit to quit: last
>5223-RemoteIp middleware trusted proxies config does not affect Rack::Request::trusted_proxy?
>2686-Attachments not visible in mail clients when additional inline attachments present
>2045-Add possibility to render partial from subfolder with inheritance
>Menu
>1. List issues
>2. Issue in detail
>3. Open new issue
>4. Close issue
>5. Add comment to an issue
>Exit or Ctrl + C to quit
>Please enter your choice: q
>Bye Bye Bye!!!
>(venv) Kumarans-MacBook-Air:githubly kumaran$