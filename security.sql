create database `security` default charset=utf8mb4 collate utf8mb4_general_ci;

use security;

create table `security`
(
    `securityKey` varchar(128) not null,
    `securityID` varchar(16) not null comment '',
    `marketID` varchar(4) not null comment '',
    `name` varchar(32) not null comment '',
    `createTime` datetime default current_timestamp comment '',
    `updateTime` datetime default current_timestamp on update current_timestamp comment '',
    `remark` varchar(16) comment '',
    primary key(`securityKey`)
) engine=innodb default charset=utf8mb4 collate utf8mb4_general_ci;

create table `candlestick`
(
    `securityKey` varchar(128) not null,
    `date` date not null,
    `kid` int not null comment '-1: day; 0-239: minute',
    `preClose` decimal(16, 2) not null,
    `open` decimal(16, 2) not null,
    `close` decimal(16, 2) not null,
    `high` decimal(16, 2) not null,
    `low` decimal(16, 2) not null,
    `volume` bigint default 0,
    `turnover` bigint default 0,
    `marketTime` datetime not null,
    `createTime` datetime default current_timestamp comment '',
    `updateTime` datetime default current_timestamp on update current_timestamp comment '',
    primary key(`securityKey`, `date`, `kid`)
) engine=innodb default charset=utf8mb4 collate utf8mb4_general_ci;

-- 600036.2 20180423 -1
-- 600036.2 20180424 -1
-- 600036.2 20180423 0
-- 600036.2 20180423 1
-- 600036.2 20180423 2
-- 600036.2 20180423 3

-- 获取日K线
select * from candlestick 
where securityKey = '600036.2'
    and kid = -1
    and date < now()
order by date desc
limit 30;

-- 获取一分钟K线
select * from candlestick 
where securityKey = '600036.2'
    and kid >= 0
    and date = date(now())
order by kid;

create table tmp(
    id int auto_increment,
    name varchar(32),
    age int,
    key(id)
) engine=innodb default charset=utf8mb4 collate utf8mb4_general_ci;

-- create table `kDay`
-- (
--     `securityKey` varchar(128) not null,
--     `kid` date not null,
--     `preClose` decimal(16, 2) not null,
--     `open` decimal(16, 2) not null,
--     `close` decimal(16, 2) not null,
--     `high` decimal(16, 2) not null,
--     `low` decimal(16, 2) not null,
--     `volume` bigint default 0,
--     `turnover` bigint default 0,
--     `marketTime` datetime not null,
--     `updateTime` timestamp not null default current_timestamp on update current_timestamp,
--     primary key(securityKey, kid)
-- ) engine=innodb default charset=utf8mb4 collate utf8mb4_general_ci;

-- create table `kM1`
-- (
--     `securityKey` varchar(128) not null,
--     `kid` bigint not null,
--     `preClose` decimal(16, 2) not null,
--     `open` decimal(16, 2) not null,
--     `close` decimal(16, 2) not null,
--     `high` decimal(16, 2) not null,
--     `low` decimal(16, 2) not null,
--     `volume` bigint default 0,
--     `turnover` bigint default 0,
--     `marketTime` datetime not null,
--     `updateTime` timestamp not null default current_timestamp on update current_timestamp,
--     primary key(securityKey, kid)
-- ) engine=innodb default charset=utf8mb4 collate utf8mb4_general_ci;