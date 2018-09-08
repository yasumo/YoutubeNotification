git checkout mine
git add .
git commit -m "add:channel"
git push heroku mine:master
heroku logs --tail
