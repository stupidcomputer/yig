prod: # execute this target on the production server in the nix-shell
	rm -r franklincce/staticfiles
	cd franklincce; python3 manage.py collectstatic
	sed -i "s/change_me/$(shell shuf -i1-1000000 -n1)/g" .env.prod
	docker-compose -f docker-compose.prod.yml up -d --build
