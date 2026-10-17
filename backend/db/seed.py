
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
                "subject": "Criar model de Usuarios",
                "channel": "API",
                "status": "open",
                "priority": "high",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Criar model de Tickets",
                "channel": "API",
                "status": "open",
                "priority": "high",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Criar crud de Usuario",
                "channel": "API",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Criar crud de Ticket",
                "channel": "API",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Criar crud de Cliente",
                "channel": "API",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Resolver bugs das seeds",
                "channel": "API",
                "status": "open",
                "priority": "low",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Criar model de Clientes",
                "channel": "API",
                "status": "open",
                "priority": "high",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Criar base do projeto NextJS",
                "channel": "web",
                "status": "closed",
                "priority": "high",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de Login",
                "channel": "web",
                "status": "closed",
                "priority": "high",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de listagem dos Tickets, com campos para filtragem dos Tickets",
                "channel": "web",
                "status": "open",
                "priority": "high",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina do Ticket em especifico, com botões para atualizar prioridade ou status",
                "channel": "web",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de listagem de usuarios, com botão para criar novo usuario e o card de cada usuario para navegar para a pagina do usuario. Somente o Admin pode ter acesso a essa pagina, verificar a role do usuario logado",
                "channel": "web",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de visualização de usuario... Ela apresenta as informações base do usuario e pode ser acessada pelo admin ou pelo usuario comum (porem no caso do usuario comum, so pode acessar a pagina do seu proprio usuario, enviar o proprio id para pagina no momento de renderização nesse caso). Esta pagina deve permitir alterar as infos do usuario (Fazer a tratativa de erros vinda do back-end, por exemplo, somente usuarios admins podem alterar a role e o is_active, se um usuario comum tentar alterar, mesmo sendo o usuario dono daquele acesso vai dar erro)",
                "channel": "web",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de metrics",
                "channel": "web",
                "status": "open",
                "priority": "low",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de Clientes (listagem de todos os clientes)",
                "channel": "web",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de Cliente especifico, nesta pagina deve ser possivel alterar os dados do cliente (somente usuario admin podem alterar dados do cliente, neste caso, fazer as tratativas de erro vindas do back-end para casos em que da errado o acesso ou sucerro de tais ações)",
                "channel": "web",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar aplicativo web para contole dos tickets enviados para cada usuario",
                "channel": "phone",
                "status": "open",
                "priority": "high",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar pagina de listagem de todos os tickets, a principio apesar de ser a geral de tickets o default para essa tela é vir apenas com os open enviados para o usuario logado... Neste caso a rota é a mesma do get all tickets porem com os parametros ?assigned_user_id=id_user&status=open",
                "channel": "phone",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": nelson.id,
            },
            {
                "subject": "Criar analise pandas de dados do dataframe/dados vindos do Kaggle. Se sobrar tempo criar para os tickets dessa aplicação, queremos um grafico de quantidade em porcentagem dos tickets concluidos por cada usuario, quantidade de tickets atribuidos para cada usuario e tickets por prioridade (existem mais tickets low, medium ou high)",
                "channel": "data",
                "status": "open",
                "priority": "high",
                "assigned_user_id": cleiton.id,
            },
            {
                "subject": "Workflow n8n",
                "channel": "workflow",
                "status": "open",
                "priority": "medium",
                "assigned_user_id": cleiton.id,
            }
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