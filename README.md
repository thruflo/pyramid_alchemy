Good frameworks, like [Pyramid][] and [Angular][], help developers write
testable code. [SQLAlchemy][] is a great framework. However, the sheer
convenience of having model instances returned from a database query
encourages developers to write large ORM classes which can be hard to test.

One way to avoid this is to keep model classes [thin][] and write separate code
to instantiate and manipulate them. The downside of this approach is the loss in
convenience: the separated, easily testable code isn't provided by default as
an attribute of the model instances returned from a database query.

[pyramid_alchemy][] provides an `add_model_method` Pyramid
[configuration directive]() that extends [SQLAlchemy ORM][] classes in the same
way that `add_request_method` [extends the Pyramid Request][]. Using this
directive allows developers to write easily testable code that is conveniently
available as a model instance attribute. For example, if you [include][] this
in your Pyramid application:

```python
from .model import Spam

def get_eggs(instance, source='hens', limit=9, offset=0):
    """Example ORM instance method, implemented as a standalone function."""
    
    query = instance.query.filter_by(source=source)
    return query.offset(offset).limit(limit)

def includeme(config):
    config.add_model_method(Spam, get_eggs, 'get_eggs')
```

You can then use the `get_eggs` method from `Spam` instances:

```python
spam = Session.query(Spam).get(1)
eggs = spam.get_eggs()
```

### Interfaces

Just as you can hang a Pyramid view off any context object implementing a
specific interface, you can extend any model instance implementing an interface.
For example, if your model looked something like this:

```python
from sqlalchemy.ext.declarative import declarative_base
from zope.interfaces import implementer

from .interfaces import IFilling

Base = declarative_base()

@implementer(IFilling)
class Ham(Base):
    # ...

@implementer(IFilling)
class Spam(Base):
    # ...
```

Then you could extend all fillings -- current and future -- with:

```python
config.add_model_method(IFilling, get_eggs, 'get_eggs')
```

### Limitations

Note that it's highly unlikely to be a good idea to use `add_model_method` to
add dynamic or hybrid methods that affect the underlying sql table or mapping.

[Pyramid]: http://docs.pylonsproject.org/projects/pyramid/en/latest
[Angular]: http://angularjs.org
[SQLAlchemy]: http://docs.sqlalchemy.org/en/latest
[pyramid_alchemy]: https://github.com/thruflo/pyramid_alchemy
[configuration directive]: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/extconfig.html
[SQLAlchemy ORM]: http://docs.sqlalchemy.org/en/latest/orm
[extends the Pyramid Request]: http://docs.pylonsproject.org/projects/pyramid/en/latest/api/config.html#pyramid.config.Configurator.add_request_method
[include]: http://docs.pylonsproject.org/projects/pyramid/en/latest/api/config.html#pyramid.config.Configurator.include
[thin]: http://blog.codeclimate.com/blog/2012/10/17/7-ways-to-decompose-fat-activerecord-models/