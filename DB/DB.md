mysql Ver 8.0.11 for osx10.13 on x86_64

**1. create scheme**

    CREATE SCHEMA 'wechatForwardDB' ;


**2. create table UserInfo**

    CREATE TABLE 'wechatForwardDB'.'UserInfo' (
      'idUserInfo' INT NOT NULL AUTO_INCREMENT,
      'UserID' VARCHAR(200) NOT NULL,
      'UserName' VARCHAR(200) NULL DEFAULT NULL,
      PRIMARY KEY ('idUserInfo'),
      UNIQUE INDEX 'UserID_UNIQUE' ('UserID' ASC));


**3. create table GroupInfo**

    CREATE TABLE `test`.`GroupInfo` (
      `idGroupInfo` INT NOT NULL AUTO_INCREMENT,
      `GroupID` VARCHAR(200) NOT NULL,
      `GroupName` VARCHAR(200) NULL DEFAULT NULL,
      PRIMARY KEY (`idGroupInfo`),
      UNIQUE INDEX `GroupID_UNIQUE` (`GroupID` ASC));


**4. create table ForwardRule**

    CREATE TABLE `test`.`ForwardRule` (
      `idForwardRule` INT NOT NULL AUTO_INCREMENT,
      `UserID` VARCHAR(200) NULL,
      `ListenerID` VARCHAR(200) NULL,
      `ForwardID` VARCHAR(200) NULL,
      `keyWord` VARCHAR(200) NULL,
      PRIMARY KEY (`idForwardRule`),
      INDEX `forward_idx` (`ForwardID` ASC),
      INDEX `listener_idx` (`ListenerID` ASC),
      INDEX `user_idx` (`UserID` ASC),
      CONSTRAINT `forward`
        FOREIGN KEY (`ForwardID`)
        REFERENCES `test`.`GroupInfo` (`GroupID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `listener`
        FOREIGN KEY (`ListenerID`)
        REFERENCES `test`.`GroupInfo` (`GroupID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT `user`
        FOREIGN KEY (`UserID`)
        REFERENCES `test`.`UserInfo` (`UserID`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION);

