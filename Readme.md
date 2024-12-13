# OwnGPT

OwnGPT is an offline and online real-time assistant that leverages advanced AI techniques to provide informative responses based on user queries. It integrates with Google search to fetch relevant information and uses a vector database for efficient context retrieval.

## Features

- Fetches search results from Google.
- Extracts and cleans text from web pages.
- Stores extracted texts in a vector database.
- Generates comprehensive responses based on user queries and retrieved context.

## Installation

Install some pre-requesites : 

1. Install Ollama from web.
2. RUN
```
ollama pull llama3.2
```
To install OwnGPT, clone the repository and install the required packages:
```
git clone https://github.com/Abhay06102003/OwnGPT.git
cd OwnGPT
pip install .
```

## Usage

### Running the Flask Application

To start the Flask application, run:

```bash
python -m OwnGPT.app
```

The application will be available at `http://127.0.0.1:8000`.

### Command Line Interface

You can also use OwnGPT from the command line. To query the assistant, use:

```bash
owngpt query "Your query here"
```

### API Endpoints

- **POST /ask**: Send a JSON request with your query to get a response.
  - **Request Body**:
    ```json
    {
      "query": "Your query here"
    }
    ```
  - **Response**:
    ```json
    {
      "response": "Generated response based on the query."
    }
    ```

- **GET /health**: Check the health status of the application.
  - **Response**:
    ```json
    {
      "status": "healthy"
    }
    ```

## Requirements

- Python 3.10 or higher
- Flask
- Flask-CORS
- Pydantic
- Aiohttp
- BeautifulSoup4
- Googlesearch-python
- Langchain
- Torch
- FastAPI
- Uvicorn

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Abhay Chourasiya  
[Abhaychourasiya945@gmail.com](mailto:Abhaychourasiya945@gmail.com)  
[GitHub Profile](https://github.com/Abhay06102003)
```
