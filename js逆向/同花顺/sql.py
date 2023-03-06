from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, VARCHAR, FLOAT, INT, create_engine
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库的基类
Base = declarative_base()


class XPC(Base):
    __tablename__ = 'ths'
    order_number = Column(INT())
    stock_code = Column(INT(), primary_key=True, nullable=False)
    stock_name = Column(VARCHAR(255), nullable=False)
    current_price = Column(FLOAT(5, 2))
    up_down_range = Column(FLOAT(5, 2))
    up_down = Column(FLOAT(5, 2))
    increase_speed = Column(FLOAT(5, 2))
    change_hands = Column(FLOAT(5, 2))
    maximum_ratio = Column(FLOAT(5, 2))
    amplitude = Column(FLOAT(5, 2))
    turnover = Column(VARCHAR(255))
    tradable_stock = Column(VARCHAR(255))
    market_value = Column(VARCHAR(255))
    p_e_ratio = Column(VARCHAR(255))

    def __init__(self, order_number, stock_code, stock_name, current_price, up_down_range, up_down, increase_speed,
                 change_hands, maximum_ratio, amplitude, turnover, tradable_stock, market_value, p_e_ratio):
        self.order_number = order_number
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.current_price = current_price
        self.up_down_range = up_down_range
        self.up_down = up_down
        self.increase_speed = increase_speed
        self.change_hands = change_hands
        self.maximum_ratio = maximum_ratio
        self.amplitude = amplitude
        self.turnover = turnover
        self.tradable_stock = tradable_stock
        self.market_value = market_value
        self.p_e_ratio = p_e_ratio


# 在 数据库 xpc 里创建表
def create_table():
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/xpc?charset=utf8mb4")
    Base.metadata.create_all(engine)


# 连接数据库
def link():
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/xpc?charset=utf8mb4")
    session = sessionmaker(bind=engine)
    s = session()
    return s


# 关闭连接
def close_link(session):
    session.close()


# 增加数据
def insert_data(session, order_number, stock_code, stock_name, current_price, up_down_range, up_down, increase_speed,
           change_hands, maximum_ratio, amplitude, turnover, tradable_stock, market_value, p_e_ratio):
    try:
        data = XPC(order_number, stock_code, stock_name, current_price, up_down_range, up_down, increase_speed,
                   change_hands, maximum_ratio, amplitude, turnover, tradable_stock, market_value, p_e_ratio)
        session.add(data)
        session.commit()
    except Exception:
        session.rollback()

