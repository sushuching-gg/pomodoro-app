import os
import re

filepath = r'c:\Users\user\.gemini\antigravity\brain\My_AI_Project\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 調整 update() 內的邏輯，移除 isRunning 限制，讓音樂即點即播
content = content.replace("if (musicOn && isRunning) startAmbient(); else stopAmbient();", "if (musicOn) startAmbient(); else stopAmbient();")

# 調整 startAmbient()，確保模式變化時切換，並增加音量
new_start_logic = """
        function startAmbient() {
            initAudio(); 
            if (noiseNode && mode === 'focus') return;
            if (oscNode && mode === 'break') return;
            stopAmbient();
            const now = audioCtx.currentTime;
            if (mode === 'focus') {
                const bufferSize = 2 * audioCtx.sampleRate, buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate), data = buffer.getChannelData(0);
                for (let i=0; i<bufferSize; i++) data[i] = Math.random() * 2 - 1;
                noiseNode = audioCtx.createBufferSource(); noiseNode.buffer = buffer; noiseNode.loop = true;
                const gain = audioCtx.createGain(); gain.gain.value = 0.15; // 再次提高音量
                noiseNode.connect(gain); gain.connect(audioCtx.destination);
                noiseNode.start();
            } else {
                oscNode = audioCtx.createOscillator(); oscNode.type = 'sine'; oscNode.frequency.value = 330;
                const gain = audioCtx.createGain();
                const lfo = audioCtx.createOscillator(); lfo.type = 'sine'; lfo.frequency.value = 0.2;
                const lg = audioCtx.createGain(); lg.gain.value = 0.05;
                lfo.connect(lg); lg.connect(gain.gain);
                gain.gain.setValueAtTime(0.08, now);
                oscNode.connect(gain); gain.connect(audioCtx.destination);
                lfo.start(); oscNode.start();
            }
        }
"""
content = re.sub(r'function startAmbient\(\) \{.*?\}', new_start_logic, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("V12: Music unlocked, volume boosted, settings preserved.")
