prod: # execute this target on the production server in the nix-shell
	cd franklincce; yes yes | python3 manage.py collectstatic
	sh gen_kb.sh
	sed "s|change_me|$(shell dd if=/dev/urandom bs=1024 count=1|base64)|g" .env.prod.orig > .env.prod
	docker-compose -f docker-compose.prod.yml up -d --build

permissions: db.sqlite3
	chmod -f 660 db.sqlite3
	echo "make sure that db.sqlite3 is owned by group users"

db.sqlite3:
	touch db.sqlite3

make_kb:
	sh gen_kb.sh

clean:
	rm -fr franklincce/staticfiles
	docker-compose -f docker-compose.prod.yml down -v
