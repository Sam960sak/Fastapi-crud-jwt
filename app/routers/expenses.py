from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Expense, User
from app.schemas import ExpenseCreate, ExpenseListResponse, ExpenseResponse, ExpenseUpdate

router = APIRouter(prefix="/expenses", tags=["expenses"])


def get_owned_expense(expense_id: int, user: User, db: Session) -> Expense:
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.owner_id == user.id)
        .first()
    )
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )
    return expense


@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = Expense(**payload.model_dump(), owner_id=current_user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=ExpenseListResponse)
def list_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Expense).filter(Expense.owner_id == current_user.id)
    total = query.count()
    items = (
        query.order_by(Expense.created_at.desc()).offset(skip).limit(limit).all()
    )
    return ExpenseListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_owned_expense(expense_id, current_user, db)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = get_owned_expense(expense_id, current_user, db)

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="No fields provided to update",
        )

    for field, value in updates.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    expense = get_owned_expense(expense_id, current_user, db)
    db.delete(expense)
    db.commit()
