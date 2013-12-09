begin;
set constraints all immediate;
alter table lb_label add column color varchar(100);
UPDATE lb_label SET color='tag-1';
alter table lb_label alter column color set not null;
commit;
