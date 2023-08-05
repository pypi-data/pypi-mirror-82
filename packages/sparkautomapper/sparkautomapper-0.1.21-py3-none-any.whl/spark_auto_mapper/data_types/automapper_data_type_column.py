from pyspark.sql import Column
# noinspection PyUnresolvedReferences
from pyspark.sql.functions import col

from spark_auto_mapper.data_types.automapper_data_type_base import AutoMapperDataTypeBase


class AutoMapperDataTypeColumn(AutoMapperDataTypeBase):
    def __init__(self, value: str):
        super().__init__()
        self.value: str = value

    def get_column_spec(self) -> Column:
        if isinstance(self.value, str):  # if the src column is just string then consider it a sql expression
            return col(self.value)

        raise ValueError(f"value: {self.value} is not str")
