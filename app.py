import streamlit as st
from sql_chain_llm import few_shots_chain


st.set_page_config(
    page_title="Retail Database Helper Q/A",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def initializechain():
    chain = few_shots_chain()
    return chain

chain = initializechain()


st.title("📊 Retail Database Helper Q/A") 
st.markdown("""
### Example Questions:
- "How many Tshirts are left in Stock which are White and size XS?"
- "What is the total revenue from discounted items?"
- "What is the average discount given on adidas products?"
- "How much sales amount will be generated if we sell all large size Nike t-shirts today after discounts?"
""")


st.sidebar.title("Instructions")
st.sidebar.markdown("""
### Welcome to the Retail Database Helper!
You can ask questions about sales, revenue, product availability, and more from your retail database.

### How to Use:
1. Type your question in the input box.
2. Click the "Submit" button to get your answer.
3. The answer will be displayed below your question.
""")


question = st.text_input("Enter your question below:")


if question:
    st.subheader("Answer")
    with st.spinner('Fetching the answer...'):
        try:
            answer = chain.run(question) 
            st.markdown(f"### {answer}") 
        except Exception as e:
            st.error(f"Database has no such Data")

st.sidebar.markdown("""
---
*Powered by LangChain and Streamlit*  
For more information on this app, check out [GitHub](https://github.com/Lakshay9296/).
""")
