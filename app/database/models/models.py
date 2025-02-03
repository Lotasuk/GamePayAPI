from sqlalchemy import Column, Integer, String, Text, DECIMAL, DATE, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    UserID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Username: Mapped[str] = mapped_column(String)
    PasswordHash: Mapped[str] = mapped_column(String)
    Email: Mapped[str] = mapped_column(String)
    RegistrationDate: Mapped[DATE] = mapped_column(DATE)

    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')
    gameAccount: Mapped['GameAccount'] = relationship('GameAccount', back_populates='user', uselist=False)
    purchaseHistory: Mapped[list['PurchaseHistory']] = relationship('PurchaseHistory', back_populates='user')
    notifications: Mapped[list['Notification']] = relationship('Notification', back_populates='user')

class Category(Base):
    __tablename__ = 'Categories'

    CategoryID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CategoryName: Mapped[str] = mapped_column(String)

    items: Mapped[list['Item']] = relationship('Item', back_populates='category')

class Item(Base):
    __tablename__ = 'Items'

    ItemID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String)
    Description: Mapped[str] = mapped_column(Text)
    Price: Mapped[DECIMAL] = mapped_column(DECIMAL)
    CategoryID: Mapped[int] = mapped_column(Integer, ForeignKey('Categories.CategoryID'))
    Status: Mapped[bool] = mapped_column(Boolean)

    category: Mapped['Category'] = relationship('Category', back_populates='items')
    orderItems: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='item')
    purchaseHistory: Mapped[list['PurchaseHistory']] = relationship('PurchaseHistory', back_populates='item')

class Order(Base):
    __tablename__ = 'Orders'

    OrderID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserID: Mapped[int] = mapped_column(Integer, ForeignKey('Users.UserID'))
    CreationDate: Mapped[DATE] = mapped_column(DATE)
    Status: Mapped[str] = mapped_column(String)

    user: Mapped['User'] = relationship('User', back_populates='orders')
    orderItems: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order')
    payment: Mapped['Payment'] = relationship('Payment', back_populates='order', uselist=False)

class OrderItem(Base):
    __tablename__ = 'OrderItems'

    OrderItemID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    OrderID: Mapped[int] = mapped_column(Integer, ForeignKey('Orders.OrderID'))
    ItemID: Mapped[int] = mapped_column(Integer, ForeignKey('Items.ItemID'))
    Quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped['Order'] = relationship('Order', back_populates='orderItems')
    item: Mapped['Item'] = relationship('Item', back_populates='orderItems')

class Payment(Base):
    __tablename__ = 'Payments'

    PaymentID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    OrderID: Mapped[int] = mapped_column(Integer, ForeignKey('Orders.OrderID'))
    PaymentMethod: Mapped[str] = mapped_column(String)
    Amount: Mapped[DECIMAL] = mapped_column(DECIMAL)
    Status: Mapped[str] = mapped_column(String)

    order: Mapped['Order'] = relationship('Order', back_populates='payment')

class GameAccount(Base):
    __tablename__ = 'GameAccounts'

    GameAccountID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserID: Mapped[int] = mapped_column(Integer, ForeignKey('Users.UserID'))
    AccountIdentifier: Mapped[str] = mapped_column(String)
    Balance: Mapped[DECIMAL] = mapped_column(DECIMAL)

    user: Mapped['User'] = relationship('User', back_populates='gameAccount')

class PurchaseHistory(Base):
    __tablename__ = 'PurchaseHistory'

    HistoryID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserID: Mapped[int] = mapped_column(Integer, ForeignKey('Users.UserID'))
    ItemID: Mapped[int] = mapped_column(Integer, ForeignKey('Items.ItemID'))
    PurchaseDate: Mapped[DATE] = mapped_column(DATE)

    user: Mapped['User'] = relationship('User', back_populates='purchaseHistory')
    item: Mapped['Item'] = relationship('Item', back_populates='purchaseHistory')

class Notification(Base):
    __tablename__ = 'Notifications'

    NotificationID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserID: Mapped[int] = mapped_column(Integer, ForeignKey('Users.UserID'))
    Message: Mapped[str] = mapped_column(Text)
    SendDate: Mapped[DATE] = mapped_column(DATE)

    user: Mapped['User'] = relationship('User', back_populates='notifications')

