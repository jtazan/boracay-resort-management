# Boracay Resort Management

A working prototype for the Boracay Island Resort Group operations dashboard, built with FastAPI and a static UI. It includes login, reservation management, property monitoring, and consistent error handling for invalid input and failed requests.

## Features

- Central dashboard for all five resort properties
- Property health and occupancy summaries
- Network segmentation overview for guest, staff, CCTV, POS, and management VLANs
- Reservation creation and tracking
- Alerts and incident visibility
- Demo authentication using a secure JWT flow
- Validation and structured API errors

## Demo login

- Username: `resortadmin`
- Password: `ChangeMe123!`

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

```text
http://localhost:8000
```

## Environment variables

```bash
export JWT_SECRET_KEY="change-this-secret"
export JWT_ALGORITHM="HS256"
export JWT_TTL_MINUTES="480"
export DEMO_USERNAME="resortadmin"
export DEMO_PASSWORD="ChangeMe123!"
```

## Notes

This is a working demo application intended to model the Boracay resort operations platform described in the project brief. It does not connect to live Cisco Meraki or PMS systems, but the dashboard structure and API design are aligned with the architecture requirements.
