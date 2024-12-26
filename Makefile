up:
	docker compose up
update:
	docker compose exec odoo odoo -u trobz_shopinvader_demo --no-http --stop-after-init
restart:
	docker compose restart odoo
drop_db:
	docker compose stop odoo
	docker compose exec db dropdb -U odoo db
	docker compose start odoo
down:
	docker compose down -v