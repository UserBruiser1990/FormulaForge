from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from ollama_service import (
    OllamaServiceError,
    explain_formula,
    fix_formula,
    generate_power_query,
    generate_vba,
    generate_formula,
)


app = FastAPI(title="FormulaForge AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1)


class GenerateResponse(BaseModel):
    formula: str


class ExplainRequest(BaseModel):
    formula: str = Field(min_length=1)


class ExplainResponse(BaseModel):
    explanation: str


class FixRequest(BaseModel):
    formula: str = Field(min_length=1)


class FixResponse(BaseModel):
    formula: str


class VbaRequest(BaseModel):
    prompt: str = Field(min_length=1)


class VbaResponse(BaseModel):
    code: str


class PowerQueryRequest(BaseModel):
    prompt: str = Field(min_length=1)


class PowerQueryResponse(BaseModel):
    code: str


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        formula = generate_formula(request.prompt)
    except OllamaServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return GenerateResponse(formula=formula)


@app.post("/explain", response_model=ExplainResponse)
def explain(request: ExplainRequest) -> ExplainResponse:
    try:
        explanation = explain_formula(request.formula)
    except OllamaServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return ExplainResponse(explanation=explanation)


@app.post("/fix", response_model=FixResponse)
def fix(request: FixRequest) -> FixResponse:
    try:
        corrected_formula = fix_formula(request.formula)
    except OllamaServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return FixResponse(formula=corrected_formula)


@app.post("/vba", response_model=VbaResponse)
def vba(request: VbaRequest) -> VbaResponse:
    try:
        code = generate_vba(request.prompt)
    except OllamaServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return VbaResponse(code=code)


@app.post("/power-query", response_model=PowerQueryResponse)
def power_query(request: PowerQueryRequest) -> PowerQueryResponse:
    try:
        code = generate_power_query(request.prompt)
    except OllamaServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return PowerQueryResponse(code=code)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)