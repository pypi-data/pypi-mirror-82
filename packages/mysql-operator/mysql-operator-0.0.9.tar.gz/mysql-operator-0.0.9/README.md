# mysql-operator
**A package for backup / cleanup / migrate mysql database.**


## Description:
A tool for backup / cleanup / migrate mysql.

This package can make you backup / cleanup / migrate mysql more earlier with python3.
## Initial testing data
1. download `https://github.com/chienfeng0719/mysql-operator/blob/develop/init.sql`
2. run command `mysql-operator -r init.sql`

## How To Use:

You can use mysql-operator through command line for backup/restore/drop database as the following example:
### CLI
```
mysql-operator -b foo_bar_db -> backup foo_bar_db
mysql-operator -d foo_bar_db -> drop foo_bar_db
mysql-operator -r backup_2020-10-10.sql -> restore data from backup_2020-10-10.sql
```
---
You can also do some advanced operate with python:
### Backup
```python
from mysql_operator import BackupOperator

# init object
backup_operator = BackupOperator(hostname='localhost', port=3306, username='root', password='root')

# backup all database
backup_operator.backup()

# backup multiple databases
backup_operator.backup(dbs=['foo_bar_db', 'hello_world_db'])

# backup database『foo_bar_db』
backup_operator.backup(db_name='foo_bar_db', filename='foo_bar_bak_test.sql')

# backup database『foo_bar_db』with tables ['foo_user', 'bar_store']
backup_operator.backup(db_name='foo_bar_db', tables=['foo_user', 'bar_store'], filename='foo_bar_bak_test.sql')

# backup database『foo_bar_db』with table which table name like '%foo%'
backup_operator.pattern_backup(db_name='foo_bar_db', pattern='%foo%', filename='foo_bar_bak_test.sql')

# backup database『foo_bar_db』with table 'bar_store' where id <= 2 AND branch '%Jammu%'
backup_operator.filter_backup(db_name='foo_bar_db',
                              table_name='bar_store',
                              filter_="id <= 2 AND branch like '%Jammu%'",
                              filename='foo_bar_bak_test.sql')

# restore backup
backup_operator.restore(db_name='foo_bar_db', filename='foo_bar_bak_test.sql')
```
***NOTICE: The filter_ argument with filter_backup must use double quotes***

### Cleanup
```python
from mysql_operator import CleanupOperator

# init object
cleanup_operator = CleanupOperator(hostname='localhost', port=3306, username='root', password='root')

# drop all tables in『foo_bar_db』
cleanup_operator.drop(db_name='foo_bar_db')

# drop database『hello_world_db』
cleanup_operator.drop(db_name='hello_world_db', keep_db=False)

# drop tables ['foo_user', 'bar_weather'] in『foo_bar_db』
cleanup_operator.drop(db_name='foo_bar_db', tables=['foo_user', 'bar_weather'])

# drop tables in『foo_bar_db』 which table name like '%foo%'
cleanup_operator.pattern_drop(db_name='foo_bar_db', pattern='%foo%')
```

### Migrate
```python
from mysql_operator import MigrateOperator
# init object
migrate_operator = MigrateOperator(hostname='localhost',
                                   port=3306,
                                   username='root',
                                   password='root',
                                   target_hostname='192.168.1.1',
                                   target_port=3306,
                                   target_username='root',
                                   target_password='root')

# import all database from target host
migrate_operator.import_database()

# import database『foo_bar_db』from target host
migrate_operator.import_database(db_name='foo_bar_db')

# export all database from to host
migrate_operator.export_database()

# export database『foo_bar_db』to target host
migrate_operator.export_database(db_name='foo_bar_db')
```

---
<a href="https://www.buymeacoffee.com/jimmyyyeh" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="40" width="175"></a>

**Buy me a coffee, if you like it!**