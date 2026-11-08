cat > README.md << 'EOF'
# Industrial Maintenance Memory Agent

An AI-powered industrial maintenance assistant that uses persistent memory to help technicians troubleshoot recurring machine failures.

## Problem Statement

Industrial maintenance teams frequently encounter recurring machine faults. Previous maintenance records and successful repair knowledge may not always be available when another technician faces the same problem.

## Our Solution

The Industrial Maintenance Memory Agent stores machine incidents and technician-reported resolutions using Hindsight. When a new fault is reported, the system analyzes relevant maintenance memories and provides context-aware troubleshooting recommendations.

## Key Features

- Machine fault reporting
- Persistent incident memory
- Retrieval of previous maintenance records
- AI-powered troubleshooting using Hindsight reflect
- Technician resolution recording
- Machine maintenance history

## Technology Stack

- Python
- Streamlit
- Hindsight Memory
- hindsight-client
- python-dotenv

## Architecture

1. Technician reports a machine fault through Streamlit.
2. Python sends the query to Hindsight.
3. Hindsight analyzes relevant stored memories.
4. The application displays historical facts and troubleshooting suggestions.
5. The new incident is stored in persistent memory.
6. Technicians can record confirmed resolutions for future use.

## Hindsight Operations

- retain(): Stores machine incidents and technician-reported resolutions.
- recall(): Retrieves relevant maintenance history.
- reflect(): Generates responses using stored memory.

## Installation

Clone the repository:

    git clone YOUR_REPOSITORY_URL

Enter the project folder:

    cd industrial-maintenance-agent

Create a virtual environment:

    python3 -m venv venv

Activate it:

    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Create a .env file containing:

    HINDSIGHT_API_KEY=your_actual_api_key
    HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io

Run the application:

    streamlit run app.py

## Demonstration Scenarios

### Machine M1

- Error: E101
- Problem: Overheating
- Previously confirmed cause: Blocked cooling filter
- Previously recorded resolution: Filter cleaning

The agent uses this history to recommend relevant checks when the fault recurs.

### Machine M2

- Error: E205
- Problem: Unusual vibration and excessive noise
- Previous history: No relevant records

The agent recognizes the lack of machine-specific history and provides general troubleshooting recommendations.

## Important Note

This is a software prototype using technician-entered and simulated industrial incidents. It is not currently connected to physical machinery, PLCs, or live industrial sensors. AI-generated recommendations must be verified by qualified technicians.

## Future Improvements

- Live sensor integration
- Machine registration and asset management
- Advanced maintenance analytics
- Improved incident timeline and reporting
- Additional industrial equipment support
EOF
