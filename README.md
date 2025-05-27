# 咖啡店进销存管理系统后端

这是一个基于Django REST框架开发的咖啡店进销存管理系统后端。该系统连接到已有的MySQL数据库，提供了完整的API接口，支持商品管理、采购管理、库存管理、销售管理、用户认证等功能。

## 功能模块

系统包含以下功能模块：

1. **商品管理**：
   - 商品分类管理
   - 商品信息管理
   - 价格管理

2. **采购管理**：
   - 供应商管理
   - 采购订单管理
   - 供应商商品管理

3. **库存管理**：
   - 库存水平监控
   - 库存批次管理
   - 库存交易记录
   - 库存盘点

4. **销售管理**：
   - 客户管理
   - 订单管理
   - 小票管理
   - 饮品票管理

5. **用户权限管理**：
   - 基于JWT的用户认证
   - 角色权限管理
   - 操作日志记录

## 技术栈

- Django 5.2
- Django REST Framework
- MySQL 
- JWT认证

## 安装与配置

1. 安装依赖：
```
pip install -r requirements.txt
```

2. 配置数据库：
在 settings.py 中已配置连接到名为"coffee_shop"的MySQL数据库，确保数据库存在且配置正确。

3. 运行开发服务器：
```
python manage.py runserver
```

## API端点

系统提供了以下主要API端点：

### 认证
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户注销
- `POST /api/auth/token/refresh/` - 刷新访问令牌

### 商品管理
- `GET/POST /api/product/categories/` - 商品分类管理
- `GET/POST /api/product/products/` - 商品管理

### 采购管理
- `GET/POST /api/procurement/suppliers/` - 供应商管理
- `GET/POST /api/procurement/purchase-orders/` - 采购订单管理

### 库存管理
- `GET /api/inventory/inventories/` - 库存水平管理
- `GET /api/inventory/batches/` - 批次管理
- `GET /api/inventory/transactions/` - 库存交易记录

### 销售管理
- `GET/POST /api/sales/customers/` - 客户管理
- `GET/POST /api/sales/orders/` - 订单管理
- `GET /api/sales/receipts/` - 小票管理

## 注意事项

- 系统使用Django的managed=False选项映射到现有数据库表
- 部分功能可能需要根据具体业务需求进行调整
- 对于没有在原始数据库中的表，使用Django自动创建 