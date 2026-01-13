import streamlit as st
import fitz
import openai

st.set_page_config(page_title="Alina's PDF Summarizer", page_icon="🍱",layout= "wide")
st.title("📄 AI-Powered PDF Summarizer")
st.write("Upload a PDF and get an instant AI-generated summary!")

with st.sidebar:
    st.header("🔑 Enter Your Key!")
    user_key = st.text_input("OpenAI API Key", type="password")
    st.info("This key is only used temporarily and not stored :D")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and user_key:
    if st.button("✨ Summarize PDF"):
        with st.spinner("Reading PDF and generating summary..."):
            try:
                with open("temp.pdf", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                with fitz.open("temp.pdf") as doc:
           
                	all_text = ""
                	for page in doc:
                    		all_text += page.get_text()
                                
                with st.expander("View a snippet to check your doc got uplaoded right!"):
                    st.text(all_text[:1000] + "...")                
                    openai.api_key = user_key
                    response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Create a summary of the users document."},
                        {"role": "user", "content": f"Please provide a clear and concise summary of this document:\n\n{all_text}"}
                    ]
                )
                
                summary = response.choices[0].message.content
                
                st.success("Summary generated successfully!")
                st.markdown("### 📝 Summary:")
                st.write(summary)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif uploaded_file is None:
    st.info("Upload a File to Get Started!")
elif not user_key:
    st.warning("First upload your API Key ⚠️")
