yig
===

`yig` is a django app for exploring bills and resolutions in previous YMCA CCE conferences.
It's sort of ballooned to also contain a knowledge-base thing.

## Deploying in production

0. Ensure that you have Docker installed and good to go.

For NixOS machines, this involves the following:
```nix
{ ... }
{
    virtualisation.docker.enable = true;
    users.users.<your user>.extraGroups = [ ... ] ++ [ "docker" ];
}
```

1. Enter the `nix-shell`.
2. `make permissions`
3. `make`

To tear down the docker container, type `make clean`.

If you've just started the instance, you also need to configure a superuser.

1. Run `docker ps | grep yig-web | awk -F' ' '{print $1}'` to get the container id
2. Run `docker exec -it <container-id> bash` to get a shell.
3. Run `python3 manage.py createsuperuser` and follow the prompts.

## Usage

In order to use the `explorer` component of this package, you need to add some legislative texts.
These are in the form of PDFs -- they come from the YMCA CCE website or are sometimes emailed or otherwise shared with you.
Only these PDFs will work because they follow a very specific format which the software exploits.

1. Login with your admin account.
2. Click on the `add` button next to `Legislation books` in the sidebar
3. Upload your book, add a name, and choose the correct `Import strategy`
4. Click save

## More information

More information about operation of this project can be found in the [knowledgebase](./kb) directory.

## License

`yig` is licensed under the AGPLv3 -- the terms of the license are available in [`LICENSE.md`](./LICENSE.md).