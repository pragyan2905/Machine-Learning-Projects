import os
import json
import re
import sys
import io
import contextlib
import warnings
from typing import Optional, List, Any, Tuple
from PIL import Image
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from together import Together
from e2b_code_interpreter import Sandbox

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)

def code_interpret(e2b_code_interpreter: Sandbox, code: str) -> Optional[List[Any]]:
    with st.spinner('🧠 Running code securely in your sandbox...'):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                exec_result = e2b_code_interpreter.run_code(code)

        if stderr_capture.getvalue():
            print("[Sandbox Warnings]", file=sys.stderr)
            print(stderr_capture.getvalue(), file=sys.stderr)

        if stdout_capture.getvalue():
            print("[Sandbox Output]", file=sys.stdout)
            print(stdout_capture.getvalue(), file=sys.stdout)

        if exec_result.error:
            print(f"[Sandbox Error] {exec_result.error}", file=sys.stderr)
            return None
        return exec_result.results

def match_code_blocks(llm_response: str) -> str:
    match = pattern.search(llm_response)
    if match:
        return match.group(1)
    return ""

def chat_with_llm(e2b_code_interpreter: Sandbox, user_message: str, dataset_path: str) -> Tuple[Optional[List[Any]], str]:
    system_prompt = f"""You are a data analysis agent running in a secure code interpreter.
The user's dataset is available at '{dataset_path}'.

**Instructions for Generating Code:**
1.  Load the dataset using the path: '{dataset_path}'.
2.  To create a visualization, generate the code for the plot using libraries like Matplotlib or Seaborn.
3.  **IMPORTANT**: Do NOT save the plot to a file (do not use `plt.savefig()`).
4.  The environment will automatically capture and display the plot if it's the last thing your code generates. You do not need to use `plt.show()`.

Based on the user's query, provide a Python code block that follows these rules to generate an analysis or visualization.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    with st.spinner('🤖 Thinking...'):
        client = Together(api_key=st.session_state.together_api_key)
        response = client.chat.completions.create(
            model=st.session_state.model_name,
            messages=messages,
        )

        response_message = response.choices[0].message
        python_code = match_code_blocks(response_message.content)
        
        if python_code:
            code_results = code_interpret(e2b_code_interpreter, python_code)
            return code_results, response_message.content
        else:
            st.warning("⚠️ Couldn't extract Python code from the AI response.")
            return None, response_message.content

def upload_dataset(code_interpreter: Sandbox, uploaded_file) -> str:
    dataset_path = f"/{uploaded_file.name}"
    try:
        # Use getvalue() to get bytes from the uploaded file
        content_bytes = uploaded_file.getvalue()
        code_interpreter.files.write(dataset_path, content_bytes)
        return dataset_path
    except Exception as error:
        st.error(f"❌ Error uploading file: {error}")
        raise error

def main():
    st.set_page_config(page_title="DataSage AI", page_icon="📈")
    st.title("📈 DataSage AI")
    st.markdown("Let **DataSage** uncover insights from your dataset with the power of AI.")

    # Session state init
    if 'together_api_key' not in st.session_state:
        st.session_state.together_api_key = ''
    if 'e2b_api_key' not in st.session_state:
        st.session_state.e2b_api_key = ''
    if 'model_name' not in st.session_state:
        st.session_state.model_name = ''

    with st.sidebar:
        st.header("🔑 Configure AI Engine")
        st.session_state.together_api_key = st.text_input("Together AI API Key", type="password")
        st.markdown("[Get Together API Key](https://api.together.ai/signin)")

        st.session_state.e2b_api_key = st.text_input("E2B API Key", type="password")
        st.markdown("[Get E2B API Key](https://e2b.dev/docs/legacy/getting-started/api-key)")

        st.subheader("💡 Pick an AI Model")
        model_options = {
            "Meta-Llama 3.1 405B": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            "DeepSeek V3": "deepseek-ai/DeepSeek-V3",
            "Qwen 2.5 7B": "Qwen/Qwen2.5-7B-Instruct-Turbo",
            "Meta-Llama 3.3 70B": "meta-llama/Llama-3.3-70B-Instruct-Turbo"
        }
        model_choice = st.selectbox("Choose a model", list(model_options.keys()))
        st.session_state.model_name = model_options[model_choice]

    uploaded_file = st.file_uploader("📂 Upload a CSV dataset", type="csv")

    if uploaded_file is not None:
        try:
            # Reset file pointer to the beginning before reading
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
            st.subheader("🧾 Data Preview")
            if st.checkbox("Show entire dataset"):
                st.dataframe(df)
            else:
                st.dataframe(df.head())

            # Reset file pointer again before uploading to sandbox
            uploaded_file.seek(0)
            
            st.markdown("### 🧠 Ask DataSage anything about your data:")
            query = st.text_area("Your question", "E.g. What are the trends in this dataset? Plot a histogram of the first numerical column.")

            if st.button("🔍 Get Insights"):
                if not st.session_state.together_api_key or not st.session_state.e2b_api_key:
                    st.error("⚠️ Please provide both API keys in the sidebar.")
                else:
                    with Sandbox(api_key=st.session_state.e2b_api_key) as code_interpreter:
                        # ✅ **CORRECTION**: Use run_code to import libraries into the sandbox environment.
                        # This ensures they are available for the AI-generated code.
                        import_code = "import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport plotly.express as px"
                        code_interpreter.run_code(import_code)
                        
                        dataset_path = upload_dataset(code_interpreter, uploaded_file)
                        code_results, llm_response = chat_with_llm(code_interpreter, query, dataset_path)

                        st.subheader("📘 AI's Response")
                        st.write(llm_response)

                        st.subheader("📊 Visual Output")
                        if code_results:
                            for result in code_results:
                                if hasattr(result, 'png') and result.png:
                                    png_data = base64.b64decode(result.png)
                                    image = Image.open(BytesIO(png_data))
                                    st.image(image, caption="📈 Visualization", use_container_width=True)
                                elif hasattr(result, 'figure'):
                                    st.pyplot(result.figure)
                                elif hasattr(result, 'show'):
                                    st.plotly_chart(result)
                                elif isinstance(result, (pd.DataFrame, pd.Series)):
                                    st.dataframe(result)
                                else:
                                    st.write(result)
                        else:
                            st.info("🤔 No visualization or other output was returned.")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()