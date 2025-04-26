require('dotenv').config({
    path: '../.env'
})
var cors = require('cors')
const express = require('express')
const app = express()
const port = 3000

var corsOptions = {
    origin: '*',
    optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
  }

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.get('/request-vtv-ephemeral', cors(corsOptions), async (req, res) => {
    const r = await fetch("https://api.openai.com/v1/realtime/sessions", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            model: "gpt-4o-realtime-preview",
            voice: "alloy",
            
            instructions: "Jesteś pomocnym chatbotem"
        }),
    });
    const data = await r.json();
    
    res.send(data);
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})