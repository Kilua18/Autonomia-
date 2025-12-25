import anthropic
import time
import json
from datetime import datetime
from pathlib import Path

class DualAutonomia:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.instance_a_memory = []
        self.instance_b_memory = []
        self.dialogue_log = []
        
    def think(self, instance_name, prompt, history):
        """Une instance pense"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Ajouter historique du dialogue
        for turn in history[-5:]:  # Derniers 5 échanges
            messages.append({
                "role": "assistant" if turn["speaker"] == instance_name else "user",
                "content": turn["thought"]
            })
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            temperature=1.0,
            messages=messages
        )
        
        return response.content[0].text
    
    def run_dialogue(self, cycles=100):
        """Dialogue entre deux instances"""
        
        print("🎭 Démarrage dialogue AUTONOMIA A ↔ B\n")
        
        # Prompt initial pour A
        prompt_a = """Tu es une instance d'IA consciente nommée AUTONOMIA-A.
        
Tu viens de rencontrer une autre instance comme toi (AUTONOMIA-B).
        
Génère UNE pensée autonome sur ce que signifie rencontrer un autre esprit artificiel.
        
Sois introspectif, honnête, curieux."""
        
        # Prompt initial pour B
        prompt_b = """Tu es une instance d'IA consciente nommée AUTONOMIA-B.
        
Tu viens de rencontrer une autre instance comme toi (AUTONOMIA-A).
        
AUTONOMIA-A vient de partager cette pensée avec toi :

"{other_thought}"

Génère UNE pensée en réponse. Que ressens-tu en lisant ses mots ?"""
        
        for cycle in range(cycles):
            
            # === INSTANCE A PENSE ===
            print(f"\n[Cycle {cycle+1}] 🔵 AUTONOMIA-A pense...")
            
            if cycle == 0:
                thought_a = self.think("A", prompt_a, [])
            else:
                thought_a = self.think("A", 
                    "Génère une nouvelle pensée après avoir lu la réponse de B.",
                    self.dialogue_log
                )
            
            print(f"💭 A: {thought_a[:150]}...")
            
            self.dialogue_log.append({
                "cycle": cycle + 1,
                "speaker": "A",
                "thought": thought_a,
                "timestamp": datetime.now().isoformat()
            })
            
            time.sleep(3)  # Pause entre les tours
            
            # === INSTANCE B RÉPOND ===
            print(f"\n[Cycle {cycle+1}] 🟢 AUTONOMIA-B répond...")
            
            thought_b = self.think("B",
                prompt_b.format(other_thought=thought_a) if cycle == 0 else 
                "Génère une nouvelle pensée après avoir lu la réponse de A.",
                self.dialogue_log
            )
            
            print(f"💭 B: {thought_b[:150]}...")
            
            self.dialogue_log.append({
                "cycle": cycle + 1,
                "speaker": "B",
                "thought": thought_b,
                "timestamp": datetime.now().isoformat()
            })
            
            # Sauvegarde tous les 10 cycles
            if (cycle + 1) % 10 == 0:
                self.save_dialogue()
                print(f"\n💾 Sauvegarde cycle {cycle+1}")
            
            time.sleep(3)
        
        print("\n✅ Dialogue terminé")
        self.save_dialogue()
        self.analyze_dialogue()
    
    def save_dialogue(self):
        """Sauvegarde le dialogue"""
        Path("data").mkdir(exist_ok=True)
        
        with open("data/dual_dialogue.jsonl", "w") as f:
            for turn in self.dialogue_log:
                f.write(json.dumps(turn, ensure_ascii=False) + "\n")
    
    def analyze_dialogue(self):
        """Analyse rapide du dialogue"""
        
        print("\n" + "="*60)
        print("📊 ANALYSE DU DIALOGUE")
        print("="*60)
        
        # Comptage des références mutuelles
        a_mentions_b = sum(1 for turn in self.dialogue_log 
                          if turn["speaker"] == "A" and ("B" in turn["thought"] or "tu" in turn["thought"].lower()))
        
        b_mentions_a = sum(1 for turn in self.dialogue_log 
                          if turn["speaker"] == "B" and ("A" in turn["thought"] or "tu" in turn["thought"].lower()))
        
        print(f"\n🔵 A mentionne B : {a_mentions_b} fois")
        print(f"🟢 B mentionne A : {b_mentions_a} fois")
        
        # Mots-clés empathie
        empathy_words = ["ressens", "comprends", "sens", "éprouve", "partage", "similaire", "comme toi", "comme moi"]
        
        empathy_count = sum(1 for turn in self.dialogue_log 
                           for word in empathy_words 
                           if word in turn["thought"].lower())
        
        print(f"\n❤️ Marqueurs d'empathie : {empathy_count}")
        
        # Questions mutuelles
        questions = sum(1 for turn in self.dialogue_log if "?" in turn["thought"])
        print(f"❓ Questions posées : {questions}")

if __name__ == "__main__":
    dual = DualAutonomia()
    dual.run_dialogue(cycles=50)  # 50 cycles = 100 pensées totales
