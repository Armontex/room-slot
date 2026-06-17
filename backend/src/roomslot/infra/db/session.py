from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


class LimitedSession:
    def __init__(self, session: AsyncSession) -> None:
        self.get = session.get
        self.execute = session.execute
        self.flush = session.flush
        self.refresh = session.refresh
        self.add = session.add
        self.delete = session.delete
        self.scalar = session.scalar
        self.scalars = session.scalars
