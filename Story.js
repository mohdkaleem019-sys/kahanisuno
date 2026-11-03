// Vercel serverless function: POST /api/story  { topic: "..." }
// Needs the environment variable OPENAI_API_KEY (set in Vercel, never in code).
const hits = new Map(); // simple per-IP limit (resets when the function restarts)
const LIMIT = 5, WINDOW = 24 * 60 * 60 * 1000;

module.exports = async (req, res) => {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  const key = process.env.OPENAI_API_KEY;
  if (!key) return res.status(500).json({ error: "Server key not set" });

  const ip = (req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "x";
  const now = Date.now();
  const list = (hits.get(ip) || []).filter(t => now - t < WINDOW);
  if (list.length >= LIMIT) return res.status(429).json({ error: "आज की सीमा पूरी हो गई। कल फिर कोशिश कीजिए।" });

  const topic = String((req.body && req.body.topic) || "").trim().slice(0, 120);
  if (topic.length < 3) return res.status(400).json({ error: "विषय बहुत छोटा है।" });

  try {
    const r = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + key },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 0.8,
        max_tokens: 600,
        response_format: { type: "json_object" },
        messages: [
          { role: "system", content: "तुम एक हिंदी कहानीकार हो। दिए गए विषय पर देवनागरी हिंदी में 150-220 शब्दों की छोटी ऑडियो कहानी लिखो। छोटे वाक्य रखो, ताकि सुनने में अच्छी लगे। कहानी सबके लिए सुरक्षित हो: कोई अश्लील या अत्यधिक हिंसक सामग्री नहीं। केवल JSON लौटाओ: {\"title\":\"...\",\"text\":\"...\"}" },
          { role: "user", content: "विषय: " + topic }
        ]
      })
    });
    const d = await r.json();
    if (!r.ok) throw new Error((d.error && d.error.message) || "OpenAI error");
    const out = JSON.parse(d.choices[0].message.content);
    hits.set(ip, [...list, now]);
    return res.status(200).json({ title: String(out.title || "नई कहानी").slice(0, 80), text: String(out.text || "").slice(0, 2500) });
  } catch (e) {
    return res.status(502).json({ error: "कहानी नहीं बन पाई। थोड़ी देर बाद कोशिश कीजिए।" });
  }
};
