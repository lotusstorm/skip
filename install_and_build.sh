#!/usr/bin/env bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install yarn
cd static/skip_table
python change_ip.py
yarn install
yarn build
python path_validator.py
sudo cp -r dist/ /var/www/
