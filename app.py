
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight


# ==================================================
# 1. CONFIGURATION
# ==================================================

load_dotenv()

API_KEY = os.getenv("HINDSIGHT_API_KEY")
BASE_URL = os.getenv("HINDSIGHT_BASE_URL")

BANK_ID = "industrial-maintenance-agent"

st.set_page_config(
    page_title="Industrial Maintenance Agent",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Industrial Maintenance Memory Agent")

st.caption(
    "An AI maintenance assistant powered by persistent Hindsight memory."
)

if not API_KEY or not BASE_URL:
    st.error("Hindsight credentials missing. Please check your .env file.")
    st.stop()


# ==================================================
# 2. SAFE HINDSIGHT CONNECTION HANDLER
# ==================================================

def run_hindsight(operation):
    """
    Run each Hindsight operation using a fresh client
    inside its own worker thread and event loop.
    """

    def worker():

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = None

        try:
            client = Hindsight(
                base_url=BASE_URL,
                api_key=API_KEY
            )

            return operation(client)

        finally:
            try:
                if client is not None:
                    client.close()

            finally:
                asyncio.set_event_loop(None)

                if not loop.is_closed():
                    loop.close()

    with ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(worker).result()


# ==================================================
# 3. SESSION STATE
# ==================================================

if "last_response" not in st.session_state:
    st.session_state.last_response = None

if "last_machine" not in st.session_state:
    st.session_state.last_machine = None


# ==================================================
# 4. SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio(
    "Select a feature",
    [
        "Report Machine Fault",
        "Record Resolution",
        "Machine History"
    ]
)

st.sidebar.divider()

st.sidebar.success("Hindsight memory connected")

st.sidebar.caption(
    "Industrial Maintenance Memory Agent"
)


# ==================================================
# 5. REPORT MACHINE FAULT
# ==================================================

if page == "Report Machine Fault":

    st.header("🔧 Report a Machine Fault")

    st.write(
        "Enter the machine details and current problem. "
        "The agent will analyze previous maintenance history "
        "before saving the new incident."
    )

    with st.form("incident_form"):

        machine_id = st.text_input(
            "Machine ID",
            placeholder="Example: M1"
        )

        machine_type = st.text_input(
            "Machine Type",
            placeholder="Example: Industrial Motor"
        )

        location = st.text_input(
            "Machine Location",
            placeholder="Example: Production Unit 1"
        )

        error_code = st.text_input(
            "Error Code",
            placeholder="Example: E101"
        )

        symptoms = st.text_area(
            "Describe the current problem",
            placeholder="Example: Machine is overheating..."
        )

        submitted = st.form_submit_button(
            "Analyze Machine Fault",
            use_container_width=True
        )

    if submitted:

        if not all([
            machine_id.strip(),
            error_code.strip(),
            symptoms.strip()
        ]):

            st.warning(
                "Please enter Machine ID, Error Code and Symptoms."
            )

        else:

            query = f"""
            A technician has reported a CURRENT machine incident.

            Machine ID: {machine_id}
            Machine Type: {machine_type or 'Not specified'}
            Location: {location or 'Not specified'}
            Current Error Code: {error_code}
            Current Symptoms: {symptoms}

            Analyze the EXISTING maintenance history for this machine.

            Instructions:

            1. Identify relevant previous incidents for this machine.
            2. Identify previously confirmed causes.
            3. Identify previously successful maintenance solutions.
            4. Suggest practical troubleshooting checks.
            5. Clearly separate historical facts from new suggestions.
            6. Never present an unverified cause as confirmed.
            7. If no relevant history exists for this machine,
               explicitly say that no relevant historical records were found.
            8. Do not invent machine records or maintenance events.
            9. Consider whether previous repairs may be relevant
               to the current symptoms.

            Provide a clear troubleshooting report for the technician.
            """

            try:

                with st.spinner(
                    "Searching maintenance memory and analyzing the fault..."
                ):

                    # STEP 1: Analyze existing memory
                    result = run_hindsight(
                        lambda client: client.reflect(
                            bank_id=BANK_ID,
                            query=query,
                            budget="low"
                        )
                    )

                    # STEP 2: Prepare the new incident record
                    timestamp = datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                    incident_record = f"""
                    NEW MACHINE INCIDENT REPORT

                    Date and Time: {timestamp}

                    Machine ID: {machine_id}
                    Machine Type: {machine_type or 'Not specified'}
                    Location: {location or 'Not specified'}

                    Error Code: {error_code}
                    Symptoms: {symptoms}

                    Status: Reported.
                    Resolution: Not yet confirmed.
                    """

                    # STEP 3: Store the new incident
                    run_hindsight(
                        lambda client: client.retain(
                            bank_id=BANK_ID,
                            content=incident_record
                        )
                    )

                    # STEP 4: Save response in Streamlit session
                    st.session_state.last_response = result.text
                    st.session_state.last_machine = machine_id

                st.success(
                    "Incident analyzed and saved to Hindsight memory!"
                )

            except Exception as error:

                st.error(
                    f"Application error: {error}"
                )

                st.exception(error)

    # Display troubleshooting report
    if st.session_state.last_response:

        st.divider()

        st.subheader("🤖 AI Troubleshooting Report")

        st.markdown(
            st.session_state.last_response
        )

        st.info(
            "The incident has been recorded. "
            "AI recommendations are suggestions, "
            "not confirmed repairs."
        )


# ==================================================
# 6. RECORD TECHNICIAN RESOLUTION
# ==================================================

elif page == "Record Resolution":

    st.header("✅ Record Maintenance Resolution")

    st.write(
        "Record the actual repair performed by the technician. "
        "This information becomes part of the machine's history."
    )

    with st.form("resolution_form"):

        machine_id = st.text_input(
            "Machine ID",
            placeholder="Example: M1",
            value=st.session_state.last_machine or ""
        )

        error_code = st.text_input(
            "Related Error Code",
            placeholder="Example: E101"
        )

        resolution = st.text_area(
            "What action fixed the problem?",
            placeholder="Example: Replaced the damaged cooling fan."
        )

        outcome = st.selectbox(
            "Final Machine Status",
            [
                "Restored to normal operation",
                "Partially restored",
                "Problem still exists"
            ]
        )

        saved = st.form_submit_button(
            "Save Confirmed Resolution",
            use_container_width=True
        )

    if saved:

        if not machine_id.strip() or not resolution.strip():

            st.warning(
                "Machine ID and resolution are required."
            )

        else:

            try:

                resolution_record = f"""
                TECHNICIAN MAINTENANCE RESOLUTION

                Date and Time:
                {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                Machine ID: {machine_id}
                Related Error Code: {error_code or 'Not specified'}

                Technician-Reported Action:
                {resolution}

                Final Machine Status: {outcome}

                This record was submitted by the technician.
                """

                # Store resolution using a fresh connection
                run_hindsight(
                    lambda client: client.retain(
                        bank_id=BANK_ID,
                        content=resolution_record
                    )
                )

                st.success(
                    "Technician resolution successfully saved to Hindsight!"
                )

            except Exception as error:

                st.error(
                    f"Error saving resolution: {error}"
                )

                st.exception(error)


# ==================================================
# 7. MACHINE MAINTENANCE HISTORY
# ==================================================

elif page == "Machine History":

    st.header("📚 Machine Maintenance History")

    st.write(
        "Retrieve previous incidents and maintenance records "
        "for a particular machine."
    )

    machine_id = st.text_input(
        "Enter Machine ID",
        placeholder="Example: M1"
    )

    if st.button(
        "Retrieve Maintenance History",
        use_container_width=True
    ):

        if not machine_id.strip():

            st.warning(
                "Please enter a Machine ID."
            )

        else:

            try:

                with st.spinner(
                    "Retrieving machine history..."
                ):

                    result = run_hindsight(
                        lambda client: client.recall(
                            bank_id=BANK_ID,
                            query=(
                                f"Show previous incidents, error codes, "
                                f"maintenance actions and confirmed resolutions "
                                f"for Machine {machine_id}. "
                                f"Prioritize records specifically involving "
                                f"Machine ID {machine_id}."
                            )
                        )
                    )

                st.divider()

                st.subheader(
                    f"Maintenance History: {machine_id}"
                )

                if result.results:

                    st.success(
                        f"Retrieved {len(result.results)} memory results."
                    )

                    for index, memory in enumerate(
                        result.results,
                        start=1
                    ):

                        with st.expander(
                            f"Maintenance Record {index}"
                        ):

                            st.write(memory.text)

                else:

                    st.info(
                        f"No relevant maintenance history found for {machine_id}."
                    )

            except Exception as error:

                st.error(
                    f"History retrieval error: {error}"
                )

                st.exception(error)


# ==================================================
# 8. FOOTER
# ==================================================

st.divider()

st.caption(
    "Industrial Maintenance Memory Agent | "
    "Powered by Python, Streamlit and Hindsight"
)
