# 咖啡店进销存管理系统

这是一个基于Django和REST框架开发的咖啡店进销存管理系统的后端部分。系统提供了完整的咖啡店经营所需的管理功能，包括商品管理、采购管理、销售管理、库存管理、财务管理、报表分析和权限管理。

## 功能模块

- **商品管理**：录入/维护咖啡豆等商品；配置饮品配方；设定售价、成本价、会员价与时段优惠价
- **采购管理**：管理咖啡豆、牛奶、糖浆、一次性杯盖/杯套等易耗品供应商资料与合同价格
- **销售管理**：POS点单，堂食/外带切换，一键打印小票或出饮条
- **库存管理**：实时扣减原料；分批次、保质期管理
- **财务管理**：每日营业额结算；毛利/纯利核算
- **报表分析**：畅销饮品榜；时段客流热力图；会员复购率
- **权限管理**：角色划分，店长、值班经理、吧台咖啡师、收银员、仓管；权限分配

## 安装和运行

### 环境要求

- Python 3.8+
- Django 5.2+
- Django REST Framework 3.16+

### 安装步骤

1. 克隆项目代码到本地
2. 创建并激活虚拟环境（可选但推荐）
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```
3. 安装依赖
   ```
   pip install -r requirements.txt
   ```
4. 执行数据库迁移
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. 创建超级用户
   ```
   python manage.py createsuperuser
   ```
6. 启动开发服务器
   ```
   python manage.py runserver
   ```

### API文档

启动服务器后，可以通过以下地址访问API浏览器界面：
- http://127.0.0.1:8000/api/

管理员界面：
- http://127.0.0.1:8000/admin/

## 技术栈

- Django
- Django REST Framework
- SQLite（开发环境）/ PostgreSQL（生产环境）
- JWT认证 