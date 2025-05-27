/*
 Navicat Premium Data Transfer

 Source Server         : mySQL
 Source Server Type    : MySQL
 Source Server Version : 80036
 Source Host           : localhost:3306
 Source Schema         : coffee_shop

 Target Server Type    : MySQL
 Target Server Version : 80036
 File Encoding         : 65001

 Date: 27/05/2025 17:07:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for daily_finance_detail
-- ----------------------------
DROP TABLE IF EXISTS `daily_finance_detail`;
CREATE TABLE `daily_finance_detail`  (
  `detail_id` bigint NOT NULL AUTO_INCREMENT,
  `biz_date` date NULL DEFAULT NULL,
  `product_id` bigint NULL DEFAULT NULL,
  `sales_qty` decimal(10, 2) NULL DEFAULT NULL,
  `revenue` decimal(12, 2) NULL DEFAULT NULL,
  `cost` decimal(12, 2) NULL DEFAULT NULL,
  `profit` decimal(12, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`detail_id`) USING BTREE,
  INDEX `fk_fin_detail_product`(`product_id` ASC) USING BTREE,
  CONSTRAINT `fk_fin_detail_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of daily_finance_detail
-- ----------------------------
INSERT INTO `daily_finance_detail` VALUES (1, '2025-05-24', 2, 40.00, 180.00, 80.00, 100.00);
INSERT INTO `daily_finance_detail` VALUES (2, '2025-05-24', 4, 50.00, 150.00, 60.00, 90.00);
INSERT INTO `daily_finance_detail` VALUES (3, '2025-05-24', 8, 30.00, 84.00, 24.00, 60.00);
INSERT INTO `daily_finance_detail` VALUES (4, '2025-05-23', 7, 25.00, 130.00, 55.00, 75.00);

-- ----------------------------
-- Table structure for daily_finance_summary
-- ----------------------------
DROP TABLE IF EXISTS `daily_finance_summary`;
CREATE TABLE `daily_finance_summary`  (
  `biz_date` date NOT NULL,
  `total_sales_amount` decimal(12, 2) NULL DEFAULT NULL,
  `total_transactions` int NULL DEFAULT NULL,
  `avg_transaction` decimal(10, 2) NULL DEFAULT NULL,
  `gross_profit` decimal(12, 2) NULL DEFAULT NULL,
  `net_profit` decimal(12, 2) NULL DEFAULT NULL,
  `generated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`biz_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of daily_finance_summary
-- ----------------------------
INSERT INTO `daily_finance_summary` VALUES ('2025-05-23', 2040.00, 170, 12.00, 1020.00, 820.00, '2025-05-24 22:05:32');
INSERT INTO `daily_finance_summary` VALUES ('2025-05-24', 850.00, 70, 12.14, 430.00, 350.00, '2025-05-24 22:05:32');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-05-24 18:30:42.774734');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2025-05-24 18:30:42.784800');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2025-05-24 18:30:42.786811');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2025-05-24 18:30:42.788816');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2025-05-24 18:30:42.791066');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2025-05-24 18:30:42.793108');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2025-05-24 18:30:42.795462');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2025-05-24 18:30:42.796631');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2025-05-24 18:30:42.798671');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2025-05-24 18:30:42.800689');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2025-05-24 18:30:42.802726');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2025-05-24 18:30:42.804755');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2025-05-24 18:30:42.808106');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2025-05-24 18:30:42.809128');
INSERT INTO `django_migrations` VALUES (15, 'user_auth', '0001_initial', '2025-05-24 18:30:42.812272');
INSERT INTO `django_migrations` VALUES (16, 'admin', '0001_initial', '2025-05-24 18:30:42.814335');
INSERT INTO `django_migrations` VALUES (17, 'admin', '0002_logentry_remove_auto_add', '2025-05-24 18:30:42.815346');
INSERT INTO `django_migrations` VALUES (18, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-24 18:30:42.817348');
INSERT INTO `django_migrations` VALUES (19, 'finance', '0001_initial', '2025-05-24 18:30:42.819445');
INSERT INTO `django_migrations` VALUES (20, 'product', '0001_initial', '2025-05-24 18:30:42.822673');
INSERT INTO `django_migrations` VALUES (21, 'procurement', '0001_initial', '2025-05-24 18:30:42.825249');
INSERT INTO `django_migrations` VALUES (22, 'inventory', '0001_initial', '2025-05-24 18:30:42.827348');
INSERT INTO `django_migrations` VALUES (23, 'reports', '0001_initial', '2025-05-24 18:30:42.829361');
INSERT INTO `django_migrations` VALUES (24, 'sales', '0001_initial', '2025-05-24 18:30:42.831366');
INSERT INTO `django_migrations` VALUES (25, 'sessions', '0001_initial', '2025-05-24 18:30:42.836560');
INSERT INTO `django_migrations` VALUES (26, 'user_auth', '0002_permission_role_remove_staff_address_and_more', '2025-05-24 18:30:42.840552');
INSERT INTO `django_migrations` VALUES (27, 'finance', '0002_auto_20250526_2014', '2025-05-26 12:16:09.348247');
INSERT INTO `django_migrations` VALUES (28, 'product', '0002_inventorylevel_alter_category_options_and_more', '2025-05-26 12:48:02.972795');
INSERT INTO `django_migrations` VALUES (29, 'sales', '0002_alter_customer_options_alter_drinkticket_options_and_more', '2025-05-26 16:13:57.394605');
INSERT INTO `django_migrations` VALUES (30, 'sales', '0003_alter_order_options_alter_orderitem_options', '2025-05-26 16:13:57.421818');

-- ----------------------------
-- Table structure for finance_costrecord
-- ----------------------------
DROP TABLE IF EXISTS `finance_costrecord`;
CREATE TABLE `finance_costrecord`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `cost_type` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(10, 2) NOT NULL,
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `reference_number` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_by` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of finance_costrecord
-- ----------------------------

-- ----------------------------
-- Table structure for finance_dailyrevenue
-- ----------------------------
DROP TABLE IF EXISTS `finance_dailyrevenue`;
CREATE TABLE `finance_dailyrevenue`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_sales` decimal(12, 2) NOT NULL,
  `total_orders` int NOT NULL,
  `average_order_value` decimal(10, 2) NOT NULL,
  `cash_amount` decimal(12, 2) NOT NULL,
  `wechat_amount` decimal(12, 2) NOT NULL,
  `alipay_amount` decimal(12, 2) NOT NULL,
  `card_amount` decimal(12, 2) NOT NULL,
  `member_card_amount` decimal(12, 2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `date`(`date` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of finance_dailyrevenue
-- ----------------------------
INSERT INTO `finance_dailyrevenue` VALUES (1, '2025-05-20', 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:24:52.321553', '2025-05-26 12:24:52.321553');
INSERT INTO `finance_dailyrevenue` VALUES (2, '2025-05-21', 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:24:52.324649', '2025-05-26 12:24:52.324649');
INSERT INTO `finance_dailyrevenue` VALUES (3, '2025-05-22', 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:24:52.327264', '2025-05-26 12:24:52.327264');
INSERT INTO `finance_dailyrevenue` VALUES (4, '2025-05-23', 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:24:52.328657', '2025-05-26 12:24:52.328657');
INSERT INTO `finance_dailyrevenue` VALUES (5, '2025-05-24', 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:24:52.330698', '2025-05-26 12:24:52.330698');
INSERT INTO `finance_dailyrevenue` VALUES (6, '2025-05-25', 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:24:52.332265', '2025-05-26 12:24:52.332265');
INSERT INTO `finance_dailyrevenue` VALUES (7, '2025-05-26', 0.00, 0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:24:52.333445', '2025-05-26 12:24:52.333445');
INSERT INTO `finance_dailyrevenue` VALUES (8, '2025-05-27', 1000.00, 80, 12.50, 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-27 02:01:02.314372', '2025-05-27 02:01:02.314372');

-- ----------------------------
-- Table structure for finance_profitreport
-- ----------------------------
DROP TABLE IF EXISTS `finance_profitreport`;
CREATE TABLE `finance_profitreport`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `report_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `period_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `total_revenue` decimal(12, 2) NOT NULL,
  `total_cost` decimal(12, 2) NOT NULL,
  `gross_profit` decimal(12, 2) NOT NULL,
  `net_profit` decimal(12, 2) NOT NULL,
  `profit_margin` decimal(5, 2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `report_id`(`report_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of finance_profitreport
-- ----------------------------
INSERT INTO `finance_profitreport` VALUES (1, 'daily-2025-05-26-2025-05-26', 'daily', '2025-05-26', '2025-05-26', 0.00, 0.00, 0.00, 0.00, 0.00, '2025-05-26 12:30:34.848004');

-- ----------------------------
-- Table structure for inventory_batches
-- ----------------------------
DROP TABLE IF EXISTS `inventory_batches`;
CREATE TABLE `inventory_batches`  (
  `batch_id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NULL DEFAULT NULL,
  `batch_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `qty` decimal(10, 2) NULL DEFAULT NULL,
  `expiry_date` date NULL DEFAULT NULL,
  `status` enum('ACTIVE','EXPIRED','USED_UP') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'ACTIVE',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`batch_id`) USING BTREE,
  INDEX `fk_batch_product`(`product_id` ASC) USING BTREE,
  CONSTRAINT `fk_batch_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of inventory_batches
-- ----------------------------
INSERT INTO `inventory_batches` VALUES (1, 1, 'B20240501', 50.00, '2025-05-01', 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `inventory_batches` VALUES (2, 1, 'B20240601', 100.00, '2025-06-01', 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `inventory_batches` VALUES (3, 9, 'MILK20240524', 80.00, '2025-05-30', 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `inventory_batches` VALUES (4, 8, 'COOKIE20240520', 120.00, '2025-07-20', 'ACTIVE', '2025-05-24 22:05:32');

-- ----------------------------
-- Table structure for inventory_levels
-- ----------------------------
DROP TABLE IF EXISTS `inventory_levels`;
CREATE TABLE `inventory_levels`  (
  `product_id` bigint NOT NULL,
  `stock_qty` decimal(10, 2) NULL DEFAULT NULL,
  `unit` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `reorder_point` decimal(10, 2) NULL DEFAULT NULL,
  `last_updated` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`product_id`) USING BTREE,
  CONSTRAINT `fk_inventory_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of inventory_levels
-- ----------------------------
INSERT INTO `inventory_levels` VALUES (1, 150.00, 'g', 20.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (2, 38.00, '杯', 10.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (3, 35.00, '杯', 10.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (4, 48.00, '杯', 15.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (5, 60.00, '杯', 20.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (6, 30.00, '杯', 10.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (7, 24.00, '杯', 10.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (8, 119.00, '个', 30.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (9, 80.00, '升', 20.00, '2025-05-24 22:05:32');
INSERT INTO `inventory_levels` VALUES (10, 500.00, '包', 100.00, '2025-05-24 22:05:32');

-- ----------------------------
-- Table structure for lookup_codes
-- ----------------------------
DROP TABLE IF EXISTS `lookup_codes`;
CREATE TABLE `lookup_codes`  (
  `code_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`code_type`, `code`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of lookup_codes
-- ----------------------------
INSERT INTO `lookup_codes` VALUES ('CHANNEL', 'DINE_IN', '堂食');
INSERT INTO `lookup_codes` VALUES ('CHANNEL', 'TAKE_AWAY', '外卖');
INSERT INTO `lookup_codes` VALUES ('OP_TYPE', 'CREATE', '创建');
INSERT INTO `lookup_codes` VALUES ('OP_TYPE', 'DELETE', '删除');
INSERT INTO `lookup_codes` VALUES ('OP_TYPE', 'LOGIN', '登录');
INSERT INTO `lookup_codes` VALUES ('OP_TYPE', 'UPDATE', '修改');
INSERT INTO `lookup_codes` VALUES ('UNIT', 'g', '克');
INSERT INTO `lookup_codes` VALUES ('UNIT', '个', '个');
INSERT INTO `lookup_codes` VALUES ('UNIT', '升', '升');
INSERT INTO `lookup_codes` VALUES ('UNIT', '杯', '杯');

-- ----------------------------
-- Table structure for operation_logs
-- ----------------------------
DROP TABLE IF EXISTS `operation_logs`;
CREATE TABLE `operation_logs`  (
  `log_id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NULL DEFAULT NULL,
  `user_id` bigint NULL DEFAULT NULL,
  `ip_addr` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `op_type` enum('LOGIN','CREATE','UPDATE','DELETE') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `entity` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `details` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `fk_log_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_log_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operation_logs
-- ----------------------------
INSERT INTO `operation_logs` VALUES (1, '2025-05-24 16:05:32', 2, '192.168.1.101', 'LOGIN', '用户', '张店长登录系统');
INSERT INTO `operation_logs` VALUES (2, '2025-05-24 17:05:32', 2, '192.168.1.101', 'CREATE', '商品', '创建商品：抹茶拿铁');
INSERT INTO `operation_logs` VALUES (3, '2025-05-24 18:05:32', 3, '192.168.1.102', 'UPDATE', '商品', '修改商品价格：焦糖玛奇朵 5.20 -> 5.50');
INSERT INTO `operation_logs` VALUES (4, '2025-05-24 19:05:32', 6, '192.168.1.103', 'CREATE', '订单', '创建销售单：S20240524-002');
INSERT INTO `operation_logs` VALUES (5, '2025-05-24 20:05:32', 1, '192.168.1.100', 'UPDATE', '权限', '赋予张店长 FIN_VIEW 权限');

-- ----------------------------
-- Table structure for order_items
-- ----------------------------
DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items`  (
  `item_id` bigint NOT NULL AUTO_INCREMENT,
  `order_id` bigint NULL DEFAULT NULL,
  `product_id` bigint NULL DEFAULT NULL,
  `product_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `qty` decimal(10, 2) NULL DEFAULT NULL,
  `unit_price` decimal(10, 2) NULL DEFAULT NULL,
  `line_total` decimal(10, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`item_id`) USING BTREE,
  INDEX `fk_order_item_order`(`order_id` ASC) USING BTREE,
  INDEX `fk_order_item_product`(`product_id` ASC) USING BTREE,
  CONSTRAINT `fk_order_item_order` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_order_item_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of order_items
-- ----------------------------
INSERT INTO `order_items` VALUES (1, 1, 4, '浓缩咖啡', 2.00, 3.00, 6.00);
INSERT INTO `order_items` VALUES (2, 1, 8, '巧克力曲奇', 1.00, 2.80, 2.80);
INSERT INTO `order_items` VALUES (3, 2, 2, '拿铁', 2.00, 4.50, 9.00);
INSERT INTO `order_items` VALUES (4, 2, 7, '焦糖玛奇朵', 1.00, 5.20, 5.20);

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `order_id` bigint NOT NULL AUTO_INCREMENT,
  `order_no` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `table_no` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `channel` enum('DINE_IN','TAKE_AWAY') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `subtotal` decimal(10, 2) NULL DEFAULT NULL,
  `tax` decimal(10, 2) NULL DEFAULT NULL,
  `total` decimal(10, 2) NULL DEFAULT NULL,
  `status` enum('OPEN','PAID','REFUNDED') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'OPEN',
  `created_by` bigint NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `paid_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`order_id`) USING BTREE,
  UNIQUE INDEX `order_no`(`order_no` ASC) USING BTREE,
  INDEX `fk_orders_user`(`created_by` ASC) USING BTREE,
  CONSTRAINT `fk_orders_user` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
INSERT INTO `orders` VALUES (1, 'S20240524-001', 'A1', 'DINE_IN', 8.00, 0.64, 8.64, 'PAID', 4, '2025-05-24 20:05:32', '2025-05-24 20:05:32');
INSERT INTO `orders` VALUES (2, 'S20240524-002', NULL, 'TAKE_AWAY', 13.50, 1.08, 14.58, 'PAID', 6, '2025-05-24 21:05:32', '2025-05-24 21:05:32');

-- ----------------------------
-- Table structure for permissions
-- ----------------------------
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions`  (
  `perm_id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`perm_id`) USING BTREE,
  UNIQUE INDEX `code`(`code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of permissions
-- ----------------------------
INSERT INTO `permissions` VALUES (1, 'PROD_VIEW', '查看商品');
INSERT INTO `permissions` VALUES (2, 'PROD_EDIT', '编辑商品');
INSERT INTO `permissions` VALUES (3, 'ORDER_VIEW', '查看订单');
INSERT INTO `permissions` VALUES (4, 'ORDER_CREATE', '创建订单');
INSERT INTO `permissions` VALUES (5, 'ORDER_REFUND', '订单退款');
INSERT INTO `permissions` VALUES (6, 'STOCK_VIEW', '查看库存');
INSERT INTO `permissions` VALUES (7, 'STOCK_ADJUST', '调整库存');
INSERT INTO `permissions` VALUES (8, 'FIN_VIEW', '查看财务');
INSERT INTO `permissions` VALUES (9, 'USER_MANAGE', '用户管理');
INSERT INTO `permissions` VALUES (10, 'ROLE_MANAGE', '角色管理');

-- ----------------------------
-- Table structure for product_categories
-- ----------------------------
DROP TABLE IF EXISTS `product_categories`;
CREATE TABLE `product_categories`  (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort_order` int NULL DEFAULT 0,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`category_id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of product_categories
-- ----------------------------
INSERT INTO `product_categories` VALUES (1, '咖啡豆', 1, '2025-05-24 22:05:32');
INSERT INTO `product_categories` VALUES (2, '饮料', 2, '2025-05-24 22:05:32');
INSERT INTO `product_categories` VALUES (3, '甜点', 3, '2025-05-24 22:05:32');
INSERT INTO `product_categories` VALUES (4, '乳制品', 4, '2025-05-24 22:05:32');
INSERT INTO `product_categories` VALUES (5, '茶类', 5, '2025-05-24 22:05:32');

-- ----------------------------
-- Table structure for products
-- ----------------------------
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products`  (
  `product_id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_id` int NULL DEFAULT NULL,
  `sku` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `unit` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '个',
  `price` decimal(10, 2) NOT NULL,
  `inventory_qty` decimal(10, 2) NULL DEFAULT 0.00,
  `reorder_point` decimal(10, 2) NULL DEFAULT 0.00,
  `status` enum('ACTIVE','INACTIVE','OUT_OF_STOCK') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'ACTIVE',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE,
  INDEX `fk_product_category`(`category_id` ASC) USING BTREE,
  CONSTRAINT `fk_product_category` FOREIGN KEY (`category_id`) REFERENCES `product_categories` (`category_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of products
-- ----------------------------
INSERT INTO `products` VALUES (1, '埃塞俄比亚 耶加雪菲', 1, 'YRG123', 'g', 25.00, 150.00, 20.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-25 13:50:41');
INSERT INTO `products` VALUES (2, '拿铁', 2, 'LATTE001', '杯', 4.50, 40.00, 10.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (3, '卡布奇诺', 2, 'CAPPU001', '杯', 4.00, 35.00, 10.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (4, '浓缩咖啡', 2, 'ESP001', '杯', 3.00, 50.00, 15.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (5, '冰咖啡', 2, 'ICED001', '杯', 8.00, 61.00, 20.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-25 14:03:52');
INSERT INTO `products` VALUES (6, '抹茶拿铁', 2, 'MATCHA01', '杯', 4.80, 30.00, 10.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (7, '焦糖玛奇朵', 2, 'CM001', '杯', 5.20, 25.00, 10.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (8, '巧克力曲奇', 3, 'COOKIE01', '个', 2.80, 120.00, 30.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (9, '牛奶', 4, 'MILK01', '升', 2.20, 80.00, 20.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (10, '红茶茶包', 5, 'TEA01', '包', 0.80, 500.00, 100.00, 'ACTIVE', '2025-05-24 22:05:32', '2025-05-24 22:05:32');
INSERT INTO `products` VALUES (11, '开心果泡芙', 3, 'KXGPF001', '个', 2.00, 20.00, 0.00, 'ACTIVE', '2025-05-26 02:07:45', '2025-05-26 02:39:56');

-- ----------------------------
-- Table structure for role_permission
-- ----------------------------
DROP TABLE IF EXISTS `role_permission`;
CREATE TABLE `role_permission`  (
  `role_id` int NOT NULL,
  `perm_id` int NOT NULL,
  PRIMARY KEY (`role_id`, `perm_id`) USING BTREE,
  INDEX `fk_rp_perm`(`perm_id` ASC) USING BTREE,
  CONSTRAINT `fk_rp_perm` FOREIGN KEY (`perm_id`) REFERENCES `permissions` (`perm_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_rp_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role_permission
-- ----------------------------
INSERT INTO `role_permission` VALUES (1, 1);
INSERT INTO `role_permission` VALUES (2, 1);
INSERT INTO `role_permission` VALUES (3, 1);
INSERT INTO `role_permission` VALUES (4, 1);
INSERT INTO `role_permission` VALUES (1, 2);
INSERT INTO `role_permission` VALUES (1, 3);
INSERT INTO `role_permission` VALUES (2, 3);
INSERT INTO `role_permission` VALUES (3, 3);
INSERT INTO `role_permission` VALUES (4, 3);
INSERT INTO `role_permission` VALUES (5, 3);
INSERT INTO `role_permission` VALUES (1, 4);
INSERT INTO `role_permission` VALUES (2, 4);
INSERT INTO `role_permission` VALUES (3, 4);
INSERT INTO `role_permission` VALUES (4, 4);
INSERT INTO `role_permission` VALUES (5, 4);
INSERT INTO `role_permission` VALUES (1, 5);
INSERT INTO `role_permission` VALUES (1, 6);
INSERT INTO `role_permission` VALUES (2, 6);
INSERT INTO `role_permission` VALUES (3, 6);
INSERT INTO `role_permission` VALUES (6, 6);
INSERT INTO `role_permission` VALUES (1, 7);
INSERT INTO `role_permission` VALUES (6, 7);
INSERT INTO `role_permission` VALUES (1, 8);
INSERT INTO `role_permission` VALUES (2, 8);
INSERT INTO `role_permission` VALUES (1, 9);
INSERT INTO `role_permission` VALUES (1, 10);

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles`  (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `description` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`role_id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES (1, '系统管理员', '拥有系统所有权限', '2025-05-24 22:05:32');
INSERT INTO `roles` VALUES (2, '店长', '管理门店日常运营', '2025-05-24 22:05:32');
INSERT INTO `roles` VALUES (3, '值班经理', '代理店长职责', '2025-05-24 22:05:32');
INSERT INTO `roles` VALUES (4, '咖啡师', '制作咖啡饮品', '2025-05-24 22:05:32');
INSERT INTO `roles` VALUES (5, '收银员', '前台收银', '2025-05-24 22:05:32');
INSERT INTO `roles` VALUES (6, '仓管员', '管理库存', '2025-05-24 22:05:32');

-- ----------------------------
-- Table structure for suppliers
-- ----------------------------
DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE `suppliers`  (
  `supplier_id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `contact_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `phone` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `status` enum('ACTIVE','INACTIVE') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'ACTIVE',
  `address` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`supplier_id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of suppliers
-- ----------------------------
INSERT INTO `suppliers` VALUES (1, '豆好兄弟', '咖啡豆', '李明', '13800000001', 'beans@example.com', 'ACTIVE', '湖南长沙', '2025-05-24 22:05:32');
INSERT INTO `suppliers` VALUES (2, '乳制品之喜', '乳制品', '张威', '13800000002', 'dairy@example.com', 'INACTIVE', '湖南株洲', '2025-05-24 22:05:32');
INSERT INTO `suppliers` VALUES (3, '甜蜜感受', '糖浆和配料', '王勇', '13800000003', 'sugar@example.com', 'INACTIVE', '湖南衡阳', '2025-05-24 22:05:32');
INSERT INTO `suppliers` VALUES (4, '杯子王国', '一次性用品', '刘兰', '13800000004', 'cup@example.com', 'ACTIVE', '广东广州', '2025-05-24 22:05:32');
INSERT INTO `suppliers` VALUES (5, '茶时光', '茶类', '周杰', '13800000005', 'tea@example.com', 'ACTIVE', '福建福州', '2025-05-24 22:05:32');
INSERT INTO `suppliers` VALUES (6, '烘焙屋', '甜点', '陈烘焙', '13800000006', 'bakery@example.com', 'ACTIVE', '湖南岳阳', '2025-05-24 22:05:32');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `full_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `role_id` int NULL DEFAULT NULL,
  `status` enum('ACTIVE','DISABLED') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'ACTIVE',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  INDEX `fk_user_role`(`role_id` ASC) USING BTREE,
  CONSTRAINT `fk_user_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '管理员', 'admin@example.com', 'pbkdf2_sha256$1000000$8ogQD9SzrvKyYUOHpBiTYZ$+tOHyfkzm1HMs5Jmr1H3lNf6VOdTx/713tcMS6qUoGY=', 1, 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `users` VALUES (2, 'manager', '张店长', 'manager@example.com', '*', 2, 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `users` VALUES (3, 'shift01', '李经理', 'shift01@example.com', '*', 3, 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `users` VALUES (4, 'barista01', '王咖啡', 'barista01@example.com', '*', 4, 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `users` VALUES (5, 'barista02', '赵咖啡', 'barista02@example.com', '*', 4, 'DISABLED', '2025-05-24 22:05:32');
INSERT INTO `users` VALUES (6, 'cashier01', '孙收银', 'cashier01@example.com', '*', 5, 'ACTIVE', '2025-05-24 22:05:32');
INSERT INTO `users` VALUES (7, 'stock01', '钱仓管', 'stock01@example.com', '*', 6, 'ACTIVE', '2025-05-24 22:05:32');

SET FOREIGN_KEY_CHECKS = 1;
