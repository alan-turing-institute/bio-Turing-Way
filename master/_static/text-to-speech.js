const styles = {
    speechButton: {
        width: "6%",
        cursor: "pointer",
    },
    container: {
        display: "flex",
        alignItems: "center",
        
    },
    voiceListContainer: {
        display: "none",
        position: "absolute",
        top: "100%",
        left: "0",
        backgroundColor: "#fff",
        border: "1px solid #ccc",
        padding: "4px",
        maxHeight: "150px",
        overflowY: "auto",
    },
    voiceListItem: {
        cursor: "pointer",
        padding: "2px 0",
        borderTop: "1px solid #ccc",
    },
};

window.createSpeechButton = async function () {
    await EasySpeech.init();
    const mainContent = document.getElementById("main-content");
    const clone = mainContent.cloneNode(true);
    Array.from(clone.getElementsByClassName("prev-next-area"))[0].remove();
    const scripts =clone.getElementsByTagName("script");
    const scriptArray = Array.from(scripts);
    scriptArray.forEach((sc)=>{
        sc.remove();
    })
   
    const figureElements =clone.childNodes[1].getElementsByClassName("figure");
    const other = clone.childNodes[1].getElementsByClassName("onlyprint");
    const array = Array.from(other);
    console.log(array);
    const figureArray = Array.from(figureElements);
    console.log(figureArray);
    array.forEach((ele)=>{
        ele.remove();
    });
    figureArray.forEach((figure) => {
        figure.remove();
    });
    let isSpeaking = false;
    const voices = EasySpeech.voices();
    console.log(clone.innerText);
    let selectedVoice = voices[0];
    let textToSpeak = clone.innerText;

    const speechButton = document.createElement("button");
    speechButton.innerHTML = '<i class="fas fa-volume-up"></i>';
    Object.assign(speechButton.style, styles.speechButton);

    var ele = mainContent.querySelectorAll("h1")[1];
    if (ele) {
        var container = document.createElement("div");
        Object.assign(container.style, styles.container);

        var h1Clone = ele.cloneNode(true);
        container.appendChild(h1Clone);
        container.appendChild(speechButton);

        ele.parentNode.replaceChild(container, ele);
    }

    const voiceListContainer = document.createElement("div");
    Object.assign(voiceListContainer.style, styles.voiceListContainer);

    const voiceList = document.createElement("ul");
    Object.assign(voiceList.style, styles.voiceList);

    function showVoiceList() {
        voiceList.innerHTML = "";

        voices.forEach((voice, index) => {
            const voiceListItem = document.createElement("li");
            Object.assign(voiceListItem.style, styles.voiceListItem);
            voiceListItem.innerText = voice.name;

            voiceListItem.addEventListener("mouseenter", () => {
                voiceListItem.style.backgroundColor = "#f0f0f0";
            });

            voiceListItem.addEventListener("mouseleave", () => {
                voiceListItem.style.backgroundColor = "transparent";
            });

            voiceListItem.addEventListener("click", () => {
                selectedVoice = voices[index];
                console.log(selectedVoice, index);
                EasySpeech.cancel();
                speakText();
                voiceListContainer.style.display = "none";
            });

            voiceList.appendChild(voiceListItem);
        });

        const buttonRect = speechButton.getBoundingClientRect();
        voiceListContainer.style.top = buttonRect.bottom + "px";
        voiceListContainer.style.left = buttonRect.left + "px";
        voiceListContainer.style.display = "block";
    }

    function speakText() {
        if (!isSpeaking) {
            speechButton.innerHTML = '<i class="fas fa-volume-up"></i>';
            EasySpeech.speak({
                text: textToSpeak,
                voice: selectedVoice,
                pitch: 2,
                rate: 1,
            });
            isSpeaking = true;
        } else {
            speechButton.innerHTML = '<i class="fas fa-stop"></i>';
            isSpeaking = false;
            EasySpeech.cancel();
        }
    }

    speechButton.addEventListener("mouseenter", () => {
        showVoiceList();
    });

    document.addEventListener("click", (event) => {
        if (!speechButton.contains(event.target) && !voiceListContainer.contains(event.target)) {
            voiceListContainer.style.display = "none";
        }
    });

    speechButton.addEventListener("click", () => {
        speakText();
    });

    voiceListContainer.appendChild(voiceList);
    document.body.appendChild(voiceListContainer);
};

window.createSpeechButton();
