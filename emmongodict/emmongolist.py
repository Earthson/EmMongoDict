from collectionbase import *

class EmMongoList(object):
    '''
    '''
    db_info = {
        'db':'EmMongoDict',
        'collection':'EmMongoDict',
    }

    def __init__(self, spec, path, db=None, collection=None):
        '''path and spec should not be None'''
        self.db_info = dict(EmMongoList.db_info)
        if collection is not None:
            self.db_info['collection'] = collection
        if db is not None:
            self.db_info['db'] = db
        self.spec = spec
        self.path = path

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

    def __getitem__(self, key):
        '''slice is not supported yet'''
        ret = collection_find_one(spec_or_id=self.spec, 
                    fields={self.path:{'$slice':[key, 1]}}, **self.db_info)
        return get_dict_property(ret, self.path)[0]

    def __setitem__(self, key, value):
        '''slice is not supported yet'''
        pos = self.path+'.'+str(key)
        return collection_update(spec=self.spec, 
                    document={'$set':{pos:value}}, **self.db_info)

    def __delitem__(self, key):
        pos = self.path+'.'+str(key)
        return collection_update(spec=self.spec,
                    document={'$unset':{pos:1}}, **self.db_info)

    def get_slice(self, start, lim=None):
        '''mongo style slice
        if lim is None:
            start is positive:
                first start object will be return
            start is negtive:
                last start object will be return
        else:
            from start lim object will be return

            (see doc of mongodb for more help...)
        '''
        if lim is None:
            ret = collection_find_one(spec_or_id=self.spec,
                    fields={self.path:{'$slice':start}}, **self.db_info)
            return get_dict_property(ret, self.path)
        ret = collection_find_one(spec_or_id=self.spec,
                    fields={self.path:{'$slice':[start, lim]}}, **self.db_info)
        return get_dict_property(ret, self.path)

    def add_to_set(self, *objs):
        return collection_update(spec=self.spec,
                        document={'$addToSet':{self.path:{'$each':objs}}},
                        **self.db_info)

    def push(self, *objs):
        return collection_update(spec=self.spec,
                        document={'$pushAll':{self.path:objs}}, **self.db_info)

    def pop(self):
        ret = collection_find_and_modify(query=self.spec, 
                update={'$pop':{self.path:1}}, 
                fields={self.path:{'$slice':[-1, 1]}}, **self.db_info)
        try:
            return get_dict_property(ret, self.path)[0]
        except:
            return None

    def pop_head(self):
        ret = collection_find_and_modify(query=self.spec, 
                update={'$pop':{self.path:-1}}, 
                fields={self.path:{'$slice':[0, 1]}}, **self.db_info)
        try:
            return get_dict_property(ret, self.path)[0]
        except:
            return None

    def pull(self, *objs):
        return collection_update(spec=self.spec,
                        document={'$pullAll':{self.path:objs}}, **self.db_info)

    def __len__(self):
        return len(self.load_list())

    def load_list(self):
        '''load list as an instance of list'''
        ret = collection_find_one(spec_or_id=self.spec,
                        fields={self.path:1}, **self.db_info)
        return get_dict_property(ret, self.path)

    def remove(self):
        '''remove list from db'''
        return collection_remove(spec_or_id=self.spec)
