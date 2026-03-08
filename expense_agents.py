import os
import json
import pandas as pd
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

def get_llm():
    # Load environment variables if needed or directly pass them via streamlit context.
    from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
    import streamlit as st
    
    # You can swap ChatOpenAI for ChatGoogleGenerativeAI or ChatGroq here
    return ChatOpenAI(
        model="gpt-3.5-turbo", 
        temperature=0,
    )

def categorization_agent(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agent 1: Categorization Agent
    Takes messy bank descriptions and categorizes them.
    We batch unique descriptions to save tokens and API calls.
    """
    llm = get_llm()
    unique_descriptions = df['Description'].unique().tolist()
    
    # Define the prompt for categorization
    prompt = PromptTemplate(
        template="""
        You are an expert financial categorizer. 
        Categorize the following bank transaction descriptions into one of these exact categories:
        - Digital Payments
        - Investments
        - Entertainment
        - Utilities
        - Cash/Transfer
        - Other

        Return ONLY a valid JSON object where keys are the exact descriptions provided and values are the categories. Do not return markdown.
        Descriptions to categorize:
        {descriptions}
        """,
        input_variables=["descriptions"]
    )
    
    # Establish the chain using the modern LCEL syntax
    chain = prompt | llm | JsonOutputParser()
    
    # Data Passing: This agent takes the unique descriptions list, invokes the LLM, and gets back a parsed JSON dictionary.
    category_mapping = chain.invoke({"descriptions": json.dumps(unique_descriptions)})
    
    # Map the LLM's categorized results back to the entire pandas dataframe
    df['Category'] = df['Description'].map(category_mapping)
    df['Category'] = df['Category'].fillna("Other") # Fallback for unmapped rows
    
    return df

def analysis_agent(df: pd.DataFrame) -> dict:
    """
    Agent 2: Analysis Agent
    Scans the categorized data, flags duplicate subscriptions, and calculates insights.
    """
    llm = get_llm()
    
    # Pre-calculate simple stats to pass context to the agent
    total_outflow = df[df['Type'] == 'Debit']['Amount'].sum()
    
    # Filter potential subscriptions (Entertainment) to find duplicates
    subscriptions = df[df['Category'] == 'Entertainment'].to_dict('records')
    
    prompt = PromptTemplate(
        template="""
        You are a financial analysis AI. 
        Total outflow is ₹{total_outflow}.
        
        Here is a list of subscription/entertainment transactions:
        {subscriptions}
        
        Your task:
        1. Identify any duplicate subscriptions (same description, same amount, occurring roughly close in dates, e.g., within a couple of days).
        2. Provide a short summary of the user's spending habits based on the total.

        Return a JSON object with this exact schema (no markdown, just valid JSON):
        {{
            "total_outflow": {total_outflow},
            "duplicate_flags": ["list of strings detailing the duplicates found"],
            "analysis_summary": "a short paragraph of insights"
        }}
        """,
        input_variables=["total_outflow", "subscriptions"]
    )
    
    chain = prompt | llm | JsonOutputParser()
    
    # Data Passing: This agent receives pre-processed aggregated data (total_outflow, filtered records) and generates structured insights.
    insights = chain.invoke({
        "total_outflow": total_outflow,
        "subscriptions": json.dumps(subscriptions, default=str)
    })
    
    return insights
