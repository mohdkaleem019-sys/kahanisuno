KAHANISUNO - NEW SITE

1. UPLOAD: open the "site" folder. Upload ALL its contents to the ROOT of your GitHub repo
   (GitHub > Add file > Upload files), replacing the old index.html. Commit. Vercel redeploys.
2. AUDIO: put MP3 files in the audio/ folder of the repo. Then set "audio":"audio/yourfile.mp3"
   for that story in builder/stories.json and rebuild (step 3).
3. ADD / EDIT STORIES: edit builder/stories.json, run:  python3 build.py
   Then upload the new contents of the "site" folder again.
4. Set SITE, SOCIAL (WhatsApp/Telegram link) and EMAIL at the top of builder/build.py.
5. Google Search Console: add the site, submit https://www.khanisuno.in/sitemap.xml
6. Never put API keys in these files.
