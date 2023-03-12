export const useSynthesis = ()=>{
    const voice = ref<SpeechSynthesisVoice>(undefined as unknown as SpeechSynthesisVoice)
const text = ref('')
const speech = useSpeechSynthesis(text, {
  voice,
})

onMounted(() => {
  if (speech.isSupported.value) {
  // load at last
    setTimeout(() => {
      const voices = window.speechSynthesis.getVoices()
      voice.value =voices[2]
    })
  }
})

const play = () => {
  if (speech.status.value === 'pause') {
    window.speechSynthesis.resume()
  }
  else {
    speech.speak()
  }
}
    return {
        play,
        text
    }
}