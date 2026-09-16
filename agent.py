import os
from typing import TypedDict, List

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


class ShoppingState(TypedDict):
    user_query: str
    search_query: str
    products: List
    analysis: str
    recommendation: str


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


def understand_request(state):

    prompt = f"""
    Analyze this shopping request:

    {state["user_query"]}

    Identify the product category, budget,
    intended use and important features.

    Then create a useful product search query.

    Return only the search query.
    """

    response = llm.invoke(prompt)

    return {
        "search_query": response.content
    }


def search_products(query):

    # Product API will be connected here.

    return []


def search_node(state):

    products = search_products(
        state["search_query"]
    )

    return {
        "products": products
    }


def analyze_products(state):

    products_text = "\n\n".join(
        [
            f"""
            Product: {p.get("title", "Unknown")}
            Price: {p.get("price", "Unknown")}
            Description: {p.get("description", "")}
            """
            for p in state["products"]
        ]
    )

    prompt = f"""
    User request:
    {state["user_query"]}

    Products:
    {products_text}

    Analyze the products based on:
    price, features, value, advantages,
    disadvantages and suitability.

    Do not invent information.
    """

    response = llm.invoke(prompt)

    return {
        "analysis": response.content
    }


def recommend_products(state):

    prompt = f"""
    User request:
    {state["user_query"]}

    Product analysis:
    {state["analysis"]}

    Give:

    1. Best overall
    2. Best budget option
    3. Best alternative

    Explain why each is recommended.

    Do not invent information.
    """

    response = llm.invoke(prompt)

    return {
        "recommendation": response.content
    }


graph = StateGraph(ShoppingState)

graph.add_node(
    "understand",
    understand_request
)

graph.add_node(
    "search",
    search_node
)

graph.add_node(
    "analyze",
    analyze_products
)

graph.add_node(
    "recommend",
    recommend_products
)

graph.add_edge(
    START,
    "understand"
)

graph.add_edge(
    "understand",
    "search"
)

graph.add_edge(
    "search",
    "analyze"
)

graph.add_edge(
    "analyze",
    "recommend"
)

graph.add_edge(
    "recommend",
    END
)

shopping_agent = graph.compile()
