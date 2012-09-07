from pymongo import *
from bson import *

'''
you should replace the argument collection as (db_name, collection_name)
'''

#connection_pool
conn = Connection(max_pool_size=40, network_timeout=1000)

def collection_do(operate):
    '''wrapper for mongodb operation
    '''
    def wrapper(db_name, collection_name, *args, **kargs):
        db = conn[db_name]
        collection = db[collection_name]
        ret = operate(collection, *args, **kargs)
        conn.end_request()
        return ret
    return wrapper

def get_dict_property(doc, names):
    '''property path is seperated by '.', 
    return the property from doc(dict instance)'''
    names = names.split('.', 1)
    try:
        to = doc[names[0]]
    except KeyError:
        return None
    if len(names) == 1:
        return to
    else:
        return get_dict_property(to, names[1])

auto_operations = ('save', 'update', 'remove', 'drop', 'find', 'find_one', 
                   'count', 'create_index', 'ensure_index', 'drop_index',
                   'drop_indexes', 'reindex', 'index_information', 'options',
                   'group', 'rename', 'distinct', 'map_reduce', 
                   'inline_map_reduce', 'find_and_modify', 'aggregate')

def auto_code_for_collection(*func_names):
    '''automaticly get code from pymongo version to collection_do version'''
    res = ''
    for each in func_names:
        tmp = '''
@collection_do
def collection_%s(collection_obj, *args, **kwargs):
    return collection_obj.%s(*args, **kwargs)

''' % (each, each)
        res += tmp    
    return res


@collection_do
def collection_inc(collection_obj, query, valname, step, **kwargs):
    return collection_obj.update(query, {'$inc':{valname:step}})

@collection_do
def collection_incb(collection_obj, query, valname, step=1, **kwargs):
    res_dict = collection_obj.find_and_modify(query, fields={valname:1},    
                    update={'$inc':{valname:step}}, **kwargs)
    return get_dict_property(res_dict, valname)

@collection_do
def collection_inca(collection_obj, query, valname, step=1, **kwargs):
    res_dict = collection_obj.find_and_modify(query, fields={valname:1},    
                    update={'$inc':{valname:step}}, new=True, **kwargs)
    return get_dict_property(res_dict, valname)

###########################################
#auto code below
###########################################

@collection_do
def collection_save(collection_obj, *args, **kwargs):
    return collection_obj.save(*args, **kwargs)


@collection_do
def collection_update(collection_obj, *args, **kwargs):
    return collection_obj.update(*args, **kwargs)


@collection_do
def collection_remove(collection_obj, *args, **kwargs):
    return collection_obj.remove(*args, **kwargs)


@collection_do
def collection_drop(collection_obj, *args, **kwargs):
    return collection_obj.drop(*args, **kwargs)


@collection_do
def collection_find(collection_obj, *args, **kwargs):
    return collection_obj.find(*args, **kwargs)


@collection_do
def collection_find_one(collection_obj, *args, **kwargs):
    return collection_obj.find_one(*args, **kwargs)


@collection_do
def collection_count(collection_obj, *args, **kwargs):
    return collection_obj.count(*args, **kwargs)


@collection_do
def collection_create_index(collection_obj, *args, **kwargs):
    return collection_obj.create_index(*args, **kwargs)


@collection_do
def collection_ensure_index(collection_obj, *args, **kwargs):
    return collection_obj.ensure_index(*args, **kwargs)


@collection_do
def collection_drop_index(collection_obj, *args, **kwargs):
    return collection_obj.drop_index(*args, **kwargs)


@collection_do
def collection_drop_indexes(collection_obj, *args, **kwargs):
    return collection_obj.drop_indexes(*args, **kwargs)


@collection_do
def collection_reindex(collection_obj, *args, **kwargs):
    return collection_obj.reindex(*args, **kwargs)


@collection_do
def collection_index_information(collection_obj, *args, **kwargs):
    return collection_obj.index_information(*args, **kwargs)


@collection_do
def collection_options(collection_obj, *args, **kwargs):
    return collection_obj.options(*args, **kwargs)


@collection_do
def collection_group(collection_obj, *args, **kwargs):
    return collection_obj.group(*args, **kwargs)


@collection_do
def collection_rename(collection_obj, *args, **kwargs):
    return collection_obj.rename(*args, **kwargs)


@collection_do
def collection_distinct(collection_obj, *args, **kwargs):
    return collection_obj.distinct(*args, **kwargs)


@collection_do
def collection_map_reduce(collection_obj, *args, **kwargs):
    return collection_obj.map_reduce(*args, **kwargs)


@collection_do
def collection_inline_map_reduce(collection_obj, *args, **kwargs):
    return collection_obj.inline_map_reduce(*args, **kwargs)


@collection_do
def collection_find_and_modify(collection_obj, *args, **kwargs):
    return collection_obj.find_and_modify(*args, **kwargs)


@collection_do
def collection_aggregate(collection_obj, *args, **kwargs):
    return collection_obj.aggregate(*args, **kwargs)

