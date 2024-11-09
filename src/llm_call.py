from enum import Enum

from openai import OpenAI
from pydantic import BaseModel


class ExpenseCategory(Enum):
    ALCOHOLESTO = "alcoholesto"
    CAPRIXOS = "caprixos"
    COMIDOUT = "comidout"
    CUCUCULTURA = "cucucultura"
    CUIDADOS = "cuidados"
    HACENDADO = "hacendado"
    MANUTENCION_AL_EMPLEADO_ACCENT = "manutención al empleado"
    REGALOS = "regalos"
    SOBREVIVIR_ES_CARO = "sobrevivir es caro"
    TRANSPORTE = "transporte"


class Expense(BaseModel):
    description: str
    amount: str
    category: ExpenseCategory


def extract_expense(transcript: str) -> Expense:
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract the expense information from the following transcript."},
            {"role": "user", "content": transcript},
        ],
        response_format=Expense,
    )
    expense = completion.choices[0].message.parsed
    # Format datapoints as I please
    expense.description = expense.description.lower()
    expense.amount = expense.amount.replace(",", ".")
    
    return expense
