prod: # execute this target on the production server in the nix-shell
	rm -r franklincce/staticfiles
	cd franklincce; python3 manage.py collectstatic
	sed "s/change_me/$(shell shuf -i1-1000000 -n1)/g" .env.prod.orig > .env.prod
	sed "s|change_me|$(shell dd if=/dev/urandom bs=1024 count=1|base64)|g" .env.prod.orig > .env.prod
	docker-compose -f docker-compose.prod.yml up -d --build
