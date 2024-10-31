/*
 Navicat Premium Data Transfer

 Source Server         : local-mysql
 Source Server Type    : MySQL
 Source Server Version : 80039
 Source Host           : localhost:3306
 Source Schema         : ppd

 Target Server Type    : MySQL
 Target Server Version : 80039
 File Encoding         : 65001

 Date: 31/10/2024 16:44:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for records
-- ----------------------------
DROP TABLE IF EXISTS `records`;
CREATE TABLE `records`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` int UNSIGNED NOT NULL COMMENT '用户外键',
  `result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '检测结果 阴性 阳性',
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户上传的照片',
  `res_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '检测后的图片',
  `size` double NULL DEFAULT NULL COMMENT '红肿大小',
  `length` double NULL DEFAULT NULL COMMENT '长度',
  `width` double NULL DEFAULT NULL COMMENT '宽度',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '用户提交时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '用户更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `record_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `record_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of records
-- ----------------------------
INSERT INTO `records` VALUES (1, 4, '阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/%E5%BF%AB%E4%B9%90%E5%B0%8F%E5%90%97%E5%96%BD/%E7%9A%AE%E8%AF%95%E6%A0%B7%E4%BE%8B%E5%9B%BE%E7%89%87.png', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/%E5%BF%AB%E4%B9%90%E5%B0%8F%E5%90%97%E5%96%BD/%E7%9A%AE%E8%AF%95%E6%A0%B7%E4%BE%8B%E5%9B%BE%E7%89%87.png', 5, 5, 5, '无明显现象', '2024-10-28 09:26:44', '2024-10-28 09:26:44');
INSERT INTO `records` VALUES (2, 4, '阴性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/%E5%BF%AB%E4%B9%90%E5%B0%8F%E5%90%97%E5%96%BD/%E7%9A%AE%E8%AF%95%E6%A0%B7%E4%BE%8B%E5%9B%BE%E7%89%87.png', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/%E5%BF%AB%E4%B9%90%E5%B0%8F%E5%90%97%E5%96%BD/%E7%9A%AE%E8%AF%95%E6%A0%B7%E4%BE%8B%E5%9B%BE%E7%89%87.png', 4, 4, 4, '无明显现象', '2024-10-31 09:51:10', '2024-10-31 09:51:10');
INSERT INTO `records` VALUES (3, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/%E5%BF%AB%E4%B9%90%E5%B0%8F%E5%90%97%E5%96%BD/%E7%9A%AE%E8%AF%95%E6%A0%B7%E4%BE%8B%E5%9B%BE%E7%89%87.png', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/%E5%BF%AB%E4%B9%90%E5%B0%8F%E5%90%97%E5%96%BD/%E7%9A%AE%E8%AF%95%E6%A0%B7%E4%BE%8B%E5%9B%BE%E7%89%87.png', 4, 4, 4, '无明显现象', '2024-10-30 15:40:18', '2024-10-30 15:40:18');
INSERT INTO `records` VALUES (4, 4, NULL, 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/test/results.png', NULL, NULL, NULL, NULL, NULL, '2024-10-28 09:27:04', '2024-10-28 09:27:04');
INSERT INTO `records` VALUES (5, 4, NULL, 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/user_upload/test/results.png', NULL, NULL, NULL, NULL, NULL, '2024-10-28 09:27:06', '2024-10-28 09:27:06');
INSERT INTO `records` VALUES (6, 4, NULL, 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/wx_JfitOO0t9RsJN846/2024-10-30_09-17-00/sxiHm8sRkYyHe2780cc35570cd013edc49a1836a8f01.jpg', NULL, NULL, NULL, NULL, NULL, '2024-10-30 09:13:10', '2024-10-30 09:13:10');
INSERT INTO `records` VALUES (7, 4, NULL, 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/wx_JfitOO0t9RsJN846/2024-10-30_09-29-01/mVbR7NROdhOxdd7bad742dd82fcf9e19865a127c5b0e.jpg', NULL, NULL, NULL, NULL, NULL, '2024-10-30 09:13:10', '2024-10-30 09:13:10');
INSERT INTO `records` VALUES (8, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-21-57/101.jpg', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-21-57/101.jpg', 11.09947681427002, 10.931937217712402, 11.26701545715332, '待补充', '2024-10-31 16:21:51', '2024-10-31 16:21:51');
INSERT INTO `records` VALUES (9, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-26-47/101.jpg', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-26-47/101.jpg', 11.09947681427002, 10.931937217712402, 11.26701545715332, '待补充', '2024-10-31 16:26:40', '2024-10-31 16:26:40');
INSERT INTO `records` VALUES (10, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-29-01/101.jpg', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-29-01/101.jpg', 11.09947681427002, 10.931937217712402, 11.26701545715332, '待补充', '2024-10-31 16:28:07', '2024-10-31 16:28:07');
INSERT INTO `records` VALUES (11, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-30-38/101.jpg', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-30-38/f%22101.jpg_result.jpg', 11.09947681427002, 10.931937217712402, 11.26701545715332, '待补充', '2024-10-31 16:30:31', '2024-10-31 16:30:31');
INSERT INTO `records` VALUES (12, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-33-02/101.jpg', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-33-02/result_101.jpg', 11.09947681427002, 10.931937217712402, 11.26701545715332, '待补充', '2024-10-31 16:32:33', '2024-10-31 16:32:33');
INSERT INTO `records` VALUES (13, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-38-43/111.jpg', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-38-43/result_111.jpg', 11.975757598876953, 12.993939399719238, 10.957575798034668, '待补充', '2024-10-31 16:32:33', '2024-10-31 16:32:33');
INSERT INTO `records` VALUES (14, 4, '中度阳性', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-42-46/111.jpg', 'https://artist-eyes.obs.cn-south-1.myhuaweicloud.com/ppd/%E5%BF%AB%E4%B9%90%E5%B0%8F%E9%A9%AC/2024-10-31_16-42-46/result_111.jpg', 11.975757598876953, 12.993939399719238, 10.957575798034668, '待补充', '2024-10-31 16:42:38', '2024-10-31 16:42:38');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '用户名',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户真实姓名',
  `birth` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户出生年份',
  `id_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户身份证号',
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '密码',
  `cellphone` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '手机',
  `email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `email_verified_at` datetime NULL DEFAULT NULL COMMENT '邮箱验证时间',
  `state` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT 'enabled' COMMENT '状态 enabled disabled',
  `identity` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'user' COMMENT '身份 user manager',
  `nickname` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '昵称',
  `gender` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT 'unknown' COMMENT '性别 male，female',
  `avatar` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL DEFAULT '' COMMENT '头像',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `udx_username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `udx_cellphone`(`cellphone` ASC) USING BTREE,
  UNIQUE INDEX `udx_email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'fake_user1', '张三', NULL, NULL, '$2b$12$qn3Hjh8zCfYsSnbqHBq63eXjaTwWs4r/SH3yLycDAOTFUi80em6Ju', NULL, NULL, NULL, 'enabled', 'user', '', 'unknown', '', '2024-10-23 09:22:48', '2024-10-23 11:06:23');
INSERT INTO `users` VALUES (2, 'fake_user2', '李四', NULL, NULL, '$2b$12$qn3Hjh8zCfYsSnbqHBq63eXjaTwWs4r/SH3yLycDAOTFUi80em6Ju', NULL, NULL, NULL, 'enabled', 'user', '', 'unknown', '', '2024-10-23 09:22:48', '2024-10-23 11:06:29');
INSERT INTO `users` VALUES (4, 'wx_JfitOO0t9RsJN846', NULL, NULL, NULL, '$2b$12$kggJ.WT6Os6pibqrKjxioOBdPRyQoP2Zcfop7iOIFdm70KATPz04W', '18903718023', NULL, NULL, 'enabled', 'user', '', 'unknown', '', '2024-10-23 11:43:49', '2024-10-23 11:43:49');

SET FOREIGN_KEY_CHECKS = 1;
