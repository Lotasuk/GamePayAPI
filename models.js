const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize('GamePay', 'postgres', 'password', {
  host: 'localhost',
  dialect: 'postgres'
});

const User = sequelize.define('User', {
  UserID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  Username: DataTypes.STRING,
  PasswordHash: DataTypes.STRING,
  Email: DataTypes.STRING,
  RegistrationDate: DataTypes.DATE,
  createdAt: {
    type: DataTypes.DATE,
    allowNull: false
  },
  updatedAt: {
    type: DataTypes.DATE,
    allowNull: false
  }
}, {
  tableName: 'Users', // Указываем название таблицы
  timestamps: true // Включаем автоматическое управление полями createdAt и updatedAt
});

const Category = sequelize.define('Category', {
  CategoryID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  CategoryName: DataTypes.STRING
});

const Item = sequelize.define('Item', {
  ItemID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  Name: DataTypes.STRING,
  Description: DataTypes.TEXT,
  Price: DataTypes.DECIMAL,
  CategoryID: DataTypes.INTEGER,
  Status: DataTypes.BOOLEAN
});

const Order = sequelize.define('Order', {
  OrderID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  UserID: DataTypes.INTEGER,
  CreationDate: DataTypes.DATE,
  Status: DataTypes.STRING
});

const OrderItem = sequelize.define('OrderItem', {
  OrderItemID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  OrderID: DataTypes.INTEGER,
  ItemID: DataTypes.INTEGER,
  Quantity: DataTypes.INTEGER
});

const Payment = sequelize.define('Payment', {
  PaymentID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  OrderID: DataTypes.INTEGER,
  PaymentMethod: DataTypes.STRING,
  Amount: DataTypes.DECIMAL,
  Status: DataTypes.STRING
});

const GameAccount = sequelize.define('GameAccount', {
  GameAccountID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  UserID: DataTypes.INTEGER,
  AccountIdentifier: DataTypes.STRING,
  Balance: DataTypes.DECIMAL
});

const PurchaseHistory = sequelize.define('PurchaseHistory', {
  HistoryID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  UserID: DataTypes.INTEGER,
  ItemID: DataTypes.INTEGER,
  PurchaseDate: DataTypes.DATE
});

const Notification = sequelize.define('Notification', {
  NotificationID: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  UserID: DataTypes.INTEGER,
  Message: DataTypes.TEXT,
  SendDate: DataTypes.DATE
});

// Определение ассоциаций
User.hasMany(Order, { foreignKey: 'UserID', as: 'orders' });
Order.belongsTo(User, { foreignKey: 'UserID', as: 'user' });

Category.hasMany(Item, { foreignKey: 'CategoryID', as: 'items' });
Item.belongsTo(Category, { foreignKey: 'CategoryID', as: 'category' });

Order.hasMany(OrderItem, { foreignKey: 'OrderID', as: 'orderItems' });
OrderItem.belongsTo(Order, { foreignKey: 'OrderID', as: 'order' });

Item.hasMany(OrderItem, { foreignKey: 'ItemID', as: 'orderItems' });
OrderItem.belongsTo(Item, { foreignKey: 'ItemID', as: 'item' });

Order.hasOne(Payment, { foreignKey: 'OrderID', as: 'payment' });
Payment.belongsTo(Order, { foreignKey: 'OrderID', as: 'order' });

User.hasOne(GameAccount, { foreignKey: 'UserID', as: 'gameAccount' });
GameAccount.belongsTo(User, { foreignKey: 'UserID', as: 'user' });

User.hasMany(PurchaseHistory, { foreignKey: 'UserID', as: 'purchaseHistory' });
PurchaseHistory.belongsTo(User, { foreignKey: 'UserID', as: 'user' });

Item.hasMany(PurchaseHistory, { foreignKey: 'ItemID', as: 'purchaseHistory' });
PurchaseHistory.belongsTo(Item, { foreignKey: 'ItemID', as: 'item' });

User.hasMany(Notification, { foreignKey: 'UserID', as: 'notifications' });
Notification.belongsTo(User, { foreignKey: 'UserID', as: 'user' });

module.exports = {
  User,
  Category,
  Item,
  Order,
  OrderItem,
  Payment,
  GameAccount,
  PurchaseHistory,
  Notification
};
