from fastapi import FastAPI, HTTPException, UploadFile, File
from session_manager import SessionManager
from security_proxy import RealDocumentManager, SecurityProxy, Document
from models import LoginRequest, LoginResponse

app = FastAPI(title="TechBuild SDMS API")

session_manager = SessionManager()
real_manager = RealDocumentManager()
security_proxy = SecurityProxy(real_manager)

MOCK_USERS = {
    "eng_01": {"password": "securepassword123", "expected_otp": "123456"}
}

@app.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    user = MOCK_USERS.get(credentials.user_id)
    
    if not user or user["password"] != credentials.password or user["expected_otp"] != credentials.otp:
        raise HTTPException(status_code=401, detail="Invalid credentials or OTP")
    
    if session_manager.enforce_single_session(credentials.user_id):
        raise HTTPException(status_code=403, detail="Active session already exists for this user.")
    
    session_manager.establish_session(credentials.user_id)
    
    return LoginResponse(
        message="Login successful. Access granted to Dashboard.",
        session_status="Active"
    )

@app.post("/upload")
async def upload_document(user_id: str, file: UploadFile = File(...)):
    if not session_manager.enforce_single_session(user_id):
        raise HTTPException(status_code=401, detail="Unauthorized. No active session found.")
    
    payload = await file.read()
    doc = Document(doc_id=file.filename, payload=payload)
    
    try:
        security_proxy.upload_document(doc)
        return {"message": f"File '{file.filename}' uploaded successfully and passed security checks."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@app.post("/logout")
async def logout(user_id: str):
    session_manager.terminate_session(user_id)
    return {"message": "Session terminated successfully."}