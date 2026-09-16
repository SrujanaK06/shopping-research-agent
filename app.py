
import streamlit as st

from agent import shopping_agent


st.set_page_config(
    page_title="Shopping Research Agent",
    page_icon="🛒"
)


st.title("🛒 Shopping Research Agent")

st.write(
    "Tell me what you want to buy, "
    "your budget and what you need it for."
)


query = st.text_area(
    "What are you looking for?",
    placeholder="Example: Find the best headphones under ₹5000 for studying"
)


if st.button("🔍 Research Products"):

    if query:

        with st.spinner("Researching products..."):

            result = shopping_agent.invoke({
                "user_query": query,
                "search_query": "",
                "products": [],
                "analysis": "",
                "recommendation": ""
            })

        st.subheader("✨ Recommendation")

        st.write(
            result["recommendation"]
        )

    else:

        st.warning(
            "Please enter a shopping request."
        )
