import os
import openai
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import AzureSearch
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

# Load environment variables
# load_dotenv('.env')

# This is an attempt that is working fine in .ipynb but here AzureChatOpenAI fails to get these credentials from this method.
#os.getenv also failed to get the variables
# openai.api_type = "azure"
# openai.api_base ="https://htioaiservice.openai.azure.com/"
# openai.api_key ="a4e7007a05654dcc97722d1671249ece"
# openai.api_version ="2023-05-15"




# Configure OpenAI API (THIS IS WORKING with and without os.getenv())
os.environ["OPENAI_API_TYPE"] ="azure"
os.environ["OPENAI_API_BASE"]="https://htioaiservice.openai.azure.com/"
os.environ["OPENAI_API_KEY"]="a4e7007a05654dcc97722d1671249ece"
os.environ["OPENAI_API_VERSION"]="2023-05-15"

llm = AzureChatOpenAI(deployment_name="htiOaiDEP")
embeddings = OpenAIEmbeddings(deployment_id="htiOaiDEPte", chunk_size=1)


#Unable to use cognitive service even after defining the variables, possibly one instance support.
# Set environment variables for Azure Cognitive Services
acs = AzureSearch(azure_search_endpoint=os.getenv('AZURE_COGNITIVE_SEARCH_SERVICE_NAME'),
                 azure_search_key=os.getenv('AZURE_COGNITIVE_SEARCH_API_KEY'),
                 index_name=os.getenv('AZURE_COGNITIVE_SEARCH_INDEX_NAME'),
                 embedding_function=embeddings.embed_query)



# llm = AzureChatOpenAI(deployment_name="htiOaiDEP")
# embeddings = OpenAIEmbeddings(deployment_id="htiOaiDEPte", chunk_size=1)


# # Connect to Azure Cognitive Search
# acs = AzureSearch(azure_search_endpoint=AZURE_COGNITIVE_SEARCH_SERVICE_NAME,
#                  azure_search_key=AZURE_COGNITIVE_SEARCH_API_KEY,
#                  index_name=AZURE_COGNITIVE_SEARCH_INDEX_NAME,
#                  embedding_function=embeddings.embed_query)