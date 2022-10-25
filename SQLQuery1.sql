DROP DATABASE Billing_System;

create database Billing_System;

use Billing_System;

create table Users
(
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username varchar(20) not null,
  name varchar(50) not null,
  role ENUM('admin', 'cashier') default 'cashier',
  password varchar(200) not null,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table In_Stocks
(
  Item_ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Items varchar(40) not null,
  Price decimal(10,2) not null,
  Item_image_link varchar(255) not null,
  Quantity numeric not null
);

create table Items_soldout
(
  Item_ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Item_name varchar(50) not null,
  Date_sold date not null
);

create table Products
(
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name varchar(40) not null,
  price decimal(10,2) not null,
  image VARCHAR(255) NULL,
  quantity int DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

create table Sales
(
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  total DECIMAL(10,2) NOT NULL,
  user_id INT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_sales_cashier FOREIGN KEY(user_id) REFERENCES Users(id) ON DELETE CASCADE
);

create table SaleItems
(
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  sales_id INT NOT NULL,
  product_id int NOT NULL,
  quantity int NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_solditem_sales FOREIGN KEY(sales_id) REFERENCES Sales(id) ON DELETE CASCADE,
  CONSTRAINT fk_solditem_product FOREIGN KEY(product_id) REFERENCES Products(id) ON DELETE CASCADE
);

INSERT INTO Users(username, name, role, password) 
  VALUES ("theonlyamos", "Amos Amissah", "admin",
  "$pbkdf2-sha512$25000$3Lv3Psc4Z8zZWytF6N17jw$XL/WQbgMMjDD9gyAngOB4LgfJI/ACC3UyooBvTt3SE/qUia14UiA9d50HdlAw8PHfnZSycXX2DHAb5bnbv0y5g");

INSERT INTO Users(username, name, role, password) 
  VALUES ("Faisal", "Faisal Issaka", "admin",
  "$pbkdf2-sha512$25000$fc9ZS2mNMWZMCeGcs/a.dw$oaDo0iVLlHNJ4xf9KJDYaJF8Sc1NOpJYq6QKZNc8O1JAtP8/PIi8Gsb2LozdG.lCpA1eFpRNb0Q1uRonSCVuaA");