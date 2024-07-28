import os
from typing import List, Optional, Union
from urllib.parse import quote_plus

from pymongo import MongoClient

from models.base import Log


class IHandler(Log):
    ...


class MongoHandler(IHandler):
    def __init__(self):
        super().__init__()
        host = os.getenv("MONGO_HOST")  # should include port
        user = quote_plus(os.getenv("MONGO_USER"))
        pswd = quote_plus(os.getenv("MONGO_PSWD"))
        auth_db = os.getenv("MONGO_AUTH_DB")
        conn_str = f"mongodb://{user}:{pswd}@{host}/?authMechanism=DEFAULT&authSource={auth_db}"
        if not user:
            conn_str = f"mongodb://{host}"
        db_name = os.getenv("MONGO_DB")
        self.client = MongoClient(conn_str)
        self.default_col = os.getenv("MONGO_COLLECTION")
        self.default_sys_col = os.getenv("MONGO_SYS_COLLECTION")
        self.db = self.client.get_database('test' if not db_name else db_name)

    def set_db(self, db_name: str):
        self.db = self.client.get_database(db_name)

    def get_collection(self, collection: Optional[str] = None, sys: bool = False):
        '''If collection is None, return default_col, else return collection'''
        if not collection:
            collection = self.default_col if not sys else self.default_sys_col
        return self.db.get_collection(collection)

    def count_documents(self, filter: Optional[dict] = None, collection: Optional[str] = None, sys: bool = False, **kwargs):
        col = self.get_collection(collection, sys)
        return col.count_documents(filter)

    def insert(self, data: Union[dict, List[dict]], collection: Optional[str] = None, sys: bool = False):
        '''If data is list, insert_many, else insert_one'''
        insert_count = 0
        col = self.get_collection(collection, sys)
        if isinstance(data, list):
            result = col.insert_many(data)
            insert_count = len(result.inserted_ids)
        else:
            result = col.insert_one(data)
            insert_count = 1
        return insert_count

    def get_projection(self, projection: Optional[dict] = None, show_id: bool = False):
        '''If projection is None, show_id is False, return None'''
        if not projection and not show_id:
            projection = {'_id': 0}
        elif projection and not show_id:
            projection.update({'_id': 0})
        elif projection and show_id:
            projection.update({'_id': 1})
        return projection

    def query(self, query: dict, projection: Optional[dict] = None, show_id: bool = False, collection: Optional[str] = None, sys: bool = False, **kwargs):
        '''If projection is None, show_id is False, return all fields except _id'''
        projection = self.get_projection(projection, show_id)
        col = self.get_collection(collection, sys)
        return col.find(query, projection, **kwargs)

    def query_one(self, query: dict, projection: Optional[dict] = None, show_id: bool = False, collection: Optional[str] = None, sys: bool = False, **kwargs):
        '''If projection is None, show_id is False, return all fields except _id'''
        projection = self.get_projection(projection, show_id)
        col = self.get_collection(collection, sys)
        return col.find_one(query, projection, **kwargs)

    def aggregate(self, pipeline: List[dict], show_id: bool = False, collection: Optional[str] = None, sys: bool = False, **kwargs):
        projection = self.get_projection(None, show_id)
        pipeline += [{'$project': projection}]
        col = self.get_collection(collection, sys)
        return col.aggregate(pipeline, **kwargs)

    def update(self, query: dict, update: Union[dict, List[dict]], collection: Optional[str] = None, sys: bool = False, **kwargs):
        '''If data is list, update_many, else update_one'''
        col = self.get_collection(collection, sys)
        result = col.update_many(query, update, **kwargs)
        return result.modified_count

    def delete(self, query: dict, collection: Optional[str] = None, sys: bool = False, **kwargs):
        '''Delete all matched documents, return deleted count'''
        col = self.get_collection(collection, sys)
        result = col.delete_many(query, **kwargs)
        return result.deleted_count
