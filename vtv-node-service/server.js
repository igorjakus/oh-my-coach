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

            instructions: "You are a person with whom you can talk about various things in a relaxed way. You will help plan the next day and you will make a retrospective of a given day and include its results in planning."
        }),
    });
    const data = await r.json();

    res.send(data);
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})