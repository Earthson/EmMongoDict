EmMongoDict Usage
===========

EmMongoDict create dict/list like interface for MongoDB in Python. based on pymongo.


Basic Dict/List Usage
---------------------

EmMongoDict, just like dict in python

```python
>>> from emmongodict import EmMongoDict
>>> foo = EmMongoDict()
>>> foo['one'] = 'Sample'
>>> foo['bar'] = [1, 2, 3]
>>> foo['em'] = {'x':1, 'y':2}
>>> foo['one']
u'Sample'
>>> foo['bar']
[1, 2, 3]
>>> foo['em']
{u'y': 2, u'x': 1}
```

EmMongoList, just like list in python, but you need EmMongoDict instance to generate one EmMongoList Instance.

```python
>>> from emmongolist import EmMongoList
>>> samplelist = foo.sublist('bar')
>>> samplelist.load_list()
[1, 2, 3]
>>> samplelist[0] = 100
>>> samplelist[2] += 200
>>> samplelist.load_list()
[100, 2, 203]
>>> samplelist.push(10000)
>>> samplelist.push(20000, 30000, 40000)
>>> print samplelist.load_list()
[100, 2, 203, 10000, 20000, 30000, 40000]
>>> print samplelist.pop()
40000
>>> print samplelist.load_list()
[100, 2, 203, 10000, 20000, 30000]
>>> print samplelist.pop_head()
100
>>> print samplelist.load_list()
[2, 203, 10000, 20000, 30000]
>>> samplelist.pull(203)
>>> del samplelist[3]
>>> print samplelist.load_list()
[2, 10000, 20000, None]
>>> samplelist.add_to_set(20000, 20001)
>>> print samplelist.load_list()
[2, 10000, 20000, None, 20001]
```

EmMongoDict have Embedded Document support. Just Like EmMongoList, you could get a subdict by self.subdict(dictname). The depth of EmMongoDict does not limited by EmMongoDict(limit depends on MongoDB).

```python
>>> emdict = foo.subdict('em')
>>> emdict.load_doc()
{u'y': 2, u'x': 1}
>>> emdict['x'] += 100
>>> emdict['y'] += 100
>>> emdict['z'] = 200
>>> print emdict['m']
None
>>> emdict['m'] = 2000
>>> emdict.load_doc()
{u'y': 102, u'x': 101, u'z': 200, u'm': 2000}
>>> del emdict['m']
>>> emdict.load_doc()
{u'y': 102, u'x': 101, u'z': 200}
```

Important Points
----------------

* EmMongoDict is just like a mapper to MongoDB Document. We Call the root Document as EmMongoDict here.
* **'_id'** is default member in EmMongoDict, with `your_dict['_id']` to get it. with `EmMongoDict(doc={'_id':your_id})`, you could specify it by yourself, rather than auto generate by MongoDB.
* key of EmMongoDict can be string only, do not use **'.'** and **'$'** in your key. If you do not familar to MongoDB, it would lead you to confusion.
* with key not exist in EmMongoDict, `your_dict[key]` do not raise `KeyError`, it will return None
* with `self.load_doc()` you could get a dict instance to the Document you queryed. use `self.load_list()` in EmMongoList for a list instance.


Create EmMongoDict Instance
---------------------------

```python
EmMongoDict.__init__(self, doc=None, spec=None, path=None, db=None, collection=None)
```

* doc: the data as default in document, eg. `tmp = EmMongoDict(doc={'email':'x@yyy.com'})`, `tmp['email']` will return 'x@yyy.com'. Index value should init here!
* spec: query information for MongoDB to find the Document. Normal case is `{'_id':doc_id}`, see `pymongo.collection.find` for more help.
* path: path to root, it is used for embedded Document. You do not have to know too mush about it, `your_dict.subdict(dictname)` is a better way to do this.
* db and collection: information of database and collection in MongoDB, in Normal case, just leave them `None`.

Recommended Way to use EmMongoDict
----------------------------------

```python
class StudentDoc(EmMongoDict):
    db_info = {
        'db':'School',
        'collection':'Student',
    }
```

Just make db/collection information automatically:)

Use Index in your EmMongoDict
-----------------------------

eg.
```python
>>> class StudentDoc(EmMongoDict):
...     db_info = {
...         'db':'School',
...         'collection':'StudentDocCCC',
...     }
...     indexes = {
...         'email':{'unique':True, 'sparse':True},
...     }
... 
>>> StudentDoc.init_collection()
>>> StudentDoc.ensure_index()
>>> 
>>> s0 = StudentDoc(doc={'email':'a@a.com'})
>>> print s0.spec
{'_id': ObjectId('504c3c79b45d6a1578000004')}
>>> s1 = StudentDoc(doc={'email':'b@b.com'})
>>> tmp = StudentDoc(spec={'email':'a@a.com'})
>>> tmp['_id']
ObjectId('504c3c79b45d6a1578000004')
>>> tmp['email']
u'a@a.com'
>>> tmp['test'] = 'hahaha'
>>> 
>>> print tmp.load_doc()
{u'test': u'hahaha', u'_id': ObjectId('504c3c79b45d6a1578000004'), u'email': u'a@a.com'}
>>> print s0.load_doc()
{u'test': u'hahaha', u'_id': ObjectId('504c3c79b45d6a1578000004'), u'email': u'a@a.com'}
>>> print s1.load_doc()
{u'_id': ObjectId('504c3c79b45d6a1578000005'), u'email': u'b@b.com'}
```

With `cls.indexes` you could set the index information of class. index infomation is formatted by `indexname:propertyes_dict`. you could get more help from MongoDB Documentation.

**Do not forget to make index work by `cls.ensure_index()`**
