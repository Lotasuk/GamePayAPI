from typing import Optional, List 
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DATE, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    UserID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    PasswordHash: Mapped[str] = mapped_column(String)
    Email: Mapped[str] = mapped_column(String)
    
    

    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')
    gameAccount: Mapped['GameAccount'] = relationship('GameAccount', back_populates='user', uselist=False)
    purchaseHistory: Mapped[list['PurchaseHistory']] = relationship('PurchaseHistory', back_populates='user')
    notifications: Mapped[list['Notification']] = relationship('Notification', back_populates='user')
    chatsAsUser1: Mapped[list['Chat']] = relationship('Chat', foreign_keys='Chat.User1ID', back_populates='user1')
    chatsAsUser2: Mapped[list['Chat']] = relationship('Chat', foreign_keys='Chat.User2ID', back_populates='user2')
    sentMessages: Mapped[list['Message']] = relationship('Message', foreign_keys='Message.SenderID', back_populates='sender')


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

class Chat(Base):
    __tablename__ = 'Chats'

    ChatID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    User1ID: Mapped[int] = mapped_column(Integer, ForeignKey('Users.UserID'), nullable=False)
    User2ID: Mapped[int] = mapped_column(Integer, ForeignKey('Users.UserID'), nullable=False)
    CreatedAt: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Связи
    user1: Mapped['User'] = relationship('User', foreign_keys=[User1ID], back_populates='chatsAsUser1')
    user2: Mapped['User'] = relationship('User', foreign_keys=[User2ID], back_populates='chatsAsUser2')
    messages: Mapped[list['Message']] = relationship('Message', back_populates='chat')

class Message(Base):
    __tablename__ = 'Messages'

    MessageID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ChatID: Mapped[int] = mapped_column(Integer, ForeignKey('Chats.ChatID'), nullable=False)
    SenderID: Mapped[int] = mapped_column(Integer, ForeignKey('Users.UserID'), nullable=False)
    Content: Mapped[str] = mapped_column(Text, nullable=False)
    SentAt: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    IsRead: Mapped[bool] = mapped_column(Boolean, default=False)

    # Связи
    chat: Mapped['Chat'] = relationship('Chat', back_populates='messages')
    sender: Mapped['User'] = relationship('User', foreign_keys=[SenderID], back_populates='sentMessages')