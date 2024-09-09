# IELTS Listening Task Generator from YouTube

This Streamlit app generates IELTS listening tasks from YouTube videos by downloading and transcribing the audio.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Enter the YouTube video URL in the input field to generate the listening task.

## Docker

1. Build the Docker image:
    ```sh
    docker build -t ielts-listening-task-generator .
    ```

2. Run the Docker container:
    ```sh
    docker run -p 8501:8501 ielts-listening-task-generator
    ```

## License

This project is licensed under the MIT License.