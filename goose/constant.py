import os, sys, json, psycopg2
from psycopg2.pool import ThreadedConnectionPool
from redis_cache import RedisCache

import goose.exceptions

class _Const(object):

    @apply
    # KNOWN_HOST_REMOVE_SELECTORS
    def get_known_host_remove_selectors():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            cached_rules = RedisCache.find_cached_value('goose_known_host_remove_selectors')
            if cached_rules:
                return cached_rules

            query_string = 'SELECT domains.url, goose_domain_settings.*, domains.url FROM goose_domain_settings INNER JOIN domains ON goose_domain_settings.domain_id=domains.id'
            records = self.get_records_list_by_query(query_string)

            data = {}
            for item in records:
                if item[7]:
                    if item[6] != None : data[item[0]] = item[6]
                    if item[4] != None : data[item[0]] = {'reference' : self.get_domain_reference(records, item[4])}
                    # if item[3] != None : data['regexs_references'] = {item[3] : {'reference' : self.get_domain_reference(records, item[4])}}

            RedisCache.cache_value('goose_known_host_remove_selectors', data)
            return data
        return property(**locals())

    @apply
    # KNOWN_HOST_CONTENT_TAGS
    def get_known_host_content_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            cached_rules = RedisCache.find_cached_value('goose_known_host_content_tags')
            if cached_rules:
                return cached_rules           

            query_string = 'SELECT domains.url, goose_domain_settings.*, domains.url FROM goose_domain_settings INNER JOIN domains ON goose_domain_settings.domain_id=domains.id'
            records = self.get_records_list_by_query(query_string)

            data = {}
            for item in records:
                if item[7]:
                    if item[5] != None : data[item[0]] = item[5]
                    if item[4] != None : data[item[0]] = {'reference' : self.get_domain_reference(records, item[4])}
                    # if item[3] != None : data['regexs_references'] = {item[3] : {'reference' : self.get_domain_reference(records, item[4])}}

            RedisCache.cache_value('goose_known_host_content_tags', data)
            return data
        return property(**locals())

    @apply
    # KNOWN_PUBLISH_DATE_META_TAGS
    def get_known_publish_date_meta_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            data = self.get_common_settings_list_by_name('KNOWN_PUBLISH_DATE_META_TAGS')
            return data
        return property(**locals())

    @apply
    # KNOWN_DESCRIPTION_META_TAGS
    def get_known_description_meta_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            data = self.get_common_settings_list_by_name('KNOWN_DESCRIPTION_META_TAGS')
            return data
        return property(**locals())

    @apply
    # KNOWN_CONTENT_TAGS
    def get_known_content_tags():
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            data = self.get_common_settings_list_by_name('KNOWN_CONTENT_TAGS')
            return data
        return property(**locals())

    def get_common_settings_list_by_name(self, name):
        cached_rules = RedisCache.find_cached_value('goose_common_settings_list_' + name)
        if cached_rules:
            return cached_rules

        query_string = "SELECT * FROM goose_common_settings WHERE name='%s'" %(name)
        records = self.get_records_list_by_query(query_string)

        common_settings_list = []
        for item in records:
            if item[4]:
                common_settings_list.append({'attribute': item[2], 'value': item[3]})

        RedisCache.cache_value('goose_common_settings_list_' + name, common_settings_list)
        return common_settings_list

    def get_records_list_by_query(self, query_string):
        cursor = self.get_connection_cursor()
        try:
            cursor.execute(query_string)
            records_list = cursor.fetchall()
            return records_list
        except Exception as error:
            raise goose.exceptions.DatabaseError(error)    

    def get_connection_cursor(self):
        try:
            pool = psycopg2.pool.ThreadedConnectionPool(1, os.environ['DB_POOL'], host=os.environ['DB_HOST'], database=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], port=os.environ['DB_PORT'])
            conn = pool.getconn()
            cursor = conn.cursor()
            return cursor
        except Exception as error:
            raise goose.exceptions.DatabaseError(error) 

    def get_domain_reference(self, list, reference_id):
        for item in list:
            if item[1] == reference_id : domain = item[0]
        return domain
