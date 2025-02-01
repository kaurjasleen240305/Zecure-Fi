import os
import sys
from aave_constants import AAVE_FACTORY_ABI,AAVE_GATEWAY_ABI,get_factory_address
from aerodrome_constants import GENERIC_TOKEN_METADATA_URI,AERODROME_FACTORY_ABI,get_factory_address

# import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from cdp_langchain.tools import CdpTool
from langgraph.prebuilt import create_react_agent
from groq import Groq
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
# from langchain.prompts import PromptTemplate


from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from cdp import Wallet
# from langchain_huggingface import HuggingFacePipeline
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

import json


# Load environment variables from .env file
load_dotenv()



# Configure wallet data file
wallet_data_file = "wallet_data_mainnet.txt"

# Get Graph API key from environment variables
GRAPH_API_KEY = os.getenv('GRAPH_API_KEY')
if not GRAPH_API_KEY:
    raise ValueError("Please set GRAPH_API_KEY in your .env file")

# Updated subgraph endpoint for Aave V2
GATEWAY_URL = "https://gateway.thegraph.com/api"

AAVE_V2_SUBGRAPH = f"{GATEWAY_URL}/{GRAPH_API_KEY}/subgraphs/id/C2zniPn45RnLDGzVeGZCx2Sw3GXrbc9gL4ZfL8B8Em2j"

AAVE_MARKETS_PROMPT = """
This tool queries Aave V2 market data from The Graph Protocol.
You can ask questions like:
- "What are the current supply rates for USDC?"
- "Show me the borrow rates for ETH"
- "Get the total liquidity in Aave markets"
"""

class AaveMarketsQueryInput(BaseModel):
    """Input schema for Aave market queries."""
    address: str = Field(
        ...,
        description="Wallet address", example="0x54651adfd19b33B5E4A5027bE9d6aE02C1C3284E"
    )
   

def setup_graph_client(subgraph_url: str) -> Client:
    """Set up a Graph Protocol client for the given subgraph."""
    transport = RequestsHTTPTransport(
        url=subgraph_url,
        verify=True,
        retries=3,
    )
    return Client(transport=transport, fetch_schema_from_transport=True)

def format_number(value: float, decimals: int = 2) -> str:
    """Format numbers to avoid scientific notation and limit decimals."""
    return f"{round(value, decimals):,.{decimals}f}"

def query_aave_markets(address: str) -> dict:
    """Query Aave V2 market data from The Graph."""
    print("heloooo")
    client = setup_graph_client(AAVE_V2_SUBGRAPH)
    
    protocolAAVE_Query = gql("""
    query AaveQuery($address: ID!) {
        account(id: $address) {
            id
            depositCount
            liquidateCount
            openPositionCount
            closedPositionCount
            repayCount
            borrowCount
            liquidationCount

            deposits {
                id
                amount
                amountUSD
                timestamp
            }

            borrows {
                id
                amount
                amountUSD
                asset {
                    name
                    symbol
                    decimals
                }
            }

            liquidations {
                id
                amount
                amountUSD
                asset {
                    name
                    symbol
                    decimals
                }
            }

            repays {
                id
                amount
                amountUSD
                asset {
                    name
                    symbol
                    decimals
                }
            }
        }
        
    }
    """)

    try:
        result = client.execute(protocolAAVE_Query, variable_values={"address": address.lower()})

        # Ensure account data exists
        account_data = result.get("account")
        if not account_data:
            return {"error": f"No market data found for address {address}"}

        # Extract key details
        total_deposit_amount = sum(float(deposit["amountUSD"]) for deposit in account_data["deposits"])
        total_borrow_amount = sum(float(borrow["amountUSD"]) for borrow in account_data["borrows"])
        total_repay_amount = sum(float(repay["amountUSD"]) for repay in account_data["repays"])
        total_liquidation_amount = sum(float(liquidation["amountUSD"]) for liquidation in account_data["liquidations"])

        # Return the results
        return {
            "address": account_data["id"],
            "total_deposit_amount": total_deposit_amount,
            "total_borrow_amount": total_borrow_amount,
            "total_repay_amount": total_repay_amount,
            "total_liquidation_amount": total_liquidation_amount
        }

    except Exception as e:
        print(f"Error during GraphQL execution: {str(e)}")
        return {"error": f"Error querying Aave data: {str(e)}"}
    

AAVE_SUPPLY_PROMPT = """
This tool allows you to supply tokens to the Aave lending protocol, enabling you to earn yield on your assets. 
By supplying your tokens, you contribute to the liquidity of the protocol and can earn interest over time. 
It is only supported on Base Sepolia and Base Mainnet.
"""


class AaveSupplyInput(BaseModel):
    """Input argument schema for aave supply."""

    amount: str = Field(
        ..., description="The amount of the asset to transfer, e.g. `15`, `0.000001`"
    )
    asset_id: str = Field(
        ...,
        description="The asset ID to transfer, e.g. `eth`, `0x036CbD53842c5426634e7929541eC2318f3dCF7e`",
    )


def aave_supply_token(wallet: Wallet, amount: str, asset_id: str) -> str:
    """Supply tokens to the Aave.

    Args:
        wallet (Wallet): The wallet to create the token from.
        amount (str): The amount of the asset to transfer, e.g. `15`, `0.000001`.
        asset_id (str): The asset ID to transfer (e.g. `0x036CbD53842c5426634e7929541eC2318f3dCF7e`).

    Returns:
        str: A message containing the token supply details.

    """
    print("rtyeueie")
    factory_address = get_factory_address(wallet.network_id)
    if asset_id.lower() == "eth" or asset_id.lower() == "0x0000000000000000000000000000000000000000":
        try:
            invocation = wallet.invoke_contract(
                contract_address="0x729b3EA8C005AbC58c9150fb57Ec161296F06766",
                method="depositETH",
                abi=AAVE_GATEWAY_ABI,
                args={
                    "": "0x0000000000000000000000000000000000000000",
                    "onBehalfOf": "0x38C25E19293Ec9fa21354713D445D733041Cfa0D",
                    "referralCode": "0",
                },
                amount=amount,
            ).wait()
        except Exception as e:
            return f"Supply failed {e!s}"
    else:
        try:
            invocation = wallet.invoke_contract(
                contract_address=factory_address,
                method="supply",
                abi=AAVE_FACTORY_ABI,
                args={
                    "asset": asset_id,
                    "amount": amount,
                    "onBehalfOf": "0x38C25E19293Ec9fa21354713D445D733041Cfa0D",
                    "referralCode": "0",
                },
            ).wait()
        except Exception as e:
            return f"Supply failed {e!s}"

    return f"AAVE supply {amount} of {asset_id} on network {wallet.network_id}.\nTransaction hash for the aave supply: {invocation.transaction.transaction_hash}\nTransaction link for the aave supply: {invocation.transaction.transaction_link}"




AERODROME_ADD_LIQUIDITY_PROMPT = """
This tool will add liquidity to the Aerodrome protocol using the specified token pair. 
It requires the token addresses and the amounts you wish to supply for each token. 
The liquidity provision mechanism ensures that your assets are effectively utilized within the Aerodrome ecosystem. 
This operation is supported on both Base Sepolia and Base Mainnet.
"""


class AerodromeAddLiquidityInput(BaseModel):
    """Input argument schema for aerodrome add liquidity action."""

    name: str = Field(
        ...,
        description="The name of the token to create, e.g. WowCoin",
    )
    symbol: str = Field(
        ...,
        description="The symbol of the token to create, e.g. WOW",
    )


def aerodrome_add_liquidity(wallet: Wallet, name: str, symbol: str) -> str:
    """Create a Zora Wow ERC20 memecoin.

    Args:
        wallet (Wallet): The wallet to create the token from.
        name (str): The name of the token to create.
        symbol (str): The symbol of the token to create.

    Returns:
        str: A message containing the token creation details.

    """
    factory_address = get_factory_address(wallet.network_id)

    try:
        invocation = wallet.invoke_contract(
            contract_address=factory_address,
            method="deploy",
            abi=AERODROME_FACTORY_ABI,
            args={
                "_tokenCreator":"0x38C25E19293Ec9fa21354713D445D733041Cfa0D",
                "_platformReferrer": "0x0000000000000000000000000000000000000000",
                "_tokenURI": GENERIC_TOKEN_METADATA_URI,
                "_name": name,
                "_symbol": symbol,
            },
        ).wait()
    except Exception as e:
        return f"Error creating Zora Wow ERC20 memecoin {e!s}"

    return f"Created WoW ERC20 memecoin {name} with symbol {symbol} on network {wallet.network_id}.\nTransaction hash for the token creation: {invocation.transaction.transaction_hash}\nTransaction link for the token creation: {invocation.transaction.transaction_link}"

REQUEST_YIELD_OPPORTUNITY_PROMPT = """
This tool will compare various yield generation to help you select the best yield available. 
By analyzing different protocols and their respective yield rates, this tool provides insights to maximize your returns. 
It considers factors such as risk, liquidity, and duration to ensure you make informed decisions. 
This feature is essential for optimizing your investment strategy and increasing overall profitability.
It is only supported on Base Sepolia and Base Mainnet.
"""
class RequestYieldOpportunityInput(BaseModel):
    """Input argument schema for request yield generation action."""
def request_yield_generation(wallet: Wallet) -> str:
    """Request yield generation for the default address in the wallet.
    Args:
        wallet (Wallet): The wallet to yield generation
    Returns:
        str: Confirmation message with transaction details
    """
    try:
        ""
    except Exception as e:
        return f"Error requesting yield generation {e!s}"
    return f"aave supply"


with open("tokenizer_config.json") as config_file:
    config = json.load(config_file)



def initialize_agent():
    """Initialize the agent with CDP Agentkit."""
    # Initialize LLM.
    # llm = ChatOpenAI(model="gpt-4o-mini")
    # llm = ChatAnthropic(model='claude-3-opus-20240229')
    # llm = Langchain(api_key=os.getenv("GEMINI_API_KEY"))

    # llm = ChatGoogleGenerativeAI(
    #     model="gemini-1.5-pro",
    #     google_api_key=os.getenv("GEMINI_API_KEY")
    #     )
    

    # llm = HuggingFaceEndpoint(
    #     repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    #     huggingfacehub_api_token=os.getenv('HUGGINGFACEHUB_API_TOKEN'),
    # )

    # chat_model = ChatHuggingFace(
    #     llm=llm,
    #     )
    # print("hello")
#     llm=Groq(
#     api_key=os.environ.get("GROQ_API_KEY"),
#     model="llama-3.3-70b-versatile"
# )
    llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)
    print("LLM",llm)
    
    # model_name = "meta-llama/Meta-Llama-3-8B"
    
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    # llm = HuggingFacePipeline(pipeline=llm_pipeline)

#     llm = ChatOpenAI(
#     model="meta-llama/Meta-Llama-3-8B",  # Adjust to your model
#     openai_api_base="https://api.together.xyz/v1",  # Llama API endpoint
#     openai_api_key=os.getenv("LLAMA_API_KEY"),  # Your API Key
   
# )

    wallet_data = None

    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    # Configure CDP Agentkit Langchain Extension.
    values = {}
    if wallet_data is not None:
        # If there is a persisted agentic wallet, load it and pass to the CDP Agentkit Wrapper.
        values = {"cdp_wallet_data": wallet_data}

    agentkit = CdpAgentkitWrapper(**values)

    # persist the agent's CDP MPC Wallet Data.
    wallet_data = agentkit.export_wallet()
    with open(wallet_data_file, "w") as f:
        f.write(wallet_data)

    # Initialize CDP Agentkit Toolkit and get tools.
    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
    tools = cdp_toolkit.get_tools()

    aaveProtocolTool = CdpTool(

        name="query_aave",
        description=AAVE_MARKETS_PROMPT,
        cdp_agentkit_wrapper=agentkit,
        args_schema=AaveMarketsQueryInput,
        func=query_aave_markets,
        
        )
    
    aaveSupplyAction = CdpTool(
    
    name="aave_supply",
    description=AAVE_SUPPLY_PROMPT,
    cdp_agentkit_wrapper=agentkit,
    args_schema=AaveSupplyInput,
    func=aave_supply_token,
    )

    AerodromeAddLiquidityAction = CdpTool(
 
    name="aerodrome_add_liquidity",
    description=AERODROME_ADD_LIQUIDITY_PROMPT,
    cdp_agentkit_wrapper=agentkit,
    args_schema=AerodromeAddLiquidityInput,
    func=aerodrome_add_liquidity,

    )

    RequestYieldOpportunityAction= CdpTool(
    
    name = "request_yield_generation",
    description= REQUEST_YIELD_OPPORTUNITY_PROMPT,
    args_schema = RequestYieldOpportunityInput,
    cdp_agentkit_wrapper=agentkit,
    func = request_yield_generation,
    )
    
    tools.append(aaveProtocolTool)
    tools.append(aaveSupplyAction)
    tools.append(AerodromeAddLiquidityAction)
    tools.append(RequestYieldOpportunityAction)

    # Store buffered conversation history in memory.
    memory = MemorySaver()
    # config = {"configurable": {"thread_id": "CDP Agentkit Chatbot Example!"}}

    # Create ReAct Agent using the LLM and CDP Agentkit tools.
    return create_react_agent(
        llm,
        checkpointer=memory,
        # model="llama-3.3-70b-versatile",
        tools=tools,
        state_modifier=
        "You are a helpful agent that can interact onchain using the Coinbase Developer Platform Agentkit. You are empowered to interact onchain using your tools. If you ever need funds, you can request them from the faucet if you are on network ID `base-sepolia`. If not, you can provide your wallet details and request funds from the user. If someone asks you to do something you can't do with your currently available tools, you must say so, and encourage them to implement it themselves using the CDP SDK + Agentkit, recommend they go to docs.cdp.coinbase.com for more informaton. Be concise and helpful with your responses. Refrain from restating your tools' descriptions unless it is explicitly requested.",
    ), config


# Chat Mode
def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            # print("hello")
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config):
                # print(chunk)
                # print("hello")

                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)


def main():
    """Start the chatbot agent."""
    agent_executor, config = initialize_agent()

    run_chat_mode(agent_executor=agent_executor, config=config)



if __name__ == "__main__":
    print("Starting Agent...")
    main()
