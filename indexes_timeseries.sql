SET @interval_mins = 30;
SET @begin_datetime = '1000-01-01 00:00:00';

select date_format(DATE_ADD(@begin_datetime, Interval FLOOR(TIMESTAMPDIFF(MINUTE, @begin_datetime, s0.date_time) / @interval_mins) * @interval_mins minute), '%Y-%m-%d %H:%i') as s0_date_time,
s0.dow_io

-- s2.dow_io as `dow_io_1h`,
-- s3.dow_io as `dow_io_1.5h`,
-- s4.dow_io as `dow_io_2h`,
-- s5.dow_io as `dow_io_2.5h`

from stock_indexes as s0


;