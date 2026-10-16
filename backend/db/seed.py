
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.customer import Customer
from models.ticket import Ticket
from models.user import User
from infra.providers.encrypt_provider import hash_password


def seed_initial_data() -> None:
    db: Session = SessionLocal()

    try:
        # 1. Criar os usuários iniciais, caso não existam.
        initial_users = [
            {
                "name": "admin",
                "email": "admin@admin.com.br",
                "password": "1234",
                "role": "admin",
                "is_active": True,
            },
            {
                "name": "cleiton",
                "email": "cleiton@gmail.com.br",
                "password": "123456",
                "role": "user",
                "is_active": True,
            },
            {
                "name": "nelson",
                "email": "nelson@gmail.com.br",
                "password": "123456",
                "role": "user",
                "is_active": True,
            },
            {
                "name": "marcos",
                "email": "marcos@gmail.com.br",
                "password": "123456",
                # O role será aplicado pelo default do modelo.
                "is_active": False,
            },
        ]

        for user_data in initial_users:
            existing_user = db.scalar(
                select(User).where(User.email == user_data["email"])
            )

            if existing_user is None:
                new_user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    password_hash=hash_password(user_data["password"]),
                    is_active=user_data["is_active"],
                    **(
                        {"role": user_data["role"]}
                        if "role" in user_data
                        else {}
                    ),
                )

                db.add(new_user)

        db.flush()

        # 2. Criar o customer inicial, caso não exista.
        customer = db.scalar(
            select(Customer).where(
                Customer.email == "stalse@stalse.com.br"
            )
        )

        if customer is None:
            customer = Customer(
                name="stalse",
                email="stalse@stalse.com.br",
                phone=None,
            )
            db.add(customer)
            db.flush()

        # 3. Consultar os usuários responsáveis pelos tickets.
        cleiton = db.scalar(
            select(User).where(User.email == "cleiton@gmail.com.br")
        )
        nelson = db.scalar(
            select(User).where(User.email == "nelson@gmail.com.br")
        )

        # 4. Criar os tickets iniciais.
        initial_tickets = [
            {
                "subject": "Problema no acesso",
                "channel": "web",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Erro no sistema",
                "channel": "email",
                "status": "open",
                "priority": "high",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Acesso restabelecido",
                "channel": "phone",
                "status": "closed",
                "priority": "medium",
                "assigned_user_id": cleiton.id,
            },
        ]

        for ticket_data in initial_tickets:
            existing_ticket = db.scalar(
                select(Ticket).where(
                    Ticket.customer_id == customer.id,
                    Ticket.subject == ticket_data["subject"],
                )
            )

            if existing_ticket is None:
                ticket = Ticket(
                    customer_id=customer.id,
                    **ticket_data,
                )
                db.add(ticket)

        # Persiste todas as inclusões em uma transação.
        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()