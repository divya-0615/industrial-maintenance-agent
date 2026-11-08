
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BASE_URL = os.getenv("HINDSIGHT_BASE_URL")

if not API_KEY:
    raise ValueError("API key not found. Check your .env file.")

client = Hindsight(
    base_url=BASE_URL,
    api_key=API_KEY
)

BANK_ID = "industrial-maintenance-agent"

try:
    # Create memory bank
    bank = client.create_bank(
        bank_id=BANK_ID,
        name="Industrial Maintenance Agent"
    )

    print("Memory bank ready:", bank.bank_id)

    # Store an incident
    client.retain(
        bank_id=BANK_ID,
        content=(
            "Machine M1 experienced overheating with error E101. "
            "The technician confirmed a blocked cooling filter "
            "and cleaned it. The machine returned to normal."
        )
    )

    print("Incident stored successfully!")

    # Retrieve the incident
    result = client.recall(
        bank_id=BANK_ID,
        query="What happened when Machine M1 overheated?"
    )

    print("\nRetrieved machine history:")

    for memory in result.results:
        print("-", memory.text)

except Exception as error:
    print("Error:", error)

finally:
    client.close()
