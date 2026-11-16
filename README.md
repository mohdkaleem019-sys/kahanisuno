# KahaniSuno system

## Publish (every time)
1. Edit `stories.json` (add stories) and the CONFIG lines at top of `build.py` (CONTACT_EMAIL, SOCIAL, YOUTUBE, GA_ID).
2. Put MP3s in `builder/audio/` named `<slug>.mp3`.
3. Run `python3 build.py`. Upload the CONTENTS of `site/` (or the zip's contents) to the GitHub repo root. Vercel redeploys.
4. Submit https://www.khanisuno.in/sitemap.xml in Google Search Console.

## Story entry format (stories.json)
{"slug":"my-story","title":"हिंदी शीर्षक","hinglish":"Hinglish Title | Hindi Horror Story","category":"horror|rahasya|bedtime","hook":"one-line teaser","paragraphs":["..."],"minutes":6}

## Weekly traffic routine
- 3-5 new episodes, 400+ words each, end on a cliffhanger.
- Use youtube_kit.md for titles, descriptions and the Shorts hook of each story.
- Upload full episode to YouTube, cut a 30-second hook as a Short and a Reel, post to WhatsApp/Telegram channel.
- Same audio to Spotify/Apple via a free podcast host using feed.xml-style RSS.
- Check Search Console weekly: make more of the stories that get impressions.
