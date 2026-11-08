
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load environment variables
load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BASE_URL = os.getenv("HINDSIGHT_BASE_URL")

if not API_KEY:
    raise ValueError("HINDSIGHT_API_KEY missing. Check .env")

# Connect to Hindsight
client = Hindsight(
    base_url=BASE_URL,
    api_key=API_KEY
)

BANK_ID = "industrial-maintenance-agent"

try:
    print("\nINDUSTRIAL MAINTENANCE MEMORY AGENT")
    print("-----------------------------------")

    # Ask Hindsight to reason using stored memories
    result = client.reflect(
        bank_id=BANK_ID,
        query=(
            "Machine M1 is overheating again with error E101. "
            "Based on its previous maintenance history, what "
            "should the technician check first? Explain the "
            "previous incident and clearly distinguish known "
            "facts from suggested checks."
        ),
        budget="low"
    )

    print("\nAI TROUBLESHOOTING RESPONSE")
    print("---------------------------")
    print(result)

except Exception as error:
    print("\nERROR:", error)

finally:
    client.close()
