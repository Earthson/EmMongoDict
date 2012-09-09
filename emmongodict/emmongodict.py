from collectionbase import *

class EmMongoDict(object):
    '''
    '''
    db_info = {
        'db':'EmMongoDict',
        'collection':'EmMongoDict',
    }

    indexes = {
        #'name':{'unique':True, 'sparse':True}
    }

    def __init__(self, doc=None, spec=None, path=None, 
                        db=None, collection=None):
        '''
        '''
        self.db_info = dict(self.db_info)
        if collection is not None:
            self.db_info['collection'] = collection
        if db is not None:
            self.db_info['db'] = db
        self.spec = spec
        self.path = path
        if not self.spec:
            if doc is None:
                doc = dict()
            self.spec = {'_id':collection_insert(doc_or_docs=doc, 
                                                **self.db_info)}
        elif doc:
            self.update(doc)

    def is_exist(self):
        '''test whether spec is in db'''
        ret = collection_find_one(spec_or_id=self.spec, fields={'_id':1}, 
                                                **self.db_info)
        return ret is not None

    def ensure_exist(self):
        '''return: True, if exist before
                   False, if not exist before
        '''
        if self.is_exist() is False:
            collection_insert(doc_or_docs=self.spec, **self.db_info)
            return False
        return True

    def subdict(self, subpath):
        path = subpath if not self.path else self.path+'.'+subpath
        return self.__class__(spec=self.spec, path=path, **self.db_info)

    def sublist(self, subpath):
        from emmongolist import EmMongoList
        path = subpath if not self.path else self.path+'.'+subpath
        return EmMongoList(spec=self.spec, path=path, **self.db_info)

    @classmethod
    def init_collection(cls):
        cls.drop()
        cls.ensure_index()

    @classmethod
    def drop(cls):
        collection_drop(**cls.db_info)

    @classmethod
    def ensure_index(cls):
        for ek, ev in cls.indexes.items():
            info = dict(cls.db_info)
            info.update(ev)
            collection_ensure_index(key_or_list=ek,
                                **info)

    def __getitem__(self, key):
        toget = key
        if self.path is not None:
            toget = self.path+'.'+toget
        ret = collection_find_one(spec_or_id=self.spec, fields={toget:1},
                                **self.db_info)
        return get_dict_property(ret, toget)

    def get_propertys(self, keylist):
        togets = keylist
        if self.path is not None:
            togets = dict((self.path+'.'+each, 1) for each in togets)
        else:
            togets = dict((each, 1) for each in togets)
        ret = collection_find_one(spec_or_id=self.spec, fields={toget:1},
                                **self.db_info)
        return [get_dict_property(ret, each) for each in togets]

    def __setitem__(self, key, value):
        if self.path is not None:
            key = self.path+'.'+key
        return collection_update(spec=self.spec, 
                document={'$set':{key:value}}, **self.db_info)

    def delete_propertys(self, keylist):
        if self.path is not None:
            keylist = [self.path+'.'+each for each in keylist]
        return collection_delete_keys(keys=keylist, spec=self.spec,
                                        **self.db_info)

    def __delitem__(self, key):
        return self.delete_propertys(key)

    def inc(self, key, step=1):
        return collection_inc(spec=self.spec, key=key, step=step
                                **self.db_info)

    def dec(self, key, step=1):
        return collection_inc(spec=self.spec, key=key, step=-step,
                                **self.db_info)

    def incb(self, key, step=1):
        '''similar to i++'''
        return collection_incb(spec=self.spec, key=key, step=step,
                                **self.db_info)

    def inca(self, key, step=1):
        '''similar to ++i'''
        return collection_inca(spec=self.spec, key=key, step=step,
                                **self.db_info)

    def decb(self, key, step=1):
        '''similar to i--'''
        return collection_incb(spec=self.spec, key=key, step=-step,
                                **self.db_info)

    def deca(self, key, step=1):
        '''similar to --i'''
        return collection_inca(spec=self.spec, key=key, step=-step,
                                **self.db_info)

    def update(self, other):
        doc = dict(other)
        if self.path is not None:
            doc = dict([(self.path+'.'+ek, ev) for ek, ev in doc.items()])
        return collection_update(spec=self.spec, document={'$set':doc},
                                    **self.db_info)

    def pop(self, key):
        ret = self[key]
        del self[key]
        return ret

    def load_doc(self):
        if self.path is None:
            ret = collection_find_one(spec_or_id=self.spec, **self.db_info)
            return ret
        ret = collection_find_one(spec_or_id=self.spec, 
                            fields={self.path:1}, **self.db_info)
        return get_dict_property(ret, self.path)

    @classmethod
    def load_docs(cls, spec_key=None, spec_values=None):
        if spec_key is None and spec_values is None:
            return collection_find(**cls.db_info)
        return collection_find(spec={spec_key:{'$in':spec_values}},
                                **cls.db_info)
        
    def __iter__(self):
        doc = self.load_doc()
        for each in doc.keys():
            yield each

    def items(self):
        doc = self.load_doc()
        return doc.items()

    def keys(self):
        doc = self.load_doc()
        return doc.keys()

    def values(self):
        doc = self.load_doc()
        return doc.values()

    def __len__(self):
        doc = self.load_doc()
        return len(doc)

    def __contains__(self, item):
        return self[item] is not None

    def remove(self):
        '''remove the dict from db'''
        if self.path is not None:
            return collection_delete_keys(keys=(self.path,), 
                            spec=self.spec, **self.db_info)
        return collection_remove(spec_or_id=self.spec)

    def rename(self, key, newkey):
        '''rename key by newkey'''
        if self.path is not None:
            key = self.path+'.'+key
            newkey=self.path+'.'+newkey
        return collection_update(spec=self.spec, 
                    document={'$rename':{key:newkey}}, **self.db_info)
