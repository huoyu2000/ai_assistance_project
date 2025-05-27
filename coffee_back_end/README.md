# 咖啡店管理系统 - 后端

这是一个咖啡店管理系统的后端API，基于Django REST Framework开发。

## 功能模块

- **商品管理**：录入/维护咖啡豆等商品；配置饮品配方；设定售价、成本价、会员价与时段优惠价
- **采购管理**：管理咖啡豆、牛奶、糖浆、一次性杯盖/杯套等易耗品供应商资料与合同价格
- **销售管理**：POS点单，堂食/外带切换，一键打印小票或出饮条
- **库存管理**：实时扣减原料；分批次、保质期管理
- **财务管理**：每日营业额结算；毛利/纯利核算
- **报表分析**：畅销饮品榜；时段客流热力图；会员复购率
- **权限管理**：角色划分，店长、值班经理、吧台咖啡师、收银员、仓管；权限分配

## 部署说明

### Koyeb部署

1. 在Koyeb上创建新的应用
2. 选择GitHub仓库作为源代码
3. 选择后端目录作为构建目录
4. 使用以下环境变量:
   - `PORT`: 8000
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: .koyeb.app
   - `DATABASE_URL`: 您的数据库URL

### 本地开发

1. 安装依赖: `pip install -r requirements.txt`
2. 运行迁移: `python manage.py migrate`
3. 创建超级用户: `python manage.py createsuperuser`
4. 启动服务器: `python manage.py runserver`

## API文档

API文档可在`/api/docs/`路径访问。

## 健康检查

健康检查接口位于`/api/auth/health/`路径。

## 技术栈

- Django
- Django REST Framework
- SQLite（开发环境）/ PostgreSQL（生产环境）
- JWT认证 