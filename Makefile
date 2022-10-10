

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

heroku_login:
	-@heroku login

heroku_upload_public_key:
	-@heroku keys:add ~/.ssh/id_ed25519.pub

heroku_create_app:
	-@heroku create --ssh-git ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

update_git_and_heroku:
	-@git -commit -m "auto"
	-@git push origin master
	-@git push heroku master
