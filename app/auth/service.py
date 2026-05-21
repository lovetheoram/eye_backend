from sqlalchemy.orm import Session

from app.auth.models import User

from app.auth.schemas import (
    UserRegister
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


def register_user(
    db: Session,
    user_data: UserRegister
):

    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise Exception(
            "Email already exists"
        )

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        name=user_data.name,

        email=user_data.email,

        password_hash=hashed_password,

        work_type=user_data.work_type
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user

def login_user(
    db: Session,
    email: str,
    password: str,
    expo_push_token: str | None = None
):

    print("INSIDE LOGIN USER")

    print("EMAIL:", email)

    print("PASSWORD:", password)

    print(
        "EXPO TOKEN:",
        expo_push_token
    )

    user = get_user_by_email(
        db,
        email
    )

    print("USER:", user)

    if not user:

        print("USER NOT FOUND")

        return None

    valid_password = verify_password(
        password,
        user.password_hash
    )

    print(
        "PASSWORD VALID:",
        valid_password
    )

    if not valid_password:

        print("INVALID PASSWORD")

        return None

    if expo_push_token:

        print(
            "UPDATING EXPO TOKEN"
        )

        user.expo_push_token = (
            expo_push_token
        )

        db.commit()

    token = create_access_token({
        "sub": str(user.id)
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }