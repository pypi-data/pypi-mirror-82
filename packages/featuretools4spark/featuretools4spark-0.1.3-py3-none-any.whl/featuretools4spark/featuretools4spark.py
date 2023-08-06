import featuretools as f
import numpy as np
import pandas as pd
from dateutil import parser
from pyspark.sql import SparkSession, Row
from pyspark.sql.dataframe import DataFrame


class EntityColumn:
    def __init__(self, entity_id: str, column_name: str):
        self.entity_id = entity_id
        self.column_name = EntitySpark.change_col_name(entity_id, column_name)
        #self._interesting_values = None #Interesting_Values(self.entity_id,self.column_name,interesting_values)
    '''
    @property
    def interesting_values(self):
        return self._interesting_values

    @interesting_values.setter
    def interesting_values(self, interesting_values):
        vals =  Interesting_Value(self.entity_id,self.column_name,interesting_values)
        #print('y is',y)
        self._interesting_values =vals
        EntitySet.interestings.append(vals)
    '''
class EntitySpark:
    def __init__(self,
                 entity_id: str,
                 df: DataFrame,
                 index: str = None,
                 variable_types: dict = None,
                 time_index: str = None,
                 secondary_time_index: str = None):
        self.entity_id = entity_id
        self.df = self._change_col_names(df)
        self.index = self.change_col_name(entity_id, index)
        self.variable_types = variable_types
        self.time_index = self.change_col_name(entity_id, time_index)
        self.secondary_time_index = self.change_col_name(entity_id, secondary_time_index)

    def drop_data(self):
        return EntitySparkWithoutData(self.entity_id, self.df.columns, self.index, self.variable_types,
                                      self.time_index, self.secondary_time_index)

    @staticmethod
    def change_col_name(entity_id: str, col_name: str):
        if col_name is None:
            return None
        return "{0}_{1}".format(entity_id, col_name)

    @staticmethod
    def recover_col_name(entity_id: str, col_name: str):
        if col_name is None:
            return None
        return col_name[len(entity_id) + 1:]

    def _change_col_names(self, df: DataFrame):
        res = df
        for col in df.columns:
            res = res.withColumnRenamed(col, self.change_col_name(self.entity_id, col))
        return res

    def __getitem__(self, column: str):
        columns = [self.recover_col_name(self.entity_id, col) for col in self.df.columns]
        if column in columns:
            col = EntityColumn(self.entity_id, column)
            return col
            #return EntityColumn(self.entity_id, column)
        raise KeyError("Column {0} doesn't exist in {1}".format(column, self.entity_id))


class EntitySparkWithoutData:
    def __init__(self,
                 entity_id: str,
                 columns: list,
                 index: str = None,
                 variable_types: dict = None,
                 time_index: str = None,
                 secondary_time_index: str = None):
        self.entity_id = entity_id
        self.columns = columns
        self.index = index
        self.variable_types = variable_types
        self.time_index = time_index
        self.secondary_time_index = secondary_time_index


class Relationship:
    def __init__(self, parent_variable: EntityColumn, child_variable: EntityColumn):
        self.parent_variable = parent_variable
        self.child_variable = child_variable

class Interesting_Value:
    def __init__(self, entityid: str,columnname: str, interesting_val: list):
        self.entity_id = entityid
        self.column = columnname
        self.vals = interesting_val


class EntitySet:
    """
    todo Current known limitations:
    """

    def __init__(self, id: str):
        self.id = id
        self.entity_dict = {}
        self.relationships = []
        self.interestings = []

    def entity_from_dataframe(self,
                              entity_id: str,
                              dataframe: DataFrame,
                              index: str = None,
                              variable_types: dict = None,
                              time_index: str = None,
                              secondary_time_index: str = None,
                              validate_data: bool = True):
        entity = EntitySpark(entity_id, dataframe, index, variable_types, time_index, secondary_time_index)
        if validate_data:
            self._validate_spark_entity(entity)
        self.entity_dict[entity_id] = entity

    def get_big_df(self):
        scannned_entities = set()

        if len(self.relationships) == 0:
            raise ValueError("No relationships defined in {0}!".format(self.id))

        relationship = self.relationships[0]
        parent_entity = relationship.parent_variable.entity_id
        parent_col = relationship.parent_variable.column_name
        child_entity = relationship.child_variable.entity_id
        child_col = relationship.child_variable.column_name
        scannned_entities.add(parent_entity)
        scannned_entities.add(child_entity)
        parent_df = self.entity_dict[parent_entity].df
        child_df = self.entity_dict[child_entity].df

        res = parent_df.join(child_df, parent_df[parent_col] == child_df[child_col])

        if len(self.relationships) > 1:
            for relationship in self.relationships[1:]:
                parent_entity = relationship.parent_variable.entity_id
                parent_col = relationship.parent_variable.column_name
                child_entity = relationship.child_variable.entity_id
                child_col = relationship.child_variable.column_name
                parent_df = self.entity_dict[parent_entity].df
                child_df = self.entity_dict[child_entity].df
                if parent_col == child_col:
                    if parent_entity in scannned_entities:
                        res = res.join(child_df, on=parent_col)
                    elif child_entity in scannned_entities:
                        res = res.join(parent_df, on=parent_col)
                    else:
                        raise ValueError(
                            "Neither {0} or {1} is in its previous relationships: {2}".format(parent_entity,
                                                                                              child_entity,
                                                                                              scannned_entities))  # todo
                else:
                    if parent_entity in scannned_entities:
                        res = res.join(child_df, res[parent_col] == child_df[child_col])
                    elif child_entity in scannned_entities:
                        res = res.join(parent_df, res[child_col] == parent_df[parent_col])
                    else:
                        raise ValueError(
                            "Neither {0} or {1} is in its previous relationships: {2}".format(parent_entity,
                                                                                              child_entity,
                                                                                              scannned_entities))
        return res

    def add_relationship(self, relationship: Relationship):
        parent_entity = relationship.parent_variable.entity_id
        child_entity = relationship.child_variable.entity_id
        if parent_entity not in self.entity_dict:
            raise KeyError("Parent entity {0} does not exist in {1}".format(parent_entity, self.id))
        if child_entity not in self.entity_dict:
            raise KeyError("Child entity {0} does not exist in {1}".format(child_entity, self.id))
        self.relationships.append(relationship)
    
    def add_intresting_values(self,interesting_value: Interesting_Value):
        entity = interesting_value.entity_id
        col = interesting_value.column
        if entity not in self.entity_dict:
            raise KeyError("Parent entity {0} does not exist in {1}".format(entity, self.id))
        columns = [EntitySpark.recover_col_name(entity, col) for col in self.entity_dict[entity].df.columns]
        if col not in columns:
            raise KeyError("Column {0} doesn't exist in {1}".format(column, entity))
        self.interestings.append(interesting_value)

    def __getitem__(self, entity_id):
        if entity_id in self.entity_dict:
            return self.entity_dict[entity_id]
        raise KeyError('Entity %s does not exist in %s' % (entity_id, self.id))

    @staticmethod
    def _validate_spark_entity(entity: EntitySpark):
        # 1. Validate the dataframe is not empty
        total_rows = entity.df.count()
        if total_rows == 0:
            raise ValueError("Given entity {0} contains 0 rows! ".format(entity.entity_id))

        # 2. Validate index and time_index column exist
        if entity.index not in entity.df.columns:
            raise ValueError("Index column '{0}' does not exist in entity {1}!".format(entity.index, entity.entity_id))
        if entity.time_index is not None and entity.time_index not in entity.df.columns:
            raise ValueError("Time index column '{0}' does not exist in entity {1}!".format(entity.time_index,
                                                                                            entity.entity_id))
        if entity.secondary_time_index is not None and entity.secondary_time_index not in entity.df.columns:
            raise ValueError(
                "Second time index column '{0}' does not exist in entity {1}!".format(entity.secondary_time_index,
                                                                                      entity.entity_id))

        # 3. Validate that index column is unique
        if entity.index is not None:
            index_distinct_rows = entity.df.select(entity.index).distinct().count()
            if total_rows != index_distinct_rows:
                raise ValueError("Index column {0} for {3} is not unqiue! ({1} != {2})".format(entity.index, total_rows,
                                                                                               index_distinct_rows,
                                                                                               entity.entity_id))

        # 4. Validate that time index column can be converted into time
        if entity.time_index is not None:
            time_index = entity.time_index
            entity_id = entity.entity_id
            EntitySet._validate_time_index_col(entity.df, entity_id, time_index)
        if entity.secondary_time_index is not None:
            second_time_index = entity.secondary_time_index
            entity_id = entity.entity_id
            EntitySet._validate_time_index_col(entity.df, entity_id, second_time_index)

    @staticmethod
    def _validate_time_index_col(df: DataFrame, entity_id: str, time_index: str):
        def validate_single_row(row: Row):
            time_str = row[time_index]
            try:
                return parser.parse(time_str)
            except Exception:
                raise ValueError("Cannot parse '{0}' of time index column "
                                 "'{1}' in entity '{2}'! ".format(time_str,
                                                                  EntitySpark.recover_col_name(entity_id, time_index),
                                                                  entity_id))
        df.foreach(validate_single_row)
        
        
def dfs(spark: SparkSession,
        entityset: EntitySet,
        target_entity: str,
        primary_entity: str,
        primary_col: str,
        cutoff_time=None,
        agg_primitives: list = None,
        trans_primitives: list = None,
        where_primitives: list = None,
        max_depth=None,
        training_window=None,
        approximate=None,
        chunk_size=None,
        n_jobs=1,
        num_partition: int = None):
    # TODO need to handle cases when `cutoff_time` is not None

    big_df = entityset.get_big_df()
    print('big_df type',type(big_df))
    repartition_col = EntitySpark.change_col_name(primary_entity, primary_col)
    n_partitions = num_partition if num_partition is not None else big_df.select(repartition_col).distinct().count()
    repartitioned = big_df.repartition(n_partitions, repartition_col)
    print('repartitioned type',type(repartitioned))
    out={'fts':None}
    def run_single_partition(iterator,
                             all_columns: list,
                             es_id: str,
                             entities: list,
                             relationships: list,
                             interestings: list=None):
        #nonlocal out
        list_iter = list(iterator)
        print('in single')
        print('iterator',list_iter[0])
        if len(list_iter) > 0:
            data = pd.DataFrame(list_iter, columns=all_columns)

            es = f.EntitySet(id=es_id)
            for entity in entities:
                columns = entity.columns

                # TODO drop_duplicates here is TOO expensive. How to avoid using it?
                df = data[columns].drop_duplicates()
                entity_id = entity.entity_id
                df.columns = [EntitySpark.recover_col_name(entity_id, col) for col in columns]

                es.entity_from_dataframe(entity_id=entity.entity_id,
                                         dataframe=df,
                                         index=EntitySpark.recover_col_name(entity_id, entity.index),
                                         variable_types=entity.variable_types,
                                         time_index=EntitySpark.recover_col_name(entity_id, entity.time_index),
                                         secondary_time_index=EntitySpark.recover_col_name(entity_id,
                                                                                           entity.secondary_time_index))

            for relationship in relationships:
                parent_entity = relationship.parent_variable.entity_id
                parent_col = EntitySpark.recover_col_name(parent_entity, relationship.parent_variable.column_name)
                child_entity = relationship.child_variable.entity_id
                child_col = EntitySpark.recover_col_name(child_entity, relationship.child_variable.column_name)
                es.add_relationship(f.Relationship(es[parent_entity][parent_col],
                                                    es[child_entity][child_col]))
            if interestings:
                for interesting in interestings:
                    entityid = interesting.entity_id 
                    col = interesting.column
                    intr_vals = interesting.vals
                    es[entityid][col].interesting_values = intr_vals

            feature_matrix, feature_dfs = f.dfs(entityset=es,
                                                 agg_primitives=agg_primitives,
                                                 trans_primitives=trans_primitives,
                                                 where_primitives=where_primitives,
                                                 target_entity=target_entity,
                                                 cutoff_time=cutoff_time,
                                                 cutoff_time_in_index=False,
                                                 n_jobs=n_jobs,
                                                 max_depth=max_depth,
                                                 training_window=training_window,
                                                 approximate=approximate,
                                                 chunk_size=chunk_size)
            
            #if not out['fts']:
            #    out['fts']=feature_dfs
            #    #output_managed_folder = '0XSY6PQb'
            #    schema_folder_path = '/opt/dss_install/managed_folders/DEV_CLAIMSEARCH_DATAENGINEERING/0XSY6PQb'
            #    ft.save_features(feature_dfs, os.path.join(schema_folder_path,"schema1.json"))

            feature_matrix.reset_index(inplace=True)

            columns = sorted(feature_matrix.columns)
            res = []
            for i in range(feature_matrix.shape[0]):
                row_res = {}
                for col in columns:
                    value = feature_matrix.loc[i, col]
                    #value 
                    # convert Numpy types to Python types, otherwise it cannot be converted
                    # to Spark DataFrame.
                    if isinstance(value, np.int64):
                        value = int(value)
                    elif isinstance(value, np.float64):
                        value = float(value)
                    elif isinstance(value, np.bool) or isinstance(value, np.bool_):
                        value = bool(value)
                    else:
                        value = ''
                    row_res[col] = value
                res.append(row_res)
            return res

        else:
            return []

    all_columns = big_df.columns
    es_id = entityset.id
    entities = [entityset.entity_dict[entity].drop_data() for entity in entityset.entity_dict]
    print('enetities are',entities)
    relationships = entityset.relationships
    interestings = entityset.interestings
    print('interestings are',interestings)
    rdd = repartitioned.rdd.mapPartitions(lambda iteration: run_single_partition(iteration, all_columns,
                                                                                 es_id, entities, relationships,interestings))

    print('before rdd')
    # using Rdd of Rows
    res_df = rdd.map(lambda x: Row(**x)).toDF()
    return res_df
