=========
M_Covers
=========
| 本の感想を保管する記憶プログラム


Usage
======

1. 使い始めるときは、必ずconfigure関数を実行してください。

.. code-block::

    from m_covers.config import configure

    sqlite_path = 'tmp/.../test.sqlite.db'
    configure(sqlite_path)

2. configureのあとは、serviceモジュールの関数群でcoverを管理できます。

.. code-block::

    from m_covers.service import *

    isbn = '97800000000'
    command = create_engine(isbn, 'your feeling for book')
    command.flush()
    command.commit()

3. commandで永続化しようとしている際に、どのような値を永続化しようとしているのか確認できます。

.. code-block::

    command = create_engine(isbn, impression)
    command.flush()
    print(command.values_recorded(['id', 'title', 'caption'])


