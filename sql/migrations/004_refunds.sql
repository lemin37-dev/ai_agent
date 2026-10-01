CREATE TABLE IF NOT EXISTS refunds (
  refund_id BIGSERIAL PRIMARY KEY,
  order_id BIGINT REFERENCES orders(order_id),
  requested_at TIMESTAMPTZ NOT NULL,
  reason VARCHAR(80) NOT NULL,
  amount NUMERIC(12,2) NOT NULL,
  status VARCHAR(30) NOT NULL
);
INSERT INTO refunds(order_id,requested_at,reason,amount,status)
SELECT 8,'2026-09-04 18:00+09','product_defect',99000,'approved'
WHERE NOT EXISTS(SELECT 1 FROM refunds);
