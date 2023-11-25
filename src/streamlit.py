import streamlit as st
from pdf2html import *
from text2graph_main import *
from text2graph_utils import *
from table_query import * 
from graph_chat import *
from concurrent.futures import ThreadPoolExecutor
from streamlit_image_select import image_select
import numpy as np

@st.cache_resource(show_spinner=False)
def load_functions(path_in):
    with ThreadPoolExecutor() as executor:
        future_graph = executor.submit(create_graph_database, path_in)
        future_tables = executor.submit(AzureReadModule, give_byte_arr(path_in))
        future_images = executor.submit(get_images_from_pdf, path_in, "image_output")
        

        # Wait for all tasks to complete
        graph_result = future_graph.result()
        tables_result = future_tables.result()
        images_result = future_images.result()
    

    return graph_result, tables_result#, images_result

@st.cache_resource(show_spinner=False)
def load_models():
    model, processor = load_model()
    return model, processor

def reset(folder_path):
    st.session_state = {}
    if folder_path!= "":
        
        files = os.listdir(folder_path)

        # Iterate through the files and delete them
        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

# Function to define the Home page
def home():
    st.image("data:image/png;base64,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", use_column_width=False, width=600)
    st.subheader(
        "Hola! 👋"
    )
    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    # Process the uploaded file
    if uploaded_file is not None:
        # st.subheader("Uploaded PDF Contents:")
        path_in = uploaded_file.name
        with st.spinner("Parsing Pdf..."):
            graph,tables = load_functions(path_in)
            model, processor = load_models()
            if 'graph' not in st.session_state:
                st.session_state['graph'] = graph
            if 'tables' not in st.session_state:
                st.session_state['tables'] = tables
            if 'model' not in st.session_state:
                st.session_state['model'] = model
            if 'processor' not in st.session_state:
                st.session_state['processor'] = processor
            st.success("PDF Loaded")
    
    reset_button = st.button("Reset")
    if reset_button:
        reset("")

# Function to define the Asbout page
def Text2Graph():
    st.title("📄 Text2Graph")
    st.write(
        "Text2Graph facilitates interactive conversations and queries with a knowledge graph through natural language text."
    )
    query = st.text_input("Query the database")
    # Create a simple button
    button_clicked = st.button("Submit")

    # Check if the button is clicked
    if button_clicked:
        output = query_graph_database(st.session_state['graph'], query)
        st.write(output)
    reset_button = st.button("Reset")
    if reset_button:
        reset("")
# Function to define the Asbout page
def graph_chat():
    st.title("📄 Graph Chat")
    st.subheader(
        "Talk to your graph/chart! 📊"
    )
    # Path to the folder containing images
    images_folder = "image_output"
    image_files = [os.path.join(images_folder, i) for i in os.listdir(images_folder)]
    if len(image_files)==0:
        st.write("Please upload a PDF with images")
    else:
        selected_image = image_select(
            label="Select a option",
            images=[np.array(Image.open(i)) for i in image_files], return_value="index"
        )
        st.image(image_files[selected_image],width=500)
        query = st.text_input("Enter your query")
        button_clicked = st.button("Submit")


        # Check if the button is clicked
        if button_clicked:
            data_table = generate_table(image_files[selected_image], st.session_state['model'], st.session_state['processor'])
            out = process_query(data_table, query)
            st.write(out)
        reset_button = st.button("Reset")
        if reset_button:
            reset(images_folder)

def table_chat():
    st.title("📄 Table Chat")
    st.subheader(
        "Talk to your table! 💻"
    )
    # Path to the folder containing images
    images_folder = "table_output"
    image_files = [os.path.join(images_folder, i) for i in os.listdir(images_folder)]
    if len(image_files)==0:
        st.write("Please upload a PDF with images")
    else:
        selected_image_idx = image_select( 
            label="Select a option",
            images=[np.array(Image.open(i)) for i in image_files],return_value="index")
        st.image(image_files[selected_image_idx],width=500)
        query = st.text_input("Query the database")
        # Create a simple button
        button_clicked = st.button("Submit")
        #st.success(st.session_state['tables'][0])
        # Check if the button is clicked
        if button_clicked:
            output = query_llm(st.session_state['tables'][selected_image_idx],query)
            st.write(output)
        reset_button = st.button("Reset")
        if reset_button:
            reset("table_output")
    

# Function to create a navigation sidebar with beautifications
def navigation():
    st.sidebar.title("🚀 Infinite exploration")
    selected_page = st.sidebar.selectbox("Select a page", ["Home", "Text2Graph","Graph Chat","Table Chat"])
    # Sidebar options that are always visible
    
    #home_ = st.sidebar.button("Home")
    #home()
    # Conditionally show additional options based on the condition
    # if 'graph' in st.session_state:
    #     text2graph = st.sidebar.button("Text2Graph")
    #     graphchat =st.sidebar.button("Graph Chat")
    #     tablechat =st.sidebar.button("Table Chat")
    #     if text2graph:
    #         Text2Graph()
    #     elif graphchat:
    #         graph_chat()
    #     elif tablechat:
    #         table_chat()
    
    #     elif home_:
    #         home()
    # Display content based on selected page
    if selected_page == "Home":
        home()
    elif selected_page == "Text2Graph":
        Text2Graph()
    elif selected_page == "Graph Chat":
        graph_chat()
    elif selected_page == "Table Chat":
        table_chat()


# Main function to run the app
def main():
    st.set_page_config(
        page_title="UiPath Multi-Purpose app",
        page_icon="✨",
        #layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
            .sidebar .sidebar-content {
                background-image: linear-gradient(to bottom, #7db9e8, #f5f5f5);
                color: #333;
            }
            .Widget>label {
                color: #555;
            }
            .st-eb {
                background-color: #f5f5f5;
            }
            .st-ec {
                color: #333;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    navigation()

# Run the app
if __name__ == "__main__":
    main()
