# mongo-operator
**A package for backup / cleanup / migrate mongodb.**

## Description:
A tool for backup / cleanup / migrate mongo.

This package can make you backup / cleanup / migrate more earlier with python3.
## Initial testing data
1. download `https://github.com/chienfeng0719/mongo-operator/tree/develop/mongo_init`
2. run command `mongo-operator -r mongo_init`

## How To Use:

You can use mongo-operator through command line for backup/restore/drop database as the following example:
### CLI
```
mongo-operator -b foo_bar -> backup foo_bar
mongo-operator -d foo_bar -> drop foo_bar
mongo-operator -r mongo_init -> restore data from mongo_init folder
```
---
You can also do some advanced operate with python:
### Backup
```python
from mongo_operator import BackupOperator

# init object
backup_operator = BackupOperator(hostname='localhost', port=27017, username='root', password='root')

# backup all database
backup_operator.backup(folder_path='./backup/')

# backup specific collection
backup_operator.backup(db_name='foo_bar', collection='foo_bar')

# backup specific collection with query
backup_operator.backup(db_name='foo_bar', collection='foo_bar', query_={'items': 'phone'})

# restore data from backup
backup_operator.restore(folder_path='./backup/', is_dropped=True)
```

### Cleanup
```python
from mongo_operator import CleanupOperator

# init object
cleanup_operator = CleanupOperator(hostname='localhost', port=27017, username='root', password='root')

# drop 'foo_bar' table in foo_bar
cleanup_operator.drop_collection(db_name='foo_bar', collection='foo_bar')

# drop foo_bar database
cleanup_operator.drop_db(db_name='foo_bar')
```

### Migrate
```python
from mongo_operator import MigrateOperator

# init object
migrate_operator = MigrateOperator(hostname='localhost',
                                   port=27017,
                                   username='root',
                                   password='root',
                                   target_hostname='192.168.1.1',
                                   target_port=27017,
                                   target_username='root',
                                   target_password='root')

# import all database from target host
migrate_operator.import_database()

# import『foo_bar』database from target host
migrate_operator.import_database(db_name='foo_bar')

# export all database from to host
migrate_operator.export_database()

# export『foo_bar』database to target host
migrate_operator.export_database(db_name='foo_bar')
```

---
<a href="https://www.buymeacoffee.com/jimmyyyeh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="40" width="175"></a>

**Buy me a coffee, if you like it!**