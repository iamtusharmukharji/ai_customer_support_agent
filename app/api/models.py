from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Text, ForeignKey, BigInteger, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.api.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_code = Column(String(20), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    status = Column(Enum("active", "inactive", name="customer_status_enum"), default="active")
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    orders = relationship("Order", back_populates="customer")
    refunds = relationship("Refund", back_populates="customer")
    support_tickets = relationship("SupportTicket", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    status = Column(Enum("active", "out_of_stock", "discontinued", name="product_status_enum"), default="in_stock")
    created_at = Column(DateTime, server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_number = Column(String(30), unique=True, nullable=False, index=True)
    customer_id = Column(BigInteger, ForeignKey("customers.id"), nullable=False)
    
    order_status = Column(Enum("pending", "processing", "shipped", "delivered", "cancelled", name="order_status_enum"))
    payment_status = Column(Enum("pending", "paid", "failed", "refunded", name="payment_status_enum"))
    payment_method = Column(Enum("credit_card", "debit_card", "net_banking", "upi", "cash_on_delivery", name="payment_method_enum"))
    
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    shipping_fee = Column(DECIMAL(10, 2), default=0.00)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    
    tracking_number = Column(String(100), nullable=True)
    estimated_delivery = Column(Date, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    refunds = relationship("Refund", back_populates="order")
    support_tickets = relationship("SupportTicket", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    refund_number = Column(String(30), unique=True, nullable=False, index=True)
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=False)
    customer_id = Column(BigInteger, ForeignKey("customers.id"), nullable=False)
    refund_amount = Column(DECIMAL(10, 2), nullable=False)
    reason = Column(String(255), nullable=True)
    status = Column(Enum("pending", "approved", "processed", "rejected", name="refund_status_enum"))
    requested_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    order = relationship("Order", back_populates="refunds")
    customer = relationship("Customer", back_populates="refunds")


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticket_number = Column(String(30), unique=True, nullable=False, index=True)
    customer_id = Column(BigInteger, ForeignKey("customers.id"), nullable=False)
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=True)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(Enum("low", "medium", "high", "urgent", name="ticket_priority_enum"))
    status = Column(Enum("open", "in_progress", "resolved", "closed", name="ticket_status_enum"))
    assigned_team = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)

    # Relationships
    customer = relationship("Customer", back_populates="support_tickets")
    order = relationship("Order", back_populates="support_tickets")


class FAQArticle(Base):
    __tablename__ = "faq_articles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    status = Column(Enum("draft", "published", "archived", name="faq_status_enum"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())