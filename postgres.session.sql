sql
create sequence queue_seq;

create table queue (
    id int check (id > 0) primary key default nextval ('queue_seq'),
    created_at timestamp(0) not null DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp(0) not null DEFAULT CURRENT_TIMESTAMP,
    status varchar(255) not null DEFAULT 'pending',
    job_id varchar(255)
)