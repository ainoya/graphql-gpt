import json
import pandas as pd
from gql import gql, Client


class GraphQLRunner:
    def __init__(self, gqlClient: Client) -> None:
        self.gqlClient = gqlClient

    def run_query(self, query):
        gql_query = gql(query)

        query_result = self.gqlClient.execute(gql_query)

        query_result_list = []
        for key in query_result:
            query_result_list.append({
                'name': key,
                'dataframe': pd.json_normalize(query_result[key])})

        # error if the query_result_list is empty
        if len(query_result_list) == 0:
            raise Exception('query_result_list is empty')

        return query_result_list
