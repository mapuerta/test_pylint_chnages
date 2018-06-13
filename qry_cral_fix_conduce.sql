--select * from stock_quant where product_id  = 5757 and quantity = 0 and reserved_quantity = 560;
--id = 2672

delete from stock_quant where id = 2672;

--select * from stock_quant where product_id  = 5757 and reserved_quantity =  1427
--id = 1479

update stock_quant set reserved_quantity = 1987 where id = 1479;
