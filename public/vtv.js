// const speakingButton = $(".speaking-button");

async function init() {
    // Get an ephemeral key from your server - see server code below
    const tokenResponse = await fetch("http://localhost:3000/request-vtv-ephemeral");
    const data = await tokenResponse.json();
    const EPHEMERAL_KEY = data.client_secret.value;

    // Create a peer connection
    const pc = new RTCPeerConnection();

    // Set up to play remote audio from the model
    const audioEl = document.createElement("audio");
    audioEl.autoplay = true;
    pc.ontrack = e => audioEl.srcObject = e.streams[0];

    // Add local audio track for microphone input in the browser
    const ms = await navigator.mediaDevices.getUserMedia({
        audio: true
    });
    pc.addTrack(ms.getTracks()[0]);
    
    const audioCtx = new AudioContext();
    const source = audioCtx.createMediaStreamSource(ms);
    const analyser = audioCtx.createAnalyser();
    const dataArray = new Uint8Array(analyser.fftSize);

    source.connect(analyser);

    function getVolume() {
        analyser.getByteTimeDomainData(dataArray);
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
          const val = (dataArray[i] - 128) / 128;
          sum += val * val;
        }
        const volume = Math.sqrt(sum / dataArray.length); // RMS volume
  
        // Style based on volume
        const scale = 1 + volume * 10;
        const red = Math.min(255, Math.floor(volume * 1000));
        $(".talking-sphere").style.outlineWidth = `${volume * 1000}px`;
        requestAnimationFrame(getVolume);
    }

    // Set up data channel for sending and receiving events
    const dc = pc.createDataChannel("oai-events");
    dc.addEventListener("message", (e) => {
        // Realtime server events appear here!
        const data = JSON.parse(e.data);
        if (data['type'] == "response.created") {
            ms.getAudioTracks()[0].enabled = false; 
            $(".talking-sphere").style.opacity = 0.8;
            // $(".talking-sphere").style.outlineWidth = '0px';
            console.log("Muted")

        }
    });
    getVolume();
    $(".talking-sphere").addEventListener("click", () => {
        ms.getAudioTracks()[0].enabled = true;
        $(".talking-sphere").style.opacity = 1;
        // $(".talking-sphere").style.outlineWidth = '40px';
    })

    // Start the session using the Session Description Protocol (SDP)
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    const baseUrl = "https://api.openai.com/v1/realtime";
    const model = "gpt-4o-realtime-preview";
    const sdpResponse = await fetch(`${baseUrl}?model=${model}`, {
        method: "POST",
        body: offer.sdp,
        headers: {
        Authorization: `Bearer ${EPHEMERAL_KEY}`,
        "Content-Type": "application/sdp"
        },
    });

    const answer = {
        type: "answer",
        sdp: await sdpResponse.text(),
    };
    await pc.setRemoteDescription(answer);
}

// init();


const selectedCheckmarks = [false, false, false];

const checkMarks = document.querySelectorAll(".retro-checkmark");
for ( const checkmark of checkMarks ) {
    checkmark.addEventListener("click", e => {
        if (e.target === checkmark) { 
            e.target.children[0].style.display = 
                e.target.children[0].style.display == 'none' ? 'block' : 'none';
        } else {
            e.target.style.display = 'none'
        }
    }, false)  
}

$(".retro-options-confirm-btn").addEventListener("click", () => {
    $(".retro-options").style.opacity = 0;
    $(".talking-sphere").style.opacity = 1;
    $(".talking-sphere").style.outlineWidth = '40px';
    init();
})