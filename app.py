import json
import traceback
import streamlit as st
import os
from langchain import OpenAI
from langchain.document_loaders import DirectoryLoader

from langchain.llms import OpenAI
from indexer import Indexer
from graphql_query_runner import GraphQLRunner

from query_converter import QueryConverter

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


llm = OpenAI(model_name="text-davinci-003", temperature=0)

transport = AIOHTTPTransport(url="http://localhost:8080/v1/graphql")
client = Client(transport=transport)


@st.cache_resource
def create_index():
    schema = json.load(open('schema.json'))

    return Indexer(schema, llm).run()


docsearch = create_index()

query_converter = QueryConverter(docsearch, llm)

graphql_query_runner = GraphQLRunner(client)

st.title("GPT + GraphQL")

text = "Show me latest 10 pets."
question = st.text_area("question", placeholder=text)

if st.button("Send"):
    try:
        with st.spinner('Wait for it...'):
            query = query_converter.run(question)
            st.markdown("## Query")
            st.markdown(f"```\n{query}\n```")
            st.markdown("## Query Result")
            query_result_list = graphql_query_runner.run_query(query)
            for query_result in query_result_list:
                st.markdown(f"### {query_result['name']}")
                st.table(query_result['dataframe'])
    except Exception as e:
        # print error and traceback
        print(f"error: {e}")
        print(traceback.format_exc())
        st.error(e)
