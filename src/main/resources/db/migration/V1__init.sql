create table Episode
(
    Id int primary key auto_increment,
    Name nvarchar(50) not null,
    PublishedDate datetime,
    Content text not null
)