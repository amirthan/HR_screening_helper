# HR - Resume Analysis Helper 🧐

## Project Description
The HR - Resume Analysis Helper is a Streamlit application designed to streamline the resume screening process for HR professionals. By automating the matching of resumes to job descriptions using artificial intelligence, this application accelerates the shortlisting process, freeing up HR personnel for more strategic tasks. The application leverages Pinecone as a vector database to store the embeddings and perform similarity search to match resumes with job descriptions. Additionally, OpenAI models are utilized for summarization to provide a quick overview of each resume.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Pip (Python's package installer)

### Installation

1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/amirthan/HR_screening_helper.git
   cd HR_screening_helper
   ```
2. Install the required packages.
   ```bash
   pip install -r requirements.txt
   ```

## Pinecone Setup

Before running the application, you'll need to set up a Pinecone vector database and create an index named "resumes". 

1. Visit [Pinecone](https://www.pinecone.io/) and create an account if you don't have one already.
2. Follow Pinecone's guide on creating a new vector database.
3. When creating the index, ensure to set the dimensions to `384` and the metric to `cosine`.
4. Name the index "resumes".
5. Retrieve your Pinecone API key and keep it handy, as you'll need to input it in the application's sidebar.

## OpenAI Setup

Before running the application, ensure you have an OpenAI API key.

1. Visit [OpenAI](https://www.openai.com/) and create an account if you don't have one already.
2. Follow OpenAI's guide on obtaining an API key.
3. Keep your OpenAI API key handy, as you'll need to input it in the application's sidebar.

## Running the Application

1. Navigate to the project directory.
   ```bash
   cd path/to/HR_screening_helper
   ```
2. Run the Streamlit application.
   ```bash
   streamlit run app.py
   ```

## Usage

1. The application opens in a new tab in your web browser.
2. In the left sidebar:
   - Input the job description in the provided text area.
   - Select the number of resumes to return using the slider.
   - Upload the resume files (in PDF format) using the file uploader.
   - Input your Pinecone API key in the provided field.
   - Input your OpenAI API key in the provided field. 
3. Click the "Analyze Resumes" button to begin the analysis.
4. The application processes the resumes, matches them to the job description, and displays the most relevant resumes along with a summary.
5. (Optional) To halt the analysis, click the "Stop Analysis" button.
6. (Optional) To search for a different job description without re-uploading the resumes:
   - Input the new job description.
   - Click the "Search for new Job Description" button.

## Troubleshooting

- If you encounter any issues while running the application, check the console for error messages.
- Ensure you have provided valid Pinecone and OpenAI API keys in the input fields.

## Contributing

Feel free to fork this project and make your own changes, or submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.