"""
`ALTER` 是 MySQL 中用于修改数据库对象（如表、列、索引等）的命令。以下是 `ALTER` 的一些常见用法：

1. 修改表名：

```
ALTER TABLE old_table_name RENAME TO new_table_name;
```

2. 修改表的字符集：

```
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4;
```

3. 修改表的存储引擎：

```
ALTER TABLE table_name ENGINE = InnoDB;
```

4. 添加列：
```
ALTER TABLE table_name ADD COLUMN column_name column_definition;
```

5. 修改列：

```
ALTER TABLE table_name MODIFY COLUMN column_name new_column_definition;
```

6. 重命名列：

```
ALTER TABLE table_name CHANGE COLUMN old_column_name new_column_name new_column_definition;
```

7. 删除列：

```
ALTER TABLE table_name DROP COLUMN column_name;
```

8. 添加主键：

```
ALTER TABLE table_name ADD PRIMARY KEY (column_name);
```

9. 删除主键：

```
ALTER TABLE table_name DROP PRIMARY KEY;
```

10. 添加外键：

```
ALTER TABLE table_name ADD CONSTRAINT constraint_name FOREIGN KEY (column_name) REFERENCES another_table(another_column)
```
"alter table test_db add constraint constraint_name foreign key(id) references another_table()"

11. 删除外键：

```
ALTER TABLE table_name DROP FOREIGN KEY constraint_name;
```

12. 添加索引：

```
ALTER TABLE table_name ADD INDEX index_name (column_name);
```

13. 删除索引：

```
ALTER TABLE table_name DROP INDEX index_name;
```
注意：在使用 `ALTER` 命令时，需要具有对数据库对象足够的权限。
"""
