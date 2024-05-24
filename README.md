# Animal Info Finder

The Animal Info Finder is a web application designed to provide detailed information about various animals. It fetches data from an external API to display information such as the scientific name, physical description, habitat, diet, social structure, conservation status, and behavior of the queried animal. Additionally, it retrieves images related to the searched animal to provide a visual representation.

## How to Use

### Prerequisites

- Node.js installed on your machine
- Basic understanding of React.js and FastAPI

### Getting Started

1. Clone this repository to your local machine:

   git clone <repository-url>

2. Navigate to the project directory:

   cd animal-info-finder

3. Install dependencies for both the frontend and backend:

   # Install frontend dependencies
   cd frontend
   npm install

   # Install backend dependencies
   cd ../backend
   pip install -r requirements.txt

### Running the Application

1. Start the backend server:

   # Navigate to the backend directory
   cd backend

   # Start the FastAPI server
   uvicorn main:app --reload

2. Start the frontend development server:

   # Navigate to the frontend directory
   cd frontend

   # Start the React development server
   npm start

3. Open your web browser and navigate to http://localhost:3000 to access the Animal Info Finder web application.

### Using the Application

1. Enter the name of the animal you want to learn about in the search bar.
2. Press the "Search" button or hit Enter to initiate the search.
3. Wait for the information to load. Once loaded, you will see details about the animal, including its scientific name, physical description, habitat, diet, social structure, conservation status, and behavior.
4. If available, an image related to the animal will also be displayed.

## Contributing

Contributions to the Animal Info Finder project are welcome! If you find any bugs, issues, or have suggestions for improvements, please feel free to open an issue or submit a pull request.
