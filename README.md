# To-do-list
## Install
Setting up:
```bash
pip install -r requriments.txt
```
Creating database:
```python
from models import db, User, Task
from app import app
with app.app_context():
  db.create_all()
```
