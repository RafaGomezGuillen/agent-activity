# Alembic

## Migrate the Alembic migrations

To create a new migration add the new model created to `app/db/base.py`.

```py
from app.db.database import Base

# Import all models...
from app.models import Agent
```

To avoid circular error you need to add all models to the following file `app/models/__init__.py`

```py
from .agent import Agent
from .keylog import Keylog
from .metric import Metric
```

And create the migration with the following command:

```sh
alembic revision --autogenerate -m "<description>"
```

To create the **SQLite** DB and migrate the models execute the following command:

```sh
alembic upgrade head
```

With this action `database.db` file will be generated.